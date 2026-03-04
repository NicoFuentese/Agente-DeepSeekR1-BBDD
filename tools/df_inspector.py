# tools/db_inspector.py
from sqlalchemy import create_engine, text
from config import db_config

def obtener_esquema_completo():
    engine = create_engine(db_config.DATABASE_URL)
    esquema = ""
    try:
        with engine.connect() as conn:
            # Obtener lista de tablas
            tablas = conn.execute(text("SHOW TABLES")).fetchall()
            for (tabla_nombre,) in tablas:
                # Obtener columnas de cada tabla
                columnas = conn.execute(text(f"DESCRIBE {tabla_nombre}")).fetchall()
                detalles = [f"{c[0]} ({c[1]})" for c in columnas]
                esquema += f"TABLA: {tabla_nombre}\nCOLUMNAS: {', '.join(detalles)}\n\n"
        return esquema
    except Exception as e:
        return f"Error leyendo esquema: {e}"