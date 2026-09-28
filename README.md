# rastro

Repositorio general del proyecto de tesis **rastro** — instalación interactiva
sobre vigilancia algorítmica y "resignación informada": el visitante sabe que
es vigilado/extraído de datos en la vida cotidiana, pero nunca lo ha sentido
en el cuerpo. rastro busca activar esa sensación de forma retroactiva.

## Arquitectura vigente (semestre 2)

Una sola estación con 4 fases (umbral → datos ajenos → transición → expediente)
que traduce gestualidad y patrones corporales del visitante en proyección por
capas. El diseño completo — hardware, materialidad, sistema de proyección,
modelo de clasificación propio, riesgos y guion de presentación — está
documentado en [`v01-rastro`](https://github.com/emiguerra/esp32Rastro/blob/main/v01-rastro),
dentro del repo del firmware.

| Componente | Repo | Estado |
| --- | --- | --- |
| 4× nodos de captura (XIAO ESP32S3 Sense) — gestualidad/patrones corporales | [esp32Rastro](https://github.com/emiguerra/esp32Rastro) | Firmware en desarrollo |
| Raspberry Pi "cerebro" (clasificación + estado de fase) | _pendiente de crear_ | No iniciado |
| Raspberry Pi × 2 de proyección (una por proyector) | _pendiente de crear_ | No iniciado |
| Raspberry Pi de redundancia caliente | _pendiente de crear_ | No iniciado |

Cronograma de avance: ver [`cronograma.md`](cronograma.md).

## Historial

La arquitectura anterior del proyecto (Entregable 1: captación de voz vía Web
Speech API + BERT, y rostro vía ml5.faceMesh, en 3 tramos) quedó abandonada
tras un pivote de diseño. Ese trabajo se conserva archivado en
[emiguerra/rastro-entregable-1](https://github.com/emiguerra/rastro-entregable-1).
