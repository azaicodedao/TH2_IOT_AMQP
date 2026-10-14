import pika

# 1. Kết nối tới Broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Khai báo exchange
channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')

# 3. Khai báo queue riêng cho critical
channel.queue_declare(queue='critical_queue', durable=True)

# 4. Bind queue với exchange bằng routing key 'critical'
channel.queue_bind(
    exchange='iot_alert_exchange',
    queue='critical_queue',
    routing_key='critical',
)

print(' [*] Critical Consumer đang chờ nhận cảnh báo. Nhấn CTRL+C để thoát.')


# 5. Hàm callback khi nhận được tin nhắn
def callback(ch, method, properties, body):
  print(f'[critical_queue] Da nhan: {body.decode("utf-8")}')


# Đăng ký nhận tin từ queue
channel.basic_consume(
    queue='critical_queue', on_message_callback=callback, auto_ack=True
)

# Bắt đầu vòng lặp lắng nghe liên tục
channel.start_consuming()