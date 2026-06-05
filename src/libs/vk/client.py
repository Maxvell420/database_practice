import requests
# Остальное содержимое файла должно быть добавлено здесь, если оно было

class Client:

    def get(self):
        response = requests.get('https://google.com')
        return response.text

