import fitz  # (Esta es la librería PyMuPDF)

class PDFService:
    def extract_text(self, file_path: str) -> str:
        """Extrae todo el texto de un archivo PDF."""
        text = ""
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        except Exception as e:
            return f"Error al leer el PDF: {str(e)}"