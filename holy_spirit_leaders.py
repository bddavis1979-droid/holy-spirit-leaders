import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Holy Spirit Leaders Adventure", page_icon="⭐", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1a365d; }
    .girl-card { padding: 15px; border-radius: 15px; margin-bottom: 15px; }
    .olivia { background-color: #f3e8ff; border-left: 6px solid #7c3aed; }
    .nora { background-color: #e0f2fe; border-left: 6px solid #0ea5e9; }
</style>
""", unsafe_allow_html=True)

st.title("⭐ Holy Spirit Leaders Adventure")
st.caption("Olivia & Nora’s Leadership Journey • Holy Spirit Catholic School • Louisville, KY")

# Characters
characters = {
    "Mary Kay Ash": "Faithful Entrepreneur",
    "Madam C.J. Walker": "Rags-to-Riches Leader",
    "Estée Lauder": "Sophisticated & Elegant",
    "Debbie Fields": "Fun & Determined",
    "Lillian Vernon": "Organized & Practical",
    "Ruth Handler": "Creative Visionary"
}

leadership_behaviors = [
    "Shows Initiative", "Leads by Example", "Takes Full Responsibility",
    "Makes Wise Choices", "Shows Courage", "Practices Self-Control",
    "Encourages Others", "Shows Perseverance", "Is Organized & Prepared",
    "Listens & Follows Directions", "Shows Honesty & Integrity", "Shows Gratitude & Humility"
]

eating_behaviors = [
    "Ate fruits or vegetables", "Drank water instead of soda",
    "Ate a balanced meal", "Limited candy/chips/sweets"
]

# Session State
if 'data' not in st.session_state:
    st.session_state.data = {
        'olivia': {'stars': 0, 'coins': 0, 'level': 1, 'character': None, 'grades': [], 'daily': []},
        'nora': {'stars': 0, 'coins': 0, 'level': 1, 'character': None, 'grades': [], 'daily': []}
    }

# Sidebar
st.sidebar.header("⚙️ Settings")
st.sidebar.write("**Incentive:** $100 every 30 days (first 90 days)")
st.sidebar.write("**Grade Rule:** Minimum **90%** on all work")

# Character Selection
st.header("👑 Choose Your Leadership Role Model")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="girl-card olivia">', unsafe_allow_html=True)
    st.subheader("Olivia (5th Grade)")
    if st.session_state.data['olivia']['character'] is None:
        choice = st.selectbox("Pick your character", list(characters.keys()), key="olivia_char")
        if st.button("Confirm Character for Olivia"):
            st.session_state.data['olivia']['character'] = choice
            st.rerun()
    else:
        st.success(f"**{st.session_state.data['olivia']['character']}**")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="girl-card nora">', unsafe_allow_html=True)
    st.subheader("Nora (4th Grade)")
    if st.session_state.data['nora']['character'] is None:
        choice = st.selectbox("Pick your character", list(characters.keys()), key="nora_char")
        if st.button("Confirm Character for Nora"):
            st.session_state.data['nora']['character'] = choice
            st.rerun()
    else:
        st.success(f"**{st.session_state.data['nora']['character']}**")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Daily Check-in
st.header("📅 Daily Leadership Check-In")

tab1, tab2 = st.tabs(["Olivia", "Nora"])

def daily_checkin(girl_name, girl_key):
    st.subheader(f"Today for {girl_name}")
    selected = st.multiselect("Leadership Behaviors", leadership_behaviors, key=f"lead_{girl_key}")
    eating = st.multiselect("Healthy Eating", eating_behaviors, key=f"eat_{girl_key}")
    
    if girl_key == "olivia":
        focus = st.checkbox("Practiced good social skills & interacting today", key="olivia_focus")
    else:
        focus = st.checkbox("Controlled talking and stayed focused today", key="nora_focus")
    
    if st.button(f"Save Check-in for {girl_name}", key=f"save_{girl_key}"):
        points = len(selected) * 5 + len(eating) * 3
        if focus: points += 8
        coins = points // 2
        
        st.session_state.data[girl_key]['stars'] += points
        st.session_state.data[girl_key]['coins'] += coins
        st.success(f"+{points} stars and +{coins} coins!")
        st.rerun()

with tab1:
    daily_checkin("Olivia", "olivia")
with tab2:
    daily_checkin("Nora", "nora")

st.divider()

# Grades
st.header("📚 Grades (Minimum 90%)")

gcol1, gcol2 = st.columns(2)

def add_grade(girl_name, girl_key):
    with gcol1 if girl_key == "olivia" else gcol2:
        st.subheader(girl_name)
        subject = st.text_input("Subject", key=f"subj_{girl_key}")
        score = st.number_input("Score %", 0, 100, 92, key=f"score_{girl_key}")
        
        if st.button(f"Add Grade", key=f"grade_{girl_key}"):
            if score < 90:
                st.error("Score must be 90% or higher!")
            else:
                stars = 20 if score >= 95 else 12
                coins = stars // 2
                st.session_state.data[girl_key]['stars'] += stars
                st.session_state.data[girl_key]['coins'] += coins
                st.success(f"+{stars} stars & +{coins} coins!")
                st.rerun()

add_grade("Olivia", "olivia")
add_grade("Nora", "nora")

st.divider()

# Coin Shop
st.header("🛍️ Leadership Coin Shop")

shop_items = {
    "Lip Gloss": 25, "Hair Bow Set": 30, "Necklace": 45,
    "Cute Dress": 80, "Makeup Palette": 65, "Perfume": 55, "Sparkly Shoes": 90
}

shop_col1, shop_col2 = st.columns(2)

for girl in ['olivia', 'nora']:
    name = "Olivia" if girl == "olivia" else "Nora"
    with shop_col1 if girl == "olivia" else shop_col2:
        st.subheader(f"{name}'s Shop")
        st.write(f"**Coins:** {st.session_state.data[girl]['coins']}")
        item = st.selectbox("Choose item", list(shop_items.keys()), key=f"shop_{girl}")
        if st.button(f"Buy {item}", key=f"buy_{girl}"):
            cost = shop_items[item]
            if st.session_state.data[girl]['coins'] >= cost:
                st.session_state.data[girl]['coins'] -= cost
                st.success(f"Purchased {item}!")
                st.rerun()
            else:
                st.error("Not enough coins!")

st.divider()

# Sunday Night Review
st.header("🌟 Sunday Night Review")

if st.button("Show Weekly Summary"):
    for girl in ['olivia', 'nora']:
        name = "Olivia" if girl == "olivia" else "Nora"
        st.subheader(name)
        st.write(f"**Total Stars:** {st.session_state.data[girl]['stars']}")
        st.write(f"**Total Coins:** {st.session_state.data[girl]['coins']}")
        st.write(f"**Character:** {st.session_state.data[girl]['character'] or 'Not chosen'}")
    st.success("Excellent work this week!")

st.divider()

# 30-Day Incentive
st.header("💰 30-Day Incentive Progress")

col1, col2 = st.columns(2)
with col1:
    st.metric("Olivia", f"{st.session_state.data['olivia']['stars']} stars")
with col2:
    st.metric("Nora", f"{st.session_state.data['nora']['stars']} stars")

st.caption("Reach your goal each 30 days to earn the full $100!")

st.caption("Built with love for Olivia & Nora • Holy Spirit Catholic School")
