# Portafolio Web Flask + Tailwind CSS

Portafolio profesional de **Euler Arturo Chapid Inagan**, enfocado en soporte IT, redes, analisis de datos, automatizacion de procesos y desarrollo de herramientas web.

La aplicacion utiliza Flask para el backend, Jinja2 para las vistas y Tailwind CSS junto con estilos propios para la interfaz. El contenido profesional se centraliza en `data/profile.py` y se renderiza dinamicamente en el portafolio y en el CV imprimible.

## Caracteristicas clave

- Arquitectura modular con rutas Flask, plantillas Jinja2, datos de perfil separados y recursos frontend independientes.
- Formulario de contacto con validacion cliente/servidor, envio mediante la API HTTPS de Resend, honeypot anti-spam y rate limiting con Flask-Limiter.
- Respuestas JSON y formulario HTML tradicional para `POST /contact`.
- Visualizacion del CV PDF existente mediante `/cv/view`.
- Descarga del PDF mediante `/cv/download`.
- Version HTML limpia y responsive para imprimir o exportar a PDF mediante `/cv/print`.
- Cabeceras de seguridad, limite de tamano de solicitudes y manejo controlado de errores HTTP.
- Animaciones, revelado progresivo e interacciones del frontend con JavaScript e IntersectionObserver.

## Stack tecnologico

- Python 3.11+
- Flask 3.1
- Jinja2
- Resend Python SDK
- Flask-Limiter
- Gunicorn
- HTML5, CSS3 y JavaScript ES6+
- Tailwind CSS mediante CDN y estilos CSS propios
- API REST HTTPS de Resend para el formulario de contacto

## Estructura principal

```text
app.py                  # Aplicacion Flask, rutas y configuracion
data/profile.py         # Datos publicos del perfil profesional
templates/              # Vistas Jinja2
static/                 # CSS, JavaScript e imagenes
hoja de vida 2026a.pdf  # CV PDF servido por la aplicacion
Procfile                # Comando de inicio con Gunicorn
render.yaml             # Configuracion de despliegue en Render
```

## Instalacion local

Requisitos: Python 3.11 o superior.

1. Clona el repositorio y entra en la carpeta del proyecto.

2. Crea y activa un entorno virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   En macOS o Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Copia `.env.example` como `.env` y completa la configuracion necesaria:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Para ejecutar pruebas locales, define una clave `RESEND_API_KEY` valida solo si deseas enviar correos. Sin esa variable, el formulario respondera con un error controlado `503`.

6. Inicia la aplicacion:

   ```bash
   python app.py
   ```

   Abre `http://127.0.0.1:5000` en el navegador.

## Variables de entorno

Las variables se cargan desde `.env` en desarrollo y desde la configuracion del servicio en produccion.

| Variable | Requerida | Descripcion |
| --- | --- | --- |
| `SECRET_KEY` | Si | Clave aleatoria de Flask; en produccion debe tener al menos 32 caracteres. |
| `FLASK_ENV` | Recomendada | Usa `production` para activar validaciones de produccion. |
| `FLASK_DEBUG` | No | Activa el modo debug local; debe ser `false` en produccion. |
| `RESEND_API_KEY` | Si para contacto | Clave privada del SDK Resend. Nunca la publiques en el repositorio. |
| `RECIPIENT_EMAIL` | Si para contacto | Destinatario de las propuestas recibidas. |
| `PUBLIC_EMAIL` | No | Correo mostrado publicamente en el portafolio. |
| `CONTACT_SUBJECT_PREFIX` | No | Prefijo de los asuntos del formulario. |
| `CV_FILE_PATH` | No | Ruta del PDF del CV; por defecto `hoja de vida 2026a.pdf`. |
| `CV_DOWNLOAD_NAME` | No | Nombre del archivo al descargar el CV. |
| `LOG_LEVEL` | No | Nivel de logging, por defecto `INFO`. |

No publiques `.env`, claves Resend ni otras credenciales privadas. El archivo `.env.example` solo contiene valores de ejemplo.

## Despliegue en Render

El repositorio incluye `render.yaml` y `Procfile`. Render puede crear el servicio web a partir de esta configuracion:

1. Conecta el repositorio de GitHub en Render.
2. Selecciona la configuracion definida en `render.yaml` o crea un Web Service con entorno Python.
3. Usa `pip install -r requirements.txt` como comando de construccion.
4. Usa `gunicorn app:app` como comando de inicio.
5. Define en Render la variable secreta `RESEND_API_KEY`.
6. Verifica `SECRET_KEY`, `RECIPIENT_EMAIL`, `PUBLIC_EMAIL` y `CV_FILE_PATH`.

`render.yaml` genera automaticamente `SECRET_KEY`, configura Gunicorn y establece los valores publicos no secretos. `RESEND_API_KEY` debe añadirse como variable secreta en Render.

Para despliegues con varios workers o reinicios, configura un almacenamiento persistente para Flask-Limiter, como Redis, en lugar del almacenamiento en memoria predeterminado.

## Rutas HTTP

- `/`: portafolio y perfil profesional.
- `/contact`: recepcion de propuestas mediante `POST`.
- `/cv/view`: visualizacion del PDF del CV en el navegador.
- `/cv/download`: descarga del PDF del CV.
- `/cv/print`: version HTML del CV preparada para imprimir o exportar a PDF.

## Demo

No hay una URL publica de demostracion definida actualmente en la configuracion del proyecto. Cuando el servicio de Render este publicado, añade aqui su URL, por ejemplo: `https://tu-servicio.onrender.com`.

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE).

## Autor

**Euler Arturo Chapid Inagan**
