import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Manager Incentive Simulator", layout="wide")

st.title("💎 Kalyan Jewellers – Manager Performance Simulator")
st.caption("Simulate performance. Understand impact. Maximize incentives.")

MAX_SCORE = 110

# ---------------------------------------------------
# INCENTIVE SLABS (As per Chart)
# ---------------------------------------------------

INCENTIVE_STRUCTURE = {
    "CHIEF MANAGER": {
        "100+": 75000,
        "90-99": 62500,
        "80-89": 50000,
        "70-79": 37500,
        "60-69": 25000,
        "<60": 15000
    },
    "CHIEF MANAGER (G2)": {
        "100+": 60000,
        "90-99": 50000,
        "80-89": 40000,
        "70-79": 30000,
        "60-69": 20000,
        "<60": 14000
    },
    "BRANCH MANAGER": {
        "100+": 50000,
        "90-99": 40000,
        "80-89": 30000,
        "70-79": 23750,
        "60-69": 17500,
        "<60": 12500
    },
    "ASSISTANT MANAGER": {
        "100+": 50000,
        "90-99": 40000,
        "80-89": 30000,
        "70-79": 23750,
        "60-69": 17500,
        "<60": 12500
    },
    "MANAGER TRAINEE": {
        "100+": 30000,
        "90-99": 25000,
        "80-89": 20000,
        "70-79": 17500,
        "60-69": 15000,
        "<60": 10000
    }
}

# ---------------------------------------------------
# SCORING LOGIC
# ---------------------------------------------------

def get_turnover_marks(pct):
    if pct >= 100: return 40.0
    elif pct >= 90: return 30.0
    elif pct >= 80: return 25.0
    elif pct >= 75: return 10.0
    return 0.0

def get_20_mark_logic(pct):
    if pct >= 100: return 20.0
    elif pct >= 90: return 12.5
    elif pct >= 80: return 7.5
    elif pct >= 75: return 4.0
    return 0.0

def get_dmd_marks(pct, studded_pct):
    if studded_pct < 75:
        return 0.0
    if pct >= 100: return 10.0
    elif pct >= 90: return 7.5
    elif pct >= 80: return 5.0
    return 0.0

def performance_level(score):
    if score >= 95:
        return "🟢 OUTSTANDING PERFORMER"
    elif score >= 80:
        return "🟡 STRONG PERFORMER"
    elif score >= 60:
        return "🟠 STABLE BUT IMPROVEMENT NEEDED"
    else:
        return "🔴 HIGH RISK ZONE"

def get_incentive(designation, score):
    if score >= 100:
        slab = "100+"
    elif score >= 90:
        slab = "90-99"
    elif score >= 80:
        slab = "80-89"
    elif score >= 70:
        slab = "70-79"
    elif score >= 60:
        slab = "60-69"
    else:
        slab = "<60"
    
    return INCENTIVE_STRUCTURE[designation][slab], slab

# ---------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------

st.sidebar.header("📊 Performance Inputs")

designation = st.sidebar.selectbox(
    "Select Designation",
    list(INCENTIVE_STRUCTURE.keys())
)

t_pct = st.sidebar.slider("Total Turnover (%)", 0.0, 120.0, 100.0, 0.5)
s_pct = st.sidebar.slider("Studded Turnover (%)", 0.0, 120.0, 100.0, 0.5)
dtso_pct = st.sidebar.slider("DTSO (AKT) (%)", 0.0, 120.0, 100.0, 0.5)
sch_pct = st.sidebar.slider("Scheme Registration (%)", 0.0, 120.0, 100.0, 0.5)
dmd_pct = st.sidebar.slider("DMD Turnover (%)", 0.0, 120.0, 100.0, 0.5)

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------

t_marks = get_turnover_marks(t_pct)
s_marks = get_20_mark_logic(s_pct)
dtso_marks = get_20_mark_logic(dtso_pct)
sch_marks = get_20_mark_logic(sch_pct)
dmd_marks = get_dmd_marks(dmd_pct, s_pct)

total_score = t_marks + s_marks + dtso_marks + sch_marks + dmd_marks

incentive_amount, slab = get_incentive(designation, total_score)

# ---------------------------------------------------
# DISPLAY
# ---------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric("TOTAL SCORE", f"{total_score} / {MAX_SCORE}")
    st.progress(int((total_score / MAX_SCORE) * 100))
    st.subheader(performance_level(total_score))

    if s_pct < 75:
        st.error("⚠️ DMD Marks Locked: Studded Achievement must be ≥ 75%")

with col2:
    st.metric("Incentive Earned (₹)", f"{incentive_amount}")
    st.write(f"### Slab Applied: {slab}")
    st.write("### Marks Breakdown")
    st.write(f"Total Turnover: {t_marks}")
    st.write(f"Studded Turnover: {s_marks}")
    st.write(f"DTSO: {dtso_marks}")
    st.write(f"Scheme Registration: {sch_marks}")
    st.write(f"DMD: {dmd_marks}")
