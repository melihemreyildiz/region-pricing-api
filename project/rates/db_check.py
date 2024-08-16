import psycopg2

try:
    connection = psycopg2.connect(
        database="postgres",  # Veritabanı ismi
        user="postgres",
        password="ratestask",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM regions;")
    result = cursor.fetchall()
    print(result)
except Exception as e:
    print("Veritabanı bağlantı hatası:", e)
finally:
    if connection:
        cursor.close()
        connection.close()
