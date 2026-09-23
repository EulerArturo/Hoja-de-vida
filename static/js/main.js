const form = document.getElementById('contactForm');
const feedback = document.getElementById('formFeedback');

/**
 * Valida los campos obligatorios del formulario antes del envio.
 *
 * @returns {string} Mensaje de validacion o una cadena vacia cuando los datos
 * son validos.
 */
function validateClientForm() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

    if (name.length < 3) {
        return 'El nombre debe tener al menos 3 caracteres.';
    }
    if (!emailPattern.test(email)) {
        return 'Ingresa un correo electronico valido.';
    }
    if (message.length < 30) {
        return 'El mensaje debe tener minimo 30 caracteres.';
    }
    return '';
}

/**
 * Procesa el envio del formulario de contacto en el navegador.
 *
 * @param {SubmitEvent} event Evento submit emitido por el formulario.
 * @returns {void}
 */
function handleContactSubmit(event) {
    const error = validateClientForm();
    if (error) {
        event.preventDefault();
        if (feedback) {
            feedback.textContent = error;
        }
        return;
    }
    if (feedback) {
        feedback.textContent = '';
    }
}

if (form) {
    form.addEventListener('submit', handleContactSubmit);
}

/**
 * Hace visibles los elementos cuando entran en el viewport.
 *
 * @param {IntersectionObserverEntry[]} entries Elementos observados y su
 * estado de interseccion.
 * @returns {void}
 */
function handleRevealIntersections(entries) {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}

const observer = new IntersectionObserver((entries) => {
    handleRevealIntersections(entries);
}, { threshold: 0.2 });

document.querySelectorAll('.animate-block, .timeline-item, .skill-card, .glass-card').forEach((el) => observer.observe(el));

const sceneTransition = document.getElementById('sceneTransition');
const panels = document.querySelectorAll('.section-panel');
let activeScene = '';

/**
 * Activa la escena visual asociada a una seccion del portafolio.
 *
 * @param {string} sceneName Identificador de la escena visual.
 * @param {Element|null} panel Panel que debe quedar activo.
 * @returns {void}
 */
function triggerScene(sceneName, panel) {
    if (!sceneName || sceneName === activeScene) return;
    activeScene = sceneName;
    document.body.dataset.scene = sceneName;

    if (sceneTransition) {
        sceneTransition.classList.remove('play');
        void sceneTransition.offsetWidth;
        sceneTransition.classList.add('play');
    }

    panels.forEach((item) => item.classList.remove('is-active'));
    if (panel) panel.classList.add('is-active');
}

/**
 * Selecciona la seccion mas visible y actualiza la escena activa.
 *
 * @param {IntersectionObserverEntry[]} entries Secciones observadas y sus
 * proporciones visibles.
 * @returns {void}
 */
function handleSceneIntersections(entries) {
    entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)
        .slice(0, 1)
        .forEach((entry) => triggerScene(entry.target.dataset.scene, entry.target));
}

const sceneObserver = new IntersectionObserver((entries) => {
    handleSceneIntersections(entries);
}, { threshold: [0.2, 0.35, 0.55], rootMargin: '-10% 0px -30% 0px' });

panels.forEach((panel) => sceneObserver.observe(panel));
if (panels.length) {
    triggerScene(panels[0].dataset.scene, panels[0]);
}

const copyButton = document.getElementById('copyBtn');

if (copyButton) {
    copyButton.addEventListener('click', copyEmail);
}

/**
 * Copia el correo publico en el portapapeles y actualiza temporalmente el
 * estado visual del boton.
 *
 * @returns {void}
 */
function copyEmail() {
    const email = document.getElementById('emailText')?.innerText;

    if (!email || !navigator.clipboard) {
        return;
    }

    navigator.clipboard.writeText(email).then(() => {
        copyButton.innerText = "¡Copiado!";
        copyButton.classList.add('text-emerald-400', 'border-emerald-500/50');
        setTimeout(() => {
            copyButton.innerText = '[Copiar]';
            copyButton.classList.remove('text-emerald-400', 'border-emerald-500/50');
        }, 2000);
    }).catch((error) => {
        console.error('Error al copiar correo:', error);
    });
}