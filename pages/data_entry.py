"""
pages/data_entry.py  —  صفحة إدخال البيانات
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_manager import init_session, classify_risk, generate_demo_data


def show():
    init_session()

    st.markdown("<div class='section-header'>📥 إدخال بيانات الطلاب</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📤 رفع ملف Excel/CSV", "✏️ إدخال يدوي", "🔄 بيانات تجريبية"])

    # ── Tab 1: File Upload ─────────────────────────────────────────────────────
    with tab1:
        st.markdown("<div class='bawsala-card'>", unsafe_allow_html=True)
        st.markdown("#### 📋 قالب البيانات المطلوب")
        st.markdown("""
        يجب أن يحتوي الملف على الأعمدة التالية:

        | العمود | الوصف | مثال |
        |--------|-------|------|
        | `student_id` | رقم الطالب | S1001 |
        | `name` | اسم الطالب | طالب 1 |
        | `grade` | الصف الدراسي | ثالثة ثانوي |
        | `school_avg` | متوسط الدرجة المدرسية | 78.5 |
        | `tahsili` | درجة التحصيلي | 65.0 |
        | `qudurat` | درجة القدرات | 70.0 |
        | `nafis` | درجة نافس | 72.0 |
        | `math_school` | درجة الرياضيات | 80.0 |
        | `science_school` | درجة العلوم | 75.0 |
        | `arabic_school` | درجة العربي | 82.0 |
        | `english_school` | درجة الإنجليزي | 71.0 |
        """)

        # Download template
        template_df = pd.DataFrame([{
            "student_id": "S1001", "name": "طالب 1", "grade": "ثالثة ثانوي",
            "grade_num": 3, "school_avg": 78.5, "tahsili": 65.0,
            "qudurat": 70.0, "nafis": 72.0, "math_school": 80.0,
            "science_school": 75.0, "arabic_school": 82.0, "english_school": 71.0
        }])
        csv_template = template_df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("⬇️ تحميل قالب CSV", csv_template, "template_bawsala.csv", "text/csv")

        uploaded = st.file_uploader("رفع الملف (CSV أو Excel)", type=["csv", "xlsx"])
        if uploaded:
            try:
                if uploaded.name.endswith(".csv"):
                    df_new = pd.read_csv(uploaded)
                else:
                    df_new = pd.read_excel(uploaded)

                # Auto-fill missing columns
                required_cols = ["student_id", "name", "grade", "school_avg", "tahsili", "qudurat", "nafis"]
                missing = [c for c in required_cols if c not in df_new.columns]
                if missing:
                    st.error(f"❌ الأعمدة التالية مفقودة: {', '.join(missing)}")
                else:
                    if "grade_num" not in df_new.columns:
                        gmap = {"أولى ثانوي": 1, "ثانية ثانوي": 2, "ثالثة ثانوي": 3}
                        df_new["grade_num"] = df_new["grade"].map(gmap).fillna(2).astype(int)
                    for col in ["math_school","science_school","arabic_school","english_school"]:
                        if col not in df_new.columns:
                            df_new[col] = df_new["school_avg"]
                    df_new["gap"] = df_new["school_avg"] - (df_new["tahsili"] + df_new["qudurat"]) / 2
                    df_new["gap"] = df_new["gap"].round(1)
                    df_new["risk_level"] = df_new["gap"].apply(classify_risk)
                    df_new["ability_est"] = ((df_new["school_avg"] + df_new["tahsili"] + df_new["qudurat"]) / 3).round(1)

                    st.success(f"✅ تم استيراد {len(df_new)} طالب بنجاح!")
                    st.dataframe(df_new.head(10), use_container_width=True, hide_index=True)
                    if st.button("💾 حفظ البيانات", key="save_upload"):
                        st.session_state.students_df = df_new
                        st.success("✅ تم حفظ البيانات في النظام!")
            except Exception as e:
                st.error(f"خطأ في قراءة الملف: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Manual Entry ────────────────────────────────────────────────────
    with tab2:
        st.markdown("<div class='bawsala-card'>", unsafe_allow_html=True)
        st.markdown("#### ✏️ إدخال بيانات طالب واحد")

        c1, c2, c3 = st.columns(3)
        with c1:
            sid   = st.text_input("رقم الطالب", "S9999")
            sname = st.text_input("اسم الطالب", "طالب جديد")
            grade = st.selectbox("الصف", ["أولى ثانوي", "ثانية ثانوي", "ثالثة ثانوي"])
        with c2:
            school_avg = st.number_input("متوسط المدرسة", 0.0, 100.0, 75.0, 0.5)
            tahsili    = st.number_input("درجة التحصيلي", 0.0, 100.0, 65.0, 0.5)
            qudurat    = st.number_input("درجة القدرات",   0.0, 100.0, 68.0, 0.5)
        with c3:
            nafis      = st.number_input("درجة نافس",      0.0, 100.0, 70.0, 0.5)
            math_s     = st.number_input("الرياضيات (مدرسة)", 0.0, 100.0, school_avg, 0.5)
            arabic_s   = st.number_input("العربي (مدرسة)",    0.0, 100.0, school_avg, 0.5)

        gap = school_avg - (tahsili + qudurat) / 2
        risk = classify_risk(gap)
        st.info(f"الفجوة المحسوبة: **{gap:.1f}** — مستوى الخطر: **{risk}**")

        if st.button("➕ إضافة الطالب"):
            gmap = {"أولى ثانوي": 1, "ثانية ثانوي": 2, "ثالثة ثانوي": 3}
            new_row = pd.DataFrame([{
                "student_id": sid, "name": sname, "grade": grade,
                "grade_num": gmap[grade], "school_avg": school_avg,
                "tahsili": tahsili, "qudurat": qudurat, "nafis": nafis,
                "gap": round(gap, 1), "risk_level": risk,
                "ability_est": round((school_avg + tahsili + qudurat) / 3, 1),
                "math_school": math_s, "science_school": school_avg,
                "arabic_school": arabic_s, "english_school": school_avg
            }])
            st.session_state.students_df = pd.concat(
                [st.session_state.students_df, new_row], ignore_index=True
            )
            st.success(f"✅ تمت إضافة الطالب {sname}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3: Demo Data ───────────────────────────────────────────────────────
    with tab3:
        st.markdown("<div class='bawsala-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔄 توليد بيانات تجريبية")
        n_students = st.slider("عدد الطلاب", 20, 200, 80, 10)
        if st.button("🎲 توليد بيانات جديدة"):
            import random
            seed = random.randint(0, 9999)
            np.random.seed(seed)
            st.session_state.students_df = generate_demo_data(n_students)
            st.success(f"✅ تم توليد {n_students} طالب بنجاح!")

        st.dataframe(st.session_state.students_df.head(10),
                     use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
