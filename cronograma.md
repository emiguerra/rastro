# Cronograma de avance — rastro (segundo semestre 2026)

Última actualización: 28 de septiembre de 2026. Grupo 2.

Este cronograma combina el calendario institucional oficial (extraído de `Plan de trabajo 2026 - Emilia.pdf`) con el plan técnico de trabajo pendiente documentado en [`v01-rastro`](https://github.com/emiguerra/esp32Rastro/blob/main/v01-rastro) del repo de firmware.

## Calendario institucional oficial

17 semanas, del 2 de septiembre al 16 de diciembre de 2026. Las entregas quincenales alternan entre Grupo 1 y Grupo 2; los hitos de fin de semestre son compartidos por ambos grupos. La semana del 21 de octubre aparece dos veces porque a esa entrega asisten ambos grupos juntos.

| Semana | Fecha | Hito | Grupo |
| --- | --- | --- | --- |
| 1 | 2 sep | Entrega G1 | G1 |
| 2 | 9 sep | Entrega G2 | **G2** |
| 3 | 16 sep | Receso (Fiestas Patrias) | — |
| 4 | 23 sep | Entrega G1 | G1 |
| 5 | 30 sep | Corrección Cruzada | ambos |
| 6 | 7 oct | Entrega G2 | **G2** |
| 7 | 14 oct | Entrega G1 | G1 |
| 8 – 9 | 21 oct | Entrega G1 + G2 (sesión conjunta) | **ambos** |
| 10 | 28 oct | Entrega G2 | **G2** |
| 11 | 4 nov | Memoria Final Grupo 1 | G1 |
| 12 | 11 nov | **Memoria Final Grupo 2** | **G2** |
| 13 | 18 nov | Entrega Pase G1 | G1 |
| 14 | 25 nov | **Entrega Pase G2** | **G2** |
| 15 | 2 dic | **Entrega Memoria a Comisión** | ambos |
| 16 | 9 dic | **Ensayo General** | ambos |
| 17 | 16 dic | **Semana de Exámenes** | ambos |

Tarea institucional a revisar: **T-02** ("Planta y sección del pasillo con los 3 tramos, proyecciones y puntos de captación") describe la arquitectura anterior de 3 tramos, abandonada tras el pivote documentado en `v01-rastro`. Al entregarla, reinterpretar como planta/sección del módulo único de 4 fases.

## Cronograma técnico (Grupo 2)

Planificado hacia atrás desde Ensayo General (9 dic), con una semana de margen antes de las entregas finales, tal como se pidió (la semana previa a la Entrega a Comisión queda reservada solo para resolver imprevistos, no para features nuevas).

| Semana | Foco técnico |
| --- | --- |
| 28 sep – 4 oct | Agendar y realizar la visita a terreno (techo/anclajes, columnas, tomas eléctricas y de red, luz base). Comprar 1–2 unidades XIAO ESP32S3 Sense adicionales (repuesto + prueba de modificación IR-cut). |
| 5 – 11 oct | Probar captura en luz baja en el espacio real (opción de luz tenue primero). Cerrar la estrategia final de luz. |
| 12 – 18 oct | Redactar la "ficha técnica de captura" (condiciones exactas de luz). Reclutar y agendar la sesión con los 20 voluntarios. |
| 19 – 25 oct | Capturar el dataset si ya está todo listo; si no, margen para cerrar lo de las 3 semanas anteriores (semana de la entrega conjunta G1+G2 del 21 oct). |
| 26 oct – 1 nov | Etiquetar el dataset. Entrenar la primera versión del modelo de clasificación propio; medir FPS real en la Raspberry Pi 5. |
| 2 – 8 nov | Medir sesgo del modelo por subgrupo. Preparar el contenido de la Memoria Final con la arquitectura y decisiones ya documentadas en `v01-rastro`. |
| 9 – 15 nov | **Memoria Final Grupo 2 (11 nov).** Prototipar la transición Fase 1→2 (crossfade por alpha blending). Avanzar el montaje físico de las capas (acrílico/scrim, estructura de aluminio) si el espacio ya está confirmado. |
| 16 – 22 nov | Integrar demo para el Pase: al menos 2 capas proyectando con datos ajenos (Fase 1) funcionando, Fase 2 en versión preliminar. |
| 23 – 29 nov | **Entrega Pase G2 (25 nov).** Aplicar correcciones/feedback recibido. Cerrar integración de las 4 fases. |
| 30 nov – 6 dic | **Semana de margen antes de la Entrega a Comisión** — solo arreglar imprevistos, no desarrollo nuevo. **Entrega Memoria a Comisión (2 dic)** con el estado real documentado (guion de presentación honesto, ver `v01-rastro`). |
| 7 – 13 dic | **Ensayo General (9 dic).** Ajustes finales post-ensayo. |
| 14 – 16 dic | **Semana de Exámenes** — defensa final. |

## Riesgo del cronograma

El tramo entre hoy (28 sep) y fines de octubre está muy apretado: visita a terreno, prueba de luz y captura del dataset de 20 voluntarios encadenados en ~4 semanas, cada paso dependiendo del anterior (ver regla de domain mismatch en `v01-rastro`). Si la visita a terreno se atrasa una semana, todo el resto se corre — conviene agendarla cuanto antes.
