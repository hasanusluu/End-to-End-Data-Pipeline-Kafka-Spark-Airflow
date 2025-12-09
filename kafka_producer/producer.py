from kafka import KafkaProducer
import json
import time
import random

# Kafka Producer oluştur
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Sahte sipariş datası üretme fonksiyonu
def generate_order():
    users = ["Ali", "Ayşe", "Mehmet", "Zeynep"]
    products = ["Laptop", "Mouse", "Keyboard", "Monitor"]

    return {
        "user": random.choice(users),
        "product": random.choice(products),
        "price": random.randint(100, 5000)
    }

# Sürekli Kafka’ya mesaj gönder
print("Producer çalışıyor... CTRL + C ile durdurabilirsiniz.\n")

while True:
    order = generate_order()
    producer.send("orders", order)
    print(f"Gönderildi → {order}")
    time.sleep(1)
