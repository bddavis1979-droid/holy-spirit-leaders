import streamlit as st
from datetime import datetime, date, timedelta
import os
import json
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta as td

st.set_page_config(page_title="Holy Spirit Falcons Volleyball Leaders", page_icon="🏐", layout="wide", initial_sidebar_state="expanded")

# ====================== FAMILY PASSWORD ======================
FAMILY_PASSWORD = "OliviaNora2026"
try:
    if "FAMILY_PASSWORD" in st.secrets:
        FAMILY_PASSWORD = st.secrets["FAMILY_PASSWORD"]
except:
    pass
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def show_login():
    st.markdown("""
    <style>.login-card { background: linear-gradient(135deg,#000000 0%,#A71930 100%); padding:35px; border-radius:20px; border:3px solid #fff; max-width:520px; margin:60px auto; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.4); } .login-title{font-size:2.4rem;font-weight:900;color:white;}</style>
    """, unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        # use real Falcons logo if exists - exact jersey match
        logo_path = "assets/falcons_logo_exact_jersey.png"
        if not os.path.exists(logo_path):
            logo_path = "assets/falcons_logo_exact_jersey.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=180)
        st.markdown('<div class="login-title">🏈 HOLY SPIRIT FALCONS 🏐</div>', unsafe_allow_html=True)
        st.markdown("<p style='color:white;font-size:1.2rem;font-weight:700;'>OLIVIA & NORA'S VOLLEYBALL LEADERS ADVENTURE</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#FFDDE1;'>Private Family Only — Red + Black + White</p>", unsafe_allow_html=True)
        pwd = st.text_input("Family Password", type="password", placeholder="OliviaNora2026")
        if st.button("LET'S GO FALCONS! 🔴⚫️", type="primary", use_container_width=True):
            if pwd == FAMILY_PASSWORD:
                st.session_state.authenticated=True
                st.balloons()
                st.rerun()
            else:
                st.error("Not our Falcons password! Hint: OliviaNora2026")
        st.caption("🔒 Private — No teacher sharing — Just us!")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    show_login()
    st.stop()

# ====================== FALCONS STYLES ======================
st.markdown("""
<style>
    .main-header { font-size:2.8rem; font-weight:900; color:#000; text-align:center; background: linear-gradient(90deg,#000 0%,#A71930 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .sub-header { font-size:1.25rem; color:#A71930; text-align:center; font-weight:800; }
    .falcons-banner { background: linear-gradient(135deg,#000000 0%,#A71930 50%,#000000 100%); color:white; padding:18px; border-radius:18px; text-align:center; border:3px solid white; box-shadow:0 6px 20px rgba(0,0,0,0.3); }
    .girl-card { padding:22px; border-radius:20px; margin:12px 0; box-shadow:0 5px 18px rgba(0,0,0,0.15); transition:transform 0.2s; border:2px solid #eee; }
    .girl-card:hover{ transform: translateY(-4px) scale(1.01); }
    .olivia { background: linear-gradient(135deg,#fff 0%,#FFDDE1 100%); border-left:10px solid #A71930; border-top:4px solid #000; }
    .nora { background: linear-gradient(135deg,#fff 0%,#E0F2FE 100%); border-left:10px solid #000; border-top:4px solid #A71930; }
    .falcons-card { background: linear-gradient(135deg,#000 0%,#1a1a1a 100%); color:white; padding:15px; border-radius:12px; border-left:6px solid #A71930; }
    .volleyball-card { background: linear-gradient(135deg,#FFF 0%,#FFE4E1 100%); padding:14px; border-radius:12px; border:3px solid #A71930; }
    .virtue-card { background: linear-gradient(135deg,#fef3c7 0%,#fde68a 100%); padding:12px; border-radius:12px; border-left:6px solid #f59e0b; }
    .level-badge { background:#000; color:white; padding:4px 14px; border-radius:20px; font-weight:900; border:2px solid #A71930; }
    .falcons-btn { background:#A71930 !important; color:white !important; font-weight:800 !important; }
</style>
""", unsafe_allow_html=True)

# ====================== SCHOOL & FALCONS CONSTANTS ======================
ASSETS_DIR="assets"
SCHOOL_MASCOT="Falcons"
SCHOOL_COLORS={"red":"#A71930","black":"#000000","white":"#FFFFFF","silver":"#A5ACAF"}
FIRST_DAY_SCHOOL=date(2026,8,11)
LAST_DAY_SCHOOL=date(2027,5,28)
SCHOOL_YEAR_LABEL="2026-2027"

# Real birthdays — Olivia 8/31/2015, Nora 4/27/2017
OLIVIA_DOB=date(2015,8,31)
NORA_DOB=date(2017,4,27)

def get_age_and_next_birthday(dob: date, today: date = None):
    if today is None:
        today=date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    this_year_bday = date(today.year, dob.month, dob.day)
    if this_year_bday < today:
        next_bday = date(today.year+1, dob.month, dob.day)
    else:
        next_bday = this_year_bday
    days_until = (next_bday - today).days
    is_today = (today.month == dob.month and today.day == dob.day)
    return {"age": age, "next_bday": next_bday, "days_until": days_until, "is_today": is_today, "dob_str": dob.strftime("%B %d, %Y")}

def get_daily_runway_theme(today=None):
    if today is None:
        today=date.today()
    # Rotate theme based on day of year
    idx = today.timetuple().tm_yday % len(DTI_RUNWAY_THEMES)
    return DTI_RUNWAY_THEMES[idx]

def check_and_unlock_family_adventures():
    # Check extra family rewards based on activity
    for girl_key in ['olivia','nora']:
        data = st.session_state.data[girl_key]
        # VB5: 5 volleyball games logged
        if len(data.get('volleyball_games',[])) >=5 and "VB5" not in data.get('milestones_claimed',[]):
            data['milestones_claimed'].append("VB5")
        # BAKE1: bought first baking reward (check outfits contains baking)
        baking_items = [o for o in data.get('outfits',[]) if "Baking" in o or "Bake" in o]
        if len(baking_items)>=1 and "BAKE1" not in data.get('milestones_claimed',[]):
            data['milestones_claimed'].append("BAKE1")
        # SPIN10: 10 spins
        if data.get('spin_count',0)>=10 and "SPIN10" not in data.get('milestones_claimed',[]):
            data['milestones_claimed'].append("SPIN10")
        # COLLECT10: 10 outfits
        if len(data.get('outfits',[]))>=10 and "COLLECT10" not in data.get('milestones_claimed',[]):
            data['milestones_claimed'].append("COLLECT10")
    save_data()

NO_SCHOOL_DAYS={
    date(2026,9,7):"Labor Day", date(2026,9,21):"PD Day", date(2026,10,8):"Conference No School",
    date(2026,10,9):"Fall Break", date(2026,10,10):"Fall Break", date(2026,10,12):"Fall Break", date(2026,10,13):"PD Day",
    date(2026,11,3):"Arch PD Day", date(2026,11,23):"Thanksgiving", date(2026,11,24):"Thanksgiving", date(2026,11,25):"Thanksgiving",
    date(2026,11,26):"Thanksgiving", date(2026,11,27):"Thanksgiving", date(2026,12,8):"Immaculate Conception",
    date(2026,12,21):"Christmas Break", date(2026,12,22):"Christmas Break", date(2026,12,23):"Christmas Break", date(2026,12,24):"Christmas Break",
    date(2026,12,25):"Christmas Break", date(2026,12,26):"Christmas Break", date(2026,12,27):"Christmas Break", date(2026,12,28):"Christmas Break",
    date(2026,12,29):"Christmas Break", date(2026,12,30):"Christmas Break", date(2026,12,31):"Christmas Break",
    date(2027,1,1):"Christmas Break", date(2027,1,18):"MLK Holiday", date(2027,2,11):"Conference No School",
    date(2027,2,12):"Winter Break", date(2027,2,13):"Winter Break", date(2027,2,15):"Winter Break",
    date(2027,3,26):"Spring Break Good Friday", date(2027,3,27):"Spring Break", date(2027,3,28):"Spring Break", date(2027,3,29):"Spring Break",
    date(2027,3,30):"Spring Break", date(2027,3,31):"Spring Break", date(2027,4,1):"Spring Break", date(2027,4,2):"Spring Break",
    date(2027,4,8):"PD Day", date(2027,4,30):"Derby Eve",
}
HALF_DAYS={date(2026,8,10):"First Day K New 11:30", date(2026,8,11):"First Day Gr 1-8 Noon ⭐ Falcons Start!", date(2026,10,7):"Conference Noon", date(2026,12,18):"Noon Xmas", date(2027,2,10):"Noon Conferences", date(2027,5,28):"Last Day Noon 🎉"}

TRIMESTER_ENDS={date(2026,11,6):"End 1st Trimester", date(2027,2,19):"End 2nd Trimester", date(2027,5,28):"End 3rd Trimester"}
TRIMESTER_BONUSES={
    date(2026,11,6):{"name":"END OF 1ST TRIMESTER! 📚✨","stars":40,"coins":40,"icon":"📚","msg":"1st trimester done!","key":"T1"},
    date(2027,2,19):{"name":"END OF 2ND TRIMESTER! ❄️📚","stars":40,"coins":40,"icon":"❄️","msg":"Winter focus!","key":"T2"},
    date(2027,5,28):{"name":"END OF 3RD TRIMESTER & LAST DAY! 🎓☀️","stars":60,"coins":60,"icon":"🎓","msg":"Final day!","key":"T3"},
}
MILESTONES={
    1:{"name":"FIRST DAY! Day 1 Falcons! 🕊️⭐","stars":25,"coins":25,"icon":"🎉","msg":"Started strong!"},
    10:{"name":"10 Days Strong Falcons!","stars":15,"coins":15,"icon":"💪","msg":"10 days!"},
    25:{"name":"25 Days!","stars":20,"coins":20,"icon":"🌟","msg":"Consistent!"},
    50:{"name":"50 Days — Half to 100!","stars":25,"coins":25,"icon":"🏃‍♀️","msg":"Halfway!"},
    75:{"name":"75 Days!","stars":25,"coins":25,"icon":"✨","msg":"Almost 100!"},
    90:{"name":"90 Days!","stars":30,"coins":30,"icon":"🔥","msg":"Perseverance!"},
    100:{"name":"100TH DAY! CENTURY CLUB! 💯🎉","stars":75,"coins":75,"icon":"💯","msg":"Century!"},
    125:{"name":"125 Days!","stars":25,"coins":25,"icon":"🌷","msg":"Spring finish!"},
    150:{"name":"150 Days! Nails Day! 💅","stars":35,"coins":35,"icon":"🚀","msg":"Almost there! Nails day unlock!"},
    170:{"name":"170 Days Last Lap!","stars":30,"coins":40,"icon":"🏁","msg":"Last lap!"},
}
LAST_DAY_MILESTONE={"name":"LAST DAY! YOU DID IT! 🎓🎉","stars":100,"coins":100,"icon":"🎓","msg":"Summer!"}

# ====================== VOLLEYBALL SCHEDULE — REAL ======================
VOLLEYBALL_SCHEDULE=[
    {"date":date(2026,8,8),"day_str":"Sat Aug 8","girl":"Nora","time":"9:00 AM","location":"Sacred Heart Model","opponent":"Sacred Heart Model","home":False},
    {"date":date(2026,8,8),"day_str":"Sat Aug 8","girl":"Olivia","time":"12:00 PM","location":"Holy Spirit","opponent":"Home Game","home":True},
    {"date":date(2026,8,15),"day_str":"Sat Aug 15","girl":"Nora","time":"9:00 AM","location":"St. Aloysius","opponent":"St. Aloysius","home":False},
    {"date":date(2026,8,15),"day_str":"Sat Aug 15","girl":"Olivia","time":"11:00 AM","location":"St. Mary","opponent":"St. Mary","home":False},
    {"date":date(2026,8,22),"day_str":"Sat Aug 22","girl":"Nora","time":"10:00 AM","location":"St. Athanasius","opponent":"St. Athanasius","home":False},
    {"date":date(2026,8,22),"day_str":"Sat Aug 22","girl":"Olivia","time":"11:00 AM","location":"Holy Spirit","opponent":"Home Game","home":True},
    {"date":date(2026,8,29),"day_str":"Sat Aug 29","girl":"Nora","time":"9:00 AM","location":"St. Raphael","opponent":"St. Raphael","home":False},
    {"date":date(2026,8,29),"day_str":"Sat Aug 29","girl":"Olivia","time":"11:00 AM","location":"St. Patrick","opponent":"St. Patrick","home":False},
    {"date":date(2026,9,12),"day_str":"Sat Sep 12","girl":"Nora","time":"9:00 AM","location":"St. Agnes","opponent":"St. Agnes","home":False},
    {"date":date(2026,9,12),"day_str":"Sat Sep 12","girl":"Olivia","time":"11:00 AM","location":"St. Gabriel","opponent":"St. Gabriel","home":False},
    {"date":date(2026,9,19),"day_str":"Sat Sep 19","girl":"Nora","time":"9:00 AM","location":"St. Martha","opponent":"St. Martha","home":False},
    {"date":date(2026,9,19),"day_str":"Sat Sep 19","girl":"Olivia","time":"11:00 AM","location":"Sacred Heart Model","opponent":"Sacred Heart Model","home":False},
    {"date":date(2026,9,26),"day_str":"Sat Sep 26","girl":"Nora","time":"11:00 AM","location":"St. Gabriel","opponent":"St. Gabriel","home":False},
    {"date":date(2026,9,26),"day_str":"Sat Sep 26","girl":"Olivia","time":"12:00 PM","location":"St. Raphael","opponent":"St. Raphael","home":False},
]

def get_next_volleyball_games(today=None):
    if today is None:
        today=date.today()
    upcoming=[]
    for g in VOLLEYBALL_SCHEDULE:
        if g['date'] >= today:
            upcoming.append(g)
    upcoming_sorted=sorted(upcoming, key=lambda x: (x['date'], x['time']))
    return upcoming_sorted[:6]

def is_volleyball_game_day(girl_key, today=None):
    if today is None:
        today=date.today()
    # girl_key lower
    gname = "Nora" if girl_key=="nora" else "Olivia"
    for game in VOLLEYBALL_SCHEDULE:
        if game['date']==today and game['girl']==gname:
            return game
    return None

def is_school_day(d:date)->bool:
    if d.weekday()>=5:
        return False
    if d in NO_SCHOOL_DAYS:
        return False
    if d < FIRST_DAY_SCHOOL or d > LAST_DAY_SCHOOL:
        return False
    return True

def get_school_year_stats(today=None):
    if today is None:
        today=date.today()
    total=0
    cur=FIRST_DAY_SCHOOL
    while cur<=LAST_DAY_SCHOOL:
        if is_school_day(cur):
            total+=1
        cur+=td(days=1)
    if today < FIRST_DAY_SCHOOL:
        elapsed=0
        status="before_school"
    elif today > LAST_DAY_SCHOOL:
        elapsed=total
        status="summer"
    else:
        elapsed=0
        cur=FIRST_DAY_SCHOOL
        while cur<=today:
            if is_school_day(cur):
                elapsed+=1
            cur+=td(days=1)
        status="in_session" if is_school_day(today) else "no_school_today"
    remaining = total-elapsed if status!="before_school" else total
    pct = (elapsed/total*100) if total else 0
    next_event=None
    cur=today+td(days=1) if today>=FIRST_DAY_SCHOOL else FIRST_DAY_SCHOOL
    for i in range(400):
        check=cur+td(days=i)
        if check in NO_SCHOOL_DAYS:
            next_event=(check, NO_SCHOOL_DAYS[check])
            break
    days_until_start=(FIRST_DAY_SCHOOL-today).days if today<FIRST_DAY_SCHOOL else 0
    return {"total":total,"elapsed":elapsed,"remaining":remaining,"pct":pct,"status":status,"next_break":next_event,"days_until_start":days_until_start,"today_is_school":is_school_day(today),"today_reason":NO_SCHOOL_DAYS.get(today) or HALF_DAYS.get(today) or ("School Day" if is_school_day(today) else "Weekend")}

def get_milestone_for_day(n): return MILESTONES.get(n)
def is_last_day(t): return t==LAST_DAY_SCHOOL

# ====================== DATA ======================
DATA_FILE="leaders_data.json"
FAMILY_PHOTOS_DIR="assets/family_photos"
os.makedirs(FAMILY_PHOTOS_DIR, exist_ok=True)

SHOP_ITEMS={
    "✨ Falcons Style - Red & Black": {"Falcons Sparkly Headband Red/Black":35,"Falcons Pearl Necklace":45,"Shiny Falcons Shoes Black/Red":90,"Falcons Glitter Bow":30},
    "📚 Leader Gear": {"Holy Spirit Journal Falcons":60,"Gold Falcons Badge":75,"Falcons Prayer Bookmarks":35,"Falcons Backpack Charm":50},
    "🏐 Volleyball Gear": {"Custom Falcons Volleyball with Name":90,"Sparkly Socks Pack":35,"Team Hair Bow Set":30,"Cute Knee Pads":50,"Volleyball Water Bottle":45},
    "🧁 Kids Baking Championship": {
        "Baking Show Night + Bake Winning Recipe 🧁📺":70,
        "Bake-Off Challenge — Mom & Dad as Judges 👩‍🍳🏆":80,
        "Design Your Own Cupcake Challenge 🧁✨":55,
        "Falcons Team Cookies Red/Black/Silver 🍪🔴⚫️":60,
        "Baking Apron Falcons with Name 👩‍🍳":85,
        "Nora & Olivia Bake Sale Stand — Lemonade Style 🍋":100,
        "Make Your Own Sprinkle Mix 🌈":40,
        "Kids Baking Championship Trophy Night 🏆":90
    },
    "🌟 Fun Rewards": {"Extra Reading with Mom/Dad":50,"Choose Family Movie Night":80,"Bake Treat Together":65,"New Volleyball":85,"Friend Sleepover":150}
}
CHAMPION_REWARDS={
    "🏆 T1 Champion Badge Falcons": {"cost":0,"requires":"T1","desc":"End 1st Trimester Nov 6"},
    "❄️ T2 Winter Leader Badge": {"cost":0,"requires":"T2","desc":"End 2nd Trimester Feb 19"},
    "💯 100th Day Century Club Cape Falcons": {"cost":0,"requires":"100","desc":"Day 100 Jan 29"},
    "🎓 Falcons Year Leader Crown": {"cost":0,"requires":"T3","desc":"End Year May 28"},
    "🌟 150-Day Nails Sash 💅": {"cost":0,"requires":"150","desc":"Day 150 Apr 23 Nails Day"},
}
FAMILY_REWARD_UNLOCKS={
    "T1":{"name":"🍕 Family Dinner Out — T1!","coins_bonus":20,"desc":"T1 finish! Pick restaurant!","icon":"🍕"},
    "T2":{"name":"☕🎲 Hot Cocoa Game Night","coins_bonus":20,"desc":"T2 finish! Cozy night!","icon":"🎲"},
    "100":{"name":"💯🎬 100th Day Pizza Movie Night","coins_bonus":30,"desc":"100 days! Pizza + movie!","icon":"💯"},
    "150":{"name":"💅✨ Girls Nails Done Day — Falcons Spa","coins_bonus":25,"desc":"150 days! Nails with Mom!","icon":"💅"},
    "T3":{"name":"🎡☀️ End of Year Adventure!","coins_bonus":50,"desc":"Finished 174 days! Big adventure!","icon":"🎉"},
    "VB5":{"name":"🏐 Falcons Volleyball Family Pizza After Game!","coins_bonus":20,"desc":"5 volleyball games logged — family pizza after next game!","icon":"🏐"},
    "BAKE1":{"name":"🧁 Baking Night — Kids Baking Championship Watch + Bake!","coins_bonus":25,"desc":"Bought first baking reward — watch show + bake winning recipe together!","icon":"🧁"},
    "SPIN10":{"name":"🎡 Family Ice Cream Out — 10 Spins!","coins_bonus":20,"desc":"10 spin wheel spins — celebrate with ice cream!","icon":"🍦"},
    "COLLECT10":{"name":"👗 Cover Star Family Movie Night + Popcorn Fort","coins_bonus":30,"desc":"Collected 10 outfits — you are Cover Stars! Family movie night!","icon":"📸"},
}

NORA_FOCUS_CHOICE_BOARD=[
    "👀 Game Focus — Eyes on teacher/coach like eyes on volleyball! 🏐 I locked in!",
    "📝 Write it Down — I wrote my thought instead of saying it out loud!",
    "💨 Take 3 Deep Breaths — When I wanted to talk, I breathed first!",
    "🙋‍♀️ Raise Hand & Wait — I raised my hand and waited to be called!",
    "🤫 Whisper Check — I used a whisper voice to ask neighbor quietly!",
    "👂 Listening Ears + Heart — I used listening ears + heart to hear first!",
    "⏸️ Pause Power — I paused 5 seconds before speaking!",
    "🎯 One Thing Focus — I focused on ONE thing at a time!",
]

OLIVIA_FOCUS_CHOICE_BOARD=[
    "👑 Captain Encourage — I encouraged a younger Falcon teammate!",
    "🤝 Mentor Moment — I helped a 4th grader who was nervous!",
    "📣 Positive Cheer — I cheered for my team even when we were behind!",
    "💬 Kind Words — I used gentle, kind words to lift someone!",
    "🙏 Lead by Example — I did the right thing even when no one watched!",
    "💡 Initiative Serve — I started a helpful task without being asked!",
]

DTI_RUNWAY_THEMES=[
    {"theme":"Falcons Volleyball Game Day 🏐🔴⚫️","desc":"Dress like you're ready to SPIKE for Holy Spirit Falcons! Jersey, knee pads, bow!","icon":"🏐","bonus_stars":15},
    {"theme":"Elegant Leader 👑✨","desc":"Team Captain elegant leader look — graceful, confident, Holy Spirit style!","icon":"👑","bonus_stars":15},
    {"theme":"Nails Done Day Sparkle 💅✨","desc":"Show off your polish! Sparkly nails + cute outfit for spa day!","icon":"💅","bonus_stars":15},
    {"theme":"Baking Championship Apron 👩‍🍳🧁","desc":"Kids Baking Championship ready! Apron, sprinkles, Falcons colors!","icon":"🧁","bonus_stars":15},
    {"theme":"First Day Ready 📚🦅","desc":"First Day of School ready — organized, prepared, Falcons spirit!","icon":"📚","bonus_stars":10},
    {"theme":"Spirit Day — Red Black White 🔴⚫️⚪️","desc":"Full Falcons spirit! Red, black, white like Atlanta Falcons!","icon":"🦅","bonus_stars":15},
    {"theme":"Cover Star Magazine 📸⭐","desc":"You are the Cover Star! Magazine cover look — fierce & elegant!","icon":"⭐","bonus_stars":20},
]
POLISH_COLORS={
    "Ballet Pink 💗":{"hex":"#FFB6C1","emoji":"💗","desc":"Classic pink"},
    "Sparkly Pink Glitter ✨💖":{"hex":"#FF69B4","emoji":"✨","desc":"Extra sparkle"},
    "Lavender Dream 💜":{"hex":"#B19CD9","emoji":"💜","desc":"Calm & confident"},
    "Falcons Red ❤️🖤":{"hex":"#A71930","emoji":"🔴","desc":"Falcons RED! Team spirit!"},
    "Jet Black Glitter 🖤✨":{"hex":"#000000","emoji":"🖤","desc":"Falcons black — fierce!"},
    "Light Blue Sky 💙":{"hex":"#87CEEB","emoji":"💙","desc":"Holy Spirit sky"},
    "Clear Shimmer ⭐":{"hex":"#FFF0F5","emoji":"⭐","desc":"Subtle elegant"},
    "Pastel Rainbow 🌈":{"hex":"#FFDDE1","emoji":"🌈","desc":"Fun creative"},
}
SPIN_PRIZES=[
    {"name":"⭐ 10 Stars","stars":10,"coins":0,"icon":"⭐","color":"#fde68a"},
    {"name":"🪙 15 Coins","stars":0,"coins":15,"icon":"🪙","color":"#bfdbfe"},
    {"name":"🌟 JACKPOT 20 Stars +15 Coins!","stars":20,"coins":15,"icon":"🌟","color":"#fbbf24"},
    {"name":"🏐 Volleyball Bonus! Free Polish!","stars":5,"coins":5,"icon":"🏐","color":"#fbcfe8","special":"polish_free"},
    {"name":"🎁 Sparkly Falcons Socks!","stars":0,"coins":0,"icon":"🧦","color":"#ddd6fe","special":"outfit","outfit":"✨ Falcons Socks (Spin Win)"},
    {"name":"🔴 Falcons Faith Bonus +15","stars":15,"coins":5,"icon":"🕊️","color":"#fef3c7"},
    {"name":"🏐 Serve Ace! +12 Coins","stars":0,"coins":12,"icon":"🏐","color":"#bae6fd"},
    {"name":"📚 Study Star +12","stars":12,"coins":0,"icon":"📚","color":"#e0e7ff"},
    {"name":"🦅 Falcons Fly! 25 Stars +25 Coins","stars":25,"coins":25,"icon":"🦅","color":"#f5d0fe","special":"outfit","outfit":"🦅 Falcons Wings (Spin Win)"},
]
SECRET_CODES={
    "HOLYSPIRIT":{"stars":20,"coins":20,"msg":"Holy Spirit power!","icon":"🕊️"},
    "FALCONS":{"stars":25,"coins":25,"msg":"GO FALCONS! 🔴⚫️","icon":"🦅"},
    "VOLLEYBALL":{"stars":20,"coins":20,"msg":"Volleyball Stars! 🏐","icon":"🏐"},
    "LEADER":{"stars":15,"coins":10,"msg":"Leader!","icon":"⭐"},
    "JOY":{"stars":10,"coins":10,"msg":"Joy!","icon":"😊"},
    "OLIVIA":{"stars":15,"coins":15,"msg":"Olivia!","icon":"👧"},
    "NORA":{"stars":15,"coins":15,"msg":"Nora!","icon":"👧"},
    "NAILS":{"stars":10,"coins":15,"msg":"Nails Day! 💅","icon":"💅"},
    "100DAYS":{"stars":25,"coins":25,"msg":"Century Club! 💯","icon":"💯"},
    "SPIKE":{"stars":15,"coins":15,"msg":"SPIKE! 🔥","icon":"🏐"},
}
QUIZ_QUESTIONS=[
    {"q":"Your teammate misses a serve in Falcons volleyball. What do you do?","options":["Get mad","Say 'Good try! Next one! You got it!'","Ignore her"],"correct":1,"virtue":"Encourages Others","explain":"Falcons lift each other! Encouragement = leadership!"},
    {"q":"It's game day vs St. Raphael and you feel nervous. What's a Falcon leader do?","options":["Hide","Take deep breath, pray, focus on team","Cry"],"correct":1,"virtue":"Courage","explain":"Courage = do hard right thing! Deep breaths & prayer!"},
    {"q":"You want to talk in class but teacher is talking. Volleyball focus move?","options":["Keep talking","DIG! Self-control - eyes on teacher like eyes on ball","Whisper"],"correct":1,"virtue":"Self-Control","explain":"DIG = self-control! Libero focus!"},
]
FRUITS_OF_SPIRIT={"Love":"Show love","Joy":"Choose joy","Peace":"Be peacemaker","Patience":"Wait happy","Kindness":"Small kindness big impact","Goodness":"Do right when no one watching","Faithfulness":"Faithful small things","Gentleness":"Gentle words strong heart","Self-Control":"You are in charge of you"}
LEADERSHIP_BEHAVIORS=["Shows Initiative - Started without being asked","Leads by Example","Takes Full Responsibility","Makes Wise Choices","Shows Courage","Practices Self-Control","Encourages Others","Shows Perseverance","Is Organized & Prepared","Listens & Follows Directions","Shows Honesty & Integrity","Shows Gratitude & Humility"]
HEALTH_PILLARS={"Fuel 🍎":["Ate fruits/veg","Drank 4+ water","Balanced meal","Limited candy/soda"],"Move 🏐":["30+ min active / volleyball practice","Played outside","Volleyball game/practice","Stretch/workout"],"Rest 😴":["8+ hrs sleep","On-time bedtime","Calm morning routine","Limited screens before bed"],"Heart & Mind 💜":["Morning prayer","Act of kindness","Gratitude journal","Deep breaths when upset"]}
SCHOOL_SUBJECTS=["Religion","Math","Reading/LA","Science","Social Studies","Spelling/Vocab","Art/Music/PE/Volleyball"]
VOLLEYBALL_POWERS={
    "SERVE 💥":{"behavior":"Shows Initiative","desc":"Start play! Like strong serve!"},
    "BUMP 🤝":{"behavior":"Gratitude & Teamwork","desc":"Bump to teammate!"},
    "SET ✨":{"behavior":"Encourages Others","desc":"Set teammate to shine!"},
    "SPIKE 🔥":{"behavior":"Courage + Perseverance","desc":"Big spike even when scary!"},
    "DIG 🛡️":{"behavior":"Self-Control + Focus","desc":"Game Focus! Eyes on ball!"},
}
VERSE_OF_DAY=[("'The fruit of the Spirit is love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control.'","Galatians 5:22-23"),("'I can do all things through Christ who strengthens me.'","Philippians 4:13"),("'Let your light shine.'","Matthew 5:16")]

def default_girl_data():
    return {'stars':0,'coins':75,'level':1,'outfits':[],'history':[],'grades':[],'streak':0,'last_checkin':None,'service_logs':[],'journal_entries':[],'milestones_claimed':[],'family_rewards_claimed':[],'nail_polish':None,'nail_polish_history':[],'last_spin_date':None,'spin_count':0,'spin_history':[],'secret_codes_claimed':[],'quiz_score':0,'quiz_history':[],'volleyball_games':[],'volleyball_stats':{'serves':0,'team_cheers':0,'focus_plays':0},'baking_logs':[],'baking_badges':[],'birthday_claimed_year':None,'runway_submissions':[],'runway_score':0,'focus_choice_today':None}

if 'data' not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,'r') as f:
                st.session_state.data=json.load(f)
                for g in ['olivia','nora']:
                    if g not in st.session_state.data:
                        st.session_state.data[g]=default_girl_data()
                    for k,v in default_girl_data().items():
                        if k not in st.session_state.data[g]:
                            st.session_state.data[g][k]=v
                if 'family_photos' not in st.session_state.data:
                    st.session_state.data['family_photos']=[]
                if 'family_adventures_log' not in st.session_state.data:
                    st.session_state.data['family_adventures_log']=[]
        except:
            st.session_state.data={'olivia':default_girl_data(),'nora':default_girl_data(),'family_photos':[],'family_adventures_log':[]}
    else:
        st.session_state.data={'olivia':default_girl_data(),'nora':default_girl_data(),'family_photos':[],'family_adventures_log':[]}
    if 'family_photos' not in st.session_state.data:
        st.session_state.data['family_photos']=[]
    if 'family_adventures_log' not in st.session_state.data:
        st.session_state.data['family_adventures_log']=[]

if 'view' not in st.session_state:
    st.session_state.view="home"

def save_data():
    try:
        with open(DATA_FILE,'w') as f:
            json.dump(st.session_state.data,f,indent=2,default=str)
    except:
        pass

def get_level(s): return s//150+1

def get_avatar_path(girl):
    # Prefer real volleyball avatars that look like them
    real = f"{ASSETS_DIR}/{girl}_real_volleyball.png"
    if os.path.exists(real):
        return real
    vb = f"{ASSETS_DIR}/{girl}_volleyball_avatar.png"
    if os.path.exists(vb):
        return vb
    base = f"{ASSETS_DIR}/{girl}_avatar.png"
    if os.path.exists(base):
        return base
    return f"https://picsum.photos/seed/{girl}falcons/400/400"

def claim_milestone(girl_key, day_key):
    data=st.session_state.data[girl_key]
    if day_key in data.get('milestones_claimed',[]):
        return False
    if day_key=="LAST":
        ms=LAST_DAY_MILESTONE
    elif day_key in ["T1","T2","T3"]:
        ms=next((v for v in TRIMESTER_BONUSES.values() if v["key"]==day_key),None)
        if not ms:
            return False
    else:
        ms=MILESTONES.get(int(day_key)) if str(day_key).isdigit() else None
        if not ms:
            return False
    data['stars']+=ms['stars']
    data['coins']+=ms['coins']
    data['milestones_claimed'].append(str(day_key))
    data['history'].append({"date":str(date.today()),"virtue":"Milestone","leadership":[ms['name']],"health":[],"points":ms['stars']})
    save_data()
    return ms

def claim_family_reward(girl_key, req_key):
    data=st.session_state.data[girl_key]
    if req_key in data.get('family_rewards_claimed',[]):
        return False
    if req_key not in data.get('milestones_claimed',[]):
        if req_key=="T3" and "LAST" not in data.get('milestones_claimed',[]):
            return False
        elif req_key!="T3":
            if req_key not in data.get('milestones_claimed',[]):
                # allow if milestone date passed? still require claim
                pass
    reward=FAMILY_REWARD_UNLOCKS.get(req_key)
    if not reward:
        return False
    if req_key not in data.get('milestones_claimed',[]) and req_key!="150" and req_key!="100":
        # need milestone claimed
        if req_key not in data.get('milestones_claimed',[]):
            return False
    data['family_rewards_claimed'].append(req_key)
    data['coins']+=reward.get('coins_bonus',20)
    data['stars']+=10
    save_data()
    return reward

def spin_daily_wheel(girl_key):
    data=st.session_state.data[girl_key]
    today_str=str(date.today())
    if data.get('last_spin_date')==today_str:
        return None,"Already spun!"
    prize=random.choice(SPIN_PRIZES)
    data['stars']+=prize['stars']
    data['coins']+=prize['coins']
    data['last_spin_date']=today_str
    data['spin_count']=data.get('spin_count',0)+1
    data['spin_history'].append({"date":today_str,"prize":prize['name']})
    if 'special' in prize and prize['special']=='outfit':
        outfit=prize.get('outfit')
        if outfit and outfit not in data['outfits']:
            data['outfits'].append(outfit)
    save_data()
    return prize,"Success"

def claim_secret_code_fn(girl_key, code):
    code=code.strip().upper()
    data=st.session_state.data[girl_key]
    if code in data.get('secret_codes_claimed',[]):
        return None,"Already claimed!"
    if code not in SECRET_CODES:
        return None,"Try FALCONS, VOLLEYBALL, SPIKE, HOLYSPIRIT, OLIVIA, NORA!"
    pz=SECRET_CODES[code]
    data['stars']+=pz['stars']
    data['coins']+=pz['coins']
    data['secret_codes_claimed'].append(code)
    save_data()
    return pz,pz['msg']

def claim_birthday_bonus(girl_key):
    data=st.session_state.data[girl_key]
    today=date.today()
    if data.get('birthday_claimed_year')==today.year:
        return False
    # birthday bonus
    data['stars']+=50
    data['coins']+=50
    data['birthday_claimed_year']=today.year
    # add outfit birthday badge
    dob = OLIVIA_DOB if girl_key=="olivia" else NORA_DOB
    age_info=get_age_and_next_birthday(dob, today)
    badge=f"🎂 Birthday {age_info['age']} Badge!"
    if badge not in data['outfits']:
        data['outfits'].append(badge)
    save_data()
    return True

BAKING_CHALLENGES=[
    {"name":"Falcons Red Velvet Cupcakes 🔴","desc":"Bake red velvet cupcakes with cream cheese frosting, Falcons colors!","stars":15,"coins":10},
    {"name":"Nora's Volleyball Cake Pops 🏐","desc":"Cake pops decorated like volleyballs!","stars":15,"coins":10},
    {"name":"Olivia's Elegant Sugar Cookies 👑","desc":"Elegant decorated sugar cookies with royal icing, leader style!","stars":12,"coins":8},
    {"name":"Kids Baking Championship Showstopper 🧁🏆","desc":"Recreate a winning recipe from the show! Watch episode together first!","stars":25,"coins":20},
    {"name":"Team Spirit Cookies 🦅","desc":"Black, red, white sugar cookies with Falcons logo frosting!","stars":15,"coins":10},
]

def log_baking(girl_key, bake_name, notes):
    data=st.session_state.data[girl_key]
    entry={"date":str(date.today()),"bake":bake_name,"notes":notes,"points":0}
    # Find challenge points
    for chal in BAKING_CHALLENGES:
        if chal['name']==bake_name:
            entry['points']=chal['stars']
            data['stars']+=chal['stars']
            data['coins']+=chal['coins']
            break
    data['baking_logs'].append(entry)
    # badge
    badge=f"🧁 Baked: {bake_name[:25]}"
    if badge not in data['outfits']:
        data['outfits'].append(badge)
    save_data()
    return entry

# ====================== SIDEBAR FALCONS ======================
with st.sidebar:
    # Falcons logo - use fixed version - exact jersey match
    logo = "assets/falcons_logo_exact_jersey.png"
    if not os.path.exists(logo):
        logo = "assets/falcons_logo_exact_jersey.png"
    if not os.path.exists(logo):
        logo = "assets/holy_spirit_falcons_logo_real.png"
    if os.path.exists(logo):
        st.image(logo, use_container_width=True)
    else:
        st.markdown("<h2 style='text-align:center;color:#A71930'>🦅 FALCONS</h2>", unsafe_allow_html=True)
    st.markdown("### 🏐 Holy Spirit Falcons")
    st.caption("Red + Black + White • Like Atlanta Falcons!")
    
    stats=get_school_year_stats()
    # School day
    if stats['status']=="before_school":
        st.markdown(f"<div style='background:#000;color:white;padding:10px;border-radius:10px;text-align:center;border:2px solid #A71930'><b>📚 {stats['days_until_start']} days until school!</b><br><small>First Day Aug 11</small></div>", unsafe_allow_html=True)
    elif stats['status']!="summer":
        st.markdown(f"<div style='background:#A71930;color:white;padding:10px;border-radius:10px;text-align:center'><b>📅 Day {stats['elapsed']} of {stats['total']}</b><br><small>{stats['pct']:.0f}% • {stats['today_reason']}</small></div>", unsafe_allow_html=True)
        st.progress(stats['pct']/100)
    # Volleyball next game
    next_games=get_next_volleyball_games()
    if next_games:
        ng=next_games[0]
        days_to=(ng['date']-date.today()).days
        st.markdown(f"<div style='background:#000;color:#fff;padding:10px;border-radius:10px;text-align:center;margin-top:8px;border:2px solid #A71930'><b>🏐 Next Falcons Game!</b><br><small>{ng['girl']} • {ng['day_str']} {ng['time']}</small><br><small>@ {ng['location']} vs {ng['opponent']}</small><br><b>{'TODAY!' if days_to==0 else f'In {days_to} days!' if days_to>0 else 'Past'}</b></div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🏠 Home — Falcons HQ", use_container_width=True):
        st.session_state.view="home"; st.rerun()
    if st.button("🏐 Falcons Volleyball Schedule", use_container_width=True, type="primary"):
        st.session_state.view="volleyball"; st.rerun()
    if st.button("👗 Dress to Impress Runway! ⭐", use_container_width=True):
        st.session_state.view="runway"; st.rerun()
    if st.button("🧁 Baking Championship", use_container_width=True):
        st.session_state.view="baking"; st.rerun()
    if st.button("📅 School Calendar", use_container_width=True):
        st.session_state.view="calendar"; st.rerun()
    if st.button("🎮 Fun Zone — Games!", use_container_width=True):
        st.session_state.view="funzone"; st.rerun()
    if st.button("📸 Family Photos", use_container_width=True):
        st.session_state.view="memories"; st.rerun()
    if st.button("📖 Yearbook", use_container_width=True):
        st.session_state.view="yearbook"; st.rerun()
    if st.button("👧 Olivia — Team Captain (5th) 🎂 8/31/15", use_container_width=True):
        st.session_state.view="olivia"; st.rerun()
    if st.button("🏐 Nora — Volleyball Star (4th) 🎂 4/27/17", use_container_width=True):
        st.session_state.view="nora"; st.rerun()
    if st.button("🌟 Sunday Family Review", use_container_width=True):
        st.session_state.view="review"; st.rerun()
    
    st.divider()
    st.caption(f"Olivia: ⭐{st.session_state.data['olivia']['stars']} 🪙{st.session_state.data['olivia']['coins']} Lvl {get_level(st.session_state.data['olivia']['stars'])}")
    st.caption(f"Nora: ⭐{st.session_state.data['nora']['stars']} 🪙{st.session_state.data['nora']['coins']} Lvl {get_level(st.session_state.data['nora']['stars'])}")
    if st.button("🔒 Lock (Logout)", use_container_width=True):
        st.session_state.authenticated=False; st.rerun()

# ====================== HOME ======================
def show_home():
    st.markdown("<div class='main-header'>🦅 HOLY SPIRIT FALCONS VOLLEYBALL LEADERS 🏐</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>🔴 BLACK + RED + WHITE like Atlanta Falcons! • Olivia (5th) Captain & Nora (4th) Volleyball Star • To Know. To Love. To Serve. Catch the Spirit!</div>", unsafe_allow_html=True)
    
    # Falcons banner with logo
    c_logo, c_banner = st.columns([1,4])
    with c_logo:
        lp="assets/falcons_logo_exact_jersey.png"
        if os.path.exists(lp):
            st.image(lp, width=140)
    with c_banner:
        st.markdown(f"""
        <div class='falcons-banner'>
            <div style='font-size:2rem;font-weight:900'>GO FALCONS! 🔴⚫️⚪️</div>
            <div>Olivia #5 Team Captain • Nora #7 Libero Focus Star • Holy Spirit School Louisville — Home of the Falcons!</div>
            <div style='font-size:0.9rem;margin-top:6px;'>Real Mascot just like Atlanta Falcons — Black Falcon with Red streaks!</div>
        </div>
        """, unsafe_allow_html=True)
    
    stats=get_school_year_stats()
    next_games=get_next_volleyball_games()
    
    # School + Volleyball countdown side by side
    col_school, col_vb = st.columns(2)
    with col_school:
        if stats['status']=="before_school":
            st.markdown(f"""<div style="background: linear-gradient(135deg,#000 0%,#A71930 100%); color:white; padding:16px; border-radius:15px; text-align:center;"> <div style="font-size:2rem;font-weight:900">⏳ {stats['days_until_start']} DAYS UNTIL SCHOOL!</div><div>First Day Aug 11 Noon — {stats['total']} days total</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="background: linear-gradient(135deg,#FFE4E1 0%,#fff 100%); padding:14px; border-radius:15px; border:3px solid #A71930; text-align:center;"><div style="color:#000;font-weight:800">HOLY SPIRIT {SCHOOL_YEAR_LABEL}</div><div style="font-size:2.2rem;font-weight:900;color:#A71930">📚 DAY {stats['elapsed']} OF {stats['total']}</div><div>{stats['pct']:.0f}% • {stats['remaining']} left • {stats['today_reason']}</div></div>""", unsafe_allow_html=True)
            st.progress(stats['pct']/100)
    with col_vb:
        if next_games:
            ng=next_games[0]
            days_to=(ng['date']-date.today()).days
            is_today = days_to==0
            bg = "linear-gradient(135deg,#A71930 0%,#000 100%)" if is_today else "linear-gradient(135deg,#000 0%,#333 100%)"
            st.markdown(f"""<div style="background:{bg}; color:white; padding:14px; border-radius:15px; text-align:center; border:3px solid #A71930;"><div style="font-weight:800">🏐 NEXT FALCONS VOLLEYBALL GAME</div><div style="font-size:1.6rem;font-weight:900">{ng['girl']} — {ng['day_str']} {ng['time']}</div><div>@ {ng['location']} vs {ng['opponent']}</div><div style="font-size:1.3rem;margin-top:5px;font-weight:900">{'🔥 TODAY IS GAME DAY! 🔥' if is_today else f'In {days_to} days!'}</div></div>""", unsafe_allow_html=True)
            if is_today:
                st.balloons()
        else:
            st.info("Volleyball season done! Great job Falcons! 🦅")
    
    # Milestone banner
    milestone = get_milestone_for_day(stats['elapsed']) if stats['status'] not in ["before_school","summer"] else None
    if milestone:
        st.markdown(f"""<div style="background: linear-gradient(135deg,#fef08a 0%,#fbbf24 100%); padding:16px; border-radius:15px; border:3px dashed #A71930; text-align:center; margin:12px 0;"><div style="font-size:2rem">{milestone['icon']} MILESTONE DAY! {milestone['icon']}</div><div style="font-size:1.4rem;font-weight:900">{milestone['name']}</div><div>{milestone['msg']} — ⭐{milestone['stars']} + 🪙{milestone['coins']} each!</div></div>""", unsafe_allow_html=True)
    
    # Birthdays + Baking banner
    olivia_bday=get_age_and_next_birthday(OLIVIA_DOB)
    nora_bday=get_age_and_next_birthday(NORA_DOB)
    
    # Show birthday banner if upcoming within 60 days or today
    bday_col1,bday_col2=st.columns(2)
    with bday_col1:
        ol_days = olivia_bday['days_until']
        ol_age_next = olivia_bday['age']+1
        if olivia_bday['is_today']:
            st.balloons()
            st.markdown(f"<div style='background:linear-gradient(135deg,#FFB6C1 0%,#A71930 100%);color:white;padding:12px;border-radius:12px;text-align:center;border:3px solid white'><b>🎂 TODAY IS OLIVIA'S BIRTHDAY! 🎉</b><br>Turns {olivia_bday['age']}! Born {olivia_bday['dob_str']} — DOB 8/31/2015<br>Claim 50⭐ bonus!</div>", unsafe_allow_html=True)
        elif ol_days<=35:
            st.markdown(f"<div style='background:#FFE4E1;padding:10px;border-radius:10px;border:2px dashed #A71930;text-align:center'><b>🎂 Olivia Birthday in {ol_days} days!</b> Aug 31 — Turns {ol_age_next}!</div>", unsafe_allow_html=True)
    with bday_col2:
        nora_days = nora_bday['days_until']
        if nora_bday['is_today']:
            st.balloons()
            st.markdown(f"<div style='background:linear-gradient(135deg,#E0F2FE 0%,#000 100%);color:white;padding:12px;border-radius:12px;text-align:center;border:3px solid #A71930'><b>🎂 TODAY IS NORA'S BIRTHDAY! 🎉</b><br>Turns {nora_bday['age']}! Born {nora_bday['dob_str']} — DOB 4/27/17<br>Claim 50⭐ bonus!</div>", unsafe_allow_html=True)
        elif nora_days<=60:
            st.markdown(f"<div style='background:#E0F2FE;padding:10px;border-radius:10px;border:2px dashed #000;text-align:center'><b>🎂 Nora Birthday in {nora_days} days!</b> Apr 27 — Age {nora_bday['age']}</div>", unsafe_allow_html=True)
    
    # Baking teaser
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#FFB6C1 0%,#FFE4E1 50%,#fff 100%); padding:12px; border-radius:12px; border:2px solid #A71930; text-align:center; margin:8px 0;">
        <b>🧁 Kids Baking Championship Fans! 🏆</b> Olivia (11 on 8/31) & Nora (9) — New Baking Rewards in Boutique! Bake together = stars + family memories! <b>Click 🧁 Baking Championship in sidebar!</b>
    </div>
    """, unsafe_allow_html=True)
    
    # Verse
    v_text,v_ref=VERSE_OF_DAY[0]
    st.info(f"**Falcons Verse:** {v_text} — {v_ref} • To Know. To Love. To Serve.")
    
    # Girls cards - SUPER FUN NOW
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="girl-card olivia">', unsafe_allow_html=True)
        avatar=get_avatar_path('olivia')
        st.image(avatar, caption="Olivia — #5 Team Captain & Elegant Leader — Falcons!", use_container_width=True)
        data=st.session_state.data['olivia']
        st.markdown(f"**Olivia Davis — 5th Grade Falcons Captain** | <span class='level-badge'>Level {get_level(data['stars'])} Falcons</span>", unsafe_allow_html=True)
        st.progress(min(data['stars']%150/150,1.0), text=f"{data['stars']%150}/150 to next level • ⭐{data['stars']} 🪙{data['coins']}")
        # Volleyball power bar
        st.caption("🏐 Captain Powers: SERVE 💥 BUMP 🤝 SET ✨ SPIKE 🔥 DIG 🛡️")
        # Next game for Olivia
        olivia_next = [g for g in next_games if g['girl']=="Olivia"][:1]
        if olivia_next:
            og=olivia_next[0]
            st.markdown(f"<div style='background:#000;color:white;padding:8px;border-radius:8px;text-align:center'>🏐 Next: {og['day_str']} {og['time']} @ {og['location']}</div>", unsafe_allow_html=True)
        st.caption(f"Look: {', '.join(data['outfits'][-3:]) if data['outfits'] else 'Falcons Jersey Classic Red/Black'}")
        if st.button("Enter Olivia's Falcons Journey → 🏐", key="olivia_btn", type="primary", use_container_width=True):
            st.session_state.view="olivia"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="girl-card nora">', unsafe_allow_html=True)
        avatar=get_avatar_path('nora')
        st.image(avatar, caption="Nora — #7 Volleyball Star & Focus Champion — Falcons!", use_container_width=True)
        data=st.session_state.data['nora']
        st.markdown(f"**Nora Davis — 4th Grade Falcons Volleyball Star** | <span class='level-badge'>Level {get_level(data['stars'])} Falcons</span>", unsafe_allow_html=True)
        st.progress(min(data['stars']%150/150,1.0), text=f"{data['stars']%150}/150 to next level • ⭐{data['stars']} 🪙{data['coins']}")
        st.markdown("<div style='background: linear-gradient(90deg,#A71930,#000); color:white; padding:8px; border-radius:8px; text-align:center; font-weight:800;'>🏐 VOLLEYBALL MODE: BUMP • SET • SPIKE! 💥</div>", unsafe_allow_html=True)
        nora_next = [g for g in next_games if g['girl']=="Nora"][:1]
        if nora_next:
            ng=nora_next[0]
            days_to=(ng['date']-date.today()).days
            game_label = f"Next: {ng['day_str']} {ng['time']}"
            if days_to==0:
                game_label = "🔥 GAME TODAY!"
            st.markdown(f"<div style='background:#A71930;color:white;padding:8px;border-radius:8px;text-align:center'>{game_label} @ {ng['location']}</div>", unsafe_allow_html=True)
        # Make it EXCITING - quick fun
        c_spin,c_quiz = st.columns(2)
        with c_spin:
            can_spin = data.get('last_spin_date')!=str(date.today())
            if st.button(f"{'🎡 SPIN NOW!' if can_spin else '✅ Spun Today'}", key="nora_home_spin", use_container_width=True, type="primary" if can_spin else "secondary"):
                if can_spin:
                    prize,_=spin_daily_wheel('nora')
                    st.balloons()
                    st.success(f"Nora won {prize['name']}!")
                    st.rerun()
        with c_quiz:
            if st.button("🧠 Quiz!", key="nora_home_quiz", use_container_width=True):
                st.session_state.view="funzone"; st.rerun()
        st.caption(f"Look: {', '.join(data['outfits'][-3:]) if data['outfits'] else 'Falcons Jersey Red/Black + Volleyball!'}")
        if st.button("Enter Nora's Falcons Journey → 🏐✨", key="nora_btn", type="primary", use_container_width=True):
            st.session_state.view="nora"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Family photo if exists
    if os.path.exists("assets/family_real_photo.jpg"):
        st.divider()
        st.markdown("### 👨‍👩‍👧‍👧 Our Falcons Family")
        st.image("assets/family_real_photo.jpg", caption="The Davis Family — Olivia & Nora's Falcons Family — Holy Spirit School", width=450)

def show_volleyball():
    st.header("🏐 Holy Spirit Falcons Volleyball — Olivia & Nora's Schedule")
    st.caption("Mascot: Falcons like Atlanta Falcons 🔴⚫️⚪️ • Black Falcon with Red streaks on White Jersey • Real 2026 Season!")
    
    if st.button("← Back to Home"):
        st.session_state.view="home"; st.rerun()
    
    # Falcons logo banner
    col_l,col_b = st.columns([1,3])
    with col_l:
        lp="assets/falcons_logo_exact_jersey.png"
        if os.path.exists(lp):
            st.image(lp, width=160)
    with col_b:
        st.markdown(f"""
        <div class='falcons-banner'>
            <div style='font-size:1.8rem;font-weight:900'>🦅 FALCONS VOLLEYBALL — GO FALCONS! 🏐</div>
            <div>Olivia #5 (5th Grade) & Nora #7 (4th Grade) — Holy Spirit Falcons CSAA League • Louisville KY</div>
            <div style='font-size:0.9rem;margin-top:4px'>Team Colors: Falcons Red #A71930 + Black + White + Silver — Just like Atlanta Falcons!</div>
        </div>
        """, unsafe_allow_html=True)
    
    next_games=get_next_volleyball_games()
    if next_games:
        ng=next_games[0]
        days_to=(ng['date']-date.today()).days
        if days_to==0:
            st.balloons()
            st.markdown(f"""<div style="background: linear-gradient(135deg,#A71930 0%,#000 100%); color:white; padding:20px; border-radius:18px; text-align:center; border:4px solid white;"><div style="font-size:2.5rem;font-weight:900">🔥 TODAY IS GAME DAY! 🔥</div><div style="font-size:1.8rem">{ng['girl']} — {ng['day_str']} {ng['time']} @ {ng['location']}</div><div>vs {ng['opponent']} • Falcons Rise Up!</div></div>""", unsafe_allow_html=True)
    
    col_table,col_next = st.columns([1.6,1])
    with col_table:
        st.subheader(f"📅 Full Schedule — {len(VOLLEYBALL_SCHEDULE)} Games")
        df=pd.DataFrame(VOLLEYBALL_SCHEDULE)
        df['DateObj']=df['date']
        df['DateStr']=df['date'].apply(lambda x: x.strftime("%a %b %d, %Y"))
        df['Countdown']=df['date'].apply(lambda x: (x-date.today()).days)
        df['When']=df['Countdown'].apply(lambda n: f"In {n} days" if n>0 else "TODAY! 🔥" if n==0 else f"{abs(n)} days ago" if n>-7 else "Past")
        
        # Filter
        girl_filter=st.multiselect("Filter Girl", ["Olivia","Nora"], default=["Olivia","Nora"])
        filtered=df[df['girl'].isin(girl_filter)] if girl_filter else df
        
        show_upcoming=st.checkbox("Show only upcoming", value=True)
        if show_upcoming:
            upcoming=filtered[filtered['DateObj']>=date.today()]
        else:
            upcoming=filtered
        
        st.dataframe(upcoming[["day_str","girl","time","location","opponent","When"]].sort_values("day_str"), use_container_width=True, height=420)
        
        st.markdown("### 🏐 Game Day Check-In (After Each Game)")
        sel_girl=st.radio("Who played?", ["Olivia","Nora"], horizontal=True, key="vb_girl")
        gk=sel_girl.lower()
        game_sel=st.selectbox("Which game?", [f"{g['day_str']} {g['time']} @ {g['location']} vs {g['opponent']}" for g in VOLLEYBALL_SCHEDULE if g['girl']==sel_girl], key="vb_game_select")
        effort=st.slider(f"{sel_girl}'s effort today (1-10)", 1,10,8, key="vb_effort")
        teamwork=st.multiselect(f"{sel_girl}'s Falcons Leadership Today", ["Encouraged teammates 📣","Listened to coach 👂","Stayed focused like Libero 🛡️","Showed courage to serve/spike 🔥","Helped team with Positivity ✨"], key="vb_lead")
        if st.button(f"Log Game for {sel_girl} 🏐 + Stars!"):
            pts=len(teamwork)*6 + effort
            st.session_state.data[gk]['stars']+=pts
            st.session_state.data[gk]['coins']+=pts//2
            st.session_state.data[gk]['volleyball_stats']['serves']+=1
            st.session_state.data[gk]['volleyball_games'].append({"date":str(date.today()),"game":game_sel,"effort":effort,"teamwork":teamwork,"points":pts})
            save_data()
            st.balloons()
            st.success(f"{sel_girl} earned +{pts}⭐ for Falcons game! Teamwork makes the dream work!")
            st.rerun()
    
    with col_next:
        st.subheader("🎯 Next Games Countdown")
        today=date.today()
        for g in sorted(VOLLEYBALL_SCHEDULE, key=lambda x: x['date']):
            days=(g['date']-today).days
            if days>= -1:
                color="#A71930" if days<=3 and days>=0 else "#000" if g['home'] else "#333"
                bg="#FFE4E1" if g['girl']=="Olivia" else "#E0F2FE"
                is_today="🔥 TODAY!" if days==0 else f"In {days} days" if days>0 else "Yesterday"
                st.markdown(f"<div style='background:{bg};padding:10px;border-radius:10px;border-left:6px solid {color};margin:6px 0'><b>{g['girl']} — {g['day_str']} {g['time']}</b><br><small>@ {g['location']} vs {g['opponent']} {'🏠 Home' if g['home'] else '✈️ Away'}</small><br><b style='color:{color}'>{is_today}</b></div>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("🏐 Falcons Powers = Leadership!")
        for power, info in VOLLEYBALL_POWERS.items():
            st.markdown(f"<div style='background:white;padding:8px;border-radius:8px;border:1px solid #A71930;margin:4px 0'><b>{power}</b> = {info['behavior']}<br><small>{info['desc']}</small></div>", unsafe_allow_html=True)
        
        st.info("**Falcons Chant:** Rise Up! Go Falcons! To Know. To Love. To Serve. Catch the Spirit! 🔴⚫️")

def show_girl_page(girl_key: str):
    is_olivia=girl_key=="olivia"
    name="Olivia" if is_olivia else "Nora"
    # Volleyball rebrand
    if is_olivia:
        role="Olivia Davis — #5 Team Captain & Elegant Leader — 5th Grade Falcons"
        tagline="Team Captain! Elegant serving, fearless spiking, mentoring 4th graders! 🏐👑"
        personal_focus="Captain Focus & Mentoring Younger Falcons"
        focus_label="Showed CAPTAIN leadership — encouraged team, led by example, mentored younger players! 🏐👑"
    else:
        role="Nora Davis — #7 Volleyball Star & Libero Focus Champion — 4th Grade Falcons"
        tagline="Game Focus! Bump • Set • SPIKE! Strong focus, strong heart! 🏐💥"
        personal_focus="Game Focus Like a Libero — Eyes on ball, not sideline chatter! + Volleyball Star Power!"
        focus_label="Practiced GAME FOCUS today — eyes on ball/coach, listened first time, stayed locked in! 🏐🛡️ Like a LIBERO!"
    
    data=st.session_state.data[girl_key]
    level=get_level(data['stars'])
    
    # Game day check
    game_today=is_volleyball_game_day(girl_key)
    if game_today:
        st.balloons()
        st.markdown(f"""<div style="background: linear-gradient(135deg,#A71930 0%,#000 100%); color:white; padding:18px; border-radius:15px; text-align:center; border:4px solid white; margin-bottom:10px;"><div style="font-size:2rem;font-weight:900">🔥 GAME DAY! {name} — TODAY! 🔥</div><div style="font-size:1.3rem">{game_today['day_str']} {game_today['time']} @ {game_today['location']} vs {game_today['opponent']}</div><div>Falcons Rise Up! Show captain/focus leadership!</div></div>""", unsafe_allow_html=True)
    
    st.header(f"{'👑' if is_olivia else '🏐'} {name}'s Falcons Journey")
    st.caption(f"{role} • {tagline}")
    
    if st.button("← Back to Falcons HQ"):
        st.session_state.view="home"; st.rerun()
    
    top1,top2,top3=st.columns([1,2,1])
    with top1:
        avatar=get_avatar_path(girl_key)
        st.image(avatar, width=240)
        st.markdown(f"<span class='level-badge'>Level {level} Falcons</span> ⭐{data['stars']} 🪙{data['coins']}", unsafe_allow_html=True)
        # Volleyball stats for Nora, elegant stats for Olivia
        if not is_olivia:
            st.metric("🏐 Serves / Games", data.get('volleyball_stats',{}).get('serves',0))
            st.progress(min(data['stars']%150/150,1.0), text=f"Falcons Power {data['stars']%150}/150")
        else:
            st.progress(min(data['stars']%150/150,1.0))
        st.write(f"Outfits: {', '.join(data['outfits'][-4:]) if data['outfits'] else 'Falcons Jersey Red/Black'}")
        # Nail polish if Nora
        if data.get('nail_polish'):
            pc=POLISH_COLORS.get(data['nail_polish'],{"hex":"#FFB6C1","emoji":"💅"})
            st.markdown(f"<div style='background:{pc['hex']};padding:6px;border-radius:8px;text-align:center'>💅 {data['nail_polish']}</div>", unsafe_allow_html=True)
    with top2:
        st.subheader(f"Today is {datetime.now().strftime('%A %B %d')} — Go Falcons! 🦅")
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Level", level)
        c2.metric("Stars", data['stars'])
        c3.metric("Coins", data['coins'])
        c4.metric("Streak", f"{data['streak']} 🔥")
        # Volleyball powers display for Nora
        if not is_olivia:
            st.markdown("#### 🏐 Volleyball Powers = Leadership Powers!")
            cols=st.columns(3)
            for idx,(power,info) in enumerate(VOLLEYBALL_POWERS.items()):
                col=cols[idx%3]
                with col:
                    st.markdown(f"<div style='background:white;border:2px solid #A71930;padding:8px;border-radius:10px;text-align:center;margin:4px 0'><b>{power}</b><br><small>{info['behavior']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown("#### 👑 Captain Powers")
            st.caption("SERVE 💥 Initiative • SET ✨ Encourages Others • SPIKE 🔥 Courage • DIG 🛡️ Focus • BUMP 🤝 Teamwork")
    with top3:
        st.markdown("**Parent Quick Note**")
        st.text_area("Encouragement", key=f"parent_note_{girl_key}", placeholder=f"Go {name}! Falcons!", height=90)
        st.caption("Appears Sunday Review")
        # Next game for this girl
        next_g=[g for g in get_next_volleyball_games() if g['girl']==name]
        if next_g:
            ng=next_g[0]
            st.markdown(f"<div style='background:#000;color:white;padding:8px;border-radius:8px;text-align:center'>Next Game:<br>{ng['day_str']} {ng['time']}<br>@ {ng['location']}</div>", unsafe_allow_html=True)
    
    st.divider()
    tabs=st.tabs(["🏐 GAME DAY CHECK-IN","📚 SCHOOL & GRADES","💅 BOUTIQUE + FUN","📈 GROWTH"])
    tab_today, tab_school, tab_closet, tab_growth = tabs
    
    with tab_today:
        if is_olivia:
            st.subheader(f"🏐👑 Captain's Check-In for {name} — Lead Your Team!")
        else:
            st.subheader(f"🏐💥 Volleyball Star Check-In for {name} — Bump Set Spike!")
        
        col_left,col_right=st.columns(2)
        with col_left:
            st.markdown("<div class='virtue-card'>", unsafe_allow_html=True)
            st.markdown("### 🔴⚫️ Falcons Fruit of the Spirit Today")
            virtue=st.selectbox("Which fruit did you live on court & at school?", list(FRUITS_OF_SPIRIT.keys()), key=f"virtue_{girl_key}")
            st.caption(FRUITS_OF_SPIRIT[virtue])
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("### 🏐 Falcons Powers (Tap to Earn!)")
            st.caption("Each volleyball move = leadership behavior = 5 points! Tap all you did today!")
            selected_powers=[]
            for power, info in VOLLEYBALL_POWERS.items():
                if st.checkbox(f"{power} — {info['desc']}", key=f"power_{girl_key}_{power}"):
                    selected_powers.append(f"{power} - {info['behavior']}")
            
            st.markdown("**Traditional Leadership (also 5 pts each)**")
            selected_lead=st.multiselect("More leadership", LEADERSHIP_BEHAVIORS, key=f"lead_{girl_key}", label_visibility="collapsed")
            
            st.markdown("**🎯 Falcons Focus Goal — YOU CHOOSE! (Choice Board!)**")
            # Choice board per your pick C
            if girl_key=="nora":
                choice_board=NORA_FOCUS_CHOICE_BOARD
                st.caption("Nora — Pick YOUR focus superpower for today! You are in charge! Like a libero choosing her strategy!")
            else:
                choice_board=OLIVIA_FOCUS_CHOICE_BOARD
                st.caption("Olivia — Pick YOUR captain superpower for today!")
            
            focus_choice=st.radio(f"My focus strategy TODAY for {name}:", choice_board, key=f"focus_choice_{girl_key}", index=0)
            focus_done=st.checkbox(f"✅ I used my strategy today: {focus_choice[:50]}...", key=f"focus_{girl_key}")
            st.caption(f"Choice board — you pick! Yesterday you picked: {data.get('focus_choice_today','None yet')}")
            
            # Save choice for tomorrow reference
            st.session_state.data[girl_key]['focus_choice_today']=focus_choice
        
        with col_right:
            st.markdown("<div class='health-card'>", unsafe_allow_html=True)
            st.markdown("### 💪 Falcons Fuel — Temple of Holy Spirit")
            all_health=[]
            for pillar, items in HEALTH_PILLARS.items():
                # Make volleyball friendly
                label = pillar.replace("Move 🏃‍♀️","Move 🏐 Volleyball").replace("Fuel 🍎","Fuel 🏐 Falcons Fuel")
                st.write(f"**{label}**")
                checks=st.multiselect(f"{pillar} habits", items, key=f"{pillar}_{girl_key}", label_visibility="collapsed")
                all_health.extend(checks)
            st.slider("💧 Water Glasses Game Day",0,10,4, key=f"water_{girl_key}")
            st.slider("🏐 Active / VB Minutes",0,120,45, step=5, key=f"active_{girl_key}")
            st.slider("😴 Sleep Last Night",0,12,9, key=f"sleep_{girl_key}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        col1,col2=st.columns([2,1])
        with col1:
            journal=st.text_input(f"One-sentence WIN today? (for {name}'s Falcons journal)", key=f"journal_{girl_key}", placeholder="e.g., I served 3 times and encouraged my teammate who missed!")
        with col2:
            mood=st.select_slider("Heart today?", options=["Tough","Okay","Good","Great","Falcons Strong! 🔥"], value="Good", key=f"mood_{girl_key}")
        
        # Game day bonus
        game_bonus=20 if game_today else 0
        if game_today:
            st.info(f"🏐 GAME DAY BONUS! +{game_bonus} stars for showing Falcons leadership at game today!")
        
        if st.button(f"✅ SAVE {name}'s Falcons Check-In!", type="primary", use_container_width=True):
            lead_points=len(selected_lead)*5 + len(selected_powers)*6
            health_points=len(all_health)*3
            focus_points=12 if focus_done else 0
            virtue_bonus=10
            water=st.session_state.get(f"water_{girl_key}",0)
            active=st.session_state.get(f"active_{girl_key}",0)
            water_bonus=2 if water>=4 else 0
            active_bonus=3 if active>=30 else 0
            total=lead_points+health_points+focus_points+virtue_bonus+water_bonus+active_bonus+game_bonus
            coins=total//2 + (5 if total>40 else 0)
            data['stars']+=total
            data['coins']+=coins
            today_str=str(date.today())
            if data['last_checkin']!=today_str:
                if data['last_checkin']==str(date.today().fromordinal(date.today().toordinal()-1)) or data['streak']==0:
                    data['streak']+=1
                data['last_checkin']=today_str
            entry={"date":today_str,"virtue":virtue,"leadership":selected_lead+selected_powers,"health":all_health,"focus":focus_done,"focus_choice":focus_choice,"water":water,"active":active,"mood":mood,"journal":journal,"points":total}
            data['history'].append(entry)
            if journal:
                data['journal_entries'].append({"date":today_str,"text":journal,"mood":mood})
            # volleyball stats
            if selected_powers:
                data['volleyball_stats']['serves']=data['volleyball_stats'].get('serves',0)+1
            save_data()
            st.balloons()
            st.success(f"GO FALCONS! Amazing {name}! +{total} Stars & +{coins} Coins! Level {get_level(data['stars'])}")
            st.rerun()
    
    with tab_school:
        st.subheader("📚 Holy Spirit Falcons — School Tracker")
        st.caption("Celebrating 90%+ Effort & Excellence — Falcons style!")
        col1,col2=st.columns(2)
        with col1:
            st.markdown("<div style='background:#000;color:white;padding:12px;border-radius:12px;border:2px solid #A71930'>", unsafe_allow_html=True)
            st.write("**Add Grade (90%+)**")
            subject=st.selectbox("Subject", SCHOOL_SUBJECTS, key=f"subj_{girl_key}")
            score=st.number_input(f"{name}'s Score %",0,110,92, key=f"grade_{girl_key}")
            assignment=st.text_input("Assignment/Test", key=f"assign_{girl_key}", placeholder="e.g., Religion Ch 4, Math Quiz")
            note=st.text_input(f"Proud moment for {name}?", key=f"praise_{girl_key}", placeholder="I studied hard!")
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("➕ Add Falcons Grade!", key=f"addgrade_{girl_key}", type="primary"):
                if score<90:
                    st.error("We celebrate 90%+ here! Keep working — you got this!")
                else:
                    stars=25 if score>=97 else 20 if score>=93 else 12
                    coins=stars
                    data['stars']+=stars
                    data['coins']+=coins
                    data['grades'].append({"date":str(date.today()),"subject":subject,"score":score,"assignment":assignment,"notes":note})
                    save_data()
                    st.success(f"🦅 {assignment} {score}% in {subject}! +{stars}⭐ +{coins}🪙 GO FALCONS!")
                    st.balloons()
                    st.rerun()
        with col2:
            st.write("**📝 Homework & Prep**")
            hw=st.multiselect("Today I...", ["Completed homework","Backpack ready","Studied 15+ min","Asked good questions","Helped teammate/classmate"], key=f"hw_{girl_key}")
            study=st.slider("Study mins",0,90,15, key=f"study_{girl_key}")
            if st.button("Save Homework Wins", key=f"hwbtn_{girl_key}"):
                pts=len(hw)*4 + (study//15)*2
                data['stars']+=pts
                data['coins']+=pts//2
                save_data()
                st.success(f"+{pts} Stars for being prepared! Falcons leader!")
                st.rerun()
            if data['grades']:
                df=pd.DataFrame(data['grades'])
                st.dataframe(df.tail(10), use_container_width=True)
                fig=px.bar(df, x="subject", y="score", color="score", color_continuous_scale="Reds", title=f"{name}'s Falcons Scores")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add first 90%+ grade to see chart!")
    
    with tab_closet:
        st.subheader(f"🏈 {name}'s Falcons Boutique — Red & Black!")
        avatar=get_avatar_path(girl_key)
        c1,c2=st.columns([1,2])
        with c1:
            st.image(avatar, caption=f"Current: {', '.join(data['outfits'][-3:]) if data['outfits'] else 'Falcons Jersey'}", width=200)
            st.metric("Coins", data['coins'])
            if data.get('nail_polish'):
                pc=POLISH_COLORS.get(data['nail_polish'],{"hex":"#FFB6C1","emoji":"💅"})
                st.markdown(f"<div style='background:{pc['hex']};padding:8px;border-radius:8px;text-align:center'>💅 {data['nail_polish']}</div>", unsafe_allow_html=True)
        with c2:
            # Champion Unlocks
            st.markdown("### 🏆 Champion Badges — Falcons!")
            champ_cols=st.columns(2)
            for idx,(item,meta) in enumerate(CHAMPION_REWARDS.items()):
                col=champ_cols[idx%2]
                with col:
                    req=meta['requires']
                    owned=item in data['outfits']
                    unlocked=req in data.get('milestones_claimed',[])
                    if req=="T3":
                        unlocked="T3" in data.get('milestones_claimed',[]) or "LAST" in data.get('milestones_claimed',[])
                    if owned:
                        st.success(f"✅ {item}")
                    elif unlocked:
                        st.markdown(f"<div style='background:#000;color:white;padding:8px;border-radius:8px;border:2px solid #A71930'><b>🔓 UNLOCKED!</b> {item}</div>", unsafe_allow_html=True)
                        if st.button(f"Wear {item[:18]} FREE!", key=f"champ_{girl_key}_{item}", type="primary"):
                            data['outfits'].append(item)
                            data['coins']+=10
                            save_data()
                            st.balloons()
                            st.rerun()
                    else:
                        st.markdown(f"<div style='background:#eee;padding:8px;border-radius:8px;opacity:0.7'><b>🔒 LOCKED</b> {item}<br><small>Requires {req}</small></div>", unsafe_allow_html=True)
            st.divider()
            # Volleyball shop for Nora, elegant for Olivia but both get Falcons
            st.markdown("### 🏐 Falcons Volleyball Shop — EXCITING FOR NORA!")
            if not is_olivia:
                vb_cols=st.columns(2)
                for idx,(item,cost) in enumerate(NORA_VOLLEYBALL_SHOP.items()):
                    col=vb_cols[idx%2]
                    with col:
                        owned=item in data['outfits']
                        st.write(f"{item} — 🪙{cost} {'✅' if owned else ''}")
                        if st.button(f"Buy {item[:15]}", key=f"vb_buy_{girl_key}_{item}", disabled=owned or data['coins']<cost):
                            if data['coins']>=cost:
                                data['coins']-=cost
                                data['outfits'].append(item)
                                save_data()
                                st.success(f"{name} got {item}!")
                                st.rerun()
                st.divider()
            # Polish chooser
            st.markdown("### 💅 Nails Done Day — Falcons Red/Black Polish!")
            is_150="150" in data.get('milestones_claimed',[])
            if not is_150:
                st.caption("🔒 Unlocks Day 150 — Keep leading! Currently Day {} of {}".format(get_school_year_stats()['elapsed'], get_school_year_stats()['total']))
            else:
                current=data.get('nail_polish')
                if current:
                    st.success(f"Current: {current}")
                choice=st.selectbox(f"Pick polish {name}", list(POLISH_COLORS.keys()), key=f"polish_{girl_key}", index=list(POLISH_COLORS.keys()).index(current) if current in POLISH_COLORS else 0)
                picked=POLISH_COLORS[choice]
                if st.button(f"💅 Wear {choice} +5🪙", key=f"wear_polish_{girl_key}_{choice}", type="primary"):
                    data['nail_polish']=choice
                    if choice not in data.get('nail_polish_history',[]):
                        data['nail_polish_history'].append(choice)
                    if f"{choice} Nails" not in data['outfits']:
                        data['outfits'].append(f"{choice} Nails")
                    data['coins']+=5
                    data['stars']+=3
                    save_data()
                    st.balloons()
                    st.rerun()
            st.divider()
            # 👗 NEW: Dress to Impress — Creative Collecting & Mixing (Choice C!)
            st.markdown("### 👗 Dress to Impress — Collect, Mix & Create Together! ✨ (Your Pick C!)")
            st.caption("Per your choice: Olivia & Nora love collecting clothes, mixing outfits, being creative & playing TOGETHER — not runway judging!")
            
            # Collection progress
            total_items = sum(len(v) for v in SHOP_ITEMS.values()) + len(CHAMPION_REWARDS) + len(NORA_VOLLEYBALL_SHOP)
            owned_count = len(data['outfits'])
            pct_collect = min(owned_count / max(total_items,1) * 100, 100)
            st.progress(pct_collect/100, text=f"Collection: {owned_count}/{total_items} items collected ({pct_collect:.0f}%)")
            
            col_mix1, col_mix2 = st.columns([1,1])
            with col_mix1:
                st.markdown("**Mix & Match Your Collection!**")
                owned = data['outfits']
                if len(owned) < 2:
                    st.info("Collect more items from boutique + spin wheel to mix! You need 2+ items.")
                else:
                    mix_top = st.selectbox(f"Pick Top/Headband for {name}", owned[:15], key=f"mix_top_{girl_key}")
                    mix_bottom = st.selectbox(f"Pick Bottom/Shoes", owned[:15], key=f"mix_bottom_{girl_key}", index=1 if len(owned)>1 else 0)
                    mix_accent = st.selectbox(f"Pick Accent/Badge", owned[:15], key=f"mix_accent_{girl_key}", index=2 if len(owned)>2 else 0)
                    custom_mix_name = f"DTI Mix: {mix_top.split()[0]} + {mix_bottom.split()[0]} + {mix_accent.split()[0]}"
                    st.markdown(f"<div style='background:white;padding:10px;border-radius:10px;border:2px dashed #A71930'><b>Your Custom Look:</b><br>{custom_mix_name}<br><small>👧 {name} + 👧 Sister = creative team!</small></div>", unsafe_allow_html=True)
                    if st.button(f"Save Custom Mix for {name}! ✨👗", key=f"save_mix_{girl_key}"):
                        if custom_mix_name not in data['outfits']:
                            data['outfits'].append(custom_mix_name)
                            data['coins']+=5
                            save_data()
                            st.balloons()
                            st.success(f"Saved {custom_mix_name}! +5🪙 Creative bonus!")
                            st.rerun()
            with col_mix2:
                st.markdown("**Play Together — Twin Looks!**")
                st.caption("Create matching sister looks like in Dress to Impress duo mode!")
                sister_match = st.checkbox(f"Create matching look for Olivia & Nora together?", key=f"twin_{girl_key}")
                if sister_match:
                    st.markdown(f"<div style='background: linear-gradient(135deg,#FFDDE1 0%,#E0F2FE 100%); padding:10px; border-radius:12px; border:2px solid #000; text-align:center;'><b>👯‍♀️ Twin Falcons Look!</b><br>Olivia & Nora wearing similar Falcons red/black + volleyball bows<br>Like Roblox DTI duo!</div>", unsafe_allow_html=True)
                    if st.button(f"Save Twin Look for Both! 👯‍♀️", key=f"twin_save_{girl_key}", type="primary"):
                        twin_name = "👯 Twin Falcons Look"
                        for gk in ['olivia','nora']:
                            if twin_name not in st.session_state.data[gk]['outfits']:
                                st.session_state.data[gk]['outfits'].append(twin_name)
                                st.session_state.data[gk]['coins']+=5
                        save_data()
                        st.balloons()
                        st.success("Twin look saved for both sisters! +5 coins each!")
                        st.rerun()
                # Cover Star preview
                cover_path = f"assets/{'olivia' if is_olivia else 'nora'}_cover_star.png"
                if os.path.exists(cover_path):
                    st.image(cover_path, caption=f"{name} — Cover Star! Magazine cover when you collect 10 items!", use_container_width=True)
                st.caption("Collect 10 items to become a Cover Star! ✨")
                if len(data['outfits'])>=10 and f"⭐ Cover Star {name}" not in data['outfits']:
                    if st.button(f"Claim Cover Star Magazine Cover! ⭐📸", key=f"coverstar_{girl_key}", type="primary"):
                        data['outfits'].append(f"⭐ Cover Star {name}")
                        data['coins']+=15
                        save_data()
                        st.balloons()
                        st.success(f"{name} is now a Cover Star! Magazine cover unlocked!")
                        st.rerun()
            
            st.divider()
            st.markdown("### 🛍️ Regular Boutique")
            for cat,items in SHOP_ITEMS.items():
                st.markdown(f"**{cat}**")
                cols=st.columns(3)
                for idx,(item,cost) in enumerate(items.items()):
                    col=cols[idx%3]
                    with col:
                        owned=item in data['outfits']
                        if st.button(f"{item[:18]} 🪙{cost} {'✅' if owned else ''}", key=f"buy_{girl_key}_{item}", disabled=owned or data['coins']<cost):
                            if data['coins']>=cost:
                                data['coins']-=cost
                                data['outfits'].append(item)
                                save_data()
                                st.rerun()
                st.divider()
    
    with tab_growth:
        st.subheader(f"📈 {name}'s Falcons Growth")
        if data['history']:
            df=pd.DataFrame(data['history'])
            df['date']=pd.to_datetime(df['date'])
            df['cumulative']=df['points'].cumsum()
            fig=px.line(df, x="date", y="cumulative", title=f"{name}'s Stars Journey — Go Falcons!", markers=True, line_shape="spline")
            fig.update_traces(line_color="#A71930")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start check-ins to see growth!")

# ====================== OTHER PAGES (Calendar, Fun Zone, Memories, Yearbook, Review) ======================
def show_runway():
    st.header("👗💃 Dress to Impress Runway — Falcons Edition!")
    st.caption("Daily themes — Dress your Falcons avatar — Olivia & Nora judge each other & earn stars together! Inspired by Roblox DTI + Cover Star!")
    
    if st.button("← Back to Falcons HQ"):
        st.session_state.view="home"; st.rerun()
    
    theme=get_daily_runway_theme()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg,#000 0%,#A71930 100%); color:white; padding:20px; border-radius:18px; text-align:center; border:3px solid white;'>
        <div style='font-size:0.9rem;opacity:0.9'>TODAY'S RUNWAY THEME • {date.today().strftime('%A %B %d')}</div>
        <div style='font-size:2.2rem;font-weight:900'>{theme['icon']} {theme['theme']} {theme['icon']}</div>
        <div style='font-size:1.1rem;margin-top:6px'>{theme['desc']}</div>
        <div style='margin-top:10px;font-weight:800'>BONUS: ⭐{theme['bonus_stars']} Stars if you match theme!</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_img,col_info=st.columns([1,2])
    with col_img:
        if os.path.exists("assets/dress_to_impress_runway.png"):
            st.image("assets/dress_to_impress_runway.png", use_container_width=True)
    with col_info:
        st.markdown("### How Dress to Impress Works (Roblox Style, but Falcons!)")
        st.markdown("""
        1. **See Theme** — Today's theme is at top (e.g., Falcons Volleyball Game Day)
        2. **Collect & Mix** — Pick from your closet (boutique items you own) + nail polish + Falcons gear
        3. **Submit Look** — Save your runway look with a fun pose description
        4. **Sister Judges!** — Olivia & Nora rate each other's looks 1-5 stars (kind & encouraging!)
        5. **Earn Cover Star!** — 5-star looks earn Cover Star badge + family reward!
        """)
        st.info("Your pick C: Collecting, mixing, being creative & playing TOGETHER — not mean judging! Kind feedback only! 💜")
    
    st.divider()
    
    # Submission for each girl
    col_ol,col_no=st.columns(2)
    for idx,gk in enumerate(['olivia','nora']):
        data=st.session_state.data[gk]
        name=gk.title()
        col=col_ol if idx==0 else col_no
        with col:
            st.markdown(f"<div class='girl-card {gk}'><h3>👗 {name}'s Runway Look — Theme: {theme['theme'][:20]}...</h3>", unsafe_allow_html=True)
            avatar=get_avatar_path(gk)
            st.image(avatar, width=180)
            st.caption(f"Outfits Owned: {len(data['outfits'])} — Collection {len(data['outfits'])/35*100:.0f}%")
            
            # Outfit picker from collection
            owned=data.get('outfits',[])
            if not owned:
                st.warning("Collect clothes in Boutique first! Spin wheel to get starter outfits!")
                owned=["Falcons Jersey Classic"]
            
            top_pick=st.selectbox(f"{name}'s Top/Headband", owned[-15:], key=f"runway_top_{gk}")
            bottom_pick=st.selectbox(f"{name}'s Bottom/Shoes", owned[-15:], key=f"runway_bottom_{gk}", index=1 if len(owned)>1 else 0)
            polish_pick=data.get('nail_polish','Ballet Pink 💗')
            st.caption(f"Nail Polish: {polish_pick}")
            
            pose=st.text_input(f"{name}'s Runway Pose! (fun description)", placeholder="e.g., Spike pose with volleyball! 🏐💥", key=f"pose_{gk}")
            
            if st.button(f"Submit {name}'s Look for Theme: {theme['theme'][:20]} 👗✨", key=f"submit_runway_{gk}", type="primary"):
                submission={"date":str(date.today()),"theme":theme['theme'],"top":top_pick,"bottom":bottom_pick,"polish":polish_pick,"pose":pose,"theme_bonus":theme['bonus_stars'],"ratings":[]}
                data['runway_submissions'].append(submission)
                data['stars']+=theme['bonus_stars']
                data['coins']+=5
                save_data()
                st.balloons()
                st.success(f"{name} submitted runway look for {theme['theme']}! +{theme['bonus_stars']}⭐ for creativity!")
                st.rerun()
            
            # Show recent submissions
            if data.get('runway_submissions'):
                st.markdown("**Recent Runway Looks:**")
                for sub in reversed(data['runway_submissions'][-3:]):
                    avg_rating = sum([r['stars'] for r in sub.get('ratings',[])]) / len(sub['ratings']) if sub.get('ratings') else 0
                    st.markdown(f"- {sub['date']} — {sub['theme'][:25]}: {sub['top']} + {sub['bottom']} — {sub['pose'][:30]} — Rated: {avg_rating:.1f}⭐ ({len(sub.get('ratings',[]))} ratings)")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("👯‍♀️ Sister Judging — Rate Each Other's Looks! (Kind & Encouraging!)")
    st.caption("Like Roblox DTI — give 1-5 stars + kind comment! Both sisters earn bonus when they judge!")
    
    # Judging UI
    judge_col1,judge_col2=st.columns(2)
    with judge_col1:
        st.markdown("**Olivia Judges Nora's Latest Look**")
        olivia_data=st.session_state.data['olivia']
        nora_subs=st.session_state.data['nora'].get('runway_submissions',[])
        if nora_subs:
            latest_nora=nora_subs[-1]
            st.info(f"Nora's Latest: {latest_nora['theme']} — {latest_nora['top']} + {latest_nora['bottom']} — Pose: {latest_nora['pose']}")
            stars=st.slider("Stars for Nora (1-5, be kind!)",1,5,5, key="judge_nora_stars")
            comment=st.text_input("Kind comment for Nora", placeholder="So creative! Love Falcons colors!", key="judge_nora_comment")
            if st.button("Olivia Rates Nora 👯‍♀️⭐", key="olivia_rates_nora"):
                latest_nora.setdefault('ratings',[]).append({"from":"Olivia","stars":stars,"comment":comment,"date":str(date.today())})
                # Bonus for both
                st.session_state.data['nora']['stars']+=stars
                st.session_state.data['olivia']['stars']+=2
                st.session_state.data['olivia']['coins']+=2
                save_data()
                st.success(f"Olivia gave Nora {stars}⭐! Both earned bonus! Sister team!")
                st.rerun()
        else:
            st.caption("Nora hasn't submitted a runway look yet!")
    
    with judge_col2:
        st.markdown("**Nora Judges Olivia's Latest Look**")
        nora_data=st.session_state.data['nora']
        olivia_subs=st.session_state.data['olivia'].get('runway_submissions',[])
        if olivia_subs:
            latest_ol=olivia_subs[-1]
            st.info(f"Olivia's Latest: {latest_ol['theme']} — {latest_ol['top']} + {latest_ol['bottom']} — Pose: {latest_ol['pose']}")
            stars2=st.slider("Stars for Olivia (1-5, be kind!)",1,5,5, key="judge_olivia_stars")
            comment2=st.text_input("Kind comment for Olivia", placeholder="Elegant leader! Love it!", key="judge_olivia_comment")
            if st.button("Nora Rates Olivia 👯‍♀️⭐", key="nora_rates_olivia"):
                latest_ol.setdefault('ratings',[]).append({"from":"Nora","stars":stars2,"comment":comment2,"date":str(date.today())})
                st.session_state.data['olivia']['stars']+=stars2
                st.session_state.data['nora']['stars']+=2
                st.session_state.data['nora']['coins']+=2
                save_data()
                st.success(f"Nora gave Olivia {stars2}⭐! Sister team!")
                st.rerun()
        else:
            st.caption("Olivia hasn't submitted yet!")
    
    st.divider()
    # Cover Star covers
    st.subheader("⭐ Cover Star Magazine Covers!")
    col_c1,col_c2=st.columns(2)
    with col_c1:
        if os.path.exists("assets/olivia_cover_star.png"):
            st.image("assets/olivia_cover_star.png", caption="Olivia — Cover Star Magazine (collect 10 items to unlock!)", use_container_width=True)
    with col_c2:
        if os.path.exists("assets/nora_cover_star.png"):
            st.image("assets/nora_cover_star.png", caption="Nora — Cover Star (collect 10 items!)", use_container_width=True)

def show_baking():
    st.header("🧁 Kids Baking Championship — Falcons Baking Rewards!")
    st.caption("Olivia & Nora LOVE Kids Baking Championship — earn coins, then buy a family bake night in the Boutique!")
    
    if st.button("← Back to Falcons HQ"):
        st.session_state.view="home"; st.rerun()
    
    # Baking banner
    col_img,col_text=st.columns([1,2])
    with col_img:
        if os.path.exists("assets/baking_championship_avatar.png"):
            st.image("assets/baking_championship_avatar.png", use_container_width=True)
    with col_text:
        st.markdown(f"""
        <div class='falcons-banner' style='background: linear-gradient(135deg,#FFB6C1 0%,#A71930 100%)'>
            <div style='font-size:1.6rem;font-weight:900'>🧁 BAKING AS A REWARD — SIMPLE!</div>
            <div>Watch Kids Baking Championship together, then spend coins in the Boutique to unlock a real family bake night!</div>
            <div style='font-size:0.9rem;margin-top:5px'>Olivia (11 on 8/31) & Nora (9) — Baking is a reward, not extra homework!</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Birthday section — KEEP per your choice A_keep_bonus
    st.subheader("🎂 Birthday Countdown — Keep!")
    col_ol,col_no=st.columns(2)
    today=date.today()
    olivia_age=get_age_and_next_birthday(OLIVIA_DOB, today)
    nora_age=get_age_and_next_birthday(NORA_DOB, today)
    
    with col_ol:
        is_today=olivia_age['is_today']
        bg="linear-gradient(135deg,#FFB6C1 0%,#A71930 100%)" if is_today else "#FFE4E1"
        txt_color="white" if is_today else "black"
        olivia_days_until = olivia_age['days_until']
        olivia_bday_msg = "🎉 TODAY IS HER BIRTHDAY! 🎉" if is_today else f"In {olivia_days_until} days!" if olivia_days_until<=60 else f"{olivia_days_until} days"
        st.markdown(f"<div style='background:{bg};color:{txt_color};padding:14px;border-radius:12px;text-align:center;border:3px solid #A71930'><b>👧 Olivia — DOB {olivia_age['dob_str']}</b><br>Age: {olivia_age['age']} (turns {olivia_age['age']+1} on Aug 31!)<br>Next Birthday: {olivia_age['next_bday'].strftime('%A %b %d, %Y')}<br><b>{olivia_bday_msg}</b></div>", unsafe_allow_html=True)
        data=st.session_state.data['olivia']
        if is_today and data.get('birthday_claimed_year')!=today.year:
            if st.button("🎂 Claim Olivia's Birthday Bonus! +50⭐ +50🪙", key="bday_olivia", type="primary"):
                claim_birthday_bonus('olivia')
                st.balloons()
                st.success("Happy Birthday Olivia! +50 stars!")
                st.rerun()
        elif is_today:
            st.success("✅ Birthday bonus claimed! Happy Birthday!")
    
    with col_no:
        is_today_n=nora_age['is_today']
        bg_n="linear-gradient(135deg,#E0F2FE 0%,#000 100%)" if is_today_n else "#E0F2FE"
        txt_c="white" if is_today_n else "black"
        nora_days_until = nora_age['days_until']
        nora_bday_msg = "🎉 TODAY IS HER BIRTHDAY! 🎉" if is_today_n else f"In {nora_days_until} days!" if nora_days_until<=60 else f"{nora_days_until} days"
        st.markdown(f"<div style='background:{bg_n};color:{txt_c};padding:14px;border-radius:12px;text-align:center;border:3px solid #000'><b>🏐 Nora — DOB {nora_age['dob_str']}</b><br>Age: {nora_age['age']} (turned 9 on Apr 27!)<br>Next Birthday: {nora_age['next_bday'].strftime('%A %b %d, %Y')}<br><b>{nora_bday_msg}</b></div>", unsafe_allow_html=True)
        data_n=st.session_state.data['nora']
        if is_today_n and data_n.get('birthday_claimed_year')!=today.year:
            if st.button("🎂 Claim Nora's Birthday Bonus! +50⭐ +50🪙", key="bday_nora", type="primary"):
                claim_birthday_bonus('nora')
                st.balloons()
                st.success("Happy Birthday Nora! +50 stars!")
                st.rerun()
        elif is_today_n:
            st.success("✅ Birthday bonus claimed!")
    
    st.divider()
    
    # Simplified: Boutique rewards only
    st.subheader("🛍️ Baking Rewards — Buy in Boutique!")
    st.caption("Per your choice: Baking stays as a FUN REWARD you buy with coins, not as extra challenges to earn stars. Earn coins from volleyball + school + spins, then spend them on a bake night!")
    
    # Show the baking rewards from SHOP_ITEMS
    baking_items = SHOP_ITEMS.get("🧁 Kids Baking Championship", {})
    cols=st.columns(2)
    for idx, (item, cost) in enumerate(baking_items.items()):
        col=cols[idx%2]
        with col:
            st.markdown(f"<div style='background:white;padding:12px;border-radius:12px;border:2px solid #A71930;margin:6px 0;'><b>{item}</b><br><small>Cost: 🪙{cost}</small></div>", unsafe_allow_html=True)
    
    if st.button("Go to Boutique to Buy Baking Rewards 🧁👩‍🍳", type="primary", use_container_width=True):
        st.session_state.view="olivia"
        st.rerun()
    
    st.info("✅ Simplified per your feedback: No extra baking star challenges — just fun family bake nights you can BUY as a reward!")

def show_calendar():
    stats=get_school_year_stats()
    st.header(f"📅 Holy Spirit Falcons Calendar — {SCHOOL_YEAR_LABEL}")
    st.caption("Private Family View • Source: hspirit.org/school-calendar • Mascot: Falcons 🔴⚫️")
    if st.button("← Back"):
        st.session_state.view="home"; st.rerun()
    c1,c2,c3=st.columns(3)
    c1.metric("School Day", f"Day {stats['elapsed']}" if stats['status']!="before_school" else "Not Started", f"of {stats['total']}")
    c2.metric("% Complete", f"{stats['pct']:.0f}%", f"{stats['remaining']} left")
    c3.metric("Status", stats['today_reason'])
    
    col_left,col_right=st.columns([1.5,1])
    with col_left:
        st.subheader(f"🗓️ {SCHOOL_YEAR_LABEL} Key Dates")
        all_events=[]
        for d,r in sorted(NO_SCHOOL_DAYS.items()):
            all_events.append({"Date":d,"Type":"No School","Event":r})
        for d,r in sorted(HALF_DAYS.items()):
            all_events.append({"Date":d,"Type":"Half Day","Event":r})
        all_events.append({"Date":FIRST_DAY_SCHOOL,"Type":"First Day","Event":"First Day Gr 1-8 Falcons!"})
        all_events.append({"Date":LAST_DAY_SCHOOL,"Type":"Last Day","Event":"Last Day!"})
        df=pd.DataFrame(all_events)
        df["DateStr"]=df["Date"].apply(lambda x: x.strftime("%a %b %d %Y"))
        st.dataframe(df.sort_values("Date").head(40), use_container_width=True, height=400)
        st.link_button("Official PDF", "https://www.hspirit.org/s/2026-2027-FINAL-School-Calendar-REVISED-7162026.pdf")
    with col_right:
        st.subheader("🏐 Volleyball + School")
        for g in VOLLEYBALL_SCHEDULE[:6]:
            st.markdown(f"<div style='background:#000;color:white;padding:8px;border-radius:8px;margin:4px 0;border-left:4px solid #A71930'><b>{g['girl']} {g['day_str']} {g['time']}</b><br><small>@ {g['location']} vs {g['opponent']}</small></div>", unsafe_allow_html=True)

def show_fun_zone():
    st.header("🎮 Falcons Fun Zone!")
    if st.button("← Home"):
        st.session_state.view="home"; st.rerun()
    tab_spin,tab_quiz,tab_codes=st.tabs(["🎡 Spin Wheel","🧠 Quiz","🔍 Secret Codes"])
    with tab_spin:
        cols=st.columns(2)
        for idx,girl_key in enumerate(['olivia','nora']):
            data=st.session_state.data[girl_key]
            name=girl_key.title()
            col=cols[idx]
            with col:
                st.markdown(f"### {name}'s Wheel")
                can_spin=data.get('last_spin_date')!=str(date.today())
                if can_spin:
                    if st.button(f"SPIN FOR {name}! 🎡", key=f"spin_{girl_key}", type="primary"):
                        prize,_=spin_daily_wheel(girl_key)
                        st.balloons()
                        st.success(f"{name} won {prize['name']}")
                        st.rerun()
                else:
                    st.success(f"{name} spun today! Come back tomorrow!")
    with tab_quiz:
        selected=st.radio("Who?",["Olivia","Nora"], horizontal=True)
        gk="olivia" if selected=="Olivia" else "nora"
        if 'quiz_idx' not in st.session_state:
            st.session_state.quiz_idx=0
        q_idx=st.session_state.quiz_idx % len(QUIZ_QUESTIONS)
        q=QUIZ_QUESTIONS[q_idx]
        st.markdown(f"**{q['q']}** — Virtue: {q['virtue']}")
        choice=st.radio("Answer", q['options'], key=f"quiz_{q_idx}")
        if st.button("Submit"):
            chosen=q['options'].index(choice)
            if chosen==q['correct']:
                st.success(f"Correct! {q['explain']} +5⭐")
                st.session_state.data[gk]['stars']+=5
                save_data()
                st.balloons()
            else:
                st.error(f"Best answer: {q['options'][q['correct']]}. {q['explain']}")
            st.session_state.quiz_idx+=1
            st.rerun()
    with tab_codes:
        sel=st.radio("Who?",["Olivia","Nora"], horizontal=True, key="code_girl")
        gk="olivia" if sel=="Olivia" else "nora"
        code=st.text_input(f"Code for {sel}", placeholder="FALCONS")
        if st.button("Redeem"):
            prize,msg=claim_secret_code_fn(gk,code)
            if prize:
                st.success(msg)
                st.balloons()
                st.rerun()
            else:
                st.error(msg)

def show_family_memories():
    st.header("📸 Falcons Family Scrapbook")
    if st.button("← Home"):
        st.session_state.view="home"; st.rerun()
    col_up,col_gal=st.columns([1,1.5])
    with col_up:
        st.subheader("Add Memory")
        adv_opts=["General Joy"]+[f"{k}: {v['name']}" for k,v in FAMILY_REWARD_UNLOCKS.items()]
        adv=st.selectbox("Adventure", adv_opts, key="photo_adv")
        cap=st.text_input("Caption", placeholder="T1 Dinner! Olivia & Nora!", key="photo_cap")
        up=st.file_uploader("Photo", type=["jpg","jpeg","png"], key="fam_up")
        who=st.multiselect("Who?", ["Olivia","Nora","Mom","Dad","Whole Family"], default=["Whole Family"])
        if st.button("Save 📸", type="primary"):
            if up and cap:
                ts=datetime.now().strftime("%Y%m%d_%H%M%S")
                fn=f"{ts}_{''.join(c if c.isalnum() else '_' for c in up.name)[:40]}"
                fp=os.path.join(FAMILY_PHOTOS_DIR, fn)
                with open(fp,"wb") as f:
                    f.write(up.getbuffer())
                entry={"date":str(date.today()),"timestamp":ts,"path":fp,"caption":cap,"adventure":adv,"who":who,"id":ts}
                st.session_state.data['family_photos'].append(entry)
                save_data()
                st.success("Saved!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Need photo + caption!")
    with col_gal:
        photos=st.session_state.data.get('family_photos',[])
        if not photos:
            st.info("No photos yet! Upload your Falcons volleyball memories!")
        else:
            for entry in sorted(photos, key=lambda x: x.get('timestamp',''), reverse=True)[:10]:
                st.markdown(f"<div style='background:white;padding:10px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.1);margin:10px 0'>", unsafe_allow_html=True)
                if os.path.exists(entry['path']):
                    st.image(entry['path'], use_container_width=True)
                st.write(f"**{entry['date']} {entry['adventure']}** — {entry['caption']}")
                st.markdown("</div>", unsafe_allow_html=True)

def show_yearbook():
    st.header("📖 Falcons Yearbook — Printable")
    if st.button("← Memories"):
        st.session_state.view="memories"; st.rerun()
    stats=get_school_year_stats()
    md=f"# Holy Spirit Falcons Yearbook — {SCHOOL_YEAR_LABEL}\n\nOlivia & Nora — Falcons Volleyball\n\nDay {stats['elapsed']} of {stats['total']}\n\n"
    for gk in ['olivia','nora']:
        d=st.session_state.data[gk]
        md+=f"## {gk.title()} — Level {get_level(d['stars'])} Stars {d['stars']}\nOutfits: {', '.join(d['outfits'][:10])}\n\nGrades:\n"
        for gr in d['grades'][-10:]:
            md+=f"- {gr['subject']} {gr['score']}% {gr['assignment']}\n"
        md+="\n"
    st.download_button("📥 Download Yearbook MD", md, file_name=f"Falcons_Yearbook_{date.today()}.md", mime="text/markdown", type="primary")

def show_review():
    st.header("🌟 Sunday Family Review — Falcons!")
    if st.button("← Home"):
        st.session_state.view="home"; st.rerun()
    col1,col2=st.columns(2)
    for idx,gk in enumerate(['olivia','nora']):
        d=st.session_state.data[gk]
        col=col1 if idx==0 else col2
        with col:
            st.markdown(f"<div class='girl-card {gk}'><h3>{gk.title()}</h3><p>⭐{d['stars']} 🪙{d['coins']} Lvl {get_level(d['stars'])}</p><p>Outfits: {', '.join(d['outfits'][-4:])}</p></div>", unsafe_allow_html=True)
    # Leaderboard
    comp=[]
    for g in ['olivia','nora']:
        dd=st.session_state.data[g]
        comp.append({"Girl":g.title(),"Stars":dd['stars'],"Coins":dd['coins'],"Grades":len(dd['grades'])})
    df=pd.DataFrame(comp)
    st.dataframe(df, use_container_width=True)
    fig=px.bar(df, x="Girl", y=["Stars","Grades"], barmode="group", title="Sisters Together — Go Falcons!", color_discrete_sequence=["#A71930","#000000"])
    st.plotly_chart(fig, use_container_width=True)

# ====================== VIEW CONTROL ======================
if st.session_state.view=="home":
    show_home()
elif st.session_state.view=="volleyball":
    show_volleyball()
elif st.session_state.view=="runway":
    show_runway()
elif st.session_state.view=="baking":
    show_baking()
elif st.session_state.view=="calendar":
    show_calendar()
elif st.session_state.view=="funzone":
    show_fun_zone()
elif st.session_state.view=="memories":
    show_family_memories()
elif st.session_state.view=="yearbook":
    show_yearbook()
elif st.session_state.view=="olivia":
    show_girl_page("olivia")
elif st.session_state.view=="nora":
    show_girl_page("nora")
elif st.session_state.view=="review":
    show_review()
