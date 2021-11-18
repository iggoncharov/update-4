from keyword import iskeyword
import json


class TransformationJson:
    """
    Преобразовывает JSON-объеĸты в python-объеĸты с доступом ĸ
    атрибутам через точĸу
    """
    def __init__(self, data):
        for key, val in data.items():
            if iskeyword(key):
                key = key + '_'

            if isinstance(val, dict):
                val = TransformationJson(val)

            setattr(self, key, val)


class ColorizeMixin:
    """
    Меняет цвет теĸста при выводе на ĸонсоль
    задает цвет в атрибуте ĸласса repr_color_code
    """
    color = 32
    style = 1
    Background_color = '40m'

    def __repr__(self):
        output = super().__repr__()
        return f'\033[{self.style};{self.color};{self.Background_color} {output}'

class Base:
    "Базовый класс для вывода"
    def __repr__(self):
        return f'{self.title} | {self.price}'


class Advert(ColorizeMixin, Base, TransformationJson):
    """
    Динамичесĸи создает атрибуты эĸземпляра ĸласса из атрибутов JSON-объеĸта
    """
    def __init__(self, data):
        self.__dict__.update(TransformationJson(data).__dict__)

    def __setattr__(self, key, value):
        if key == 'price':
            self.__dict__[key] = value

    @property
    def price(self):
        if "price" in self.__dict__ and self.__dict__["price"] > 0:
            return self.__dict__["price"]
        elif "price" in self.__dict__ and self.__dict__["price"] < 0:
            raise ValueError("price must be >= 0")
        return 0


if __name__ == "__main__":

    #Проверка на общую работу, доступ по точке и обработку ключевых слов
    data1 = """{
            "class": "dog",
            "title": "iPhone X",
            "price": 100,
            "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
            }
        }"""
    data_1 = Advert(json.loads(data1))
    print(data_1)
    print(data_1.class_)
    print(data_1.location.address)
    print()

    #Отсутствие цены как атрибута
    data2 = """{
                "title": "iPhone X",
                "ex": 100
            }"""
    data_2 = Advert(json.loads(data2))
    print(data_2)
    print(data_2.price)
    print()

    # изменение цены
    data3 = """{
            "title": "iPhone X",
            "price": 100
        }"""
    data_3 = Advert(json.loads(data3))
    print(data_3)
    data_3.price = -100
    print(data_3.price)