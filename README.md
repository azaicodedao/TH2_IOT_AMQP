# 🐇 TH2 — Giao thức AMQP với RabbitMQ

> **Môn học:** IoT & Ứng dụng — Thực hành 2  
> **Chủ đề:** Lập trình giao tiếp với Message Broker sử dụng giao thức AMQP  
> **Thư viện:** `pika` (Python AMQP client)

---

## ⚙️ Cài đặt thư viện

```powershell
pip install pika
```

---

## 📡 Broker sử dụng

| Thông tin           | Chi tiết                                       |
| ------------------- | ---------------------------------------------- |
| **Broker**          | [RabbitMQ](https://www.rabbitmq.com/)          |
| **Giao thức**       | AMQP 0-9-1 (Advanced Message Queuing Protocol) |
| **Host mặc định**   | `localhost`                                    |
| **Port**            | `5672` (AMQP) · `15672` (Management UI)        |
| **Thư viện Python** | `pika`                                         |

RabbitMQ đóng vai trò **Message Broker** trung gian — nhận tin từ **Producer**, lưu vào **Queue** và chuyển đến **Consumer** phù hợp theo cơ chế Exchange.

### Khởi động RabbitMQ

```powershell
# Cách 1 — Dùng Docker (khuyến nghị)
docker run -d --name rabbitmq `
  -p 5672:5672 -p 15672:15672 `
  rabbitmq:3-management

# Cách 2 — Dịch vụ Windows (nếu đã cài đặt)
net start RabbitMQ
```

> 🌐 Truy cập Management UI: **http://localhost:15672** (user/pass: `guest`/`guest`)

---

## 📁 Cấu trúc thư mục

```
TH2_AMQP/
├── producer_bai1.py            # Bài 1: Producer gửi tin cơ bản
├── consumer_bai1.py            # Bài 1: Consumer nhận tin cơ bản
├── sensor_producer_bai2.py     # Bài 2: Producer mô phỏng cảm biến
├── monitor_consumer_bai2.py    # Bài 2: Consumer theo dõi dữ liệu
├── alert_producer_bai3.py      # Bài 3: Producer gửi cảnh báo (Direct Exchange)
├── warning_consumer_bai3.py    # Bài 3: Consumer nhận mức Warning
├── critical_consumer_bai3.py   # Bài 3: Consumer nhận mức Critical
└── README.md
```

---

## 🔖 Bài 1 — Hello World (Queue cơ bản)

**Mô hình:** Producer → Queue → Consumer (Default Exchange)

```powershell
# Terminal 1
python consumer_bai1.py

# Terminal 2
python producer_bai1.py
```

---

## 🔖 Bài 2 — Cảm biến IoT (Fanout / Topic Exchange)

**Mô hình:** Sensor Producer → Exchange → Monitor Consumer

```powershell
# Terminal 1
python monitor_consumer_bai2.py

# Terminal 2
python sensor_producer_bai2.py
```

---

## 🔖 Bài 3 — Hệ thống cảnh báo (Direct Exchange) ✅

### Mô hình kiến trúc

```
                         ┌─────────────────────────┐
                         │   iot_alert_exchange     │
                         │     (Direct Exchange)    │
                         └────────────┬────────────┘
                                      │
              ┌───────────────────────┼────────────────────────┐
              │                       │                        │
        routing_key:            routing_key:            routing_key:
          "info"                 "warning"               "critical"
              │                       │                        │
              ▼                       ▼                        ▼
        ❌ Không có           ┌──────────────┐      ┌──────────────────┐
           consumer           │ warning_queue│      │  critical_queue  │
                              └──────┬───────┘      └────────┬─────────┘
                                     │                       │
                                     ▼                       ▼
                            warning_consumer_bai3   critical_consumer_bai3
```

### Mô tả các file

| File                        | Vai trò                                 | Routing Key lắng nghe           |
| --------------------------- | --------------------------------------- | ------------------------------- |
| `alert_producer_bai3.py`    | Gửi 3 loại cảnh báo tới exchange        | `info` · `warning` · `critical` |
| `warning_consumer_bai3.py`  | Nhận và xử lý cảnh báo mức **warning**  | `warning`                       |
| `critical_consumer_bai3.py` | Nhận và xử lý cảnh báo mức **critical** | `critical`                      |

### ▶️ Cách chạy

> ⚠️ **Yêu cầu:** RabbitMQ đang chạy trên `localhost:5672` trước khi chạy các lệnh dưới đây.

Mở **3 terminal** và chạy theo thứ tự:

**🟢 Terminal 1 — Khởi động Warning Consumer trước**

```powershell
python warning_consumer_bai3.py
```

**🟠 Terminal 2 — Khởi động Critical Consumer**

```powershell
python critical_consumer_bai3.py
```

**🔵 Terminal 3 — Chạy Alert Producer (sau khi 2 consumer đã sẵn sàng)**

```powershell
python alert_producer_bai3.py
```

---

### 📊 Kết quả đạt được

**Terminal 3 — Alert Producer:**

```
Đang gửi các cảnh báo tới exchange...
 [x] Đã gửi [info]: He thong hoat dong binh thuong info
 [x] Đã gửi [warning]: Nhiet do phong may vuot nguong warning
 [x] Đã gửi [critical]: Cam bien kho lanh mat ket noi critical
Đã hoàn tất việc gửi cảnh báo.
```

**Terminal 1 — Warning Consumer:**

```
 [*] Warning Consumer đang chờ nhận cảnh báo. Nhấn CTRL+C để thoát.
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
```

**Terminal 2 — Critical Consumer:**

```
 [*] Critical Consumer đang chờ nhận cảnh báo. Nhấn CTRL+C để thoát.
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

### 🔍 Phân tích kết quả

| Tin nhắn gửi                             | Routing Key | Nơi nhận               | Ghi chú                        |
| ---------------------------------------- | ----------- | ---------------------- | ------------------------------ |
| `He thong hoat dong binh thuong info`    | `info`      | ❌ Không ai nhận       | Không có queue bind với `info` |
| `Nhiet do phong may vuot nguong warning` | `warning`   | ✅ `warning_consumer`  | Nhận qua `warning_queue`       |
| `Cam bien kho lanh mat ket noi critical` | `critical`  | ✅ `critical_consumer` | Nhận qua `critical_queue`      |

> 💡 **Kết luận:** Direct Exchange định tuyến tin nhắn **chính xác** dựa trên `routing_key`. Tin nhắn có `routing_key = "info"` bị **loại bỏ** vì không có queue nào bind với routing key đó — đây là đặc điểm cốt lõi của Direct Exchange so với Fanout Exchange (gửi đến tất cả).

---
