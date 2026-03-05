import streamlit as st
import pandas as pd
# Importamos SOLO la clase DataAgent de tu archivo (sin ejecutar el chat_sql)
from data_analyst_bot import DataAgent

# 1. Configuración de la página web
st.set_page_config(page_title="Analista BBDD", page_icon="🤖", layout="wide")
st.title("🤖 Agente Analista de Base de Datos")
st.markdown("Hazme preguntas sobre los tickets y áreas en lenguaje natural.")

# 2. Caché para la Base de Datos
# Esto es vital en Streamlit para que no se reconecte a MariaDB con cada clic
@st.cache_resource
def iniciar_agente():
    return DataAgent()

# Inicializamos el motor
try:
    bot = iniciar_agente()
except Exception as e:
    st.error(f"❌ Error crítico al conectar con la base de datos: {e}")
    st.stop()

# 3. Definimos el Prompt (el mismo que tenías)
prompt_sistema = f"""Eres un experto DBA y Analista de Datos.
ESTRUCTURA DE LA BASE DE DATOS:
{bot.esquema}

INSTRUCCIONES:
1. Responde preguntas analíticas usando queries SQL complejas (JOINs, GROUP BY, etc).
2. Envía SIEMPRE el código SQL dentro de bloques ```sql ```.
3. Si el usuario te pide guardar la consulta, incluye la etiqueta [SAVE: nombre_archivo].
4. Usa solo SELECT. No intentes modificar la data.

CONSIDERACIONES:
- Cuando te pregunte por 'áreas', se refiere a departamentos/grupos de trabajo.
"""

# 4. Memoria del chat en la sesión web
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# 5. Dibujar el historial de mensajes
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["texto"])
        if mensaje.get("datos") is not None:
            st.dataframe(mensaje["datos"])

# 6. Lógica cuando el usuario escribe algo
if prompt := st.chat_input("Ej: ¿Cuál es el top 5 de áreas con más tickets?"):
    
    # Mostrar pregunta del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensajes.append({"rol": "user", "texto": prompt})

    # Procesar respuesta del bot
    with st.chat_message("assistant"):
        with st.spinner("🧠 Pensando y analizando datos..."):
            
            # Le preguntamos a AWS Bedrock (usando tu clase)
            respuesta_ai = bot.ai.preguntar(f"{prompt_sistema}\n\nPregunta: {prompt}")
            
            texto_final = respuesta_ai
            df_resultado = None

            # Si detectamos código SQL, lo extraemos y lo ejecutamos en Pandas para que Streamlit lo dibuje bonito
            if "```sql" in respuesta_ai:
                try:
                    sql_code = respuesta_ai.split("```sql")[1].split("```")[0].strip()
                    df_resultado = pd.read_sql(sql_code, bot.engine)
                    
                    if df_resultado.empty:
                        texto_final += "\n\n⚠️ *La consulta se ejecutó correctamente, pero no devolvió resultados.*"
                except Exception as e:
                    texto_final += f"\n\n❌ **Error en SQL:** `{str(e)}`"

            # Si detectamos la etiqueta SAVE, usamos tu función de guardado
            if "[SAVE:" in respuesta_ai:
                try:
                    nombre = respuesta_ai.split("[SAVE:")[1].split("]")[0].strip()
                    path = bot.guardar_sql(nombre, sql_code)
                    texto_final += f"\n\n💾 *Query guardada exitosamente en:* `{path}`"
                except Exception as e:
                    texto_final += f"\n\n❌ *Error al guardar:* `{str(e)}`"

            # Renderizamos en pantalla
            st.markdown(texto_final)
            if df_resultado is not None and not df_resultado.empty:
                st.dataframe(df_resultado, use_container_width=True)

    # Guardar en memoria
    st.session_state.mensajes.append({
        "rol": "assistant", 
        "texto": texto_final, 
        "datos": df_resultado
    })