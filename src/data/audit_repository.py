import requests
import json
from src.core.config import Config
from src.domain.entities import AuditResult

class AuditRepository:
    def __init__(self, retriever):
        self.retriever = retriever

    def audit_contract(self, contract_text: str) -> AuditResult:
        # 1. البحث عن الضوابط ذات الصلة في ChromaDB
        relevant_docs = self.retriever.invoke(contract_text[:2000])
        context = "\n---\n".join([doc.page_content for doc in relevant_docs])

        # 2. إعداد التوجيه المحسن للذكاء الاصطناعي (Prompt)
        prompt = f"""
أنت خبير تدقيق سيبراني وقانوني في المملكة العربية السعودية.
قم بمطابقة العقد المرفق مع الضوابط الوطنية المتاحة في السياق (NCA ECC / PDPL).

السياق التنظيمي المتاح:
{context}

نص العقد المراد فحصه:
{contract_text}

يجب أن تكون إجابتك حصراً بتنسيق JSON صحيح يمتلك المفاتيح التالية:
{{
  "compliance_status": "غير ممتثل",
  "violations": "شرح الثغرة إن وجدت",
  "referenced_control": "اسم ورقم المادة أو ضابط NCA/PDPL المخالف",
  "suggested_clause": "الصياغة البديلة القانونية والأمنية الموصى بها",
  "compliance_score": 75
}}
"""

        # 3. إرسال الطلب لـ OpenRouter API
        headers = {"Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:8501", # لتحديد المصدر لـ OpenRouter
            "X-Title": "SANAD Compliance Audit",
            "Content-Type": "application/json"
            # "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            # "Content-Type": "application/json"
        }

        payload = {
            "model": Config.OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            # استخراج الـ JSON من إجابة النموذج
            clean_json = content[content.find('{'):content.rfind('}')+1]
            data = json.loads(clean_json)
            
            return AuditResult(
                compliance_status=data.get("compliance_status", "غير معروف"),
                violations=data.get("violations", "لا يوجد"),
                referenced_control=data.get("referenced_control", "غير محدد"),
                suggested_clause=data.get("suggested_clause", "لا يوجد"),
                compliance_score=data.get("compliance_score", 100)
            )
        else:
            raise Exception(f"خطأ في الاتصال بـ OpenRouter: {response.text}")