import streamlit as st
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

# ====================== CUSTOM CHARACTERS ======================
# Olivia's character
olivia_character = {
    "name": "Olivia the Elegant Leader",
    "description": "A classy, confident 5th grader who leads with kindness and courage."
}

# Nora's character
nora_character = {
    "name": "Nora the Graceful Achiever",
    "description": "A bright, focused 4th grader who leads with determination and joy."
}

# ====================== LEADERSHIP & EATING ======================
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

# ====================== SESSION STATE ======================
if 'data' not in st.session_state:
    st.session_state.data = {
        'olivia': {'stars': 0, 'coins': 50, 'level': 1, 'outfits': [], 'daily': []},
        'nora': {'stars': 0, 'coins': 50, 'level': 1, 'outfits': [], 'daily': []}
    }

# ====================== SIDEBAR ======================
st.sidebar.header("⚙️ Settings")
st.sidebar.write("**Incentive:** $100 every 30 days (first 90 days)")
st.sidebar.write("**Grade Rule:** Minimum **90%** on all work")

# ====================== CHARACTER DISPLAY ======================
st.header("👑 Your Leadership Characters")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="girl-card olivia">', unsafe_allow_html=True)
    st.subheader("Olivia (5th Grade)")
    st.write(f"**{olivia_character['name']}**")
    st.write(olivia_character['description'])
    st.write(f"**Current Outfits:** {', '.join(st.session_state.data['olivia']['outfits']) if st.session_state.data['olivia']['outfits'] else 'Basic Look'}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="girl-card nora">', unsafe_allow_html=True)
    st.subheader("Nora (4th Grade)")
    st.write(f"**{nora_character['name']}**")
    st.write(nora_character['description'])
    st.write(f"**Current Outfits:** {', '.join(st.session_state.data['nora']['outfits']) if st.session_state.data['nora']['outfits'] else 'Basic Look'}")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ====================== DAILY CHECK-IN ======================
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

# ====================== GRADES ======================
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

# ====================== CHARACTER SHOP ======================
st.header("🛍️ Dress Your Character Shop")

shop_items = {
    "Pink Lip Gloss": 25,
    "Sparkly Hair Bow": 30,
    "Pearl Necklace": 45,
    "Pretty Pink Dress": 80,
    "Makeup Palette": 65,
    "Sweet Perfume": 55,
    "Shiny Shoes": 90,
    "Elegant Headband": 35
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
                st.session_state.data[girl]['outfits'].append(item)
                st.success(f"{item} added to {name}'s character!")
                st.rerun()
            else:
                st.error("Not enough coins!")

st.divider()

# ====================== SUNDAY NIGHT REVIEW ======================
st.header("🌟 Sunday Night Review")

if st.button("Show This Week's Summary"):
    for girl in ['olivia', 'nora']:
        name = "Olivia" if girl == "olivia" else "Nora"
        st.subheader(name)
        st.write(f"**Total Stars:** {st.session_state.data[girl]['stars']}")
        st.write(f"**Total Coins:** {st.session_state.data[girl]['coins']}")
        st.write(f"**Current Look:** {', '.join(st.session_state.data[girl]['outfits']) if st.session_state.data[girl]['outfits'] else 'Basic Look'}")
    st.success("Excellent work this week, leaders!")

st.divider()

# ====================== INCENTIVE ======================
st.header("💰 30-Day Incentive Progress")

col1, col2 = st.columns(2)
with col1:
    st.metric("Olivia", f"{st.session_state.data['olivia']['stars']} stars")
with col2:
    st.metric("Nora", f"{st.session_state.data['nora']['stars']} stars")

st.caption("Reach your goal each 30 days to earn the full $100!")

st.caption("Built with love for Olivia & Nora • Holy Spirit Catholic School")
