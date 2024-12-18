import sqlite3


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


def add_material(material_name, quantity, unit_price):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE Materials SET quantity = quantity + ?, unit_price = ? WHERE material_name = ?",
                   (quantity, unit_price, material_name))

    conn.commit()
    conn.close()

    print(f"Поступление материала '{material_name}' на {quantity} единиц по цене {unit_price} за единицу добавлено.")