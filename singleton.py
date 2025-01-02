# 1. Синглтон с помощью метаклассов
class SingletonMeta(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class SingletonClassMeta(metaclass=SingletonMeta):
    pass


# 2. Синглтон с помощью метода __new__ класса
class SingletonNew:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance


if __name__ == '__main__':
    # Проверка метакласса
    a = SingletonClassMeta()
    b = SingletonClassMeta()
    print(a is b)

    # Проверка __new__
    c = SingletonNew()
    d = SingletonNew()
    print(c is d)

    # Проверка через импорт
    import singleton_module

    print(singleton_module.instance is singleton_module.instance)
