Tuyệt vời, bổ sung Docker vào dự án Cơ sở dữ liệu phân tán sẽ giúp việc triển khai các node/site mô phỏng trở nên dễ dàng và đồng bộ hơn rất nhiều.

Dưới đây là file `README.md` đã được cập nhật toàn diện, bổ sung phần hướng dẫn cấu hình và khởi chạy bằng **Docker / Docker Compose**:

```markdown
# Đồ Án Cơ Sở Dữ Liệu Phân Tán (Distributed Database Project)

Chào mừng bạn đến với kho lưu trữ mã nguồn cho **Đồ án Cơ sở dữ liệu phân tán**. Dự án này được phát triển bằng Python, tập trung vào việc mô phỏng và quản lý các giao dịch trên môi trường cơ sở dữ liệu phân tán, được đóng gói và triển khai linh hoạt bằng Docker.

## 📁 Cấu trúc thư mục (Repository Structure)

Dự án được tổ chức với cấu trúc như sau:

```text
do_an_csdlpt/
│
├── data/               # Chứa các tệp dữ liệu mẫu (CSV, JSON, v.v.) hoặc dữ liệu đầu ra.
├── db/                 # Mã nguồn xử lý kết nối, truy vấn và cấu hình cơ sở dữ liệu (các phân mảnh, replication).
├── simulator/          # Chứa các script Python để mô phỏng các node, giao dịch (transactions), hoặc quy trình phân tán.
├── requirements.txt    # Danh sách các thư viện Python cần thiết để chạy dự án.
├── Dockerfile          # Cấu hình Docker để đóng gói ứng dụng Python.
├── docker-compose.yml  # Cấu hình Docker Compose để khởi chạy đồng thời các node/site mô phỏng.
├── .gitignore          # Các file/thư mục được bỏ qua khi commit lên Git.
└── readme              # File giới thiệu ban đầu.

```

## 🛠️ Công nghệ sử dụng (Tech Stack)

* **Ngôn ngữ lập trình:** Python (100%)
* **Công cụ đóng gói & Triển khai:**  Docker Compose
* **Hệ quản trị cơ sở dữ liệu:** *(Ví dụ: SQL Server, MySQL, PostgreSQL - Vui lòng cập nhật cụ thể)*
* **Kiến trúc:** Phân mảnh dữ liệu (Fragmentation), Đồng bộ hóa và Xử lý giao dịch phân tán giữa các node mô phỏng.

---

## 🚀 Hướng dẫn cài đặt và Khởi chạy

Bạn có thể lựa chọn chạy dự án bằng **Docker** (khuyến nghị để giả lập nhiều node dễ dàng) hoặc **Chạy trực tiếp trên máy cục bộ**.

### Cách 1: Triển khai bằng Docker & Docker Compose (Khuyến nghị)

Đảm bảo máy máy tính của bạn đã cài đặt sẵn **Docker Compose**.

#### Bước 1: Clone repository

```bash
git clone (https://github.com/TiVox9805/do_an_csdlpt.git)
cd do_an_csdlpt

```

#### Bước 2: Khởi dựng và chạy các Container

Hệ thống Docker Compose sẽ tự động build `Dockerfile` và thiết lập các container (mô phỏng các phân mảnh/site):

```bash
docker-compose up --build

```

*Lệnh này sẽ tự động cài đặt các thư viện trong `requirements.txt` bên trong môi trường Docker cách ly và khởi chạy các dịch vụ.*

#### Bước 3: Dừng hệ thống

Để dừng các container đang chạy mà không làm mất dữ liệu (nếu có cấu hình volume):

```bash
docker-compose down

```

---

### Cách 2: Khởi chạy trực tiếp bằng Python trên máy cục bộ

#### Bước 1: Tạo môi trường ảo (Virtual Environment)

```bash
python -m venv venv

# Kích hoạt trên Windows:
venv\Scripts\activate

# Kích hoạt trên macOS/Linux:
source venv/bin/activate

```

#### Bước 2: Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt

```

#### Bước 3: Cấu hình Cơ sở dữ liệu

1. Mở các file cấu hình trong thư mục `db/` (hoặc tạo file `.env` nếu có).
2. Cập nhật thông tin kết nối (Host, User, Password, Port) trỏ đến các site/node tương ứng của hệ cơ sở dữ liệu phân tán.

#### Bước 4: Chạy mô phỏng (Run Simulator)

```bash
python simulator/gui.py  # 

```

---

## 📝 Ghi chú (Notes)

* **Docker Network:** Khi chạy bằng Docker, hãy lưu ý cấu hình kết nối giữa các container qua mạng nội bộ của Docker (thường được định nghĩa sẵn trong file `docker-compose.yml`). Thay vì dùng `localhost`, các container sẽ gọi nhau thông qua `service_name`.
* Đảm bảo rằng tất cả các node của cơ sở dữ liệu đều đang hoạt động và có thể kết nối trước khi chạy simulator.

---

*Dự án được phát triển cho học phần Cơ sở dữ liệu phân tán.*

```

### Bạn cần chuẩn bị thêm gì cho file Docker cục bộ của bạn?
Để Docker hoạt động chuẩn xác nhất, bạn nên tạo thêm file này ở thư mục gốc (nếu chưa có):

1. **docker-compose.yml:**
```yaml
version: '3.9'
services:
  site1:
    build: .
    volumes:
      - .:/app
    environment:
      - NODE_NAME=SITE_1
  site2:
    build: .
    volumes:
      - .:/app
    environment:
      - NODE_NAME=SITE_2
