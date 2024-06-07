import requests
class Categories_jokes():
    '''Создание новой шутки'''

    def get_categories_joke(self):
        '''1.Отправить запрос для получения всех категорий'''
        url_categories = 'https://api.chucknorris.io/jokes/categories'
        result_categories = requests.get(url_categories)
        assert 200 == result_categories.status_code # проверкa на статус код
        result_categories.encoding = 'utf-8'
        return list(result_categories.json())

    def get_category_joke(self, category):
        '''2.Получить 1 шутку по каждой из категорий (16 шт) - всего 16 шуток'''
        url_category_joke = 'https://api.chucknorris.io/jokes/random?category=' + category
        result = requests.get(url_category_joke)
        assert 200 == result.status_code # проверкa на статус код
        result.encoding = 'utf-8'
        return result.json()


categories_list = Categories_jokes()
joke_categories = categories_list.get_categories_joke()

for i,category in enumerate(joke_categories):
    joke = categories_list.get_category_joke(category)
    print(f'Joke number {i+1} (category - {category}) - {joke.get("value")}')