import sqlite3


def show_all_orders():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders")
    orders = cursor.fetchall()
    conn.close()

    if orders:
        for order in orders:
            print(f"ID: {order[0]}, Название: {order[2]}, Статус: {order[3]}, Ответственный: {order[4]}")
    else:
        print("Нет заказов для отображения.")


def approve_or_reject_order(order_id, action, manager_id):
    if action not in ["одобрен", "отклонён"]:
        print("Неверное действие. Выберите 'одобрен' или 'отклонён'.")
        return

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE Orders SET status = ? WHERE id = ?", (action, order_id))

    if action == "одобрен":
        cursor.execute("UPDATE Orders SET responsible_id = ? WHERE id = ?", (manager_id, order_id))

    conn.commit()
    conn.close()

    print(f"Заказ {order_id} был {action}. Менеджер с ID {manager_id} назначен ответственным за заказ." if action == "одобрен" else f"Заказ {order_id} был отклонен.")


def update_order_status(order_id, new_status):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

    print(f"Статус заказа {order_id} изменен на '{new_status}'.")
