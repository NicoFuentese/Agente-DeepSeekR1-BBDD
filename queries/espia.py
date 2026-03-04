import os
import pandas as pd
from sqlalchemy import create_engine

# Leemos las credenciales que inyectó Docker desde el .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT", "3306")

# URL de conexión (Notar que termina en "/" sin nombrar a ticketsDB)
db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/"
engine = create_engine(db_url)

print("\n INICIANDO ESPIONAJE DE PERMISOS DE LA BBDD\n")

try:
    print("1. BASES DE DATOS QUE SE PUEDEN VER ---")
    df_dbs = pd.read_sql("SHOW DATABASES;", engine)
    print(df_dbs.to_string(index=False))
    
    print("\n2. LOS PERMISOS REALES (GRANTS) ---")
    df_grants = pd.read_sql("SHOW GRANTS;", engine)
    for index, row in df_grants.iterrows():
        print(f"-> {row[0]}")
        
except Exception as e:
    print(f"ERROR al consultar: {e}")