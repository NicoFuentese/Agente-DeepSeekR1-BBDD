import boto3
import os

class BedrockAgent:
    def __init__(self):
        # Lee las credenciales del entorno inyectado por Docker
        self.client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
        self.model_id = os.getenv("MODEL_ID", "us.deepseek.r1-v1:0")

    def preguntar(self, prompt):
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": 2000, "temperature": 0.5}
            )
            return response['output']['message']['content'][0]['text']
        except Exception as e:
            return f"Error técnico: {str(e)}"