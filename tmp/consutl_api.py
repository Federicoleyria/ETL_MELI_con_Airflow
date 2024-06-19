import requests
import json
import csv
import datetime

def get_item_ml(category):
    url = f"https://api.mercadolibre.com/sites/MLA/search?category={category}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data["results"]
        return result
    else:
        return None

def write_to_csv(items):
    headers = ['id', 'title', 'price', 'thumbnail', 'date']
    with open('/opt/airflow/data/file.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for item in items:
            _id = get_key_item(item, 'id')
            title = get_key_item(item, 'title')
            price = get_key_item(item, 'price')
            thumbnail = get_key_item(item, 'thumbnail')
            date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')  # Formato de fecha y hora

            # Validar que todos los campos estén presentes
            if not all([_id, title, price, thumbnail]):
                print(f"Fila inválida: {_id}, {title}, {price}, {thumbnail}")
                continue  # Saltar filas inválidas

            # Asegurarse de que los valores no sean demasiado largos
            if len(_id) > 255 or len(title) > 255 or len(thumbnail) > 255:
                print(f"Datos truncados: {_id[:255]}, {title[:255]}, {thumbnail[:255]}")
                writer.writerow([_id[:255], title[:255], price, thumbnail[:255], date])
            else:
                writer.writerow([_id, title, price, thumbnail, date])
                print(f"{_id} {title} {price} {thumbnail} {date}")

def get_key_item(item, key):
    return str(item.get(key, '')).replace(',', '').strip()  # Remover comas para evitar problemas en CSV

def main():
    category = "MLA1577"
    items = get_item_ml(category)
    if items:
        for item in items:
            print(item)
        write_to_csv(items)  # Llama write_to_csv con la lista de items
    else:
        print("No se encontraron resultados.")

if __name__ == "__main__":
    main()
