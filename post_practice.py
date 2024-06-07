import requests

class TestMap():
    def __init__(self):
        pass
    def methods(self):
        base_url = 'https://rahulshettyacademy.com' #базовая ссылка
        key = '?key=qaclick123'  # параметр для всех запросов

        '''начинается метод пост'''
        post_redource = '/maps/api/place/add/json' #путь для метода пост

        post_url = base_url + post_redource + key

        json_for_post = {

                "location": {

                    "lat": -38.383494,

                    "lng": 33.427362

                }, "accuracy": 50,

                "name": "Frontline house",

                "phone_number": "(+91) 983 893 3937",

                "address": "29, side layout, cohen 09",

                "types": [

                    "shoe park",

                    "shop"

                ],

                "website": "http://google.com",

                "language": "French-IN"

        }

        result_post = requests.post(post_url, json = json_for_post)
      #  print(result_post.text)
        assert result_post.status_code == 200, "status code is not correct"

        check = result_post.json()
        check_info = check.get('status')
        assert 'OK' in check_info, 'status code from response is not correct'
        print(f'status code from response is - {check_info}')

        place_id = check.get('place_id')
      #  print(place_id)
        #return place_id

        def check_place_id(place_id):
            '''проверка создания новой локации'''
            get_resource = '/maps/api/place/get/json'

            get_url = base_url + get_resource + key + f"&place_id={place_id}"
        #    print(get_url)
            result_get = requests.get(get_url)
            assert 200 == result_get.status_code, 'status is not correct'
         #  print(result_get.text)
            check_get = result_get.json()
            check_get_info = check_get.get('address')    #тут проверка на одинаковые поля изначальные и то что прислал гет н оя пока не могу понять как это сделать
         #   print(check_get)
            assert check_get_info == json_for_post.get('address'), 'address is not correct'
            print('address is - OK')

        check_place_id(place_id)


        '''отправляем put'''

        put_resource = '/maps/api/place/update/json'

        put_url = base_url + put_resource + key

        json_for_put = {
            "place_id": "fff", #place_id, #тут может быть устаревший плейс ид поэтому мы заменяем на переменную, которую получаем выше

            "address": "100 Lenina street, RU",

            "key": "qaclick123"
        }

        result_put = requests.put(put_url, json = json_for_put)

        assert 200 == result_put.status_code, 'status is not 200'
        check_put = result_put.json()
        check_put_ihfo = check_put.get('msg')
        assert check_put_ihfo == 'Address successfully updated', 'msg is not correct'
        print('update passed')

        assert 404 == result_put.status_code, 'status is not 404'
        assert check_put_ihfo == "Update address operation failed, looks like the data doesn't exists"
        print('negative test passed, update failed')




new_place = TestMap()
new_place.methods()