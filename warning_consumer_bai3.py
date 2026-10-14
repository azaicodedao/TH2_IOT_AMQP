import pika

# 1. Kết nối tới Broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Khai báo exchange (để đảm bảo tính đồng bộ)
channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')

# 3. Khai báo queue riêng cho warning
channel.queue_declare(queue='warning_queue',durable= True)

# 4. Bind queue với exchange bằng routing key 'warning'
channel.queue_bind(
    exchange='iot_alert_exchange',
    queue='warning_queue',
    routing_key='warning',
)

print(' [*] Warning Consumer đang chờ nhận cảnh báo. Nhấn CTRL+C để thoát.')


# 5. Hàm callback khi nhận được tin nhắn
def callback(ch, method, properties, body):
  print(f'[warning_queue] Da nhan: {body.decode("utf-8")}')


# Đăng ký nhận tin từ queue
channel.basic_consume(
    queue='warning_queue', on_message_callback=callback, auto_ack=True
)

# Bắt đầu vòng lặp lắng nghe liên tục
channel.start_consuming()