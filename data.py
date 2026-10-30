# Content of the site. A value that differs per language is {"pl": ..., "en": ...}; build.py
# resolves it before rendering. Tech names stay Polish (they also give the chip color class);
# their English labels live in texts.TECH_LABELS.

PROFILE: dict = {
    "name": "Tomasz Koralewski",
    "role": {"pl": "Inżynier ds. danych produktowych", "en": "Product Data Engineer"},
    "location": {"pl": "Polska, Tarnowskie Góry", "en": "Poland, Tarnowskie Góry"},
    "email": "tomaszkoralewski1@gmail.com",
    "linkedin": "https://www.linkedin.com/in/tomasz-koralewski-a7233a154/",
    "github": "https://github.com/tomkor96",
    "site_url": "https://tkoralewski.toadres.pl",
    "newsletter": "https://pythondigest.toadres.pl/",
    "cv_path": "docs/Tomasz_Koralewski_CV.pdf",
    "tagline": {"pl": "dane. aplikacje. automatyzacja.", "en": "data. apps. automation."},
    "about": {
        "pl": "Mam na imię Tomek i lubię rozwiązywać problemy z użyciem technologii. Na co dzień pobieram, czyszczę i porządkuję dane produktowe dla e-commerce, a po godzinach buduję własne aplikacje.",
        "en": "I'm Tomek and I like solving problems with technology. By day I collect, clean and organise product data for e-commerce; after hours I build my own applications.",
    },
    "status": {
        "pl": "Senetic · inżynier ds. danych produktowych",
        "en": "Senetic · product data engineer",
    },
}

EDUCATION: list[dict] = [
    {
        "institution": {
            "pl": "Uniwersytet Śląski w Katowicach",
            "en": "University of Silesia in Katowice",
        },
        "degree": {"pl": "Magister", "en": "Master's degree"},
        "field": {"pl": "Socjologia", "en": "Sociology"},
        "specialization": {
            "pl": "HR w nowoczesnej organizacji",
            "en": "HR in a modern organisation",
        },
        "start_date": "2020",
        "end_date": "2022",
    },
    {
        "institution": {
            "pl": "Uniwersytet Śląski w Katowicach",
            "en": "University of Silesia in Katowice",
        },
        "degree": {"pl": "Licencjat", "en": "Bachelor's degree"},
        "field": {"pl": "Zarządzanie zasobami ludzkimi", "en": "Human resource management"},
        "specialization": "",
        "start_date": "2017",
        "end_date": "2020",
    },
    {
        "institution": {
            "pl": 'ZSTiO "Mechanik" w Tarnowskich Górach',
            "en": 'ZSTiO "Mechanik" technical school, Tarnowskie Góry',
        },
        "degree": {"pl": "Technik informatyk", "en": "IT technician"},
        "field": {"pl": "Informatyka", "en": "Computer science"},
        "specialization": "",
        "start_date": "2012",
        "end_date": "2016",
    },
]


EXPERIENCE: list[dict] = [
    {
        "job_title": {"pl": "Inżynier ds. danych produktowych", "en": "Product Data Engineer"},
        "company": "Senetic Global Services",
        "start_date": "2024-08-01",
        "responsibilities": {
            "pl": [
                "Automatyczne pobieranie danych ze źródeł takich jak API lub strony internetowe",
                "Zarządzanie bazą produktową z użyciem Akeneo i SQL",
                "Obróbka danych i dostosowanie ich do określonych wymagań i standardów",
                "Tworzenie materiałów takich jak opisy produktowe z wykorzystaniem API OpenAI",
            ],
            "en": [
                "Automated data collection from sources such as APIs and websites",
                "Managing the product database with Akeneo and SQL",
                "Processing data and adapting it to specific requirements and standards",
                "Creating content such as product descriptions with the OpenAI API",
            ],
        },
        "tech": ["Python", "SQL", "Pandas", "Akeneo", "API OpenAI"],
    },
    {
        "job_title": {
            "pl": "Pełnomocnik Beneficjenta programu Czyste Powietrze",
            "en": "Beneficiary representative, Clean Air Programme",
        },
        "company": "Ekoconsult.pl",
        "start_date": "2023-01-01",
        "end_date": "2024-07-31",
        "responsibilities": {
            "pl": [
                "Własna działalność nierejestrowana polegająca na pozyskiwaniu dotacji z programu Czyste Powietrze w imieniu klientów",
            ],
            "en": [
                "Own small-scale business securing grants from the Polish Clean Air Programme (Czyste Powietrze) on behalf of clients",
            ],
        },
        "tech": ["MS Excel", "Systemy rządowe"],
    },
    {
        "job_title": {
            "pl": "Pracownik obsługi sprzedaży internetowej",
            "en": "Online sales specialist",
        },
        "company": "Auto Kram sp. j.",
        "start_date": "2021-01-01",
        "responsibilities": {
            "pl": [
                "Zarządzanie sprzedażą internetową",
                "Wystawianie aukcji na platformie Allegro, automatyzacja sprzedaży w aplikacji Baselinker",
            ],
            "en": [
                "Managing online sales",
                "Listing offers on Allegro and automating sales in Baselinker",
            ],
        },
        "tech": ["Allegro", "Baselinker", "MS Excel"],
    },
    {
        "job_title": "Copywriter",
        "company": "EACTIVE",
        "start_date": "2019-01-01",
        "end_date": "2020-12-31",
        "responsibilities": {
            "pl": [
                "Pisanie tekstów blogowych oraz tekstów optymalizacyjnych opartych o promocję",
                "Wykorzystanie słów kluczowych pomagających znaleźć stronę zleceniodawcy poprzez wyszukiwarki",
            ],
            "en": [
                "Writing blog posts and promotion-focused SEO copy",
                "Using keywords that help clients' websites get found in search engines",
            ],
        },
        "tech": ["SEO", "Content Marketing", "Google Analytics"],
    },
    {
        "job_title": {
            "pl": "Koordynator ds. rozwoju i innowacji",
            "en": "Development and Innovation Coordinator",
        },
        "company": "Autoszyby.pl sp. z o.o.",
        "start_date": "2018-08-01",
        "end_date": "2023-01-01",
        "responsibilities": {
            "pl": [
                "Wsparcie techniczne użytkowników",
                "Wdrażanie nowych użytkowników do systemu IT",
                "Tworzenie wizualizacji w celu komunikacji wyników",
                "Szkolenie pracowników w zakresie obsługi systemów IT",
                "Współpraca z zespołem programistów w celu rozwoju systemu do obsługi zleceń",
                "Bieżąca naprawa komputerów, konfiguracja nowych stanowisk",
                "Pozyskiwanie firm współpracujących w celu likwidacji szkód szybowych",
            ],
            "en": [
                "Technical support for users",
                "Onboarding new users to the IT system",
                "Building visualisations to communicate results",
                "Training staff to use the IT systems",
                "Working with the development team on the order-management system",
                "Day-to-day computer repairs and new workstation setup",
                "Recruiting partner companies to handle windscreen damage claims",
            ],
        },
        "tech": ["Python", "MS Power BI", "MS Excel", "Systemy IT"],
    },
    {
        "job_title": {"pl": "Doradca klienta", "en": "Customer advisor"},
        "company": "RTV euro AGD",
        "start_date": "2016-10-01",
        "end_date": "2017-08-31",
        "responsibilities": {
            "pl": ["Doradztwo w sprzedaży sprzętu RTV i AGD"],
            "en": ["Advising customers on consumer electronics and home appliances"],
        },
        "tech": ["Systemy sprzedażowe", "Obsługa klienta"],
    },
]


SKILLS: list[dict] = [
    {
        "name": {"pl": "Claude i Claude Code", "en": "Claude and Claude Code"},
        "level": 90,
        "keywords": {
            "pl": ["Skille", "Harness", "MCP", "Hooki", "Subagenty", "Workflow CI/CD z agentem"],
            "en": ["Skills", "Harness", "MCP", "Hooks", "Subagents", "Agent-driven CI/CD workflow"],
        },
    },
    {
        "name": "Python",
        "level": 80,
        "keywords": {
            "pl": [
                "Streamlit",
                "Pandas",
                "Web Scraping",
                "Selenium",
                "Langchain",
                "Programowanie funkcyjne i obiektowe",
            ],
            "en": [
                "Streamlit",
                "Pandas",
                "Web Scraping",
                "Selenium",
                "Langchain",
                "Functional and object-oriented programming",
            ],
        },
    },
    {
        "name": "OpenAI API",
        "level": 80,
        "keywords": {
            "pl": ["Agenty", "RAG", "Fine Tuning", "Structured Output", "Web search API"],
            "en": ["Agents", "RAG", "Fine Tuning", "Structured Output", "Web search API"],
        },
    },
    {
        "name": "SQL",
        "level": 60,
        "keywords": ["PostgreSQL", "MySQL", "SQLite", "SQL Server"],
    },
    {
        "name": "Git",
        "level": 70,
        "keywords": ["GitHub", "Branching", "Merging"],
    },
    {
        "name": "Docker",
        "level": 50,
        "keywords": {
            "pl": ["Sieci", "Wolumeny", "Docker Compose"],
            "en": ["Networks", "Volumes", "Docker Compose"],
        },
    },
    {
        "name": "Django",
        "level": 70,
        "keywords": ["MTV", "Django ORM"],
    },
]


CERTS: list[dict] = [
    {
        "title": {"pl": "Data Science Bootcamp w Python", "en": "Data Science Bootcamp in Python"},
        "issuer": "Udemy",
        "date": "2024-02-01",
    },
    {
        "title": {
            "pl": "Certyfikat językowy B2 - język angielski",
            "en": "English language certificate, level B2",
        },
        "issuer": {"pl": "SPNJO Uniwersytet Śląski", "en": "SPNJO, University of Silesia"},
        "date": "2019-02-01",
    },
    {
        "title": {
            "pl": "E14. Tworzenie aplikacji internetowych i baz danych oraz administrowanie bazami",
            "en": "E14. Building web applications and databases, and database administration",
        },
        "issuer": {"pl": "Ośrodek Egzaminacyjny", "en": "Vocational examination centre"},
        "date": "2016-08-01",
    },
    {
        "title": {
            "pl": "E13. Projektowanie lokalnych sieci komputerowych i administrowanie sieciami",
            "en": "E13. Designing local computer networks and network administration",
        },
        "issuer": {"pl": "Ośrodek Egzaminacyjny", "en": "Vocational examination centre"},
        "date": "2015-08-01",
    },
    {
        "title": {
            "pl": "E12. Montaż i eksploatacja komputerów osobistych oraz urządzeń peryferyjnych",
            "en": "E12. Assembling and maintaining personal computers and peripherals",
        },
        "issuer": {"pl": "Ośrodek Egzaminacyjny", "en": "Vocational examination centre"},
        "date": "2014-11-01",
    },
]


PROJECTS: list[dict] = [
    {
        "title": "Python Digest Polska",
        "description": {
            "pl": "Dwutygodniowy newsletter o ekosystemie Pythona po polsku: przegląd artykułów, tutoriali, bibliotek i książek. W selekcji linków i przygotowaniu wstępnych opisów do nich pomaga mi AI, a ostateczny wybór i redakcja należą do mnie. Strona z archiwum wydań, wpisami i wyszukiwarką, zapisy na newsletter oraz wysyłka wydań z panelu administracyjnego.",
            "en": "A biweekly Polish-language newsletter about the Python ecosystem: a round-up of articles, tutorials, libraries and books. AI helps me shortlist links and draft their descriptions; the final selection and editing are mine. The site has an issue archive, posts and search, newsletter sign-up, and sending issues from the admin panel.",
        },
        "address": "https://pythondigest.toadres.pl/",
        "tech": ["Python", "Django", "PostgreSQL", "Docker", "AI"],
        "photo_urls": [
            "static/img/python-digest-strona-glowna.webp",
            "static/img/python-digest-wydanie.webp",
        ],
        "featured": True,
    },
    {
        "title": {"pl": "Domowa biblioteka", "en": "Home Library"},
        "description": {
            "pl": "Aplikacja PWA do katalogowania domowej kolekcji książek i gier planszowych: miejsca na półkach, skanowanie kodów ISBN/EAN, automatyczne pobieranie metadanych i okładek, wypożyczenia, oceny oraz zapowiedzi wydawnicze z powiadomieniami e-mail.",
            "en": "A PWA for cataloguing a home collection of books and board games: shelf locations, ISBN/EAN scanning, automatic metadata and cover lookup, loans, ratings, and upcoming releases with email alerts.",
        },
        "address": "https://biblioteczka.toadres.pl/",
        # Checked every 5 minutes: one light request instead of the redirect to the login page.
        "status_url": "https://biblioteczka.toadres.pl/health",
        "access_on_request": True,
        "tech": ["SvelteKit", "TypeScript", "SQLite", "Tailwind CSS", "Playwright", "Docker"],
        "photo_urls": [
            "static/img/biblioteczka-zapowiedzi.webp",
            "static/img/biblioteczka-katalog.webp",
        ],
        "featured": True,
    },
    {
        "title": {
            "pl": "Aplikacja Django do oglądania streamów z wydarzeń sportowych oraz śledzenia wyników na żywo",
            "en": "Django app for watching sports streams and following live scores",
        },
        "description": {
            "pl": "Aplikacja umożliwiająca oglądanie streamów z wydarzeń sportowych oraz śledzenie wyników na żywo. Aplikacja została stworzona z użyciem frameworka Django i wykorzystuje API do pobierania danych o wydarzeniach sportowych.",
            "en": "An app for watching sports event streams and following live scores. Built with Django, using an API for sports event data.",
        },
        "address": "https://mecze.byst.re/",
        "offline": True,
        "tech": ["Python", "Django", "Tailwind CSS", "PostgreSQL"],
        "photo_urls": [
            "static/img/zrzut-ekranu-2026-02-22-103539.webp",
            "static/img/zrzut-ekranu-2026-02-22-1036211.webp",
        ],
    },
    {
        "title": {
            "pl": "Skrypt do wysyłania powiadomień mailowych z API Too Good To Go",
            "en": "Email alerts from the Too Good To Go API",
        },
        "description": {
            "pl": "Projekt polegający na napisaniu systemu powiadomień z użyciem API aplikacji Too Good To Go. Aplikacja pozwala na zarządzanie konfiguracją skryptu z poziomu przeglądarki. Jest hostowana z użyciem Raspberry Pi.",
            "en": "A notification system built on the Too Good To Go app's API, with the script's configuration managed from the browser. Hosted on a Raspberry Pi.",
        },
        "tech": ["Python", "Streamlit", "Raspberry Pi"],
        "photo_urls": [
            "static/img/zrzut-ekranu-2025-09-22-220324.webp",
            "static/img/zrzut-ekranu-2025-09-22-215653.webp",
        ],
    },
    {
        "title": {
            "pl": "Aplikacja do śledzenia cen z funkcją powiadomień mailowych",
            "en": "Price tracker with email alerts",
        },
        "description": {
            "pl": "Aplikacja umożliwiająca śledzenie zmian cen produktów. Jeżeli cena spada poniżej zadeklarowanej przez użytkownika to wówczas otrzymuje on e-mail z powiadomieniem. Ceny pobierane są ze stron z użyciem web scrapingu.",
            "en": "Tracks product prices and emails the user when a price drops below their target. Prices are collected from shop pages with web scraping.",
        },
        "tech": ["Python", "Streamlit", "PostgreSQL", "Raspberry Pi"],
        "photo_urls": [
            "static/img/zrzut-ekranu-2025-09-22-221224.webp",
        ],
    },
    {
        "title": {
            "pl": "Aplikacja do zbierania informacji na temat podróży",
            "en": "Travel research assistant",
        },
        "description": {
            "pl": "Aplikacja umożliwiająca zbieranie informacji na temat podróży, takich jak miejsca, ceny lotów, ceny transportu na miejscu i inne. Aplikacja opiera się o Structured output i Web search z API OpenAI",
            "en": "Gathers travel information such as places to see, flight prices and local transport costs. Built on Structured Outputs and web search from the OpenAI API.",
        },
        "tech": ["Python", "Streamlit", "OpenAI API", "Raspberry Pi"],
        "photo_urls": [
            "static/img/zrzut-ekranu-2025-09-23-212411.webp",
            "static/img/zrzut-ekranu-2025-09-23-212151.webp",
        ],
    },
]
