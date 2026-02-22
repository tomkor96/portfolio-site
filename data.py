from typing import List, Dict, Union

PROFILE: Dict[str, str] = {
    "name": "Tomasz Koralewski",
    "role": "Inżynier ds. danych produktowych",
    "location": "Polska, Tarnowskie Góry",
    "email": "tomaszkoralewski1@gmail.com",
    "linkedin": "https://www.linkedin.com/in/tomasz-koralewski-a7233a154/",
    "github": "https://github.com/tomkor96",
    "cv_path": "docs/Tomasz_Koralewski_CV.pdf",
    "skills": [
        "Python",
        "Analiza danych",
        "SQL",
        "Streamlit",
        "Docker",
        "Akeneo",
        "Postman",
        "API OpenAI",
        "Web Scraping",
        "Git",
    ],
}

EDUCATION: List[Dict[str, str]] = [
    {
        "institution": "Uniwersytet Śląski w Katowicach",
        "degree": "Magister",
        "field": "Socjologia",
        "specialization": "HR w nowoczesnej organizacji",
        "start_date": "2020",
        "end_date": "2022",
        "level": "wyższe",
    },
    {
        "institution": "Uniwersytet Śląski w Katowicach",
        "degree": "Licencjat",
        "field": "Zarządzanie zasobami ludzkimi",
        "specialization": "",
        "start_date": "2017",
        "end_date": "2020",
        "level": "wyższe",
    },
    {
        "institution": 'ZSTiO "Mechanik" w Tarnowskich Górach',
        "degree": "Technik informatyk",
        "field": "Informatyka",
        "specialization": "",
        "start_date": "2012",
        "end_date": "2016",
        "level": "średnie",
    },
]


EXPERIENCE: List[Dict[str, str]] = [
    {
        "job_title": "Inżynier ds. danych produktowych",
        "company": "Senetic Global Services",
        "location": "Polska",
        "start_date": "2024-08-01",
        "responsibilities": [
            "Automatyczne pobieranie danych ze źródeł takich jak API lub strony internetowe",
            "Zarządzanie bazą produktową z użyciem Akeneo i SQL",
            "Obróbka danych i dostosowanie ich do określonych wymagań i standardów",
            "Tworzenie materiałów takich jak opisy produktowe z wykorzystaniem API OpenAI",
        ],
        "tech": ["Python", "SQL", "Pandas", "Akeneo", "API OpenAI"],
    },
    {
        "job_title": "Pełnomocnik Beneficjenta programu Czyste Powietrze",
        "company": "Ekoconsult.pl",
        "location": "Polska",
        "start_date": "2023-01-01",
        "end_date": "2024-07-31",
        "responsibilities": [
            "Własna działalność nierejestrowana polegająca na pozyskiwaniu dotacji z programu Czyste Powietrze w imieniu klientów",
        ],
        "tech": ["MS Excel", "Systemy rządowe"],
    },
    {
        "job_title": "Pracownik obsługi sprzedaży internetowej",
        "company": "Auto Kram sp. j.",
        "location": "Polska",
        "start_date": "2021-01-01",
        "responsibilities": [
            "Zarządzanie sprzedażą internetową",
            "Wystawianie aukcji na platformie Allegro, automatyzacja sprzedaży w aplikacji Baselinker",
        ],
        "tech": ["Allegro", "Baselinker", "MS Excel"],
    },
    {
        "job_title": "Copywriter",
        "company": "EACTIVE",
        "location": "Polska",
        "start_date": "2019-01-01",
        "end_date": "2020-12-31",
        "responsibilities": [
            "Pisanie tekstów blogowych oraz tekstów optymalizacyjnych opartych o promocję",
            "Wykorzystanie słów kluczowych pomagających znaleźć stronę zleceníodawcy poprzez wyszukiwarki",
        ],
        "tech": ["SEO", "Content Marketing", "Google Analytics"],
    },
    {
        "job_title": "Koordynator ds. rozwoju i innowacji",
        "company": "Autoszyby.pl sp. z o.o.",
        "location": "Polska",
        "start_date": "2018-08-01",
        "end_date": "2023-01-01",
        "responsibilities": [
            "Wsparcie techniczne użytkowników",
            "Wdrażanie nowych użytkowników do systemu IT",
            "Tworzenie wizualizacji w celu komunikacji wyników",
            "Szkolenie pracowników w zakresie obsługi systemów IT",
            "Współpraca z zespołem programistów w celu rozwoju systemu do obsługi zleceń",
            "Bieżąca naprawa komputerów, konfiguracja nowych stanowisk",
            "Pozyskiwanie firm współpracujących w celu likwidacji szkód szybrowych",
        ],
        "tech": ["Python", "MS Power BI", "MS Excel", "Systemy IT"],
    },
    {
        "job_title": "Doradca klienta",
        "company": "RTV euro AGD",
        "location": "Polska",
        "start_date": "2016-10-01",
        "end_date": "2017-08-31",
        "responsibilities": [
            "Doradztwo w sprzedaży sprzętu RTV i AGD",
        ],
        "tech": ["Systemy sprzedażowe", "Obsługa klienta"],
    },
]


SKILLS: List[Dict[str, Union[str, int, List[str]]]] = [
    {
        "name": "Python",
        "level": 80,
        "keywords": [
            "Streamlit",
            "Pandas",
            "Web Scraping",
            "Selenium",
            "Langchain",
            "Programowanie funkcyjne i obiektowe",
        ],
    },
    {
        "name": "OpenAI API",
        "level": 80,
        "keywords": [
            "Agenty",
            "RAG",
            "Fine Tuning",
            "Structured Output",
            "Web search API",
        ],
    },
    {
        "name": "SQL",
        "level": 60,
        "keywords": ["PostgreSQL", "MySQL", "SQLite", "SQL Server"],
    },
    {
        "name": "MS Excel",
        "level": 60,
        "keywords": ["Excel", "Pivot", "Power Query"],
    },
    {
        "name": "Git",
        "level": 60,
        "keywords": ["GitHub", "Branching", "Merging"],
    },
    {
        "name": "Docker",
        "level": 50,
        "keywords": ["Sieci", "Wolumeny", "Docker Compose"],
    },
    {
        "name": "Django",
        "level": 40,
        "keywords": ["MTV", "Django ORM"],
    },
]


CERTS: List[Dict[str, str]] = [
    {
        "title": "Data Science Bootcamp w Python",
        "issuer": "Udemy",
        "date": "2024-02-01",
    },
    {
        "title": "Certyfikat językkowy B2 - język angielski",
        "issuer": "SPNJO Uniwersytet Śląski",
        "date": "2019-02-01",
    },
    {
        "title": "E14. Tworzenie aplikacji internetowych i baz danych oraz administrowanie bazami",
        "issuer": "Ośrodek Egzaminacyjny",
        "date": "2016-08-01",
    },
    {
        "title": "E13. Projektowanie lokalnych sieci komputerowych i administrowanie sieciami",
        "issuer": "Ośrodek Egzaminacyjny",
        "date": "2015-08-01",
    },
    {
        "title": "E12. Montaż i eksploatacja komputerów osobistych oraz urządzeń peryferyjnych",
        "issuer": "Ośrodek Egzaminacyjny",
        "date": "2014-11-01",
    },
]


PROJECTS: List[Dict[str, Union[str, int]]] = [
    {
        "title": "Aplikacja Django do oglądania streamów z wydarzeń sportowych oraz śledzenia wyników na żywo",
        "description": "Aplikacja umożliwiająca oglądanie streamów z wydarzeń sportowych oraz śledzenie wyników na żywo. Aplikacja została stworzona z użyciem frameworka Django i wykorzystuje API do pobierania danych o wydarzeniach sportowych.",
        "address": "https://mecze.byst.re/",
        "tech": ["Python", "Django", "Tailwind CSS", "PostgreSQL"],
        "photo_urls": [
            "https://i.ibb.co/B2DxgxQL/Zrzut-ekranu-2026-02-22-103539.png",
            "https://i.ibb.co/CXnZbhs/Zrzut-ekranu-2026-02-22-1036211.png",
        ],
    },
    {
        "title": "Skrypt do wysyłania powiadomień mailowych z API Too Good To Go",
        "description": """Projekt polegający na napisaniu systemu powiadomień z użyciem API aplikacji To Good To Go. Aplikacja pozwala na zarządzanie konfiguracją skryptu z poziomu przeglądarki. Jest hostowana z użyciem Raspberry Pi.""",
        "tech": ["Python", "Streamlit", "Raspberry Pi"],
        "photo_urls": [
            "https://i.ibb.co/cS7XXgnw/Zrzut-ekranu-2025-09-22-220324.png",
            "https://i.ibb.co/yB0Wn9Rg/Zrzut-ekranu-2025-09-22-215653.png",
        ],
    },
    {
        "title": "Aplikacja do śledzenia cen z funkcją powiadomień mailowych",
        "description": "Aplikacja umożliwiająca śledzenie zmian cen produktów. Jeżeli cena spada poniżej zadeklarowanej przez użytkownika to wówczas otrzymauje on e-mail z powiadommieniem. Ceny pobierane są ze stron z użyciem web scrapingu.",
        "tech": ["Python", "Streamlit", "PostgreSQL", "Raspberry Pi"],
        "photo_urls": [
            "https://i.ibb.co/YT46F6Vv/Zrzut-ekranu-2025-09-22-221224.png",
            "https://i.ibb.co/zW5XXj0H/Zrzut-ekranu-2025-09-23-212622.png",
        ],
    },
    {
        "title": "Aplikacja do zbierania informacji na temat podróży",
        "description": "Aplikacja umożliwiająca zbieranie informacji na temat podróży, takich jak miejsca, ceny lotów, ceny transportu na miejscu i inne. Aplikacja opiera się o Structured output i Web search z API OpenAI",
        "tech": ["Python", "Streamlit", "OpenAI API", "Raspberry Pi"],
        "photo_urls": [
            "https://i.ibb.co/NdwBqcnb/Zrzut-ekranu-2025-09-23-212411.png",
            "https://i.ibb.co/DDfKPdTJ/Zrzut-ekranu-2025-09-23-212151.png",
        ],
    },
    {
        "title": "Kalkulator alternatywnych produktów e-commerce",
        "description": "Kalkulator alternatywnych produktów dla e-commerce. Pozwala określić atrybuty, które muszą mieć dokładnie takie same wartości oraz atrybuty, których wartości powinny być podobne. Na podstawie tak zafiltrowanych produktów otrzymujemy najbardziej podobne produkty, które następnie są wyświetlane jako zamienniki do produktów już niedostępnych.",
        "tech": ["Python", "Docker", "MySQL", "SQL Server"],
    },
]
