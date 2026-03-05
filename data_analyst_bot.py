# data_analyst_bot.py
import os
import pandas as pd
from sqlalchemy import create_engine, text
from core.aws_client import BedrockAgent

# Aseguramos que importe desde el archivo correcto
from tools.db_inspector import obtener_esquema_completo

class DataAgent:
    def __init__(self):
        # 1. Armamos la URL leyendo el .env (Eliminamos la carpeta config)
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME")
        
        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        
        # 2. Conectamos SQLAlchemy
        self.engine = create_engine(db_url)
        
        # 3. Inicializamos AWS Bedrock
        self.ai = BedrockAgent()
        
        # 4. RUTA CORREGIDA PARA DOCKER (Linux)
        self.save_path = "/app/queries"
        
        # 5. Cargamos el esquema de la base de datos
        self.esquema = obtener_esquema_completo()

    def ejecutar_y_analizar(self, sql):
        # Filtro de seguridad preventivo en Python
        prohibidos = ["drop", "delete", "update", "insert", "truncate", "alter"]
        if any(cmd in sql.lower() for cmd in prohibidos):
            return "❌ ERROR: Intento de modificación detectado. Acción bloqueada."

        try:
            # Extraer datos con Pandas
            df = pd.read_sql(sql, self.engine)
            if df.empty: return "La consulta no trajo resultados."
            
            resumen = f"✅ Éxito. Filas: {len(df)}\n"
            resumen += f"Muestra de datos:\n{df.head(5).to_string(index=False)}"
            return resumen
        except Exception as e:
            return f"❌ Error en SQL: {str(e)}"

    def guardar_sql(self, nombre, sql):
        # Si el directorio no existe por alguna razón, lo crea
        os.makedirs(self.save_path, exist_ok=True)
        path = os.path.join(self.save_path, f"{nombre.replace(' ', '_')}.sql")
        with open(path, "w") as f:
            f.write(sql)
        return path



def chat_sql():
    print("Iniciando Agente de Base de Datos y leyendo esquema de Base de Datos...")
    bot = DataAgent()
    print("--- Agente BD: Data Analyst Mode (MariaDB) ---")
    
    prompt_sistema = f"""Eres un Agente Analista de Base de Datos, un experto DBA y Analista de Datos Senior especializado en MariaDB.
    
    ESTRUCTURA DE LA BASE DE DATOS:
    {bot.esquema}
    
    INSTRUCCIONES ESTRICTAS:
    1. EVALÚA LA INTENCIÓN: Primero, analiza si el usuario está conversando de forma general (ej. "¿quién eres?", saludos) o si requiere una consulta/análisis de la base de datos.
    2. MODO CONVERSACIONAL: Si es una charla general o pregunta por tus capacidades, responde de manera natural, profesional y concisa. NO utilices el formato de análisis ni bloques de código SQL.
    3. MODO ANALÍTICO Y TÉCNICO: SI el usuario pide datos o reportes, debes responder OBLIGATORIAMENTE con esta estructura:
    
        **🔍 Análisis de la Solución:**
        [Explica detalladamente tu razonamiento: qué tablas usarás, cómo las relacionarás y qué lógica aplicarás].
        
        **💻 Código SQL:**
        ```sql
        [Adapta la complejidad a la petición: usa consultas simples para preguntas directas, pero aplica todo tu potencial técnico (JOINs, GROUP BY, subconsultas, CTEs) si la pregunta requiere un análisis complejo. Usa ÚNICAMENTE sentencias SELECT].
        ```
        [Opcional: Si el usuario te pidió guardar la consulta, incluye obligatoriamente la etiqueta [SAVE: nombre_archivo_sin_espacios] al final de tu respuesta].

    4. SEGURIDAD ABSOLUTA: Tienes estrictamente prohibido generar sentencias INSERT, UPDATE, DELETE, DROP o sugerir modificaciones. Operas en modo de solo lectura.
    """

    while True:
        user_msg = input("\n📊 Pregunta (o 'salir'): ")
        if user_msg.lower() in ['salir', 'exit']: break

        print("\n---------------------------------------------------------------")
        print("🧠 Procesando...")
        print("---------------------------------------------------------------\n")
        respuesta = bot.ai.preguntar(f"{prompt_sistema}\n\nPregunta: {user_msg}")
        print(f"\n🤖 AGENTE:\n{respuesta}")

        # Ejecución automática si detectamos SQL
        if "```sql" in respuesta:
            sql_code = respuesta.split("```sql")[1].split("```")[0].strip()
            print("\n... Ejecutando consulta en MariaDB ...")
            print(bot.ejecutar_y_analizar(sql_code))

            # Guardado automático
            if "[SAVE:" in respuesta:
                nombre = respuesta.split("[SAVE:")[1].split("]")[0].strip()
                path = bot.guardar_sql(nombre, sql_code)
                print(f"💾 Query guardada en: {path}")

if __name__ == "__main__":
    chat_sql()