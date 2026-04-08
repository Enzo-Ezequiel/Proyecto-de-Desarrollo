from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """
    Clase encargada de gestionar la comunicación con los modelos de 
    Inteligencia Artificial de Google Gemini.
    """

    def __init__(self):
        """
        Inicializa el cliente de la API y define el modelo a utilizar.
        Configura el acceso mediante la API KEY almacenada en las variables de entorno.
        """
        # Usamos la configuración estándar
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # IMPORTANTE: Usa este nombre exacto, es el más estable para el Free Tier
        self.model_id = "gemini-1.5-flash" 

    def summarize_content(self, text: str) -> str:
        """
        Procesa un texto extenso y genera un resumen sintético utilizando IA. 

        Args:
            text (str): El contenido textual extraído del documento PDF. 

        Returns:
            str: Una oración con el resumen del contenido o un mensaje de error descriptivo. 
        """
        if not text: 
            return "Texto vacío"
        
        try:
            # ENVIAMOS MENOS TEXTO (Solo los primeros 5000 caracteres)
            # Esto evita que Google nos bloquee por "pesados"
            recorte = text[:5000] 
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"Resume esto en una oración: {recorte}"
            )
            return response.text
        except Exception as e:
            # Captura excepciones para mantener el flujo del código limpio [cite: 152]
            return f"Error de cuota/modelo: {str(e)}"