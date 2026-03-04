# core/aws_client.py
import boto3
from config import settings

class BedrockAgent:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
        # El cliente DEBE ser bedrock-runtime para invocar modelos
        self.client = self.session.client("bedrock-runtime")

    def preguntar(self, prompt):
        try:
            # Validamos si el método existe antes de llamar
            if not hasattr(self.client, 'converse'):
                return "Error: Tu versión de boto3 es muy antigua. Ejecuta 'pip install --upgrade boto3'."

            response = self.client.converse(
                modelId=settings.MODEL_ID,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": 2000, "temperature": 0.5}
            )
            return response['output']['message']['content'][0]['text']
        except Exception as e:
            return f"Error técnico: {str(e)}"