# 🤖 Agente Analista de Base de Datos (GLPI)

## Descripción
Este proyecto implementa un Agente de Inteligencia Artificial (basado en AWS Bedrock) diseñado para actuar como un Administrador de Bases de Datos (DBA) y Analista de Datos Senior. El agente se conecta directamente a una base de datos MariaDB (específicamente al esquema de GLPI), comprende su estructura y responde a preguntas en lenguaje natural generando y ejecutando consultas SQL complejas en tiempo real.

Cuenta con una arquitectura híbrida que permite a los usuarios de negocio interactuar mediante una **Interfaz Web (Streamlit)** y a los administradores operar directamente desde la **Consola de Comandos (CLI)**.

## Stack Tecnológico
* **Lenguaje:** Python 3.9+
* **Framework Web:** Streamlit
* **Base de Datos:** MariaDB / MySQL (SQLAlchemy + Pandas)
* **IA:** AWS Bedrock (Modelos LLM)
* **Infraestructura:** Docker & Docker Compose

## Requisitos Previos

### Sistema Operativo
* **Producción/Servidor:** Linux (Red Hat, CentOS, Rocky Linux 9, Ubuntu, Debian).
* **Desarrollo:** Windows (con WSL2 habilitado) o macOS.

### Dependencias de Infraestructura
* **Docker** (v20.10 o superior)
* **Docker Compose** (v2.0 o superior)
* **Git** (Opcional, se puede descargar el código fuente vía `wget` o `curl`)

### Requisitos de Base de Datos
* Acceso a un servidor MariaDB/MySQL.
* Un usuario de base de datos con permisos estrictamente de lectura (`GRANT SELECT, SHOW VIEW ON database.* TO 'usuario'@'%'`).

## Instalación y Configuración

**1. Clonar el repositorio**
```bash
git clone [https://github.com/TuUsuario/Agente-DeepSeekR1-BBDD.git](https://github.com/TuUsuario/Agente-DeepSeekR1-BBDD.git)
cd Agente-DeepSeekR1-BBDD
```

**2. Configurar Variables de Entorno**
Crea un archivo llamado .env en la raíz del proyecto. No compartas este archivo ni lo subas al control de versiones.

```bash
# Configuración de Base de Datos
DB_USER=tu_usuario_lectura
DB_PASS=tu_contraseña_segura
DB_HOST=10.x.x.x
DB_PORT=3306
DB_NAME=glpiprd

# Credenciales AWS Bedrock (Si aplica)
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=us-east-1
```
## Como hacerlo funcionar?
La aplicación está contenerizada para garantizar que funcione igual en cualquier entorno.

**1. Levantar la infraestructura**
Ejecuta el siguiente comando para construir la imagen e iniciar el contenedor en segundo plano:

```bash
docker compose up -d --build
```

**2. Acceder a la interfab web (UI)**
Abre tu navegador web y dirígete a:
```bash
http://<IP_DEL_SERVIDOR>:8502
```

**3. Acceder al Modo Consola (CLI)**
Si deseas interactuar con el bot directamente desde la terminal del servidor (sin interfaz gráfica), ejecuta:

```bash
docker exec -it agente-bbdd python data_analyst_bot.py
```

## Formato de Respuesta del Agente
El agente está instruido (mediante Prompt Engineering) para responder siempre con un formato analítico estructurado:

    1. Análisis de la Solución: Explica paso a paso qué tablas (ej. glpi_tickets, glpi_groups) utilizará, los JOINs necesarios y la lógica matemática aplicada.
    2. Código SQL: Genera la consulta optimizada (usando CTEs, subconsultas y funciones de agregación si la complejidad lo amerita).
    3. Guardado Automático: Si el usuario incluye en su petición la instrucción de guardar el reporte, el agente añade la etiqueta [SAVE: nombre_archivo], lo que genera un archivo .sql físico en el volumen mapeado ./queries/ del servidor anfitrión.

## Seguridad

    - Ejecución Protegida: El agente tiene una directiva estricta de solo usar sentencias SELECT.
    - Capa de Base de Datos: Se delega la seguridad final al motor de MariaDB mediante políticas RBAC (Role-Based Access Control). El usuario configurado en el .env debe carecer de privilegios INSERT, UPDATE, DELETE o DROP.
    - Aislamiento Docker: La aplicación corre en un entorno aislado sin acceso directo a los binarios del host.

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles. 

Siéntete libre de utilizar, modificar y distribuir este código para adaptarlo a las necesidades de análisis de datos de tu propia empresa o proyecto personal.