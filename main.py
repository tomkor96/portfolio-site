import datetime as dt
import streamlit as st

from typing import List

from data import EXPERIENCE, PROFILE, CERTS, SKILLS, EDUCATION, PROJECTS


def setup_page():
    """Setup page"""
    st.set_page_config(
        page_title="tkoralewski - Tomasz Koralewski Portfolio",
        layout="wide",
        page_icon="✨",
        menu_items={
            "Get Help": None,
            "Report a Bug": None,
            "About": "Portfolio wykonane z użyciem Streamlit.",
        },
    )


def chips(items: List[str]) -> str:
    """Creates a chip-style representation of a list of items."""
    return ", ".join(
        [
            f"<span class='chip'>{st.session_state.get('_emoji_map', {}).get(item.lower(), '')} {item}</span>"
            for item in items
        ]
    )


def collect_all_tech() -> List[str]:
    """Collect all unique technologies from experience and skills."""
    tech = set()
    for e in EXPERIENCE:
        tech.update(e.get("tech", []))

    for s in SKILLS:
        tech.add(s.get("name", ""))
    return sorted(list(tech))


def show_side_bar():
    """Shows the sidebar content"""
    with st.sidebar:
        st.title("tkoralewski")
        st.write(
            "Mam na imię Tomek i lubię rozwiązywać problemy z użyciem technologii."
        )

        st.caption("Kontakt")
        st.markdown(
            f"""
                    - 🪧 [Email](mailto:{PROFILE.get("email", "")})
                    - 🔗 [LinkedIn]({PROFILE.get("linkedin", "")})
                    - ⌨️ [GitHub]({PROFILE.get("github", "")})
                    """
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        cv_path = PROFILE.get("cv_path", "")
        if cv_path:
            try:
                with open(cv_path, "rb") as pdf_file:
                    st.download_button(
                        label="📄 Pobierz CV",
                        data=pdf_file,
                        file_name="CV_Tomasz_Koralewski.pdf",
                        mime="application/pdf",
                    )
            except FileNotFoundError:
                st.button(label="📄 Pobierz CV (niedostępne)", disabled=True)
        else:
            st.button(label="📄 Pobierz CV", disabled=True)


def show_experience():
    """Shows work experience"""
    st.subheader("Doświadczenie")
    for exp in EXPERIENCE:
        st.write(f"##### 🧑‍💼 {exp.get('job_title', '')}")
        st.write(
            f"**🏢 {exp.get('company', '')}** | 📅 {exp.get('start_date', '')} - {exp.get('end_date', 'Obecnie')}"
        )
        for resp in exp.get("responsibilities", []):
            st.write(f"- {resp}")
        with st.container():
            st.write(
                f"**Technologie:** {chips(exp.get('tech', []))}", unsafe_allow_html=True
            )
        st.markdown("---")


def show_about_me():
    """Shows information about me"""
    st.subheader("O mnie")
    st.write(
        "Jestem inżynierem ds. danych produktowych z doświadczeniem w automatyzacji procesów oraz analizie danych."
    )


def show_education():
    """Shows education"""
    st.subheader("Edukacja")
    for edu in EDUCATION:
        st.write(f"##### 🎓 {edu.get('degree', '')} - {edu.get('field', '')}")
        st.write(
            f"**🏫 {edu.get('institution', '')}** | 📅 {edu.get('start_date', '')} - {edu.get('end_date', 'Obecnie')}"
        )
        st.write(f"**Specjalizacja:** {edu.get('specialization', '')}")
        st.write(f"**Poziom:** {edu.get('level', '')}")

        st.markdown("---")


def show_skills():
    """Shows skills"""
    st.subheader("Umiejętności")
    for s in SKILLS:
        col1, col2 = st.columns([1, 3])
        with col1:
            if s.get("keywords"):
                st.caption(", ".join(s.get("keywords", [])))
        with col2:
            st.progress(s.get("level", 0), text=s.get("name", ""))


def show_projects():
    """Shows projects"""
    for project in PROJECTS:
        with st.expander(f"💡 {project.get('title', '')}", expanded=False):
            st.write(f"📄 **Opis:** {project.get('description', '')}")
            address = project.get("address", "")
            if address:
                st.write(f"🌍 **Link:** [{address}]({address})")
            st.write(
                f"🔧 **Technologie:** {chips(project.get('tech', []))}",
                unsafe_allow_html=True,
            )

            photos = project.get("photo_urls", [])
            if photos:
                st.write("📷 **Galeria:**")

                num_cols = 3 if len(photos) > 4 else 2

                for i in range(0, len(photos), num_cols):
                    cols = st.columns(num_cols)
                    for j, photo_url in enumerate(photos[i : i + num_cols]):
                        with cols[j]:
                            st.image(photo_url)


def show_certs():
    """Shows certifications"""
    st.subheader("Certyfikaty")
    for cert in CERTS:
        st.write(f"##### {cert.get('title', '')}")
        st.write(f"🏫 **Wydawca:** {cert.get('issuer', '')}")
        st.write(f"📅 **Data:** {cert.get('date', '')}")

        st.markdown("---")


def main():
    setup_page()
    show_side_bar()

    left, right = st.columns([3, 1])

    with left:
        st.markdown(f'## {PROFILE.get("name", "")}')
        st.markdown(f'{PROFILE.get("role", "")}')
        st.markdown(f'📍 {PROFILE.get("location", "")}')
    with right:
        st.metric("Doświadczenie", value=f"{max(1, dt.datetime.now().year - 2024)}+")

    experience_tab, education_tab, skills_tab, projects_tab, certs_tab, about_tab = (
        st.tabs(
            [
                "💼 Doświadczenie",
                "🎓 Edukacja",
                "🛠️ Umiejętności",
                "📁 Projekty",
                "📜 Certyfikaty",
                "🙋 O mnie",
            ]
        )
    )

    with experience_tab:
        show_experience()

    with education_tab:
        show_education()

    with skills_tab:
        show_skills()

    with projects_tab:
        show_projects()

    with certs_tab:
        show_certs()

    with about_tab:
        show_about_me()


if __name__ == "__main__":
    main()
