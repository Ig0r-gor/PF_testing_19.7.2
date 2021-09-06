from app.api import PetFriends
from config import valid_password, valid_email
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(emal=valid_email, password=valid_password):
    """Тест работы авторизации: API возвращает статус 200 и ключ (key)"""
    # Через запрос получаем значения переменных status и result
    status, result = pf.get_api_key(emal, password)
    # проверка полученных значений:
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Тест получения списка всех питомцев. Ответ на запрос должен возвращать не пустой список.
    Для авторизации и получения ключа auth_key используем запрос из метода get_api_key"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    print(auth_key)
    status, result = pf.get_list_pets(auth_key, filter)
    assert  status == 200
    assert len(result['pets']) > 0

def test_post_add_new_pet(name='Fishka', animal_type='seal', age='10',
                          pet_photo='images/fishka.jpg'):
    """Тест добавления питомца с корректными данными"""

    # Создание пути к файлу изображения питомца в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создавние питомца:
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # проверка успешности добавления питомца по статусу и наличию имени
    assert  status == 200
    assert result['name'] == name


def test_delete_pet():
    """Тест на удаление питомца"""

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список своих питомцев
    _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')
    # print(my_pets_list)

    # если список пустой, то добавляем питомца
    if len(my_pets_list['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'крот-удалить', 'крот', '2', 'images/krot2.jpg')
        # снова получаем список питомцев
        _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')

    # получаем id первого (последнего созданного) питомца, отправляем запрос на удаление
    pet_id = my_pets_list['pets'][0]['id']
    status, _ = pf.delete_my_pet(auth_key, pet_id)

    # список питомцев после удаления:
    _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')

    # проверка статуса и отсутствия питомца с удаленным id
    assert status == 200
    assert pet_id not in my_pets_list.values()


def test_change_pet_data(name='кротик2', animal_type='Krot2', age='1'):
    """Тест на изменение данных питомца"""

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список своих питомцев
    _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')

    # если список не пустой, то обновляем 0-го (последнего добавленного) питомца
    if len(my_pets_list['pets']) > 0:
        status, result = pf.put_update_pet_data(auth_key, my_pets_list['pets'][0]['id'],
                                                name, animal_type, age)

        # проверка что статус успешный (200) и имя питомца соответствует отправленному
        assert status == 200
        assert result['name'] == name
    else:
        # если питомцев нет, то сообщение об этом в исключении
        raise Exception("Нет питомцев для изменения данных")


# def test_post_add_simple_pet(name='кротик', animal_type='крот', age='5'):
#     """Тест добавления питомца с корректными данными без фото"""
#
#     # получение ключа авторизации
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#
#     # создание питомца:
#     status, result = pf.post_add_simple_pet(auth_key, name, animal_type, age)
#
#     # проверка успешности добавления питомца по статусу и наличию имени
#     assert  status == 200
#     assert result['name'] == name
#
#
# def test_set_pet_photo(pet_photo='images/krot2.jpg'):
#     """Тест добавления питомца с корректными данными"""
#
#     # Создание пути к файлу изображения питомца в переменной pet_photo
#     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
#
#     # получение ключа авторизации
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     # получаем список своих питомцев
#     _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')
#
#     # если список пустой, то добавляем питомца
#     if len(my_pets_list['pets']) == 0:
#         pf.post_add_new_pet(auth_key, 'крот-удалить', 'крот', '2', 'images/wall_bricks.jpg')
#         # снова получаем список питомцев
#         _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')
#
#     # получаем id первого (последнего созданного) питомца
#     pet_id = my_pets_list['pets'][0]['id']
#     # добавление нового фото питомца:
#     status, _ = pf.post_add_photo_pet(auth_key, pet_id, pet_photo)
#
#     # проверка успешности добавления фото по статусу
#     assert  status == 200