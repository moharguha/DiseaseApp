import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime
import os

# --- Disease dictionary ---
disease_dict = {
   "flu": {
       "symptoms": ["fever", "cough", "sore throat", "fatigue"],
       "prevention": ["Get vaccinated yearly", "Wash hands regularly", "Avoid close contact with sick people"]
   },
   "malaria": {
       "symptoms": ["timed fever", "chills", "sweating", "severe headache"],
       "prevention": ["Use mosquito nets", "Apply insect repellent", "Drain stagnant water"]
   },
   "dengue": {
       "symptoms": ["timed fever", "severe headache", "pain behind eyes", "joint pain", "muscle pain", "rash", "nausea"],
       "prevention": ["Prevent mosquito bites", "Avoid water collection around home", "Use protective clothing"]
   },
   "typhoid": {
       "symptoms": ["timed fever", "abdominal pain", "headache", "loss of appetite"],
       "prevention": ["Drink boiled/filtered water", "Wash fruits & vegetables", "Maintain hygiene"]
   },
   "covid-19": {
       "symptoms": ["fever", "cough", "loss of taste", "shortness of breath", "fatigue"],
       "prevention": ["Wear masks in crowded areas", "Maintain distance", "Wash hands often", "Get vaccinated"]
   },
   "chikungunya": {
         "symptoms": ["fever", "joint pain", "headache", "muscle pain", "rash"],
         "prevention": ["Use mosquito repellents", "Wear long-sleeved clothing", "Eliminate mosquito breeding sites"]
    },
    "tuberculosis": {
        "symptoms": ["persistent cough", "chest pain", "coughing blood", "weight loss", "night sweats", "fatigue"],
        "prevention": ["Get vaccinated with BCG", "Avoid close contact with TB patients", "Ensure proper ventilation"]
    },
    "asthma": {
        "symptoms": ["shortness of breath", "chest tightness", "wheezing", "cough", "difficulty breathing"],
        "prevention": ["Avoid triggers like smoke and allergens", "Use prescribed inhalers", "Maintain clean air environment"]
    },
    "pneumonia": {
        "symptoms": ["fever", "cough with phlegm", "chest pain", "shortness of breath", "fatigue", "chills"],
        "prevention": ["Get vaccinated", "Avoid smoking", "Wash hands frequently", "Seek prompt treatment for respiratory infections"]
    },
    "diabetes": {
        "symptoms": ["frequent urination", "increased thirst", "increased hunger", "fatigue", "blurred vision", "slow healing wounds"],
        "prevention": ["Maintain healthy diet", "Exercise regularly", "Monitor blood sugar levels"]
    },
    "hypertension": {
        "symptoms": ["headache", "dizziness", "nosebleeds", "shortness of breath", "chest pain", "fatigue"],
        "prevention": ["Reduce salt intake", "Exercise regularly", "Monitor blood pressure", "Avoid stress"]
    },
    "migraine": {
        "symptoms": ["severe headache", "nausea", "vomiting", "sensitivity to light", "sensitivity to sound", "visual disturbances"],
        "prevention": ["Avoid triggers", "Manage stress", "Maintain regular sleep", "Stay hydrated"]
    },
    "jaundice": {
        "symptoms": ["yellow skin", "yellow eyes", "dark urine", "abdominal pain", "fatigue", "nausea"],
        "prevention": ["Avoid contaminated food and water", "Practice good hygiene", "Get vaccinated for hepatitis"]
    },
    "chickenpox": {
        "symptoms": ["itchy rash", "blisters", "fever", "loss of appetite", "tiredness", "headache"],
        "prevention": ["Get vaccinated", "Avoid contact with infected people", "Maintain hygiene"]
    },
    "hepatitis": {
        "symptoms": ["fatigue", "nausea", "vomiting", "abdominal pain", "jaundice", "dark urine"],
        "prevention": ["Get vaccinated", "Avoid contaminated food and water", "Practice safe hygiene"]
    },
    "cholera": {
        "symptoms": ["watery diarrhea", "vomiting", "leg cramps", "dehydration", "rapid heartbeat"],
        "prevention": ["Drink clean water", "Practice good sanitation", "Avoid raw or undercooked food"]
    },
    "bronchitis": {
        "symptoms": ["persistent cough", "mucus production", "fatigue", "shortness of breath", "chest pain"],
        "prevention": ["Avoid smoking", "Stay hydrated", "Use humidifiers", "Seek treatment for infections"]
    },
    "measles": {
        "symptoms": ["fever", "dry cough", "runny nose", "rash", "red eyes", "sore throat"],
        "prevention": ["Get vaccinated", "Avoid contact with infected people", "Maintain hygiene"]
    },
    "appendicitis": {
        "symptoms": ["abdominal pain", "loss of appetite", "nausea", "vomiting", "fever", "constipation"],
        "prevention": ["No guaranteed prevention", "Maintain healthy diet", "Seek prompt medical care if symptoms appear"]
    },
    "anemia": {
        "symptoms": ["fatigue", "weakness", "pale skin", "shortness of breath", "dizziness", "cold hands and feet"],
        "prevention": ["Eat iron-rich foods", "Take supplements if prescribed", "Regular health check-ups"]
    },
    "gastroenteritis": {
        "symptoms": ["diarrhea", "vomiting", "cramps", "fever", "nausea", "dehydration"],
        "prevention": ["Practice good hygiene", "Drink clean water", "Avoid contaminated food"]
    },
    "urinary tract infection": {
        "symptoms": ["burning sensation during urination", "frequent urination", "cloudy urine", "strong-smelling urine", "pelvic pain"],
        "prevention": ["Drink plenty of water", "Urinate after intercourse", "Wipe front to back", "Avoid irritating feminine products"]
    },
    "sinusitis": {
        "symptoms": ["facial pain", "nasal congestion", "runny nose", "headache", "fever", "cough"],
        "prevention": ["Avoid upper respiratory infections", "Manage allergies", "Use humidifiers"]
    },
    "eczema": {
        "symptoms": ["itchy skin", "red patches", "swelling", "crusting", "thickened skin"],
        "prevention": ["Moisturize regularly", "Avoid irritants", "Use gentle skin care products", "Manage stress"]
    },
    "psoriasis": {
        "symptoms": ["red patches", "silvery scales", "itchy skin", "dry cracking skin", "joint pain"],
        "prevention": ["Avoid triggers", "Moisturize skin", "Manage stress", "Follow treatment plan"]
    },
    "allergy": {
        "symptoms": ["sneezing", "itchy eyes", "runny nose", "rash", "hives", "swelling"],
        "prevention": ["Avoid known allergens", "Use antihistamines", "Keep environment clean"]
    },
    "food poisoning": {
        "symptoms": ["nausea", "vomiting", "diarrhea", "cramps", "fever", "weakness"],
        "prevention": ["Practice good food hygiene", "Cook food thoroughly", "Avoid cross-contamination"]
    },
    "conjunctivitis": {
        "symptoms": ["red eyes", "itchy eyes", "tearing", "discharge", "swelling", "sensitivity to light"],
        "prevention": ["Avoid touching eyes", "Practice good hygiene", "Avoid sharing personal items"]
    },
    "mumps": {
        "symptoms": ["swollen salivary glands", "fever", "headache", "muscle aches", "fatigue", "loss of appetite"],
        "prevention": ["Get vaccinated", "Avoid contact with infected people", "Maintain hygiene"]
    },
    "rubella": {
        "symptoms": ["rash", "fever", "swollen lymph nodes", "joint pain", "headache", "runny nose"],
        "prevention": ["Get vaccinated", "Avoid contact with infected people", "Maintain hygiene"]
    }
}

# --- Collect all unique symptoms ---
all_symptoms = sorted({s for info in disease_dict.values() for s in info["symptoms"]})

# --- Helper function ---
def match_disease(symptoms):
    results = []
    for disease, info in disease_dict.items():
        disease_symptoms = info["symptoms"]
        matches = set(symptoms).intersection(set(disease_symptoms))
        if matches:
            confidence = round((len(matches) / len(disease_symptoms)) * 100, 2)
            results.append({
                "disease": disease,
                "confidence": confidence,
                "matched": list(matches),
                "prevention": info.get("prevention", [])
            })
    return sorted(results, key=lambda x: x["confidence"], reverse=True)


# --- Page Config ---
st.set_page_config(page_title="Healix Health Tracker", layout="wide")

# --- Custom CSS (green background + styling) ---
st.markdown(
    """
    <style>
    .stApp {background-color: #d9fdd3;} /* Light green */
    h1, h2, h3, h4, h5, h6 {color: #064e3b;} /* Dark green headings */
    .main {padding: 2rem 3rem;}
    .card {background-color: #f5f5f5; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin-bottom: 2rem;}
    .card-col {background-color: #fefefe; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 1rem;}
    .stTabs [role="tab"] {font-weight: bold; font-size: 16px;}
    .big-font { font-size:22px !important; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Front Page ---
st.title("💊 HEALIX :mask:")
st.header("Your Personal Health Assistant")
st.subheader("👋 Hello! Welcome to Healix")
st.write("Track symptoms, wellness, BMI, water intake, and your daily journal. *(For educational purposes only.)*")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Symptom Checker", "📖 Search by Disease", "💧 Health & Wellness", "📔 Journal"])

# ---------- TAB 1: SYMPTOM CHECKER ----------
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Select Symptoms")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_symptoms1 = st.multiselect("Symptoms Group 1", all_symptoms[:len(all_symptoms)//2], key="symptoms1")
    with col2:
        selected_symptoms2 = st.multiselect("Symptoms Group 2", all_symptoms[len(all_symptoms)//2:], key="symptoms2")
    
    selected = selected_symptoms1 + selected_symptoms2
    
    if st.button("Check Disease", key="check_disease"):
        if selected:
            results = match_disease([s.lower() for s in selected])
            if results:
                for r in results:
                    st.markdown(f"### {r['disease'].title()}")
                    st.markdown(f"- **Confidence:** {r['confidence']}%")
                    st.markdown(f"- **Matched Symptoms:** {', '.join(r['matched'])}")
                    if r["prevention"]:
                        st.markdown("**Prevention Tips:**")
                        for tip in r["prevention"]:
                            st.markdown(f"- {tip}")
                    st.markdown("---")
            else:
                st.warning("⚠️ No matching diseases found.")
        else:
            st.info("Please select at least one symptom.")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- TAB 2: DISEASE SEARCH ----------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Search Disease by Name")
    
    disease_name = st.text_input("Enter disease name (e.g., malaria)", key="disease_input")
    if disease_name:
        disease_info = disease_dict.get(disease_name.strip().lower())
        if disease_info:
            st.markdown(f"### {disease_name.title()} Symptoms:")
            for s in disease_info["symptoms"]:
                st.markdown(f"- {s}")
            if "prevention" in disease_info:
                st.markdown("**Prevention Tips:**")
                for tip in disease_info["prevention"]:
                    st.markdown(f"- {tip}")
        else:
            st.error("❌ Disease not found in database.")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- TAB 3: HEALTH & WELLNESS ----------
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("💧 Daily Health & Wellness Records")

    # --- Water Intake Tracker ---
    st.subheader("Water Intake Tracker")
    if "water_log" not in st.session_state:
        st.session_state["water_log"] = []

    if st.button("Add 1 Glass (250ml)", key="add_glass"):
        st.session_state["water_log"].append(datetime.now())

    water_count = len(st.session_state["water_log"])
    st.write(f"Glasses today: {water_count} ({water_count*250} ml)")

    if water_count > 7:
        st.success("Good job! You're well hydrated 💦")
    else:
        st.info("Aim for 8+ glasses daily!")

    if st.session_state["water_log"]:
        daily_data = pd.DataFrame({"time": st.session_state["water_log"]})
        daily_data["hour"] = daily_data["time"].dt.hour

        fig, ax = plt.subplots()
        daily_data["hour"].value_counts().sort_index().plot(kind="bar", ax=ax)
        ax.set_title("Water Intake by Hour")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Glasses")
        st.pyplot(fig)

    # --- BMI Calculator ---
    st.subheader("⚖️ BMI Calculator")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Enter Height (cm)", min_value=50, max_value=250, value=170, key="height")
    with col2:
        weight = st.number_input("Enter Weight (kg)", min_value=10, max_value=200, value=65, key="weight")

    if height and weight:
        bmi = round(weight / ((height/100) ** 2), 2)
        st.metric("Your BMI", bmi)
        if bmi < 18.5:
            st.warning("You are Underweight. 🍲")
        elif 18.5 <= bmi < 24.9:
            st.success("You are Healthy ✅")
        elif 25 <= bmi < 29.9:
            st.warning("Overweight ⚠️ - Exercise regularly")
        else:
            st.error("Obese ❌ - Consult a doctor")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- TAB 4: JOURNAL ----------
import os

# ---------- TAB 4: JOURNAL ----------
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📔 Personal Journal")

    # Reflection question bank
    reflection_questions = {
        "Self & Identity": [
            "Who am I when no one is watching?",
            "What values do I refuse to compromise on?",
            "Am I living more out of habit or out of choice?",
            "Which parts of myself do I hide from others, and why?"
        ],
        "Life Direction": [
            "If my life were a book, what chapter am I in right now?",
            "Am I moving closer to the life I want, or just staying busy?",
            "What’s something I’ve always wanted to try but keep postponing?",
            "If I continue living the way I am now, where will I be in 5 years?"
        ],
        "Growth & Learning": [
            "What have I learned about myself in the last month?",
            "Do I listen more than I speak, or speak more than I listen?",
            "What scares me but also excites me?",
            "What’s the most recent belief I let go of, and why?"
        ],
        "Relationships": [
            "Who are the people that bring out the best version of me?",
            "Am I giving as much love as I want to receive?",
            "Which relationships drain me, and which energize me?",
            "Who do I need to forgive (including myself)?"
        ],
        "Perspective & Meaning": [
            "When do I feel most alive?",
            "What am I chasing that might not actually matter in the end?",
            "How much of my life is shaped by my own choices vs. expectations of others?",
            "If I stripped away fear, what would I be doing right now?"
        ]
    }

    # File path for storage
    journal_file = "journal_entries.csv"

    # Load existing journal entries
    if os.path.exists(journal_file):
        journal_df = pd.read_csv(journal_file)
    else:
        journal_df = pd.DataFrame(columns=["date", "category", "question", "response"])

    today = date.today()

    # Select reflection category
    category = st.selectbox("Choose a reflection topic:", list(reflection_questions.keys()))
    if category:
        import random
        question = random.choice(reflection_questions[category])
        st.write(f"💭 **Reflection Question:** {question}")

    # Input journal entry
    journal_entry = st.text_area(f"Write your thoughts for {today}:", "", key="journal_notes")

    if st.button("Save Journal", key="save_journal"):
        new_entry = {
            "date": today,
            "category": category,
            "question": question,
            "response": journal_entry
        }
        # Append to dataframe
        journal_df = pd.concat([journal_df, pd.DataFrame([new_entry])], ignore_index=True)
        # Save to CSV
        journal_df.to_csv(journal_file, index=False)
        st.success("✅ Journal saved permanently!")

    # Display past entries
    if not journal_df.empty:
        st.subheader("📖 Past Journal Entries")
        for _, rec in journal_df[::-1].iterrows():  # reverse order
            st.markdown(f"**{rec['date']}** - *{rec['category']}*")
            st.markdown(f"**Q:** {rec['question']}")
            st.markdown(f"**A:** {rec['response']}")
            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)
