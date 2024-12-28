from functools import wraps

current_user_role = None

def set_user_role(role):
    """Функция для установки текущей роли пользователя"""

    global current_user_role
    current_user_role = role


def access_control(roles):
    """Декоратор для управления доступом на основе ролей пользователя"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user_role not in roles:
                raise PermissionError(f'У {current_user_role} нет прав на выполнение этой функции')
            return func(*args, **kwargs)
        return wrapper
    return decorator


@access_control(roles=['admin', 'moderator'])
def restricted_function():
    return 'Доступ к функции разрешен'


if __name__ == '__main__':
    try:
        set_user_role('user')
        print(restricted_function())
    except PermissionError as e:
        print(e)

    set_user_role('admin')
    print(restricted_function())