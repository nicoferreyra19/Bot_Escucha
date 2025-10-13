import time
import requests

TOKEN = "8069070333:AAFCY5U2N2z6xKCIt8nC2Tmv2yP2Afc44uk"
CHAT_ID_GROUP = "-4986505595"
CHAT_ID_PRIVADO = "347020516"

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_message(chat_id, text):
    try:
        requests.post(URL, data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"Error enviando mensaje: {e}")

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 100}
    if offset:
        params['offset'] = offset
    response = requests.get(url, params=params)
    try:
        return response.json()['result']
    except:
        return []

def main():
    last_seen = time.time()
    heartbeat_timeout = 70  # segundos
    offset = None

    print("Bot escuchando heartbeat del grupo...")

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update['update_id'] + 1
            message = update.get('message')
            if message and str(message['chat']['id']) == CHAT_ID_GROUP:
                text = message.get('text', '')
                # Envía "PC Online" o el mensaje de heartbeat que uses
                if "PC Online" in text:
                    last_seen = time.time()
                    print("Heartbeat recibido del grupo")
        # Checkea timeout solo después de analizar todos los mensajes nuevos
        if time.time() - last_seen > heartbeat_timeout:
            send_message(CHAT_ID_PRIVADO, "¡Alerta! No se recibió señal de vida en el grupo.")
            print("Alerta enviada por inactividad.")
            last_seen = time.time()
        time.sleep(2)  # Pequeña pausa para no abusar de requests

if __name__ == "__main__":
    main()
