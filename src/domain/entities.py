from dataclasses import dataclass
from typing import Optional

@dataclass
class AuditResult:
    compliance_status: str       # (ممتثل / غير ممتثل / يحتاج تعديل)
    violations: str              # الثغرة أو المخالفة
    referenced_control: str      # رقم الضابط أو المادة (NCA / PDPL)
    suggested_clause: str        # النص البديل الموصى به
    compliance_score: int        # نسبة الامتثال (مثل 80%)