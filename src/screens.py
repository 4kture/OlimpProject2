from utils.customer_functions import *
from utils.manager_functions import *
from utils.warehouse_functions import *
from utils.director_functions import *


def customer_screen(user_id):
    while True:
        print("\nЭкран заказчика:")
        print("1. Создать заказ")
        print("2. Редактировать заказ")
        print("3. Просмотреть мои заказы")
        print("4. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            order_name = input("Введите название заказа: ")
            create_order(user_id, order_name)
        elif choice == '2':
            order_id = int(input("Введите ID заказа для редактирования: "))
            new_order_name = input("Введите новое название заказа: ")
            update_order(user_id, order_id, new_order_name)
        elif choice == '3':
            show_user_orders(user_id)
        elif choice == '4':
            print("Выход...")
            break
        else:
            print("Неверный выбор.")


def manager_screen(manager_id):
    while True:
        print("\nЭкран менеджера:")
        print("1. Просмотреть все заказы")
        print("2. Одобрить/Отклонить заказ")
        print("3. Изменить статус заказа")
        print("4. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            show_all_orders()
        elif choice == '2':
            order_id = int(input("Введите ID заказа для одобрения/отклонения: "))
            action = input("Введите действие (одобрить/отклонить): ").lower()
            approve_or_reject_order(order_id, action, manager_id)
        elif choice == '3':
            order_id = int(input("Введите ID заказа для изменения статуса: "))
            new_status = input("Введите новый статус заказа: ")
            update_order_status(order_id, new_status)
        elif choice == '4':
            print("Выход...")
            break
        else:
            print("Неверный выбор.")


def warehouse_screen():
    while True:
        print("\nЭкран кладовщика:")
        print("1. Просмотреть все материалы")
        print("2. Добавить материал")
        print("3. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            show_materials()
        elif choice == '2':
            material_name = input("Введите название материала: ")
            quantity = int(input("Введите количество: "))
            unit_price = float(input("Введите цену за единицу: "))
            add_material(material_name, quantity, unit_price)
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор.")


def director_screen():
    while True:
        print("\nЭкран директора:")
        print("1. В разработке")
        print("2. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            pass
        elif choice == '2':
            print("Выход...")
            break
        else:
            print("Неверный выбор.")