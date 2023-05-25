from api import PetFriends
from settings import valid_email, valid_password, invalid_auth_key
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200 и результат в формате JSON с уникальным ключом пользователя, найденного по указанным email и паролем"""

    # Отправляем запрос и сохраняем полученный ответ с кодом в status, а результат в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key.
    Далее используя этот ключ запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet(name= 'Конек', animal_type= 'мейн-кун', age= '5', pet_photo= 'images/wolf.jpg'):
    """Проверяем, что можно добавить питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Конек", "мейн-кун", "5", "images/wolf.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

   #10 тестов.Итоговое задание 24.7.2

   # №1

def test_post_create_pet_simple_with_valid_data(name= 'Карл', animal_type= 'кот', age= '4'):
    """Проверка простого добавления питомца без фото с валидными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pet_simple_with_valid_data(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

 # №2

def test_add_pets_photo_with_valid_data(pet_photo= 'images/wolf.jpg'):
    """Проверка метода добавления фото к существующему питомцу с валидными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) == 0:
        pf.post_create_pet_simple_with_valid_data(auth_key, "Карл", "кот", "4")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pets_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] is not None

  # №3

def test_get_api_key_for_valid_user_with_invalid_email(email='petu@mail.ru', password=valid_password):
    """Получение API ключа с данными зарегистрированного пользователя,но неверно введенным email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом в status, а результат в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
    assert 'key' not in result

  # №4

def test_get_api_key_for_valid_user_with_invalid_password(email=valid_email, password='125'):
    """Получение API ключа с данными зарегистрированного пользователя, но неверно введенным паролем"""

    # Отправляем запрос и сохраняем полученный ответ с кодом в status, а результат в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
    assert 'key' not in result

  # №5

def test_get_api_key_for_valid_user_without_password(email=valid_email, password=''):
    """Получение API ключа с данными зарегистрированного пользователя без введенного пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом в status, а результат в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
    assert 'key' not in result

# №6

def test_get_all_pets_with_invalid_key(filter=''):
   """Получение списка питомцев с несуществующим API-ключом (замена api-ключа на несуществующий у существующего пользователя)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # замена ключа на несуществующий
    auth_key = invalid_auth_key

    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200

 # №7

def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Получение списка "my_pets" зарегистрированного пользователя"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) >= 0

# №8

def test_create_pet_simple_with_invalid_data(name="", animal_type="", age=""):
    """Проверка метода простого добавления питомца без фото с пустыми полями.
    Баг. Должен быть негативный результат, потому что заполнение данных полей обязательно."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

 # №9

def test_get_api_key_for_invalid_user(email="not_real_email@mail.ru", password="not_real_password"):
    """Получение API-ключа с данными незарегистрированного пользователя"""

    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result

 # №10

def test_create_pet_simple_negative_age(name="Пол", animal_type="рыба", age="-1"):
    """Добавление питомца без фото с отрицательным возрастом."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age