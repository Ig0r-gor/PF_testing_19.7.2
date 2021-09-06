import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        c уникальным ключом пользователяб найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password
        }

        resp = requests.get(self.base_url+'api/key', headers=headers)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except:
            result = resp.text
        return status, result

    def get_list_pets(self, auth_key: json, filter: str = ""):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат со списком
        найденных питомцев, совпадающтх с фильтром. На данный момент фильтр либо принимает пустое
        значение - получить список всей питомцев, либо 'my_pets' - получить список своих питомцев"""

        headers = {'auth_key' : auth_key['key']}
        filter = {'filter' : filter}

        resp = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except:
            result = resp.text
        return status, result

    def post_add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo) -> json:
        """Метод делает запрос к API сервера и отправляет данные для добавления нового питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/png')
            }
        )
        headers = {'auth_key' : auth_key['key'], 'Content-Type': data.content_type}
        resp = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except:
            result = resp.text
        return status, result

    def delete_my_pet(self, auth_key: json, pet_id) -> json:
        """Метод отправляет запрос delete на удаление питомца с указанным id"""

        headers = {'auth_key' : auth_key['key']}

        resp = requests.delete(self.base_url+'api/pets/' + pet_id, headers=headers)

        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        return status, result

    def put_update_pet_data(self, auth_key: json, pet_id: str, name: str,
                            animal_type: str, age: str) -> json:
        """Метод делает запрос к API сервера для обновления данных питомца с указанным id,
        возвращает статус и result - строка json с новыми данными"""

        headers = {'auth_key' : auth_key['key']}
        data={
            'name': name,
            'animal_type': animal_type,
            'age': age
            }

        resp = requests.put(self.base_url+'api/pets/' + pet_id, headers=headers, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        return status, result

    def post_add_simple_pet(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод делает запрос к API сервера и отправляет данные для добавления нового питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
                })
        headers = {'auth_key' : auth_key['key'], 'Content-Type': data.content_type}
        resp = requests.post(self.base_url+'api/create_pet_simple', headers=headers, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except:
            result = resp.text
        return status, result

    def post_add_photo_pet(self, auth_key: json, pet_id: str, pet_photo) -> json:
        """Метод делает запрос к API сервера и отправляет данные
        для установки нового фото питомца"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {'auth_key' : auth_key['key'], 'Content-Type': data.content_type}
        resp = requests.post(self.base_url+'api/pets/set_photo/' + pet_id,
                             headers=headers, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except:
            result = resp.text
        return status, result
