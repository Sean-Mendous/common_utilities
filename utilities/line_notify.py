import requests
from logger import logger

def send_line_notify(message: str, access_token: str):
    user_id = 'U51db96863351e36f656219f8afc437d9'
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logger.info(f' >Success to send message to Line Notify')
            return True
        else:
            raise RuntimeError(f' >Failed to send message to Line Notify: {response.status_code} - {response.text}')
    except Exception as e:
        raise RuntimeError(f' >Failed to send message to Line Notify: {e}')



if __name__ == "__main__":
    send_line_notify("test", "XDF/xNKsMkc7kFi238mdMH3+Z63cyEboj4Qzk004ybGsstTy3eSuHKhEVqRLVYyj3+K9V1UnOkT4bEJ7mzeczGaEij6ErFmc7mjf9rb1TZ1TJkZI5U1cpsAup675anmBwHZqaaYrTjtRN4/mVSnUqgdB04t89/1O/w1cDnyilFU=")
