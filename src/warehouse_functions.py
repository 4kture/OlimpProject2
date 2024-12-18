import sqlite3
from datetime import date


def show_incoming_documents():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM IncomingDocuments")
    documents = cursor.fetchall()
    conn.close()

    if documents:
        for doc in documents:
            print(f"ID: {doc[0]}, Материал ID: {doc[1]}, Количество: {doc[2]}, Цена: {doc[3]}, Сумма: {doc[4]}, Дата: {doc[5]}")
    else:
        print("Нет поступлений для отображения.")


def add_incoming_document(material_id, quantity, unit_price):
    total_price = quantity * unit_price
    today = date.today()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO IncomingDocuments (material_id, quantity, unit_price, total_price, date) VALUES (?, ?, ?, ?, ?)",
                   (material_id, quantity, unit_price, total_price, today))
    cursor.execute("UPDATE Materials SET quantity = quantity + ? WHERE id = ?", (quantity, material_id))

    conn.commit()
    conn.close()

    print(f"Поступление материала с ID {material_id} на {quantity} единиц по цене {unit_price} за единицу добавлено.")


def show_materials():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Materials")
    materials = cursor.fetchall()
    conn.close()

    if materials:
        for material in materials:
            print(f"ID: {material[0]}, Название: {material[1]}, Количество: {material[2]}, Цена за единицу: {material[3]}")
    else:
        print("Нет материалов для отображения.")