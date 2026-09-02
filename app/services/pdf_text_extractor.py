"""Extracción de texto de PDFs. Aísla la dependencia de pypdf del resto del servicio."""

import io

import pypdf


class PdfTextExtractor:
    """Convierte los bytes de un PDF en texto plano."""

    def extraer_texto(self, contenido_bytes: bytes) -> str:
        lector_pdf = pypdf.PdfReader(io.BytesIO(contenido_bytes))
        texto_extraido = ""
        for pagina in lector_pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_extraido += texto + "\n"
        return texto_extraido.strip()
