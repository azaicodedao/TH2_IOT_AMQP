import pika
import json
import random
import time
from datetime import datetime

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'sensor_data_queue'
    channel.queue_declare(queue=queue_name)

    print(" [*] Dang gui du lieu cam bien. Nhan Ctrl+C de thoat.")
    
    try:
        while True:
            # Sinh dữ liệu ngẫu nhiên
            temp = round(random.uniform(25.0, 40.0), 1)
            humidity = round(random.uniform(30.0, 80.0), 1)
            
            payload = {
                "device_id": "sensor01",
                "temperature": temp,
                "humidity": humidity,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Chuyển đổi dict sang chuỗi JSON
            message = json.dumps(payload)
            
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message
            )
            print(f" [x] Da gui: {message}")
            
            # Đợi 3 giây trước khi gửi tiếp
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nDa dung producer.")
        connection.close()

if __name__ == '__main__':
    main()