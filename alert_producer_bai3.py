import time
import pika

# 1. Kết nối tới RabbitMQ Broker (mặc định localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Khai báo Direct Exchange tên 'iot_alert_exchange'
exchange_name = 'iot_alert_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

# 3. Danh sách các cảnh báo với các mức (routing key tương ứng)
alerts = [
    ('info', 'He thong hoat dong binh thuong info'),
    ('warning', 'Nhiet do phong may vuot nguong warning'),
    ('critical', 'Cam bien kho lanh mat ket noi critical'),
]

print('Đang gửi các cảnh báo tới exchange...')
for severity, message in alerts:
  # Gửi thông điệp kèm routing_key tương ứng (info, warning, critical)
  channel.basic_publish(exchange=exchange_name, routing_key=severity, body=message)
  print(f" [x] Đã gửi [{severity}]: {message}")
  time.sleep(1)

# Đóng kết nối
connection.close()
print('Đã hoàn tất việc gửi cảnh báo.')