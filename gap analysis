"""
pages/gap_analysis.py  —  صفحة تحليل الفجوة
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_manager import init_session, risk_color


def show():
    init_session()
    df = st.session_state.students_df

    st.markdown("<div class='section-header'>📊 تحليل الفجوة الأكاديمية</div>", unsafe_allow_html=True)

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.expander("🔍 فلاتر البحث", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            grades = ["الكل"] + df["grade"].unique().tolist()
            sel_grade = st.selectbox("الصف", grades)
        with fc2:
            risks = ["الكل", "فجوة حرجة", "فجوة متوسطة", "فجوة بسيطة", "متوافق"]
            sel_risk = st.selectbox("مستوى الخطر", risks)
        with fc3:
            min_gap, max_gap = float(df["gap"].min()), float(df["gap"].max())
            gap_range = st.slider("نطاق الفجوة", min_gap, max_gap, (min_gap, max_gap), 0.5)

    filtered = df.copy()
    if sel_grade != "الكل":
        filtered = filtered[filtered["grade"] == sel_grade]
    if sel_risk != "الكل":
        filtered = filtered[filtered["risk_level"] == sel_risk]
    filtered = filtered[(filtered["gap"] >= gap_range[0]) & (filtered["gap"] <= gap_range[1])]

    st.caption(f"عدد الطلاب المعروضين: **{len(filtered)}** من أصل **{len(df)}**")

    # ── Distribution chart ────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>توزيع الفجوات</div>", unsafe_allow_html=True)
        fig = px.histogram(
            filtered, x="gap", nbins=25,
            color_discrete_sequence=["#0a4f6e"],
            labels={"gap": "الفجوة", "count": "عدد الطلاب"}
        )
        fig.add_vline(x=0,  line_dash="dash", line_color="#27ae60", annotation_text="لا فجوة")
        fig.add_vline(x=10, line_dash="dash", line_color="#f39c12", annotation_text="فجوة متوسطة")
        fig.add_vline(x=20, line_dash="dash", line_color="#e74c3c", annotation_text="فجوة حرجة")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                          font_family="Cairo", height=340, margin=dict(t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>مقارنة اختبارات القياس</div>", unsafe_allow_html=True)
        avg_data = pd.DataFrame({
            "الاختبار": ["المدرسة", "التحصيلي", "القدرات", "نافس"],
            "المتوسط": [
                filtered["school_avg"].mean(),
                filtered["tahsili"].mean(),
                filtered["qudurat"].mean(),
                filtered["nafis"].mean()
            ]
        })
        fig2 = px.bar(
            avg_data, x="الاختبار", y="المتوسط",
            color="المتوسط",
            color_continuous_scale=["#e74c3c", "#f39c12", "#27ae60"],
            text=avg_data["المتوسط"].round(1)
        )
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                           font_family="Cairo", height=340,
                           margin=dict(t=10,b=10), coloraxis_showscale=False,
                           yaxis=dict(range=[0, 100]))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Subject gap radar ─────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>مخطط الرادار — الفجوة حسب المادة</div>", unsafe_allow_html=True)

    subjects = {
        "الرياضيات": "math_school",
        "العلوم":    "science_school",
        "العربي":    "arabic_school",
        "الإنجليزي": "english_school",
    }
    avg_school_by_subject   = [filtered[v].mean() for v in subjects.values()]
    avg_qiyas = filtered["tahsili"].mean()
    avg_qiyas_by_subject = [avg_qiyas] * 4  # approximate

    fig3 = go.Figure()
    fig3.add_trace(go.Scatterpolar(
        r=avg_school_by_subject + [avg_school_by_subject[0]],
        theta=list(subjects.keys()) + [list(subjects.keys())[0]],
        fill="toself", name="المدرسة",
        line_color="#0a4f6e", fillcolor="rgba(10,79,110,0.15)"
    ))
    fig3.add_trace(go.Scatterpolar(
        r=avg_qiyas_by_subject + [avg_qiyas_by_subject[0]],
        theta=list(subjects.keys()) + [list(subjects.keys())[0]],
        fill="toself", name="القياس",
        line_color="#e74c3c", fillcolor="rgba(231,76,60,0.1)"
    ))
    fig3.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        font_family="Cairo", height=400,
        legend=dict(orientation="h", y=-0.1),
        margin=dict(t=30, b=50)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── Students Table ────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>📋 جدول الطلاب التفصيلي</div>", unsafe_allow_html=True)

    display_df = filtered[[
        "student_id", "name", "grade", "school_avg",
        "tahsili", "qudurat", "nafis", "gap", "risk_level"
    ]].rename(columns={
        "student_id": "الرقم", "name": "الاسم", "grade": "الصف",
        "school_avg": "المدرسة", "tahsili": "التحصيلي",
        "qudurat": "القدرات", "nafis": "نافس",
        "gap": "الفجوة", "risk_level": "المستوى"
    }).sort_values("الفجوة", ascending=False)

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Export
    csv = display_df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("⬇️ تصدير النتائج CSV", csv, "gap_analysis.csv", "text/csv")
