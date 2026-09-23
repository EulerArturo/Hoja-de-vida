"""Aplicacion Flask para el portafolio profesional y formulario de contacto.

El modulo configura Flask-Mail y Flask-Limiter, registra las rutas publicas y
expone las vistas del portafolio, el formulario de contacto y el CV.
"""

import logging
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, send_file, url_for
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from data.profile import PROFILE


load_dotenv()

mail = Mail()
limiter = Limiter(key_func=get_remote_address, default_limits=[])
logger = logging.getLogger(__name__)


NAME_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s.'-]{3,80}$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DEFAULT_SECRET_KEY = "change-this-secret"


def profile_context() -> dict:
    """Construye el contexto publico utilizado por las plantillas.

    Returns:
        dict: Copia superficial de ``PROFILE`` con el correo publico
            sobrescrito por ``PUBLIC_EMAIL`` cuando esta definido.
    """

    profile = dict(PROFILE)
    profile["email"] = os.getenv("PUBLIC_EMAIL", PROFILE["email"])
    return profile


def is_secure_secret_key(secret_key: str | None) -> bool:
    """Comprueba si una clave de Flask cumple los requisitos de produccion.

    Args:
        secret_key: Valor candidato configurado para ``SECRET_KEY``.

    Returns:
        bool: ``True`` cuando la clave tiene longitud suficiente y no es un
            valor conocido de reemplazo; en caso contrario, ``False``.
    """

    if not secret_key:
        return False

    candidate = secret_key.strip()
    if candidate == DEFAULT_SECRET_KEY:
        return False

    if len(candidate) < 32:
        return False

    if candidate.lower() in {"changeme", "change-me", "secret", "secret-key", "replace-me", "replace_with_a_long_random_secret"}:
        return False

    return True


def create_app() -> Flask:
    """Crea y configura la instancia Flask de la aplicacion.

    Returns:
        Flask: Aplicacion configurada con extensiones, rutas y manejadores.

    Raises:
        RuntimeError: Si el entorno es produccion y ``SECRET_KEY`` no es
            suficientemente segura.
        ValueError: Si una variable numerica de configuracion SMTP no es valida.
    """

    app = Flask(__name__)
    secret_key = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
    is_production = os.getenv("FLASK_ENV", "").strip().lower() == "production"

    if is_production and not is_secure_secret_key(secret_key):
        raise RuntimeError(
            "SECRET_KEY insegura o ausente en produccion. Define una clave aleatoria de al menos 32 caracteres antes de iniciar la aplicacion."
        )

    app.config.update(
        SECRET_KEY=secret_key,
        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "true").lower() == "true",
        MAIL_USE_SSL=os.getenv("MAIL_USE_SSL", "false").lower() == "true",
        MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME", "")),
        MAIL_SUPPRESS_SEND=os.getenv("MAIL_SUPPRESS_SEND", "false").lower() == "true",
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )

    mail.init_app(app)
    limiter.init_app(app)
    configure_logging(app)
    register_routes(app)
    register_error_handlers(app)

    @app.after_request
    def set_security_headers(response):
        """Añade cabeceras de seguridad a cada respuesta HTTP.

        Args:
            response: Respuesta Flask que se enviara al cliente.

        Returns:
            Response: La misma respuesta con las cabeceras aplicadas.
        """
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.tailwindcss.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self';"
        )
        return response

    return app


def configure_logging(app: Flask) -> None:
    """Configura el nivel y formato de logging de la aplicacion.

    Args:
        app: Instancia Flask cuyo logger se configurara.

    Returns:
        None: La configuracion se aplica directamente sobre ``app``.
    """

    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    app.logger.setLevel(level)


def validate_contact_payload(payload: dict) -> dict:
    """Valida y normaliza los datos recibidos desde el formulario.

    Args:
        payload: Diccionario con los campos enviados por formulario o JSON.

    Returns:
        dict: Diccionario con ``errors`` y los datos normalizados en ``clean``.
            Los errores se indexan por nombre de campo.
    """

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    subject = (payload.get("subject") or "").strip()
    message = (payload.get("message") or "").strip()
    company = (payload.get("company") or "").strip()
    honeypot = (payload.get("website") or "").strip()

    errors = {}

    if not NAME_REGEX.match(name):
        errors["name"] = "Ingresa un nombre valido (3-80 caracteres)."

    if not EMAIL_REGEX.match(email) or len(email) > 120:
        errors["email"] = "Ingresa un correo electronico valido."

    if subject and len(subject) > 120:
        errors["subject"] = "El asunto no puede superar 120 caracteres."

    if len(message) < 30 or len(message) > 2000:
        errors["message"] = "El mensaje debe tener entre 30 y 2000 caracteres."

    if company and len(company) > 80:
        errors["company"] = "El nombre de la empresa es demasiado largo."

    if honeypot:
        errors["website"] = "Solicitud bloqueada."

    return {
        "errors": errors,
        "clean": {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "company": company,
        },
    }


def mail_configuration_error(app: Flask) -> str | None:
    """Detecta si faltan credenciales necesarias para SMTP.

    Args:
        app: Instancia Flask con la configuracion de correo cargada.

    Returns:
        str | None: Mensaje descriptivo cuando faltan credenciales; ``None``
            si el servicio esta configurado o los envios estan suprimidos.
    """

    if app.config.get("MAIL_SUPPRESS_SEND"):
        return None

    missing = [
        setting
        for setting in ("MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_DEFAULT_SENDER")
        if not app.config.get(setting)
    ]
    if missing:
        return "El servicio de correo no esta configurado. Define las credenciales SMTP en el archivo .env."

    return None


def register_routes(app: Flask) -> None:
    """Registra las rutas publicas, de contacto y de descarga del CV.

    Args:
        app: Instancia Flask donde se registraran las rutas.

    Returns:
        None: Las funciones de vista quedan registradas como efectos secundarios.
    """

    @app.get("/")
    def index():
        """Renderiza la pagina principal con el perfil profesional.

        Returns:
            str: HTML renderizado de la pagina principal.
        """

        return render_template("index.html", profile=profile_context())

    @app.post("/contact")
    @limiter.limit("5 per hour; 1 per minute")
    def contact():
        """Valida una propuesta y la envia al destinatario configurado.

        Returns:
            Response: JSON con el resultado para clientes API o redireccion al
                formulario para solicitudes HTML.

        Raises:
            SMTPException: La excepcion del transporte se captura y se traduce
                en una respuesta controlada de servicio no disponible.
        """

        payload = request.get_json(silent=True) if request.is_json else request.form.to_dict()
        payload = payload or {}

        result = validate_contact_payload(payload)
        errors = result["errors"]
        data = result["clean"]

        if errors:
            if request.is_json:
                return jsonify({"ok": False, "errors": errors}), 400
            for msg in errors.values():
                flash(msg, "error")
            return redirect(url_for("index") + "#contact")

        recipient = os.getenv("RECIPIENT_EMAIL", "euler.chapid.it@gmail.com")
        prefix = os.getenv("CONTACT_SUBJECT_PREFIX", "[CV Web]")
        subject = data["subject"] or "Nueva propuesta profesional"

        configuration_error = mail_configuration_error(app)
        if configuration_error:
            if request.is_json:
                return jsonify({"ok": False, "message": configuration_error}), 503
            flash(configuration_error, "error")
            return redirect(url_for("index") + "#contact")

        body = (
            "Nueva solicitud desde tu Hoja de Vida web\n\n"
            f"Nombre: {data['name']}\n"
            f"Correo: {data['email']}\n"
            f"Empresa: {data['company'] or 'No especificada'}\n"
            f"Asunto: {subject}\n\n"
            "Mensaje:\n"
            f"{data['message']}\n"
        )

        try:
            msg = Message(
                subject=f"{prefix} {subject}",
                recipients=[recipient],
                body=body,
                reply_to=data["email"],
            )
            mail.send(msg)
        except Exception as exc:  # pragma: no cover
            logger.exception("Error enviando correo de contacto: %s", exc)
            if request.is_json:
                return jsonify({"ok": False, "message": "No se pudo enviar el mensaje en este momento. Revisa la configuracion SMTP."}), 503
            flash("No se pudo enviar el mensaje. Revisa la configuracion SMTP e intenta nuevamente.", "error")
            return redirect(url_for("index") + "#contact")

        if request.is_json:
            return jsonify({"ok": True, "message": "Mensaje enviado correctamente."}), 200

        flash("Mensaje enviado. Te respondere lo antes posible.", "success")
        return redirect(url_for("index") + "#contact")

    @app.get("/cv/view")
    def view_cv():
        """Muestra el archivo PDF del CV en el navegador.

        Returns:
            Response: Archivo PDF servido inline.

        Raises:
            NotFound: Si el archivo PDF configurado no existe.
        """

        cv_path = resolve_cv_path()
        if not cv_path.exists():
            abort(404, description="No se encontro el archivo CV en el servidor.")
        return send_file(cv_path, mimetype="application/pdf", as_attachment=False)

    @app.get("/cv/print")
    def print_cv():
        """Renderiza una version ligera del CV preparada para imprimir.

        Returns:
            str: HTML del CV con estilos optimizados para papel A4.
        """

        return render_template("cv_print.html", profile=profile_context())

    @app.get("/cv/download")
    def download_cv():
        """Descarga el CV con el nombre definido en la configuracion.

        Returns:
            Response: Archivo PDF servido como descarga.

        Raises:
            NotFound: Si el archivo PDF configurado no existe.
        """

        cv_path = resolve_cv_path()
        if not cv_path.exists():
            abort(404, description="No se encontro el archivo CV en el servidor.")
        return send_file(
            cv_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=os.getenv("CV_DOWNLOAD_NAME", "Euler_Arturo_Chapid_Inagan_CV.pdf"),
        )


def resolve_cv_path() -> Path:
    """Resuelve la ruta absoluta del PDF configurado para el CV.

    Returns:
        Path: Ruta expandida y absoluta al archivo PDF configurado.
    """

    configured = os.getenv("CV_FILE_PATH", "hoja de vida 2026a.pdf")
    return Path(configured).expanduser().resolve()


def register_error_handlers(app: Flask) -> None:
    """Registra respuestas controladas para errores HTTP comunes.

    Args:
        app: Instancia Flask donde se registraran los manejadores.

    Returns:
        None: Los manejadores quedan asociados a la aplicacion.
    """

    @app.errorhandler(429)
    def too_many_requests(error):
        """Responde al exceso de solicitudes segun el tipo de cliente.

        Args:
            error: Excepcion HTTP generada por Flask-Limiter.

        Returns:
            Response: JSON para clientes API o redireccion al formulario.
        """

        message = "Has superado el limite de intentos permitidos. Espera un momento e intenta nuevamente mas tarde."

        if request.is_json or request.accept_mimetypes.best == "application/json":
            return jsonify({"ok": False, "message": message}), 429

        flash(message, "error")
        return redirect(url_for("index") + "#contact")

    @app.errorhandler(404)
    def not_found(error):
        """Renderiza la pagina principal para recursos inexistentes.

        Args:
            error: Excepcion HTTP 404 generada por Flask.

        Returns:
            tuple: HTML renderizado junto con el estado HTTP 404.
        """

        profile = profile_context()
        profile["focus"] = ""
        return render_template("index.html", profile=profile, error_message=str(error)), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Registra y presenta una respuesta controlada para errores internos.

        Args:
            error: Excepcion HTTP 500 generada por Flask.

        Returns:
            tuple: HTML renderizado junto con el estado HTTP 500.
        """

        logger.exception("Error interno no controlado: %s", error)
        profile = profile_context()
        profile["focus"] = ""
        return render_template("index.html", profile=profile, error_message="Ocurrio un error interno inesperado."), 500


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
