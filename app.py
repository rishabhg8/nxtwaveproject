import streamlit as st
import requests
import re

# --- Branding and Theme ---
st.set_page_config(page_title="Career & Salary Estimator – Powered by AI", layout="centered")

# Add a logo/banner (replace with your logo path or URL)
st.image("https://nxtwave.imgix.net/ccbp-website/ccbp_logo.png", width=180)

# Inject IBM Plex Mono font via custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'IBM Plex Mono', monospace !important;
    }
    .stButton>button, .stTextInput>div>input, .stTextArea textarea, .stSelectbox>div>div, .stMultiSelect>div>div, .stSlider>div {
        font-family: 'IBM Plex Mono', monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Career & Salary Estimator – Powered by AI")

# --- Progress Bar ---
TOTAL_STEPS = 9
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

st.progress((st.session_state.step-1)/TOTAL_STEPS)

def next_step():
    st.session_state.step += 1

def reset():
    st.session_state.step = 1
    st.session_state.user_data = {}
    st.session_state.selected_popular_langs = set()

st.button("Start Over", on_click=reset)

# --- Modularized Form Steps ---
def step_education():
    with st.form(key="form1", clear_on_submit=False):
        st.header("Step 1: Your Highest Education Qualification")
        education = st.selectbox(
            "Select your highest qualification:",
            ["High School", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD", "Other"],
            help="This helps us tailor recommendations to your background."
        )
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.user_data['education'] = education
            next_step()
            st.rerun()

def step_experience():
    with st.form(key="form2", clear_on_submit=False):
        st.header("Step 2: Previous Work Experience")
        experience = st.text_input(
            "Do you have any work experience?",
            placeholder="e.g., 1 year as a QA tester, No experience",
            help="Include internships, part-time, or full-time roles."
        )
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.user_data['experience'] = experience
            next_step()
            st.rerun()

def step_tech_knowledge():
    st.header("Step 3: Previous Technical Knowledge")
    popular_langs = [
        "Python", "JavaScript", "Java", "C#", "C++", "TypeScript", "Go", "Ruby", "PHP", "SQL", "HTML/CSS"
    ]
    if 'selected_popular_langs' not in st.session_state:
        st.session_state.selected_popular_langs = set()
    def toggle_lang(lang):
        if lang in st.session_state.selected_popular_langs:
            st.session_state.selected_popular_langs.remove(lang)
        else:
            st.session_state.selected_popular_langs.add(lang)
    st.write("**Select from popular/in-demand languages:**")
    cols = st.columns(4)
    for i, lang in enumerate(popular_langs):
        with cols[i % 4]:
            if lang in st.session_state.selected_popular_langs:
                if st.button(f"✅ {lang}", key=f"pop_{lang}"):
                    toggle_lang(lang)
            else:
                if st.button(lang, key=f"pop_{lang}"):
                    toggle_lang(lang)
    st.write("")
    st.write("**Or search and add any programming language(s):**")
    all_langs = popular_langs + [
        "Kotlin", "Swift", "Scala", "Rust", "Dart", "Perl", "MATLAB", "R", "Objective-C", "Shell", "Assembly", "Other"
    ]
    custom_langs = st.multiselect(
        "Search or add languages:",
        options=sorted(set(all_langs)),
        default=list(st.session_state.selected_popular_langs),
        key="custom_langs"
    )
    tech_knowledge = list(set(custom_langs) | st.session_state.selected_popular_langs)
    with st.form(key="form3", clear_on_submit=False):
        submitted = st.form_submit_button("Next")
        if submitted:
            if not tech_knowledge:
                st.warning("Please select at least one programming language or skill.")
                st.stop()
            st.session_state.user_data['tech_knowledge'] = tech_knowledge
            next_step()
            st.rerun()

def step_interests():
    with st.form(key="form4", clear_on_submit=False):
        st.header("Step 4: Main Interests in Tech or IT")
        interests = st.text_area(
            "What are your main interests in tech or IT?",
            placeholder="e.g., Web Development, Data Analytics, Automation, Software Testing",
            help="This helps us recommend the best track for you."
        )
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.user_data['interests'] = interests
            next_step()
            st.rerun()

def step_goal():
    with st.form(key="form5", clear_on_submit=False):
        st.header("Step 5: Your Career Goal")
        goal = st.selectbox(
            "What is your main career goal?",
            ["Software Developer", "Data Analyst", "QA/Automation Tester", "Full Stack Developer", "Other"],
            help="Choose the role you aspire to."
        )
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.user_data['goal'] = goal
            next_step()
            st.rerun()

def step_companies():
    with st.form(key="form6", clear_on_submit=False):
        st.header("Step 6: Dream Companies or Industries")
        companies = st.text_input(
            "Any dream companies or industries?",
            placeholder="e.g., Amazon, Microsoft, FinTech, Healthcare",
            help="Optional, but helps us personalize your report."
        )
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.user_data['companies'] = companies
            next_step()
            st.rerun()

def step_learning_style():
    with st.form(key="form7", clear_on_submit=False):
        st.header("Step 7: Preferred Learning Style")
        learning_style = st.radio(
            "Preferred learning style:",
            ["Self-paced", "Instructor-led", "Hybrid", "No preference"],
            help="How do you prefer to learn?"
        )
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.user_data['learning_style'] = learning_style
            next_step()
            st.rerun()

def step_time_commitment():
    with st.form(key="form8", clear_on_submit=False):
        st.header("Step 8: Time Commitment")
        time_commitment = st.slider(
            "How many hours per week can you commit?",
            min_value=1, max_value=40, value=10,
            help="This helps us recommend a realistic upskilling plan."
        )
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.user_data['time_commitment'] = time_commitment
            next_step()
            st.rerun()

def step_constraints():
    with st.expander("Step 9: Other Preferences or Constraints (Optional)"):
        with st.form(key="form9", clear_on_submit=False):
            st.header("Other Preferences or Constraints")
            other_constraints = st.text_area(
                "Any other preferences or constraints?",
                placeholder="e.g., Only remote courses, Need weekend classes, etc.",
                help="Optional, but helps us personalize your plan."
            )
            submitted = st.form_submit_button("Save Preferences")
            if submitted:
                st.session_state.user_data['other_constraints'] = other_constraints
    # Move the 'See Suggestions' button outside the expander
    if st.button("See Suggestions"):
        # Ensure the value is set even if user didn't open the expander
        if 'other_constraints' not in st.session_state.user_data:
            st.session_state.user_data['other_constraints'] = ""
        next_step()
        st.rerun()

def format_inr(amount):
    try:
        num = int(amount.replace(",", ""))
        s = str(num)
        if len(s) <= 3:
            return s
        else:
            last3 = s[-3:]
            rest = s[:-3]
            parts = []
            while len(rest) > 2:
                parts.append(rest[-2:])
                rest = rest[:-2]
            if rest:
                parts.append(rest)
            return ','.join(parts[::-1]) + ',' + last3
    except Exception:
        return amount

# --- Main Stepper Logic ---
if st.session_state.step == 1:
    step_education()
elif st.session_state.step == 2:
    step_experience()
elif st.session_state.step == 3:
    step_tech_knowledge()
elif st.session_state.step == 4:
    step_interests()
elif st.session_state.step == 5:
    step_goal()
elif st.session_state.step == 6:
    step_companies()
elif st.session_state.step == 7:
    step_learning_style()
elif st.session_state.step == 8:
    step_time_commitment()
elif st.session_state.step == 9:
    step_constraints()

# --- Recommendation Preview ---
elif st.session_state.step == 10:
    st.header("Your Career & Salary Estimation")
    user_data = st.session_state.user_data
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Your Profile Summary")
        st.markdown(f"""
        **Education:** {user_data.get('education', '')}  
        **Experience:** {user_data.get('experience', '')}  
        **Technical Knowledge:** {', '.join(user_data.get('tech_knowledge', []))}  
        **Interests:** {user_data.get('interests', '')}  
        **Career Goal:** {user_data.get('goal', '')}  
        **Dream Companies/Industries:** {user_data.get('companies', '')}  
        **Learning Style:** {user_data.get('learning_style', '')}  
        **Time Commitment:** {user_data.get('time_commitment', '')} hours/week  
        **Other Constraints:** {user_data.get('other_constraints', '')}
        """)
    with col2:
        st.subheader(":sparkles: AI-Powered Recommendation")
        try:
            response = requests.post(
                "http://127.0.0.1:8000/recommend",
                json=user_data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            report = result.get("report", "No report received.")
            # Extract only Dream Job and salary amount
            dream_job = ""
            salary_potential = ""
            if 'Dream Job:' in report and 'Salary Potential:' in report:
                dream_job = report.split('Dream Job:')[1].split('Salary Potential:')[0].strip()
                salary_section = report.split('Salary Potential:')[1].replace('---', '').strip()
                salary_match = re.search(r'\b\d[\d,\.]*\b', salary_section)
                if salary_match:
                    salary_potential = salary_match.group(0)
                else:
                    salary_potential = salary_section.split(" ")[0] if salary_section else ""
            dream_job_display = dream_job if dream_job.strip() else '<span style="color:#888">(No job title returned)</span>'
            salary_display = format_inr(salary_potential) if salary_potential.strip() else '<span style="color:#888">(No salary returned)</span>'
            if salary_potential.strip():
                salary_display = f'₹ {salary_display}'
            st.markdown(
                f"""
                <div style='padding:22px 18px 16px 18px;border-radius:14px;box-shadow:0 2px 8px #0006;font-family:"IBM Plex Mono",monospace;'>
                <h4 style='margin-bottom:8px;'>🚀 Dream Job</h4>
                <div style='margin-bottom:18px;font-size:1.2em;font-weight:600;'>{dream_job_display} <span style="font-size:1.2em;">💼</span></div>
                <h4 style='margin-bottom:8px;'>💰 Salary Potential</h4>
                <div style='font-size:1.5em;font-weight:700;'>{salary_display}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # CTA Button as a link
            st.markdown(
                """
                <a href="https://www.ccbp.in/intensive" target="_blank">
                    <button style='background-color:#ee4822;color:white;padding:0.7em 1.5em;border:none;border-radius:6px;font-size:1.1em;font-family:"IBM Plex Mono",monospace;cursor:pointer;margin-top:1em;'>🚀 Upskill with Our Courses</button>
                </a>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Failed to get recommendation from backend: {e}")
    # Footer
    st.markdown(
        "<hr style='margin-top:2em'>"
        "<div style='text-align:center; color: #888; font-family: IBM Plex Mono, monospace; font-size: 0.95em;'>"
        "Made with ❤️ by Your Team | <a href='mailto:contact@yourdomain.com'>Contact Us</a>"
        "</div>",
        unsafe_allow_html=True
    ) 