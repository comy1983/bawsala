"""
utils/data_manager.py
مدير البيانات - يتحكم في session state وتوليد البيانات التجريبية
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random

# ─── Subject Maps ─────────────────────────────────────────────────────────────
SUBJECTS_TAHSILI = ["الرياضيات", "الفيزياء", "الكيمياء", "الأحياء", "اللغة العربية", "اللغة الإنجليزية"]
SUBJECTS_QUDURAT = ["الكمي - الرياضيات", "الكمي - المنطق", "اللفظي - اللغة", "اللفظي - القراءة"]
SUBJECTS_NAFIS   = ["الجزء النفسي", "الجزء المعرفي"]
GRADES_SCHOOL    = ["أولى ثانوي", "ثانية ثانوي", "ثالثة ثانوي"]

# ─── Session Init ─────────────────────────────────────────────────────────────
def init_session():
    if "students_df" not in st.session_state:
        st.session_state.students_df = generate_demo_data()
    if "school_name" not in st.session_state:
        st.session_state.school_name = "ثانوية الملك عبدالعزيز"
    if "region_name" not in st.session_state:
        st.session_state.region_name = "إدارة التعليم - المنطقة الشرقية"
    if "academic_year" not in st.session_state:
        st.session_state.academic_year = "1446/1447"

# ─── Demo Data Generator ──────────────────────────────────────────────────────
def generate_demo_data(n=80):
    random.seed(42)
    np.random.seed(42)
    records = []
    grades_map = {1: "أولى ثانوي", 2: "ثانية ثانوي", 3: "ثالثة ثانوي"}

    for i in range(n):
        grade_num = random.choice([1, 2, 3])
        # Base ability (latent factor)
        ability = np.random.normal(65, 18)
        ability = np.clip(ability, 20, 100)

        # School grades ~ ability + noise (teachers sometimes inflate)
        school_avg = ability + np.random.normal(8, 6)
        school_avg = np.clip(school_avg, 30, 100)

        # Qiyas scores ~ ability + noise (harder, less inflation)
        tahsili = ability + np.random.normal(-5, 9)
        tahsili = np.clip(tahsili, 20, 100)

        qudurat = ability + np.random.normal(-3, 10)
        qudurat = np.clip(qudurat, 20, 100)

        nafis = ability + np.random.normal(0, 7)
        nafis = np.clip(nafis, 20, 100)

        gap = school_avg - ((tahsili + qudurat) / 2)

        records.append({
            "student_id": f"S{1000+i}",
            "name": f"طالب {i+1}",
            "grade": grades_map[grade_num],
            "grade_num": grade_num,
            "school_avg": round(school_avg, 1),
            "tahsili": round(tahsili, 1),
            "qudurat": round(qudurat, 1),
            "nafis": round(nafis, 1),
            "gap": round(gap, 1),
            "ability_est": round(ability, 1),
            "risk_level": classify_risk(gap),
            "math_school": round(school_avg + np.random.normal(0, 8), 1),
            "science_school": round(school_avg + np.random.normal(0, 8), 1),
            "arabic_school": round(school_avg + np.random.normal(0, 8), 1),
            "english_school": round(school_avg + np.random.normal(0, 8), 1),
        })

    df = pd.DataFrame(records)
    df[["math_school","science_school","arabic_school","english_school"]] = \
        df[["math_school","science_school","arabic_school","english_school"]].clip(30, 100)
    return df

def classify_risk(gap: float) -> str:
    if gap > 20:   return "فجوة حرجة"
    if gap > 10:   return "فجوة متوسطة"
    if gap > 0:    return "فجوة بسيطة"
    return "متوافق"

def risk_color(risk: str) -> str:
    return {
        "فجوة حرجة":   "#e74c3c",
        "فجوة متوسطة": "#f39c12",
        "فجوة بسيطة":  "#3498db",
        "متوافق":      "#27ae60",
    }.get(risk, "#888")

def risk_badge_class(risk: str) -> str:
    return {
        "فجوة حرجة":   "gap-critical",
        "فجوة متوسطة": "gap-warning",
        "فجوة بسيطة":  "gap-warning",
        "متوافق":      "gap-ok",
    }.get(risk, "gap-ok")
