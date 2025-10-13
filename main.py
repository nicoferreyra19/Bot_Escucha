import time
import requests

# Credenciales reales del bot y los chats
TOKEN = "8069070333:AAFCY5U2N2z6xKCIt8nC2Tmv2yP2Afc44uk"
CHAT_ID_GROUP = "-4986505595"
CHAT_ID_PRIVADO = "347020516"

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_message(chat_id, text):
    """Envia mensaje a Telegram."""
    try:
        requests.post(URL, data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"Error enviando mensaje: {e}")

def main():
    last_seen = time.time()
    heartbeat_timeout = 10  # segundos

    print("Bot escuchando heartbeat...")

    while True:
        # Simulación de espera por inactividad; ajusta según tu lógica real de heartbeat.
        time.sleep(1)
        if time.time() - last_seen > heartbeat_timeout:
            send_message(CHAT_ID_PRIVADO, "¡Alerta! No se recibió señal de vida.")
            print("Alerta enviada por inactividad.")
            last_seen = time.time()  # Para evitar spam

if __name__ == "__main__":
    main()
