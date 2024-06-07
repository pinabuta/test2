import requests
class TestDart():

    """Класс включающий сценарии по отправке запросов, с целью получения имени корабля"""

    def __init__(self):
        pass

    def test_create_positive(self):
        """Тест по получению информации, включает:
                 отправку запроса, проверка на статус-код, печать информации"""

        url = 'https://swapi.dev/api/planets/3/'
        #print(url)
        result = requests.get(url)
        print(f"Результат: {result.json()}")
        print(f'Статус-код: {result.status_code}')

        assert result.status_code == 200, 'ОШИБКА, Статус-код не совпадает'
        print('Статус-код корректен')
        result.encoding = "utf-8"
        #print(result.text)

        #check = result.json()    #тут про проверку конкретного значения из json
       # check_info = check.get('name')
        #print(check_info)

    def test_create_negative(self):
        url = 'https://swapi.dev/api/planets/3888/'
        # print(url)
        result = requests.get(url)
        print(f"Результат: {result.json()}")
        print(f'Статус-код: {result.status_code}')

        assert result.status_code == 404, 'ОШИБКА, Статус-код не совпадает'
        print('Статус-код корректен (negative test)')
        result.encoding = "utf-8"
        #print(result.text)


infor = TestDart() #экземпляр класса
infor.test_create_positive() #вот таким способом надо использовать методы внутри класса( сначала создаем экземпляр, а потом к нему используем метод)
infor.test_create_negative()