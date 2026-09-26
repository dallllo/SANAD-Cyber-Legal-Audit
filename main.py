import os
from src.data.vector_store import VectorStoreManager

if __name__ == "__main__":
    print("تجهيز وتأسيس قواعد بيانات الامتثال لـ SANAD...")
    vm = VectorStoreManager()
    vm.build_database()
    print("تم إعداد البيانات بنجاح! يمكنك الآن تشغيل التطبيق عبر:")
    print("streamlit run src/presentation/app.py")