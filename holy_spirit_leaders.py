import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Holy Spirit Leaders Adventure", page_icon="⭐", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1a365d; }
    .girl-card { padding: 20px; border-radius: 15px; margin: 10px 0; }
    .olivia { background-color: #f3e8ff; border-left: 8px solid #7c3aed; }
    .nora { background-color: #e0f2fe; border-left: 8px solid #0ea5e9; }
</style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
if 'view' not in st.session_state:
    st.session_state.view = "home"
if 'data' not in st.session_state:
    st.session_state.data = {
        'olivia': {'stars': 0, 'coins': 50, 'level': 1, 'outfits': [], 'daily': []},
        'nora': {'stars': 0, 'coins': 50, 'level': 1, 'outfits': [], 'daily': []}
    }

# ====================== HOME PAGE ======================
def show_home():
    st.title("⭐ Holy Spirit Leaders Adventure")
    st.caption("Olivia & Nora’s Leadership Journey • Holy Spirit Catholic School")

    st.write("### Click on your name to start your journey")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="girl-card olivia">', unsafe_allow_html=True)
        st.subheader("👧 Olivia (5th Grade)")
        st.write("**Olivia the Elegant Leader**")
        if st.button("Enter Olivia's Journey", key="olivia_btn"):
            st.session_state.view = "olivia"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="girl-card nora">', unsafe_allow_html=True)
        st.subheader("👧 Nora (4th Grade)")
        st.write("**Nora the Graceful Achiever**")
        if st.button("Enter Nora's Journey", key="nora_btn"):
            st.session_state.view = "nora"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🌟 Sunday Night Review"):
        st.session_state.view = "review"
        st.rerun()

# ====================== OLIVIA'S PAGE ======================
def show_olivia():
    st.header("👧 Olivia's Leadership Journey")
    st.write("**Olivia the Elegant Leader** — 5th Grade")

    if st.button("← Back to Home"):
        st.session_state.view = "home"
        st.rerun()

    data = st.session_state.data['olivia']

    # Avatar Section
    st.subheader("🖼️ Your Character")
    st.image("https://picsum.photos/id/1011/300/300", caption="Olivia's Avatar", width=250)
    st.write(f"**Current Look:** {', '.join(data['outfits']) if data['outfits'] else 'Basic Look'}")

    st.divider()

    st.subheader("⭐ Your Stats")
    st.write(f"**Stars:** {data['stars']}")
    st.write(f"**Coins:** {data['coins']}")

    st.divider()

    # Daily Check-in
    st.subheader("📅 Today's Check-In")
    selected = st.multiselect("Leadership Behaviors", [
        "Shows Initiative", "Leads by Example", "Takes Full Responsibility",
        "Makes Wise Choices", "Shows Courage", "Practices Self-Control",
        "Encourages Others", "Shows Perseverance", "Is Organized & Prepared",
        "Listens & Follows Directions", "Shows Honesty & Integrity", "Shows Gratitude & Humility"
    ], key="olivia_lead")

    eating = st.multiselect("Healthy Eating", [
        "Ate fruits or vegetables", "Drank water instead of soda",
        "Ate a balanced meal", "Limited candy/chips/sweets"
    ], key="olivia_eat")

    social = st.checkbox("Practiced good social skills & interacting today")

    if st.button("Save Check-in"):
        points = len(selected) * 5 + len(eating) * 3
        if social: points += 8
        coins = points // 2
        data['stars'] += points
        data['coins'] += coins
        st.success(f"+{points} stars and +{coins} coins!")
        st.rerun()

    st.divider()

    # Grades
    st.subheader("📚 Add Grade (90%+)")
    subject = st.text_input("Subject")
    score = st.number_input("Score %", 0, 100, 92, key="olivia_grade")

    if st.button("Add Grade"):
        if score < 90:
            st.error("Must be 90% or higher!")
        else:
            stars = 20 if score >= 95 else 12
            coins = stars // 2
            data['stars'] += stars
            data['coins'] += coins
            st.success(f"+{stars} stars & +{coins} coins!")
            st.rerun()

    st.divider()

    # Shop with visual update
    st.subheader("🛍️ Dress Your Character")
    shop = {
        "Pink Lip Gloss": 25, "Sparkly Hair Bow": 30, "Pearl Necklace": 45,
        "Pretty Pink Dress": 80, "Makeup Palette": 65, "Sweet Perfume": 55,
        "Shiny Shoes": 90, "Elegant Headband": 35
    }
    item = st.selectbox("Choose item", list(shop.keys()), key="olivia_shop")
    if st.button("Buy & Wear"):
        cost = shop[item]
        if data['coins'] >= cost:
            data['coins'] -= cost
            data['outfits'].append(item)
            st.success(f"{item} added to your look!")
            st.rerun()
        else:
            st.error("Not enough coins!")

# ====================== NORA'S PAGE ======================
def show_nora():
    st.header("👧 Nora's Leadership Journey")
    st.write("**Nora the Graceful Achiever** — 4th Grade")

    if st.button("← Back to Home"):
        st.session_state.view = "home"
        st.rerun()

    data = st.session_state.data['nora']

    st.subheader("🖼️ Your Character")
    st.image("https://picsum.photos/id/1005/300/300", caption="Nora's Avatar", width=250)
    st.write(f"**Current Look:** {', '.join(data['outfits']) if data['outfits'] else 'Basic Look'}")

    st.divider()

    st.subheader("⭐ Your Stats")
    st.write(f"**Stars:** {data['stars']}")
    st.write(f"**Coins:** {data['coins']}")

    st.divider()

    st.subheader("📅 Today's Check-In")
    selected = st.multiselect("Leadership Behaviors", [
        "Shows Initiative", "Leads by Example", "Takes Full Responsibility",
        "Makes Wise Choices", "Shows Courage", "Practices Self-Control",
        "Encourages Others", "Shows Perseverance", "Is Organized & Prepared",
        "Listens & Follows Directions", "Shows Honesty & Integrity", "Shows Gratitude & Humility"
    ], key="nora_lead")

    eating = st.multiselect("Healthy Eating", [
        "Ate fruits or vegetables", "Drank water instead of soda",
        "Ate a balanced meal", "Limited candy/chips/sweets"
    ], key="nora_eat")

    focus = st.checkbox("Controlled talking and stayed focused today")

    if st.button("Save Check-in"):
        points = len(selected) * 5 + len(eating) * 3
        if focus: points += 8
        coins = points // 2
        data['stars'] += points
        data['coins'] += coins
        st.success(f"+{points} stars and +{coins} coins!")
        st.rerun()

    st.divider()

    st.subheader("📚 Add Grade (90%+)")
    subject = st.text_input("Subject")
    score = st.number_input("Score %", 0, 100, 92, key="nora_grade")

    if st.button("Add Grade"):
        if score < 90:
            st.error("Must be 90% or higher!")
        else:
            stars = 20 if score >= 95 else 12
            coins = stars // 2
            data['stars'] += stars
            data['coins'] += coins
            st.success(f"+{stars} stars & +{coins} coins!")
            st.rerun()

    st.divider()

    st.subheader("🛍️ Dress Your Character")
    shop = {
        "Pink Lip Gloss": 25, "Sparkly Hair Bow": 30, "Pearl Necklace": 45,
        "Pretty Pink Dress": 80, "Makeup Palette": 65, "Sweet Perfume": 55,
        "Shiny Shoes": 90, "Elegant Headband": 35
    }
    item = st.selectbox("Choose item", list(shop.keys()), key="nora_shop")
    if st.button("Buy & Wear"):
        cost = shop[item]
        if data['coins'] >= cost:
            data['coins'] -= cost
            data['outfits'].append(item)
            st.success(f"{item} added to your look!")
            st.rerun()
        else:
            st.error("Not enough coins!")

# ====================== SUNDAY REVIEW ======================
def show_review():
    st.header("🌟 Sunday Night Review")

    if st.button("← Back to Home"):
        st.session_state.view = "home"
        st.rerun()

    for girl in ['olivia', 'nora']:
        name = "Olivia" if girl == "olivia" else "Nora"
        data = st.session_state.data[girl]
        st.subheader(name)
        st.write(f"**Stars:** {data['stars']}")
        st.write(f"**Coins:** {data['coins']}")
        st.write(f"**Current Look:** {', '.join(data['outfits']) if data['outfits'] else 'Basic Look'}")

    st.success("Great work this week!")

# ====================== VIEW CONTROL ======================
if st.session_state.view == "home":
    show_home()
elif st.session_state.view == "olivia":
    show_olivia()
elif st.session_state.view == "nora":
    show_nora()
elif st.session_state.view == "review":
    show_review()
