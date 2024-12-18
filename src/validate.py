import re


def validate_username(username):
    min_length = 3
    max_length = 16

    if len(username) < min_length:
        print(f"Длина имени пользователя должна составлять не менее {min_length} символов.")
        return False
    if len(username) > max_length:
        print(f"Длина имени пользователя не должна превышать {max_length} символов.")
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        print("Имя пользователя может содержать только буквы, цифры и символы подчеркивания.")
        return False
    return True


def validate_password(password):
    min_length = 6
    max_length = 20

    if len(password) < min_length:
        print(f"Длина пароля должна составлять не менее {min_length} символов.")
        return False
    if len(password) > max_length:
        print(f"Длина пароля не должна превышать {max_length} символов.")
        return False
    if not re.search(r'[A-Z]', password):
        print("Пароль должен содержать хотя бы одну заглавную букву.")
        return False
    if not re.search(r'[a-z]', password):
        print("Пароль должен содержать хотя бы одну строчную букву.")
        return False
    if not re.search(r'[0-9]', password):
        print("Пароль должен содержать хотя бы одну цифру.")
        return False
    if not re.search(r'[!@#$%^]', password):
        print("Пароль должен содержать хотя бы один специальный символ (!@#$%^).")
        return False
    return True
