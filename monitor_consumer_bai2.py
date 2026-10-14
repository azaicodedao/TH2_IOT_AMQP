import pika
import json

def callback(ch, method, properties, body):
    # Phân tích cú pháp JSON
    try:
        data = json.loads(body.decode('utf-8'))
        device_id = data.get("device_id")
        temp = data.get("temperature")
        humidity = data.get("humidity")
        timestamp = data.get("timestamp", "")
        
        print(f"[{timestamp}] Device: {device_id}")
        print(f"Temperature: {temp} C")
        print(f"Humidity: {humidity} %")
        
        # Xử lý logic cảnh báo
        if temp > 35:
            print(" -> CANH BAO: Nhiet do cao")
        if humidity < 40:
            print(" -> CANH BAO: Do am thap")
            
        print("-" * 30)
        
    except json.JSONDecodeError:
        print("Loi: Du lieu khong phai format JSON hop le.")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'sensor_data_queue'
    channel.queue_declare(queue=queue_name)

    print(" [*] Dang lang nghe du lieu cam bien. Nhan Ctrl+C de thoat.")
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDa dung consumer.")
        connection.close()

if __name__ == '__main__':
    main()