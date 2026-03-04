import os
from sqlalchemy import create_engine, text

def obtener_esquema_completo():
    # Python lee las variables limpias del .env
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME")
    
    # Python SÍ entiende las f-strings y arma la URL aquí:
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    
    engine = create_engine(db_url)
    esquema = ""
    try:
        with engine.connect() as conn:
            tablas = conn.execute(text("SHOW TABLES")).fetchall()
            for (tabla_nombre,) in tablas:
                columnas = conn.execute(text(f"DESCRIBE {tabla_nombre}")).fetchall()
                detalles = [f"{c[0]} ({c[1]})" for c in columnas]
                esquema += f"TABLA: {tabla_nombre}\nCOLUMNAS: {', '.join(detalles)}\n\n"
        return esquema
    except Exception as e:
        return f"Error leyendo esquema: {e}"