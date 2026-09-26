import sys
import os

# إضافة مجلد المشروع الرئيسي إلى المسارات
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import streamlit as st
from src.data.pdf_parser import PDFParser
from src.data.vector_store import VectorStoreManager
from src.data.audit_repository import AuditRepository


st.set_page_config(page_title="سند | SANAD Audit", layout="wide")

st.title("🛡️ منصة سند (SANAD)")
st.caption("نظام أتمتة تدقيق الامتثال والعقود السيبرانية - هاكثون سيف")

# تهيئة المحرك وقواعد البيانات
@st.cache_resource
def init_system():
    vector_mgr = VectorStoreManager()
    retriever = vector_mgr.get_retriever()
    return AuditRepository(retriever)

try:
    audit_repo = init_system()
except Exception:
    st.warning("جاري إعداد قاعدة بيانات اللوائح الوطنية لأول مرة...")
    vector_mgr = VectorStoreManager()
    vector_mgr.build_database()
    audit_repo = init_system()

uploaded_file = st.file_uploader("قم برفع العقد التقني (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("تم رفع الملف بنجاح!")
    
    if st.button("بدء التدقيق الآلي والامتثال 🚀"):
        with st.spinner("جاري تفكيك بنود العقد ومطابقتها مع اللوائح الوطنية عبر الذكاء الاصطناعي..."):
            contract_text = PDFParser.extract_text(uploaded_file)
            result = audit_repo.audit_contract(contract_text)
            
            st.markdown("---")
            st.header("📋 تقرير الامتثال والتدقيق الآلي")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="نسبة الامتثال التقديرية", value=f"{result.compliance_score}%")
            with col2:
                st.metric(label="حالة العقد", value=result.compliance_status)
                
            st.markdown("### ⚠️ الثغرات والمخالفات المرصودة:")
            st.error(result.violations)
            
            st.markdown("### 📌 الضابط التنظيمي المرجعي:")
            st.warning(result.referenced_control)
            
            st.markdown("### 💡 الصياغة البديلة المعتمدة (المقترحة):")
            st.success(result.suggested_clause)