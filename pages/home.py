"""
pages/home.py  —  الصفحة الرئيسية
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_manager import init_session, risk_color


def show():
    init_session()
    df = st.session_state.students_df

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0a4f6e 0%,#072d40 100%);
                border-radius:20px; padding:32px 36px; margin-bottom:28px;
                box-shadow:0 8px 32px rgba(10,79,110,0.22);'>
        <div style='font-size:2.4rem;font-weight:900;color:white;'>🧭 بوصلة</div>
        <div style='font-size:1rem;color:#a0c4d4;margin-top:4px;'>
            {st.session_state.region_name} — العام الدراسي {st.session_state.academic_year}
        </div>
        <div style='font-size:0.9rem;color:#7aadc0;margin-top:2px;'>
            {st.session_state.school_name}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total   = len(df)
    critical = len(df[df["risk_level"] == "فجوة حرجة"])
    medium   = len(df[df["risk_level"] == "فجوة متوسطة"])
    ok       = len(df[df["risk_level"].isin(["متوافق", "فجوة بسيطة"])])
    avg_gap  = df["gap"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, total,    "إجمالي الطلاب",      "#0a4f6e"),
        (c2, critical, "فجوة حرجة",           "#e74c3c"),
        (c3, medium,   "فجوة متوسطة",          "#f39c12"),
        (c4, ok,       "أداء متوافق",          "#27ae60"),
        (c5, f"{avg_gap:.1f}", "متوسط الفجوة", "#3498db"),
    ]
    for col, val, label, color in kpis:
        with col:
            st.markdown(f"""
            <div class='kpi-box' style='border-top-color:{color};'>
                <div class='kpi-value' style='color:{color};'>{val}</div>
                <div class='kpi-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ────────────────────────────────────────────────────────────
    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.markdown("<div class='section-header'>توزيع مستويات الفجوة</div>", unsafe_allow_html=True)
        risk_counts = df["risk_level"].value_counts().reset_index()
        risk_counts.columns = ["المستوى", "العدد"]
        colors = [risk_color(r) for r in risk_counts["المستوى"]]
        fig = px.bar(
            risk_counts, x="المستوى", y="العدد",
            color="المستوى",
            color_discrete_sequence=colors,
            text="العدد"
        )
        fig.update_layout(
            showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
            font_family="Cairo", margin=dict(t=10, b=10),
            xaxis=dict(title=""), yaxis=dict(title="عدد الطلاب"),
            height=320
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-header'>الفجوة حسب الصف</div>", unsafe_allow_html=True)
        grade_gap = df.groupby("grade")["gap"].mean().reset_index()
        fig2 = px.bar(
            grade_gap, x="grade", y="gap",
            color="gap",
            color_continuous_scale=["#27ae60", "#f39c12", "#e74c3c"],
            text=grade_gap["gap"].round(1)
        )
        fig2.update_layout(
            showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
            font_family="Cairo", margin=dict(t=10, b=10),
            xaxis=dict(title=""), yaxis=dict(title="متوسط الفجوة"),
            coloraxis_showscale=False, height=320
        )
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Scatter: School vs Qiyas ──────────────────────────────────────────────
    st.markdown("<div class='section-header'>مقارنة الدرجة المدرسية بدرجة القياس</div>", unsafe_allow_html=True)
    fig3 = px.scatter(
        df, x="school_avg", y="tahsili",
        color="risk_level",
        color_discrete_map={
            "فجوة حرجة": "#e74c3c",
            "فجوة متوسطة": "#f39c12",
            "فجوة بسيطة": "#3498db",
            "متوافق": "#27ae60"
        },
        hover_data=["name", "grade", "gap"],
        labels={"school_avg": "متوسط المدرسة", "tahsili": "التحصيلي"},
        opacity=0.75
    )
    # reference line y=x
    fig3.add_shape(type="line", x0=20, y0=20, x1=100, y1=100,
                   line=dict(color="#aaa", dash="dot", width=1.5))
    fig3.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Cairo", height=420,
        margin=dict(t=10, b=10), legend_title="مستوى الفجوة"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── Top At-Risk Table ─────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>⚠️ أعلى 10 طلاب في خطر</div>", unsafe_allow_html=True)
    top_risk = df[df["risk_level"] == "فجوة حرجة"].nlargest(10, "gap")[
        ["name", "grade", "school_avg", "tahsili", "qudurat", "gap"]
    ].rename(columns={
        "name": "الطالب", "grade": "الصف",
        "school_avg": "متوسط المدرسة",
        "tahsili": "التحصيلي", "qudurat": "القدرات",
        "gap": "الفجوة"
    })
    st.dataframe(top_risk, use_container_width=True, hide_index=True)
