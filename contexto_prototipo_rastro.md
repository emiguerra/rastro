# rastro — Contexto completo del prototipo técnico

Este documento existe para que no tengas que recordar todo de memoria. Si en algún momento te pierdes, vuelve aquí.

---

## 1. Qué estamos construyendo, en una frase

Un visitante habla (1 sola persona, 1 solo canal de audio). Ese audio se transcribe con Amazon Transcribe, el texto se analiza con Amazon Comprehend, y el resultado (una de 4 categorías de sentimiento) se muestra como output — por ahora en texto plano en la terminal, más adelante como luz.

## 2. Decisiones ya tomadas — no las vuelvas a discutir, solo ejecútalas

- **1 usuario, 1 canal de audio (mono).** No es una conversación entre 2 personas. Esto ya no cambia.
- **Hardware:** Shure SM57 (micrófono dinámico, cardioide) conectado a un Arturia MiniFuse 2 OTG (interfaz de audio USB-C con 2 entradas — usas solo 1).
- **Software:** Amazon Transcribe **estándar** (no Call Analytics — eso se descartó hace varias vueltas) + Amazon Comprehend (`BatchDetectSentiment`).
- **Por qué Comprehend y no Call Analytics:** Call Analytics exige 2 canales con roles AGENT/CUSTOMER, lo cual no aplica a 1 solo visitante. Comprehend + Transcribe estándar no tienen esa restricción.
- **Enfoque crítico (para la tesis/presentación):** Comprehend fuerza cualquier estado afectivo humano, sin importar cuán matizado sea, dentro de exactamente 4 categorías fijas (Positive / Negative / Neutral / Mixed). El argumento no es "el clasificador se equivoca" — es que la taxonomía misma es una imposición arbitraria, tratada como si fuera un hecho objetivo.
- **Cuenta AWS:** ya creada, plan de pago (no el plan gratuito), soporte Básico (gratis).
- **La tesis (documento escrito) ya fue entregada** (miércoles 8 de julio). No se edita más. Todo lo que queda es prototipo + presentación.
- **Para la presentación del 20 de julio, no olvidar:**
  - Antes de mostrar el prototipo en vivo, incluir un segmento que explique que la vigilancia de la demo es deliberadamente visible/consentida (no oculta) — esto resuelve la tensión con el argumento sobre invisibilidad.
  - Incluir la frase: *"esto que ven no es solo el resultado de una API, es la arquitectura del argumento — la conversación entera fue forzada a caber en una sola caja."*

## 3. Checklist de AWS — marca lo que ya tengas hecho

- [ ] Cuenta AWS creada (plan de pago)
- [ ] Usuario IAM creado (no la cuenta root) con permisos: `AmazonS3FullAccess`, `AmazonTranscribeFullAccess`, `ComprehendFullAccess`
- [ ] Access Key ID + Secret Access Key generadas y guardadas en un lugar seguro
- [ ] AWS CLI instalado en la Mac (`brew install awscli`)
- [ ] `aws configure` corrido con esas credenciales
- [ ] Verificado con `aws sts get-caller-identity` (debe mostrar tu usuario, no "root")
- [ ] Bucket S3 creado

## 4. Pasos detallados, en orden — no te saltes ninguno

### Paso 1 — Crear usuario IAM (si no está hecho)
1. Ve a console.aws.amazon.com, busca "IAM" en la barra superior.
2. Panel izquierdo → **Users** → **Create user**.
3. Nombre: `rastro-prototipo` (o el que quieras).
4. En permisos, elige **Attach policies directly**.
5. Marca: `AmazonS3FullAccess`, `AmazonTranscribeFullAccess`, `ComprehendFullAccess`.
6. Crea el usuario → entra a él → **Security credentials** → **Access keys** → **Create access key**.
7. Elige **Command Line Interface (CLI)** como caso de uso.
8. Guarda el Access Key ID y el Secret Access Key ahora mismo (el secreto se muestra una sola vez).

### Paso 2 — Instalar el AWS CLI en tu Mac
En Terminal:
```
brew install awscli
```
Verifica:
```
aws --version
```

### Paso 3 — Configurar las credenciales
```
aws configure
```
Te va a preguntar, uno por uno (presiona Enter después de cada respuesta):
- `AWS Access Key ID`: pega el que guardaste en el Paso 1.
- `AWS Secret Access Key`: pégalo (no vas a ver los caracteres al escribir/pegar — es normal).
- `Default region name`: escribe `us-east-1`.
- `Default output format`: escribe `json`.

No aparece ningún mensaje de éxito — simplemente vuelve a la línea de comandos. Por dentro, guardó las credenciales en un archivo oculto (`~/.aws/credentials`).

### Paso 4 — Verificar que quedó bien configurado
```
aws sts get-caller-identity
```
Debería devolver algo como:
```json
{
    "UserId": "...",
    "Account": "...",
    "Arn": "arn:aws:iam::123456789012:user/rastro-prototipo"
}
```
Si el `Arn` muestra tu usuario (`rastro-prototipo`), está listo. Si da error, copia el mensaje exacto y lo resolvemos.

### Paso 5 — Crear el bucket S3
```
aws s3 mb s3://rastro-prototipo-emiliano --region us-east-1
```
Si dice "bucket already exists" (el nombre debe ser único en todo AWS, no solo en tu cuenta), cámbialo por algo más específico.

### Paso 6 — Conectar el hardware
1. Conecta el MiniFuse 2 a la Mac por USB-C.
2. Verifica en Preferencias del Sistema → Sonido que aparece como dispositivo de entrada.
3. Conecta el SM57 a la **entrada 1** (XLR) del MiniFuse 2.
4. En el MiniFuse 2: Phantom power **apagado**, switch Hi-Z **apagado** (el SM57 es dinámico, no necesita ninguno de los dos).

### Paso 7 — Grabar un clip de prueba
1. Abre QuickTime Player → Archivo → Nueva grabación de audio.
2. Elige el MiniFuse 2 como fuente de entrada (flechita al lado del botón de grabar).
3. Graba ~20-30 segundos hablando algo simple.
4. Revisa que no se sature (el nivel no debe llegar al rojo) y que se escuche claro al reproducirlo.
5. Guarda el archivo, por ejemplo como `clip_prueba.wav` (Archivo → Exportar como → Audio only, si QuickTime lo guarda como .m4a, conviértelo a .wav con `ffmpeg -i clip_prueba.m4a clip_prueba.wav`).

### Paso 8 — Correr el pipeline
Usa el archivo `rastro_pipeline.py` (el otro archivo que te generé).
1. Instala boto3 si no lo tienes: `pip3 install boto3`
2. Abre `rastro_pipeline.py` y cambia:
   - `BUCKET` por el nombre real de tu bucket (Paso 5).
   - `LOCAL_AUDIO_FILE` por la ruta de tu `clip_prueba.wav` (Paso 7).
3. Corre:
   ```
   python3 rastro_pipeline.py
   ```
4. Debería imprimir la transcripción completa, cuántos fragmentos se generaron, y una categoría de sentimiento final.

## 5. Qué sigue después de que esto funcione

- Repetir la prueba con una grabación más larga (varios minutos) para confirmar que el fragmentado por el límite de 5 KB de Comprehend realmente se activa y funciona bien.
- Solo después de que el pipeline de software funcione sin errores, pasar a diseñar el output físico (la luz). No antes — si el software falla, el diseño de la luz es tiempo perdido.

## 6. Si algo falla

Copia el mensaje de error exacto (completo, no resumido) y pregúntame. No asumas qué significa ni intentes adivinar la solución — en este pipeline hay varios puntos donde un error de un paso anterior se manifiesta como un error distinto más adelante (ej. un problema de credenciales puede aparecer como un error de permisos en Transcribe).
