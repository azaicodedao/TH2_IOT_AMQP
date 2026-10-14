import pika
from datetime import datetime

def callback(ch, method, properties, body):
    # Lấy thời gian hiện tại
    current_time = datetime.now().strftime('%H:%M:%S')
    message = body.decode('utf-8')
    
    print(f"Da nhan message: {message}")
    print(f"Thoi gian nhan: {current_time}\n")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'iot_lab_queue'
    channel.queue_declare(queue=queue_name)

    print(f" [*] Dang cho message trong queue '{queue_name}'. Nhan Ctrl+C de thoat.")
    
    # Đăng ký hàm callback xử lý message
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    # Chạy vòng lặp lắng nghe liên tục
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDa dung consumer.")
        connection.close()

if __name__ == '__main__':
    main()