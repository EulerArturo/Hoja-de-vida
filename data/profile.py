"""Datos publicos del perfil profesional mostrados por la aplicacion.

``PROFILE`` es la fuente de datos compartida por las vistas del portafolio y
del CV imprimible. Sus listas agrupan informacion profesional, habilidades,
experiencias y proyectos sin introducir persistencia en base de datos.
"""

PROFILE = {
    "name": "Euler Arturo Chapid Inagan",
    "title": "Tecnólogo en Gestión de Redes de Datos",
    "focus": "Analista de Datos y Automatización orientado a optimizar procesos, integrar fuentes de información y desarrollar herramientas dinámicas. Trabajo con Python y Pandas, SQL/MySQL, Excel Avanzado, scripts de automatización, CommCare y flujos con Power Automate y Power Apps.",
    "email": "euler.chapid.it@gmail.com",
    "location": "Ipiales, Nariño, Colombia",
    "telefono": "+57 300 136 0549",
    "residencia": "Disponible para cambio de residencia",
    "availability_status": True,
    "availability_text": "Disponible para vacantes IT y proyectos de automatización",
    "summary_bullets": [
        "Soporte IT N1/N2 y gestión documentada de incidentes.",
        "Administración de redes Cisco, VPN y Winbox/MikroTik.",
        "Automatización de procesos y análisis de datos con Python y Pandas.",
        "Desarrollo de herramientas dinámicas con Google Apps Script (GAS), Drive y Sheets API.",
    ],
    "hero_badges": ["Desarrollo Web", "Python & ETL", "SQL & Datos", "Power Platform"],
    "skills": [
        {
            "category": "Datos & Cloud",
            "items": [
                "SQL / MySQL",
                "Python (Pandas / ETL)",
                "Excel Avanzado",
                "Azure Data Factory",
            ],
        },
        {
            "category": "Automatización & Low-Code",
            "items": [
                "Power Automate",
                "Power Apps",
                "CommCare",
                "Google Apps Script",
            ],
        },
        {
            "category": "Desarrollo & Infraestructura",
            "items": [
                "PHP",
                "JavaScript (ES6+)",
                "Flask",
                "Redes Cisco",
                "Winbox / MikroTik",
                "VPNs",
            ],
        },
    ],
    "experiences": [
        {
            "company": "Fundación Conexión Salud",
            "role": "Tecnólogo en Redes / Soporte Técnico",
            "period": "Sep 2025 – Actualidad",
            "achievements": [
                "Diseño y automatización de flujos de captura y seguimiento de información operativa mediante CommCare y herramientas de integración de datos.",
                "Desarrollo de scripts en Python para extracción, transformación y validación de datos, reduciendo tareas manuales y mejorando la trazabilidad.",
                "Optimización de consultas SQL y estructuras de información para reportes, control de integridad y acceso confiable a datos operativos.",
                "Implementación de flujos con Power Automate y Power Apps para conectar formularios, responsables, notificaciones y registros institucionales.",
                "Administración de sistemas y soporte N1/N2 con enfoque en continuidad, calidad de datos y resolución documentada de incidentes."
            ]
        },
        {
            "company": "SOLINDTEC",
            "role": "Técnico de Mantenimiento",
            "period": "Oct 2021 – Jun 2022",
            "achievements": [
                "Estandarización de procesos operativos y automatización de controles para mejorar la consistencia y trazabilidad de la información.",
                "Desarrollo de scripts y consultas para consolidar datos de operación, generar reportes y apoyar la toma de decisiones.",
                "Gestión de procesos de alta precisión con controles de calidad, validación de registros e integridad de la información."
            ]
        },
        {
            "company": "L'Oréal Colombia",
            "role": "Aprendiz Auxiliar de TI",
            "period": "Abr 2020 – Oct 2020",
            "achievements": [
                "Construcción de informes técnicos y consolidación de datos de activos de TI para facilitar análisis, seguimiento y control de inventario.",
                "Participación en el despliegue de la imagen corporativa 'Modern Bill', coordinando información, validaciones y cumplimiento de tiempos.",
                "Documentación de procedimientos y controles de integridad para mejorar la confiabilidad de los datos de soporte."
            ]
        }
    ],
    "projects": [
        {
            "title": "Google Sheets Active Assets Mapping Tool",
            "tech": "Google Apps Script · JavaScript · Google Drive API · Google Sheets API",
            "description": "Herramienta web para el mapeo, registro y trazabilidad de activos de hardware en tiempo real. Integra control de concurrencia (LockService), generación de hojas de vida técnicas, control de responsables de equipos y módulo de carga e inspección de evidencias multimedia en Google Drive.",
            "link": "https://github.com/EulerArturo/Google-Sheets-Active-Assets-Mapping-Tool"
        },
        {
            "title": "Sistema de Control y Hojas de Vida de Equipos de Cómputo",
            "tech": "Google Apps Script · JavaScript · Google Drive API · HTML5 · CSS3",
            "description": "Plataforma web para la creación, consulta y actualización de hojas de vida técnicas de activos de cómputo. Incluye registro de componentes de hardware, asignación de responsables, gestión de estados operativos y vinculación automática de documentación técnica en Google Drive.",
            "link": "https://github.com/EulerArturo/Hoja_de_vida_pcs"
        },
        {
            "title": "Sistema de Gestión de Órdenes Ópticas",
            "tech": "Google Apps Script · JS ES6+ · Google Sheets API · HTML5 · CSS3",
            "description": "Aplicación web integral para digitalizar, registrar y controlar órdenes en laboratorios ópticos. Incluye arquitectura modular en JavaScript, persistencia en Google Sheets API, validación de datos y automatización del flujo de trabajo.",
            "link": "https://github.com/EulerArturo/Sistema-de-Gesti-n-de-rdenes-pticas-Google-Apps-Script-JS-ES6-Google-Sheets-API-HTML5-CSS3"
        },
        {
            "title": "Sistema de Generación de Certificados RIPS",
            "tech": "Google Apps Script · JavaScript · Google Docs API · Google Sheets API · PDF Generation",
            "description": "Herramienta automatizada para la extracción de datos asistenciales, procesamiento de registros RIPS y generación dinámica de certificados médicos en PDF. Optimiza la plantilla mediante tags personalizados e integra envío automático o almacenamiento centralizado en Google Drive.",
            "link": "https://github.com/EulerArturo/Sistema-de-Generaci-n-de-Certificados-rips-en-Google-Apps-Script"
        },
    ],
    "automation_achievements": [
        "Desarrollo de lógica en Google Apps Script (GAS) para la gestión segura de transacciones y asignación secuencial de folios/IDs mediante LockService.",
        "Implementación de módulos de captura y seguimiento de responsables, equipos y actas mediante formularios, CommCare y flujos automatizados.",
        "Creación de visor y gestor de evidencias técnicas con integración directa a Google Drive SDK y controles de integridad.",
        "Orquestación de procesos de integración y transformación de datos mediante SQL, Python, Power Automate y Azure Data Factory."
    ]
}