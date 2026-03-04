# Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo el requirements primero (para aprovechar el caché de Docker)
COPY requirements.txt .

# Instalar las librerías sin guardar caché basura
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Crear la carpeta de queries por si no existe
RUN mkdir -p /app/queries

# Comando por defecto al levantar el contenedor
CMD ["python", "data_analyst_bot.py"]