"""
pages/settings.py  —  صفحة الإعدادات
"""

import streamlit as st
from utils.data_manager import init_session


def show():
    init_session()

    st.markdown("<div class='section-header'>⚙️ إعدادات النظام</div>", unsafe_allow_html=True)

    with st.form("settings_form"):
        st.markdown("#### 🏫 معلومات المدرسة والمنطقة")
        school = st.text_input("اسم المدرسة", st.session_state.school_name)
        region = st.text_input("إدارة التعليم / المنطقة", st.session_state.region_name)
        year   = st.text_input("العام الدراسي", st.session_state.academic_year)

        st.markdown("#### 📐 عتبات تصنيف الفجوة")
        c1, c2 = st.columns(2)
        with c1:
            thresh_critical = st.number_input("عتبة الفجوة الحرجة (درجة)", 5, 50, 20)
        with c2:
            thresh_medium   = st.number_input("عتبة الفجوة المتوسطة (درجة)", 2, 30, 10)

        submitted = st.form_submit_button("💾 حفظ الإعدادات")
        if submitted:
            st.session_state.school_name  = school
            st.session_state.region_name  = region
            st.session_state.academic_year= year
            st.success("✅ تم حفظ الإعدادات بنجاح!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ℹ️ معلومات النظام")
    st.info("""
    **بوصلة** — منصة تحليل الفجوة الأكاديمية  
    الإصدار: 1.0.0  
    مطوَّرة خصيصاً لإدارات التعليم  
    تستخدم: Python · Streamlit · Scikit-learn · Plotly
    """)
