# AI Research Agents — laboratorio abierto de investigación en IA, basado en pruebas

**Nuestra misión:** crear herramientas de investigación de código que verifiquen de forma reproducible las modificaciones propuestas por modelos de IA de pesos abiertos, aprovechando recursos gratuitos cuando sea posible.

**Estado actual:** prototipo experimental; no es un servicio comercial ni un agente capaz de corregir cualquier programa por sí solo. Tiene siete etapas coordinadas, pero **no son siete modelos inteligentes independientes**.

## Qué hemos demostrado
- Análisis estático limitado de Python y algunas dependencias.
- Resúmenes depurados de investigación entre ejecuciones de GitHub.
- Inferencia real con modelos Qwen y Ollama sin una clave API de pago.
- Una corrección en código real escrita por Qwen2.5-Coder 1.5B para rechazar URLs falsas de GitHub. Superó las pruebas y el propietario la incorporó después de revisarla en el [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17).
- Un conjunto pequeño de pruebas **sintéticas** reproducibles, que no demuestra precisión general en proyectos desconocidos.

## Cómo probarlo
En GitHub, abre **Actions → Research Lab - Persistent Missions → Run workflow**. No incluyas contraseñas ni información privada. Para ejecutar un modelo local abierto, elige **Zero-Key Local Qwen Research**. Consulta [QUICKSTART.md](QUICKSTART.md).

## Participación
Consulta [CONTRIBUTING](CONTRIBUTING.md), [ROADMAP](ROADMAP.md), [SECURITY](SECURITY.md), [GOVERNANCE](GOVERNANCE.md) y [alcance y limitaciones](docs/PROJECT_SCOPE.md). Agradecemos experimentos reproducibles, informes de errores y críticas fundamentadas.

## Licencia y derechos
El código del proyecto se distribuye bajo [Apache License 2.0](LICENSE), aprobada por el propietario en octubre de 2026. Permite modificar, redistribuir y utilizar comercialmente el código respetando sus condiciones; **no concede exclusividad comercial sobre el código abierto**. Los autores conservan los derechos de autor de sus propias contribuciones. Véanse [NOTICE](NOTICE), [marcas](TRADEMARKS.md) y [derechos y condiciones](docs/LICENSING_DECISION.md). Las dependencias externas conservan sus propias licencias.

**Principio:** ninguna capacidad de IA se declarará probada sin evidencia y pruebas reproducibles.

Idiomas: [English](README.md) · [العربية](README.ar.md) · [Português](README.pt-BR.md) · [中文](README.zh-CN.md).
