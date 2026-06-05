import requests
# Остальное содержимое файла должно быть добавлено здесь, если оно было

class Client:

    API_URL = 'https://api.vk.com/method/'
    VK_API_VERSION = '5.199'

    def __init__(self, token: str, group_id: int):
        self.token = token
        self.group_id = group_id

    def getLognPollServer(self):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'group_id': self.group_id,
            'v': self.VK_API_VERSION
        }
        response = self.sendPostRequest(self.API_URL + 'messages.getLongPollServer', headers, data=data)
        return response

    def sendGetRequest(self, url: str, headers: dict, params: dict):
        response = requests.get(url, headers=headers, params=params)
        return response.text

    def sendPostRequest(self, url: str, headers: dict, data: dict):
        response = requests.post(url, headers=headers, data=data)
        return response.text