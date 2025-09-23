import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime

# --- Disease dictionary ---
disease_dict = {
   "flu": {
       "symptoms": ["fever", "cough", "sore throat", "fatigue"],
       "prevention": ["Get vaccinated yearly", "Wash hands regularly", "Avoid close contact with sick people"]
   },
   "malaria": {
       "symptoms": ["fever", "chills", "sweating", "headache"],
       "prevention": ["Use mosquito nets", "Apply insect repellent", "Drain stagnant water"]
   },
   "dengue": {
       "symptoms": ["high fever", "severe headache", "pain behind eyes", "joint pain", "muscle pain", "rash", "nausea"],
       "prevention": ["Prevent mosquito bites", "Avoid water collection around home", "Use protective clothing"]
   },
   # (rest of your diseases unchanged) ...
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

# --- Custom CSS ---
st.markdown(
    """
    <style>
    .main {padding: 2rem 3rem;}
    .card {background-color: #f5f5f5; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin-bottom: 2rem;}
    .card-col {background-color: #fefefe; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 1rem;}
    .stTabs [role="tab"] {font-weight: bold; font-size: 16px;}
    .big-font { font-size:22px !important; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.title("💊 HEALIX :mask:")
st.header("Your Personal Health Assistant")
st.write("Select symptoms to check possible diseases, see prevention tips, and track your health. *(Educational use only, not medical advice.)*")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Symptom Checker", "📖 Search by Disease", "💧 Health & Wellness"])

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
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-col">', unsafe_allow_html=True)
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
    
    with col2:
        st.markdown('<div class="card-col">', unsafe_allow_html=True)
        st.write("💡 Tips:")
        st.write("- Type full or partial disease names")
        st.write("- Use the Symptom Checker to narrow possibilities")
        st.markdown('</div>', unsafe_allow_html=True)
    
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

    # --- Weekly Graph Placeholder ---
    st.subheader("📊 Weekly Water Intake")
    st.info("Future update: Show last 7 days water consumption")

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

    # --- Health Notes ---
    st.subheader("📝 Daily Health Notes")
    today = date.today()
    notes = st.text_area(f"Write health notes for {today}:", "", key="health_notes")
    if st.button("Save Record", key="save_notes"):
        st.success("Record saved! (Demo only, not stored permanently)")
        st.write(f"📝 **{today}:** {notes}")

    # --- Dashboard Cards ---
    st.markdown("### 📊 Dashboard Overview")
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown('<div class="card-col">🩺 <span class="big-font">Symptom Checker</span><br>Detects possible conditions</div>', unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="card-col">⚖️ <span class="big-font">BMI Calculator</span><br>Tracks your weight status</div>', unsafe_allow_html=True)
    with colC:
        st.markdown('<div class="card-col">💧 <span class="big-font">Water Tracker</span><br>Keeps hydration in check</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
