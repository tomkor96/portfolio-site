// PreToolUse guard: hard blocks for actions that must go through review or that are known to break production.
// Exit code 2 blocks the tool call and shows stderr to Claude.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';

const PROTECTED = new Set(['main', 'master']);
const GIT = /(^|[\\/])git(\.exe)?$/i;
const GLOBAL_WITH_VALUE = new Set(['-C', '-c', '--git-dir', '--work-tree', '--namespace']);
const PUSH_WITH_VALUE = new Set(['-o', '--push-option', '--repo', '--receive-pack', '--exec']);

function readInput() {
	try {
		return JSON.parse(fs.readFileSync(0, 'utf8'));
	} catch {
		return null;
	}
}

function git(cwd, args) {
	try {
		return execFileSync('git', args, {
			cwd,
			encoding: 'utf8',
			stdio: ['ignore', 'pipe', 'ignore']
		});
	} catch {
		return null;
	}
}

function block(message) {
	process.stderr.write(`Blocked by .claude/hooks/guard.mjs: ${message}\n`);
	process.exit(2);
}

/** Flags and refspecs of a `git push` segment, or null when the segment isn't one. */
function parsePush(segment) {
	const tokens = segment
		.trim()
		.split(/\s+/)
		.map((t) => t.replace(/^["'&]+|["']+$/g, ''));
	const gitAt = tokens.findIndex((t) => GIT.test(t));
	if (gitAt === -1) return null;

	let i = gitAt + 1;
	while (tokens[i]?.startsWith('-')) i += GLOBAL_WITH_VALUE.has(tokens[i]) ? 2 : 1;
	if (tokens[i] !== 'push') return null;

	const flags = [];
	const positional = [];
	for (let j = i + 1; j < tokens.length; j++) {
		if (PUSH_WITH_VALUE.has(tokens[j])) {
			j++;
			continue;
		}
		(tokens[j].startsWith('-') ? flags : positional).push(tokens[j]);
	}
	// The first positional argument is the remote; the rest are refspecs.
	return { flags, refspecs: positional.slice(1) };
}

/** Why a shell command pushes to a protected branch, or null when it doesn't. */
function protectedPushReason(command, cwd) {
	let current;
	const currentBranch = () => (current ??= (git(cwd, ['branch', '--show-current']) ?? '').trim());

	for (const segment of command.split(/&&|\|\||;|\||\n/)) {
		const push = parsePush(segment);
		if (!push) continue;

		if (push.flags.some((f) => f === '--all' || f === '--mirror')) return 'pushes every branch';

		if (push.refspecs.length === 0) {
			if (PROTECTED.has(currentBranch())) return `pushes the current branch "${currentBranch()}"`;
			continue;
		}

		for (const spec of push.refspecs) {
			const dest = spec
				.replace(/^\+/, '')
				.split(':')
				.pop()
				.replace(/^refs\/heads\//, '');
			const target = dest === 'HEAD' || dest === '@' ? currentBranch() : dest;
			if (PROTECTED.has(target)) return `pushes to "${target}"`;
		}
	}
	return null;
}

const input = readInput();
if (!input) process.exit(0);
const { tool_name: tool, tool_input: toolInput = {}, cwd = process.cwd() } = input;

if (tool === 'Bash' || tool === 'PowerShell') {
	const reason = protectedPushReason(String(toolInput.command ?? ''), cwd);
	if (reason) {
		block(
			`this command ${reason}. main changes only through a pull request: push a feat/*, fix/* or chore/* branch and open a PR (/dev-kit:pr-open).`
		);
	}
}

if (tool === 'mcp__mikrus__exec') {
	const cmd = String(toolInput.cmd ?? '');
	const sedInPlaceOnNginxConf =
		/\bsed\b[^|;&]*(\s-[A-Za-z]*i|--in-place)/.test(cmd) && /nginx\.conf/.test(cmd);
	if (sedInPlaceOnNginxConf) {
		block(
			'nginx.conf is a single-file bind mount; `sed -i` creates a new inode the container never sees. Write it with `cat > file` instead.'
		);
	}
}

process.exit(0);
