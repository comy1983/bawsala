import streamlit as st

st.set_page_config(
    page_title="بوصلة | Bawsala",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Tajawal:wght@300;400;500;700&display=swap');

:root {
    --primary:   #0a4f6e;
    --accent:    #00c9a7;
    --accent2:   #f7b731;
    --danger:    #e74c3c;
    --warning:   #f39c12;
    --success:   #27ae60;
    --bg:        #f4f7fb;
    --card:      #ffffff;
    --text:      #1a2332;
    --muted:     #6c7a8d;
    --border:    #e2e8f0;
}

html, body, [class*="css"] {
    font-family: 'Cairo', 'Tajawal', sans-serif !important;
    direction: rtl;
    background: var(--bg);
    color: var(--text);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--primary) 0%, #072d40 100%);
    border-left: none;
}
section[data-testid="stSidebar"] * { color: #e8f4f8 !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 15px; }

/* Cards */
.bawsala-card {
    background: var(--card);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(10,79,110,0.08);
    border: 1px solid var(--border);
    margin-bottom: 16px;
    transition: box-shadow 0.2s;
}
.bawsala-card:hover { box-shadow: 0 6px 24px rgba(10,79,110,0.14); }

/* KPI boxes */
.kpi-box {
    background: var(--card);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    border-top: 4px solid var(--accent);
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.kpi-value { font-size: 2.2rem; font-weight: 900; color: var(--primary); line-height:1; }
.kpi-label { font-size: 0.85rem; color: var(--muted); margin-top: 6px; }

/* Gap badge */
.gap-critical { background:#fde8e8; color:#c0392b; border-radius:8px; padding:4px 12px; font-weight:700; }
.gap-warning  { background:#fef3cd; color:#856404; border-radius:8px; padding:4px 12px; font-weight:700; }
.gap-ok       { background:#d4edda; color:#155724; border-radius:8px; padding:4px 12px; font-weight:700; }

/* Section header */
.section-header {
    font-size: 1.4rem; font-weight: 700;
    color: var(--primary);
    border-right: 5px solid var(--accent);
    padding-right: 12px;
    margin-bottom: 18px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, var(--accent) 0%, #00a88e 100%);
    color: white; font-weight: 700; border: none;
    border-radius: 10px; padding: 10px 28px;
    font-family: 'Cairo', sans-serif; font-size: 15px;
    transition: transform 0.15s, box-shadow 0.15s;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,201,167,0.35);
}

/* Tables */
.dataframe { border-radius: 10px; overflow: hidden; }
thead { background: var(--primary) !important; color: white !important; }

/* Progress bars */
.stProgress > div > div { background: linear-gradient(90deg, var(--accent), var(--primary)); border-radius: 4px; }

/* Metrics */
[data-testid="metric-container"] {
    background: white; border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid var(--border);
}

/* Hide default menu items */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:3rem;'>🧭</div>
        <div style='font-size:1.6rem; font-weight:900; color:white; letter-spacing:1px;'>بوصلة</div>
        <div style='font-size:0.8rem; color:#a0c4d4; margin-top:4px;'>منصة تحليل الفجوة الأكاديمية</div>
    </div>
    <hr style='border-color:#1a5f7e; margin:12px 0;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "التنقل",
        ["🏠  الرئيسية", "📥  إدخال البيانات", "📊  تحليل الفجوة", "🤖  التنبؤ بالنتائج", "📋  التقارير", "⚙️  الإعدادات"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1a5f7e; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; font-size:0.75rem; color:#7aadc0; padding-bottom:10px;'>
        الإصدار 1.0.0<br>إدارة التعليم - المنطقة
    </div>
    """, unsafe_allow_html=True)

# ─── Route Pages ──────────────────────────────────────────────────────────────
if "الرئيسية" in page:
    from pages import home
    home.show()
elif "إدخال البيانات" in page:
    from pages import data_entry
    data_entry.show()
elif "تحليل الفجوة" in page:
    from pages import gap_analysis
    gap_analysis.show()
elif "التنبؤ" in page:
    from pages import prediction
    prediction.show()
elif "التقارير" in page:
    from pages import reports
    reports.show()
elif "الإعدادات" in page:
    from pages import settings
    settings.show()
