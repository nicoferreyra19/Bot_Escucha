import time
import requests

TOKEN = "8069070333:AAFCY5U2N2z6xKCIt8nC2Tmv2yP2Afc44uk"
CHAT_ID_GROUP = "-4986505595"
CHAT_ID_PRIVADO = "347020516"

def send_message(chat_id, text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": chat_id, "text": text}
        )
    except Exception as e:
        print(f"Error enviando mensaje: {e}")

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {'timeout': 60}
    if offset:
        params['offset'] = offset
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get('result', [])
    return []

def main():
    last_seen = time.time()
    heartbeat_timeout = 10  # segundos (ajustable)
    offset = None
    print("Bot escuchando cualquier mensaje en el grupo...")

    while True:
        updates = get_updates(offset)
        for upd in updates:
            offset = upd['update_id'] + 1
            msg = upd.get('message', {})
            chat_id = str(msg.get('chat', {}).get('id', ''))
            if chat_id == CHAT_ID_GROUP:
                last_seen = time.time()
                print("Recibido mensaje en el grupo, timer reseteado")
        if time.time() - last_seen > heartbeat_timeout:
            send_message(
                CHAT_ID_PRIVADO,
                "¡Alerta! No se recibió ningún mensaje en el grupo en los últimos 10 segundos."
            )
            print("Alerta enviada por inactividad.")
            last_seen = time.time()
        time.sleep(2)

if __name__ == "__main__":
    main()
