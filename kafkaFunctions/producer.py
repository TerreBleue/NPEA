from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def send_message(topic, message):
    producer.send(topic, message.encode('utf-8'))
    producer.flush()
    print("Message sent!")