"""
pages/reports.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_manager import init_session, risk_color


def _recommendations(row):
    recs = []
    gap = row["gap"]
    if gap > 20:
        recs += [
            "📌 تحويل الطالب لجلسات دعم أكاديمي فردية أسبوعية",
            "📌 مراجعة أساليب التقييم المدرسي — احتمال تضخم الدرجات",
            "📌 إشراك ولي الأمر في خطة التحسين",
            "📌 وضع الطالب على قائمة المتابعة الدورية",
        ]
    elif gap > 10:
        recs += [
            "📘 توجيه الطالب لمجموعات المذاكرة التعاونية",
            "📘 تقديم تدريبات مكثفة على نماذج اختبارات القياس",
            "📘 تحليل الفجوة بين المادة الأعلى والأدنى درجة",
        ]
    else:
        recs += [
            "✅ الاستمرار في نهج الدراسة الحالي",
            "✅ المشاركة في برامج الإثراء والتطوير",
        ]
    if row.get("math_school", 0) - row.get("tahsili", 0) > 15:
        recs.append("📐 الرياضيات: فجوة واضحة — التركيز على الرياضيات التطبيقية في القياس")
    return recs


def show():
    init_session()
    df = st.session_state.students_df

    st.markdown("<div class='section-header'>📋 التقارير والتوصيات</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 تقرير المدرسة", "👤 تقرير طالب", "💡 خطة علاجية"])

    with tab1:
        st.markdown(f"""
        <div class='bawsala-card'>
        <b>المدرسة:</b> {st.session_state.school_name} &nbsp;|&nbsp;
        <b>العام:</b> {st.session_state.academic_year} &nbsp;|&nbsp;
        <b>إجمالي الطلاب:</b> {len(df)}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-header'>توزيع مستويات الخطر حسب الصف</div>", unsafe_allow_html=True)
        pivot = df.groupby(["grade", "risk_level"]).size().reset_index(name="العدد")
        fig = px.bar(
            pivot, x="grade", y="العدد", color="risk_level",
            color_discrete_map={
                "فجوة حرجة": "#e74c3c", "فجوة متوسطة": "#f39c12",
                "فجوة بسيطة": "#3498db", "متوافق": "#27ae60"
            },
            barmode="stack",
            labels={"grade": "الصف", "risk_level": "المستوى"}
        )
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="Cairo", height=360, margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        summary = df.groupby("grade").agg(
            عدد_الطلاب=("student_id", "count"),
            متوسط_المدرسة=("school_avg", "mean"),
            متوسط_التحصيلي=("tahsili", "mean"),
            متوسط_الفجوة=("gap", "mean"),
        ).round(1).reset_index().rename(columns={"grade": "الصف"})
        st.dataframe(summary, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("⬇️ تصدير التقرير الكامل", csv, "school_report.csv", "text/csv")

    with tab2:
        student_names = df["name"].tolist()
        sel = st.selectbox("اختر الطالب", student_names)
        row = df[df["name"] == sel].iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        for col, val, label, color in [
            (c1, row["school_avg"], "المدرسة", "#0a4f6e"),
            (c2, row["tahsili"],    "التحصيلي", "#3498db"),
            (c3, row["qudurat"],    "القدرات", "#9b59b6"),
            (c4, row["nafis"],      "نافس", "#1abc9c"),
        ]:
            with col:
                st.markdown(f"""
                <div class='kpi-box' style='border-top-color:{color};'>
                    <div class='kpi-value' style='color:{color};'>{val}</div>
                    <div class='kpi-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        categories = ["المدرسة", "التحصيلي", "القدرات", "نافس"]
        values_radar = [row["school_avg"], row["tahsili"], row["qudurat"], row["nafis"]]
        fig2 = go.Figure(go.Scatterpolar(
            r=values_radar + [values_radar[0]],
            theta=categories + [categories[0]],
            fill="toself", line_color="#0a4f6e",
            fillcolor="rgba(10,79,110,0.15)"
        ))
        fig2.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            font_family="Cairo", height=350, margin=dict(t=30, b=30)
        )
        st.plotly_chart(fig2, use_container_width=True)

        risk = row["risk_level"]
        badge = {
            "فجوة حرجة": "gap-critical",
            "فجوة متوسطة": "gap-warning",
            "متوافق": "gap-ok"
        }.get(risk, "gap-ok")

        st.markdown(f"""
        <div class='bawsala-card'>
            <b>الصف:</b> {row['grade']} &nbsp;|&nbsp;
            <b>الفجوة:</b> {row['gap']:.1f} &nbsp;|&nbsp;
            <span class='{badge}'>{risk}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**التوصيات المخصصة:**")
        for rec in _recommendations(row):
            st.markdown(f"- {rec}")

    with tab3:
        critical_df = df[df["risk_level"] == "فجوة حرجة"].nlargest(20, "gap")
        st.markdown(f"#### الطلاب ذوو الفجوة الحرجة ({len(critical_df)} طالباً)")

        if critical_df.empty:
            st.success("🎉 لا يوجد طلاب ذوو فجوة حرجة!")
        else:
            for _, row in critical_df.iterrows():
                with st.expander(f"⚠️ {row['name']} — فجوة {row['gap']:.1f} | {row['grade']}"):
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.metric("المدرسة",  f"{row['school_avg']:.1f}")
                        st.metric("التحصيلي", f"{row['tahsili']:.1f}")
                    with cc2:
                        st.metric("القدرات",  f"{row['qudurat']:.1f}")
                        st.metric("الفجوة",   f"{row['gap']:.1f}",
                                  delta=f"-{row['gap']:.1f}", delta_color="inverse")
                    st.markdown("**الخطة العلاجية:**")
                    for rec in _recommendations(row):
                        st.markdown(f"  {rec}")
