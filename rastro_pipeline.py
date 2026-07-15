"""
rastro - pipeline de audio -> Transcribe -> Comprehend
Version de 1 solo canal (1 usuario), version final del prototipo.

CONFIGURA ESTO ANTES DE CORRER:
- Tener el AWS CLI configurado (aws configure) con el usuario IAM creado.
- Cambiar BUCKET por el nombre real de tu bucket S3.
- Cambiar LOCAL_AUDIO_FILE por la ruta de tu archivo .wav grabado con el SM57 + MiniFuse 2.
- Instalar boto3 si no lo tienes: pip3 install boto3

Correr con: python3 rastro_pipeline.py
"""

import boto3
import time
import json

# ---- CONFIGURACION ----
REGION = "us-east-1"
BUCKET = "rastro-prototipo-emiliano"        # <-- cambia esto por tu bucket real
LOCAL_AUDIO_FILE = "pruebaAudio01.wav"      # <-- cambia esto por tu archivo real
S3_KEY = "audio/pruebaAudio01.wav"
JOB_NAME = f"rastro-job-{int(time.time())}"  # nombre unico por corrida, no lo repitas
LANGUAGE_CODE_TRANSCRIBE = "es-US"          # prueba "es-ES" tambien si la precision no convence
LANGUAGE_CODE_COMPREHEND = "es"
MAX_CHUNK_BYTES = 4900                      # bajo el limite de 5 KB de Comprehend, con margen

s3 = boto3.client("s3", region_name=REGION)
transcribe = boto3.client("transcribe", region_name=REGION)
comprehend = boto3.client("comprehend", region_name=REGION)


def subir_audio():
    print(f"Subiendo {LOCAL_AUDIO_FILE} a s3://{BUCKET}/{S3_KEY} ...")
    s3.upload_file(LOCAL_AUDIO_FILE, BUCKET, S3_KEY)
    print("Listo.")


def iniciar_transcripcion():
    s3_uri = f"s3://{BUCKET}/{S3_KEY}"
    print(f"Iniciando job de Transcribe: {JOB_NAME}")
    transcribe.start_transcription_job(
        TranscriptionJobName=JOB_NAME,
        LanguageCode=LANGUAGE_CODE_TRANSCRIBE,
        MediaFormat="wav",
        Media={"MediaFileUri": s3_uri},
        OutputBucketName=BUCKET,
        OutputKey=f"transcripts/{JOB_NAME}.json",
    )


def esperar_transcripcion():
    print("Esperando a que termine el job (polling cada 5s)...")
    while True:
        resp = transcribe.get_transcription_job(TranscriptionJobName=JOB_NAME)
        status = resp["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            print("Job completado.")
            return
        elif status == "FAILED":
            reason = resp["TranscriptionJob"].get("FailureReason", "sin detalle")
            raise RuntimeError(f"El job de Transcribe fallo: {reason}")
        time.sleep(5)


def obtener_texto():
    print("Descargando y parseando la transcripcion desde S3...")
    transcript_key = f"transcripts/{JOB_NAME}.json"
    obj = s3.get_object(Bucket=BUCKET, Key=transcript_key)
    data = json.loads(obj["Body"].read())
    texto = data["results"]["transcripts"][0]["transcript"]
    print(f"Transcripcion obtenida ({len(texto)} caracteres).")
    return texto


def fragmentar_texto(texto, max_bytes=MAX_CHUNK_BYTES):
    """Parte el texto en fragmentos que no excedan max_bytes en UTF-8,
    cortando por oraciones para no partir palabras a la mitad."""
    oraciones = (
        texto.replace("? ", "?|").replace("! ", "!|").replace(". ", ".|").split("|")
    )
    fragmentos = []
    actual = ""
    for oracion in oraciones:
        candidato = (actual + " " + oracion).strip() if actual else oracion
        if len(candidato.encode("utf-8")) > max_bytes:
            if actual:
                fragmentos.append(actual.strip())
            actual = oracion
        else:
            actual = candidato
    if actual:
        fragmentos.append(actual.strip())
    print(f"Texto fragmentado en {len(fragmentos)} parte(s).")
    return fragmentos


def analizar_sentimiento(fragmentos):
    print("Enviando fragmentos a Comprehend (BatchDetectSentiment)...")
    # BatchDetectSentiment acepta maximo 25 documentos por llamada
    resultados = []
    for i in range(0, len(fragmentos), 25):
        lote = fragmentos[i:i + 25]
        resp = comprehend.batch_detect_sentiment(
            TextList=lote,
            LanguageCode=LANGUAGE_CODE_COMPREHEND,
        )
        resultados.extend(resp["ResultList"])
        if resp.get("ErrorList"):
            print("Advertencia, hubo errores en algunos fragmentos:", resp["ErrorList"])
    return resultados


def agregar_resultado(resultados):
    """Promedia los scores de las 4 categorias a traves de todos los fragmentos
    y elige la categoria con mayor promedio como resultado final unico."""
    categorias = ["Positive", "Negative", "Neutral", "Mixed"]
    promedios = {c: 0.0 for c in categorias}
    for r in resultados:
        for c in categorias:
            promedios[c] += r["SentimentScore"][c]
    n = len(resultados)
    for c in categorias:
        promedios[c] /= n
    categoria_final = max(promedios, key=promedios.get)
    return categoria_final, promedios


def main():
    subir_audio()
    iniciar_transcripcion()
    esperar_transcripcion()
    texto = obtener_texto()
    fragmentos = fragmentar_texto(texto)
    resultados = analizar_sentimiento(fragmentos)
    categoria_final, promedios = agregar_resultado(resultados)

    print("\n--- RESULTADO FINAL ---")
    print(f"Transcripcion completa:\n{texto}\n")
    print(f"Fragmentos analizados: {len(fragmentos)}")
    print(f"Promedios por categoria: {promedios}")
    print(f"Categoria final: {categoria_final}")


if __name__ == "__main__":
    main()
