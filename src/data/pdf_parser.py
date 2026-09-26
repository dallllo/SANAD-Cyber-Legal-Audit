import fitz  # PyMuPDF

class PDFParser:
    @staticmethod
    def extract_text(pdf_file) -> str:
        """استخراج النص الكامل من ملف PDF العقد"""
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text