from app.api import PetFriends
from config import valid_password, valid_email
import os

pf = PetFriends()


def test_post_add_simple_pet(name='кротик', animal_type='крот', age='5'):
    """ --01-- Тест добавления питомца с корректными данными без фото - простое добавление
    через функцию add_simple_pet"""

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создание питомца:
    status, result = pf.post_add_simple_pet(auth_key, name, animal_type, age)

    # проверка успешности добавления питомца по статусу и наличию имени
    assert status == 200
    assert result['name'] == name


def test_set_pet_photo(pet_photo='images/krot2.jpg'):
    """ --02-- Тест добавления фото питомца с корректными данными"""

    # Создание пути к файлу изображения питомца в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список своих питомцев
    _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')

    # если список пустой, то добавляем питомца
    if len(my_pets_list['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'крот-удалить', 'крот', '2', 'images/wall_bricks.jpg')
        # снова получаем список питомцев
        _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')

    # получаем id первого (последнего созданного) питомца
    pet_id = my_pets_list['pets'][0]['id']
    # добавление нового фото питомца:
    status, _ = pf.post_add_photo_pet(auth_key, pet_id, pet_photo)

    # проверка успешности добавления фото по статусу
    assert status == 200


def test_delete_pet_name():
    """ --03-- Тест на удаление питомца по указанному имени"""

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список своих питомцев
    _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')
    pet_id = None

    # если список не пустой, то проверяем наличие нужного имени питомца
    if len(my_pets_list['pets']) > 0:
        for num in my_pets_list['pets']:
            if num['name'] == 'крот-удалить':
                pet_id = num['id']

    # если список пустой или нет нужного имени, то добавляем питомца
    if len(my_pets_list['pets']) == 0 or pet_id is None:
        pf.post_add_simple_pet(auth_key, 'крот-удалить', 'крот', '2')
        # снова получаем список питомцев
        _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')

        # получаем id питомца c заданным именем "крот-удалить"
        for num in my_pets_list['pets']:
            if num['name'] == 'крот-удалить':
                pet_id = num['id']

    status, _ = pf.delete_my_pet(auth_key, pet_id)

    # список питомцев после удаления:
    _, my_pets_list = pf.get_list_pets(auth_key, 'my_pets')

    # проверка статуса и отсутствия питомца с удаленным id
    assert status == 200
    assert pet_id not in my_pets_list.values()
    # assert 'крот-удалить' not in my_pets_list.values()


def test_post_add_new_png_pet(name='Тюлень', animal_type='seal', age='10',
                          pet_photo='images/sealpng.png'):
    """ --04-- Тест добавления питомца с корректными данными
    с изображением в формате png - данный формат заявлен в документации"""

    # Создание пути к файлу изображения питомца в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создавние питомца:
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # проверка успешности добавления питомца по статусу и наличию имени
    assert status == 200
    assert result['name'] == name


def test_post_add_new_pet_incorrectkey(name='Fishka2', animal_type='seal2', age='10',
                          pet_photo='images/fishka.jpg'):
    """ --05-- Тест невозможности добавления питомца с некорректным ключом авторизации"""

    # Создание пути к файлу изображения питомца в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # неправильный ключ:
    auth_key = {'key': '0f0759a77da86140646d27eb5a33018a680e9fc97010c666974b6a76'}

    # создание питомца:
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # проверка, что питомец не был доюавлен по статусу
    assert status == 403


def test_post_add_new_pdf_pet(name='Хедвига', animal_type='сова', age='4',
                          pet_photo='images/owl_01.pdf'):
    """ --06-- Тест на невозможность добавления питомца с изображением в некорректном формате"""

    # Создание пути к файлу изображения питомца в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создание питомца:
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # проверка невозможности добавления питомца по статусу
    assert status == 500


def test_post_add_new_blank_pet(name=None, animal_type=None, age=None,
                          pet_photo='images/krot2.jpg'):
    """ --07-- Тест на невозможность добавления питомца с пустыми данными, но приложенным фото.
    При заполнении через вэб-форму выходит предупреждение"""

    # Создание пути к файлу изображения питомца в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создание питомца:
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # проверка невозможности добавления питомца по статусу
    assert status != 200


def test_post_add_blank_simple_pet(name=None, animal_type=None, age=None):
    """ --08-- Тест на невозможность добавления питомца без фото с пустыми данными"""

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создание питомца:
    status, result = pf.post_add_simple_pet(auth_key, name, animal_type, age)

    # проверка что питомец не был добавлен - по статусу
    assert status != 200


def test_post_add_new_incorrect_pet(name='23@#$%-=*hbh', animal_type='23@#$%-=*hbh', age='-2',
                          pet_photo='images/wall_bricks.jpg'):
    """ --09-- Тест на невозможность добавления питомца с некорректными данными:
    цифры и спецсимволы в имени и породе, отрицательный возраст"""

    # Создание пути к файлу изображения питомца в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создание питомца:
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # проверка невозможности добавления питомца по статусу
    assert status != 200


def test_delete_another_pet_name():
    """ --10-- Тест на невозможность удаления чужого питомца по указанному номеру в списке всех питомцев.
    Список начинается с 0 - соответствует последнему добавленному питомцу.
    С учетом всего вышесказанного, пробуем удалить наугад питомца №20"""

    # получение ключа авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список ВСЕХ питомцев
    _, pets_list = pf.get_list_pets(auth_key, '')

    # выбираем id питомца для удаления
    pet_id = pets_list['pets'][20]['id']

    # удаляем выбранного
    status, _ = pf.delete_my_pet(auth_key, pet_id)

    # список питомцев после удаления:
    _, pets_list = pf.get_list_pets(auth_key, '')

    # проверка статуса и наличие питомца с id, предложенным к удалению
    assert status != 200
    assert pet_id in pets_list.values()
