
import streamlit as st
import pandas as pd
from mini_ai_smart import analyze_text
from recommender import recommend

def workers_page(sheets):
    st.header("👷 قسم العمال")
    st.write("حاسبة الأجور والإجازات ومراجعة الحقوق.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("حاسبة بدل الإجازة ومكافأة نهاية الخدمة")
        salary = st.number_input("الراتب الشهري (د.أ)", min_value=0.0, value=350.0, step=1.0)
        years = st.number_input("عدد سنوات الخدمة", min_value=0.0, value=2.0, step=0.1)
        calc = st.button("احسب للمرة")
        if calc:
            annual_salary = salary * 12
            # simple end-of-service example: one month per year
            eos = salary * years
            leave_pay = (salary/30) * 21  # مثال: 21 يوم إجازة
            st.success(f"مكافأة نهاية الخدمة تقريبية: {eos:.2f} د.أ")
            st.info(f"بدل إجازة (21 يوم): {leave_pay:.2f} د.أ")
    with col2:
        st.subheader("بحث سريع في القوانين")
        q = st.text_input("اكتب نص أو رقم مادة للبحث")
        if q:
            if sheets:
                results = []
                for name, df in sheets.items():
                    # search in string columns
                    mask = df.apply(lambda col: col.astype(str).str.contains(q, case=False, na=False)).any(axis=1)
                    found = df[mask]
                    if not found.empty:
                        results.append((name, found.head(5)))
                if results:
                    for n, f in results:
                        st.markdown(f"**جدول:** {n}")
                        st.dataframe(f)
                else:
                    st.warning("لا توجد نتائج مطابقة في القاعدة.")
            else:
                st.error("قاعدة البيانات غير متاحة.")

def employers_page(sheets):
    st.header("🧑‍💼 قسم أصحاب العمل")
    st.write("أدوات فحص التوافق مع قانون العمل.")
    with st.expander("تحقق من بند في عقد عمل"):
        wage = st.number_input("الراتب المتفق عليه (د.أ)", min_value=0.0, value=300.0, step=1.0)
        hours = st.number_input("ساعات العمل الأسبوعية", min_value=0.0, value=48.0, step=1.0)
        check = st.button("تحقق")
        if check:
            violations = []
            if wage < 260:  # مثال: حد أدنى
                violations.append("الراتب أقل من الحد الأدنى الافتراضي")
            if hours > 48:
                violations.append("ساعات العمل تتجاوز الحد المعياري (48 ساعة)")
            if violations:
                st.error("تم العثور على مخالفات:")
                for v in violations:
                    st.write("- " + v)
            else:
                st.success("لا توجد مخالفات واضحة حسب القواعد الافتراضية.")

def inspectors_page(sheets):
    st.header("🕵️ قسم المفتشين")
    st.write("نموذج تفتيش سريع وحفظ تقارير.")
    with st.form("inspection_form"):
        company = st.text_input("اسم المنشأة")
        violations = st.multiselect("المخالفات الملاحظة", ["عدم وجود عقد", "تأخير رواتب", "ساعات إضافية غير مدفوعة", "عدم تسجيل تأمين"])
        comments = st.text_area("ملاحظات")
        submitted = st.form_submit_button("حفظ تقرير التفتيش")
        if submitted:
            st.success("تم حفظ التقرير (محليًا في الواجهة) — لاحقًا سنضيف تصدير/حفظ للقاعدة.")
            st.write("التفاصيل:")
            st.write({"company": company, "violations": violations, "comments": comments})

def researchers_page(sheets):
    st.header("📚 قسم الباحثين")
    st.write("بحث متقدم وتحليل نصي ذكي.")
    query = st.text_input("ابحث في نصوص القوانين أو اطلب ملخصًا")
    if st.button("حلّل النص"):
        if query.strip() == "":
            st.warning("اكتب نصًا للتحليل أولًا.")
        else:
            res = analyze_text(query)
            st.subheader("الملخص")
            st.write(res.get("summary", ""))
            st.subheader("الكلمات المفتاحية")
            st.write(res.get("keywords", []))
    if sheets:
        st.markdown("### الجداول المتاحة في القاعدة")
        st.write(list(sheets.keys()))

def settings_page():
    st.header("⚙️ الإعدادات")
    st.write("إعدادات المزامنة والتمييز.")
    use_sync = st.checkbox("مزامنة تلقائية من Google Sheets", value=True)
    default_user = st.selectbox("نوع المستخدم الافتراضي", ["عامل", "صاحب عمل", "مفتش"])
    st.write("تم ضبط النوع الافتراضي:", default_user)
