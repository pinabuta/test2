import requests     # импорт библиотеки Requests

url = 'https://swapi.dev/api/planets/3/'     # url по которой будет отправляться запрос

result = requests.get(url)     # отправка запроса
print(result.json(), result.status_code) #result.status_code переменная+метод который выводит код ответа


assert result.status_code == 200, 'ОШИБКА, Статус-код не совпадает' #здесь показано что через запятую можно сразу написать тест ошибки
print('Статус-код корректен')



check_joke = result.json()     # cохраняем в переменную тело нашего ответа в формате JSON
joke_value = check_joke.get("name")     # если пишем название параметра внутри метода .get можем получить содержимое
print(joke_value)
#####
check_joke = result.json()
joke_value = check_joke.get("value")
print(joke_value)
print("Тест прошел успешно")