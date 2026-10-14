import pika

def main():
    # Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Khai báo queue 
    queue_name = 'iot_lab_queue'
    channel.queue_declare(queue=queue_name)

    # Thông tin sinh viên 
    message = "Xin chao tu ung dung Python AMQP - B23DCCN092 - Dang Quang Chien"

    # Gửi message
    channel.basic_publish(
        exchange='', # Default exchange
        routing_key=queue_name,
        body=message
    )
    print(f" [x] Da gui message: '{message}'")

    # Đóng kết nối
    connection.close()

if __name__ == '__main__':
    main()