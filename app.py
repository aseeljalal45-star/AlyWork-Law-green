
import streamlit as st
import pandas as pd
import time
from helpers.pages import workers_page, employers_page, inspectors_page, researchers_page, settings_page

# Page config
st.set_page_config(page_title="منصة قانون العمل الأردني الذكية", layout="wide", initial_sidebar_state="expanded")

# Load CSS
def local_css(path):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/styles.css")

# Loading screen
with st.spinner("جارٍ تحميل منصة قانون العمل الأردني الذكية..."):
    time.sleep(1.0)
    sheet_url = "https://docs.google.com/spreadsheets/d/1OgGi8nhzU_FshUsJyh5NWKA5jT9qG1Og/export?format=xlsx"
    try:
        sheets = pd.read_excel(sheet_url, sheet_name=None)
        DATA_LOADED = True
    except Exception as e:
        sheets = {}
        DATA_LOADED = False
        st.error("فشل تحميل قاعدة البيانات من Google Sheets. تحقق من مشاركة الملف.")
        # st.exception(e)

# Header
st.markdown(f"""
<div class="header">
  <img src="assets/logo.png" class="logo" />
  <div class="title-area">
    <h1>منصة قانون العمل الأردني الذكية</h1>
    <p class="subtitle">نظام متكامل لمساعدة العمال، أصحاب العمل، والمفتشين على تطبيق القانون بسهولة.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("القسم")
choice = st.sidebar.radio("", ["🏠 الرئيسية", "👷 العمال", "🧑‍💼 أصحاب العمل", "🕵️ المفتشين", "📚 الباحثين", "⚙️ الإعدادات"])

if choice == "🏠 الرئيسية":
    st.write("مرحبًا بك في منصة قانون العمل الأردني الذكية — اختر قسمًا من الشريط الجانبي للبدء.")
elif choice == "👷 العمال":
    workers_page(sheets if DATA_LOADED else None)
elif choice == "🧑‍💼 أصحاب العمل":
    employers_page(sheets if DATA_LOADED else None)
elif choice == "🕵️ المفتشين":
    inspectors_page(sheets if DATA_LOADED else None)
elif choice == "📚 الباحثين":
    researchers_page(sheets if DATA_LOADED else None)
elif choice == "⚙️ الإعدادات":
    settings_page()
