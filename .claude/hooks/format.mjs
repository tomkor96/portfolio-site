// PostToolUse: format every Python file Claude writes with ruff (project config in pyproject.toml).
// Never blocks; a missing uv or a syntax error is left to `ruff check` and the tests.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

let input;
try {
	input = JSON.parse(fs.readFileSync(0, 'utf8'));
} catch {
	process.exit(0);
}
const cwd = input.cwd ?? process.cwd();
const file = input.tool_input?.file_path ?? input.tool_response?.filePath;
if (!file || !file.endsWith('.py')) process.exit(0);

const rel = path.relative(cwd, path.resolve(cwd, file));
if (rel.startsWith('..') || path.isAbsolute(rel)) process.exit(0);

try {
	execFileSync('uv', ['run', '--quiet', 'ruff', 'format', '--quiet', rel], {
		cwd,
		stdio: 'ignore',
		timeout: 20_000
	});
} catch {
	// Formatting must not get in the way.
}
process.exit(0);
