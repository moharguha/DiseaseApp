import streamlit as st
from datetime import date
from diseases import disease_dict

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

# --- Function to display results as a table ---
def display_results_table(results):
    if not results:
        st.warning("⚠️ No matching diseases found.")
        return

    # Start Markdown table
    table = "| Sr. No | Disease | Confidence (%) | Symptoms Matched | Prevention |\n"
    table += "|--------|---------|----------------|-----------------|------------|\n"

    for idx, r in enumerate(results, start=1):
        matched_symptoms = ", ".join(r["matched"])
        prevention = ", ".join(r["prevention"])
        table += f"| {idx} | {r['disease'].title()} | {r['confidence']} | {matched_symptoms} | {prevention} |\n"

    st.markdown(table, unsafe_allow_html=True)

# --- Streamlit App ---
st.set_page_config(page_title="Healix Health Tracker", layout="wide")

# Custom CSS for cards, spacing, and tabs
st.markdown(
    """
    <style>
    .main {padding: 2rem 3rem;}
    .card {background-color: #f5f5f5; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin-bottom: 2rem;}
    .card-col {background-color: #fefefe; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 1rem;}
    .stTabs [role="tab"] {font-weight: bold; font-size: 16px;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💊 HEALIX :mask:")
st.header("Your Personal Health Assistant")
st.write("Select symptoms to check possible diseases, see prevention tips, and track your health. *(Educational use only, not medical advice.)*")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["🔍 Symptom Checker", "📖 Search by Disease", "💧 Health & Water Records"])

# ---------- SYMPTOM CHECKER TAB ----------
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Select Symptoms")
    
    # Two-column layout for symptoms
    col1, col2 = st.columns(2)
    with col1:
        selected_symptoms1 = st.multiselect("Symptoms Group 1", all_symptoms[:len(all_symptoms)//2])
    with col2:
        selected_symptoms2 = st.multiselect("Symptoms Group 2", all_symptoms[len(all_symptoms)//2:])
    
    selected = selected_symptoms1 + selected_symptoms2
    
    if st.button("Check Disease"):
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

# ---------- DISEASE SEARCH TAB ----------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Search Disease by Name")
    
    # Two-column layout for input + tips
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-col">', unsafe_allow_html=True)
        disease_name = st.text_input("Enter disease name (e.g., malaria)")
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

# ---------- HEALTH & WATER RECORDS TAB ----------
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("💧 Daily Health & Water Records")
    
    # Water intake tracker
    st.subheader("Water Intake")
    water = st.slider("How many glasses of water did you drink today?", 0, 20, 8)
    st.progress(water / 20)
    st.markdown(f"✅ You drank **{water} glasses** today.")
    
    # Health notes
    st.subheader("Health Notes")
    today = date.today()
    notes = st.text_area(f"Write health notes for {today}:", "")
    if st.button("Save Record"):
        st.success("Record saved! (In real app, this would be stored in a database.)")
        st.write(f"📝 **{today}:** {notes}")
    
    st.markdown('</div>', unsafe_allow_html=True)
