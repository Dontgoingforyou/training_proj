from datetime import datetime


class AddCreatedAtMeta(type):
    """ Метакласс для добавления атрибута created_at """

    def __new__(cls, name, bases, dct):
        dct['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, dct)


class MyClass(metaclass=AddCreatedAtMeta):
    pass


if __name__ == '__main__':
    instance = MyClass()
    print(f"Класс 'MyClass' был создан в: {MyClass.created_at}")
