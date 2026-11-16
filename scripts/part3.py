# -*- coding: utf-8 -*-
# Part 3: Q51 to Q75 (File Handling, Data Processing, Libraries & Frameworks, Networking & Databases)

DATA_PART_3 = [
    {
        "id": 51,
        "category": "File Handling and Data Processing",
        "title_en": "How do you open and close a file in Python?",
        "title_vi": "Cách mở và đóng file chuẩn mực trong Python?",
        "level": "Junior",
        "short_answer": "Cách chuẩn mực nhất là sử dụng câu lệnh `with open(filename, mode) as f:` (Context Manager). Câu lệnh này tự động đóng file (gọi `f.close()`) ngay cả khi xảy ra lỗi hoặc exception trong quá trình đọc ghi.",
        "deep_dive": """Cơ chế đóng file và quản lý file descriptor:
1. <b>Cách cũ (Không khuyến khích)</b>: <code>f = open(...); ...; f.close()</code>. Nếu giữa chừng xảy ra lỗi, lệnh <code>close()</code> sẽ không bao giờ được gọi, dẫn đến rò rỉ File Descriptor (File Descriptor Leak) trên OS.
2. <b>Cơ chế Context Manager (Chuẩn Pythonic)</b>: Dùng <code>with open()</code>, phương thức <code>__exit__</code> tự động dọn dẹp file descriptor.
3. <b>Encoding</b>: Luôn chỉ định rõ <code>encoding='utf-8'</code> khi đọc/ghi file text để tránh lỗi font chữ tiếng Việt trên Windows (mặc định dùng CP1252/ANSI).""",
        "code_example": """#  Cách chuẩn mực nhất trong Python:
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("Xin chào Python 2026!\\n")
    f.write("Dòng thứ hai.\\n")

# Đọc lại nội dung:
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("Nội dung file:\\n", content)

# File tự động đóng sau khi ra khỏi khối 'with'
print("File đã đóng chưa?", f.closed)  # Output: True""",
        "tips": "Luôn luôn ghi nhớ tham số `encoding='utf-8'`. Đây là chi tiết nhỏ nhưng thể hiện tác phong lập trình viên cẩn thận với dự án đa nền tảng."
    },
    {
        "id": 52,
        "category": "File Handling and Data Processing",
        "title_en": "What are the different modes for opening a file?",
        "title_vi": "Các chế độ mở file (File Modes) trong Python và sự khác biệt?",
        "level": "Junior",
        "short_answer": "Các mode chính gồm: `'r'` (chỉ đọc), `'w'` (ghi mới - xóa trắng nội dung cũ), `'a'` (ghi nối tiếp vào cuối file), `'x'` (tạo mới độc quyền - lỗi nếu file đã có), `'b'` (chế độ nhị phân - binary), và `'+'` (mở để vừa đọc vừa ghi).",
        "deep_dive": """Bảng tổng hợp các mode mở file:
<table>
  <tr><th>Mode</th><th>Mô tả chi tiết</th><th>Vị trí con trỏ</th><th>Nếu file chưa tồn tại</th></tr>
  <tr><td><code>'r'</code></td><td>Read only (chỉ đọc)</td><td>Đầu file</td><td>Ném ngoại lệ <code>FileNotFoundError</code></td></tr>
  <tr><td><code>'w'</code></td><td>Write only (ghi đè)</td><td>Đầu file (cắt ngắn file về 0)</td><td>Tự động tạo file mới</td></tr>
  <tr><td><code>'a'</code></td><td>Append (ghi nối tiếp)</td><td>Cuối file</td><td>Tự động tạo file mới</td></tr>
  <tr><td><code>'x'</code></td><td>Exclusive creation (tạo độc quyền)</td><td>Đầu file</td><td>Tạo file mới, nếu đã có văng <code>FileExistsError</code></td></tr>
  <tr><td><code>'r+'</code></td><td>Đọc và Ghi (không xóa trắng file)</td><td>Đầu file</td><td>Ném ngoại lệ <code>FileNotFoundError</code></td></tr>
  <tr><td><code>'w+'</code></td><td>Ghi và Đọc (xóa trắng file)</td><td>Đầu file</td><td>Tự động tạo file mới</td></tr>
  <tr><td><code>'rb' / 'wb'</code></td><td>Đọc/Ghi dạng nhị phân (ảnh, pdf, zip)</td><td>Tùy mode</td><td>Xử lý kiểu dữ liệu <code>bytes</code></td></tr>
</table>""",
        "code_example": """# 1. Chế độ 'x' tạo file độc quyền (tránh vô tình ghi đè file có sẵn)
try:
    with open("config.json", "x", encoding="utf-8") as f:
        f.write("{\\"status\\": \\"init\\"}")
except FileExistsError:
    print("⚠️ File 'config.json' đã tồn tại, không ghi đè!")

# 2. Chế độ 'a' thêm log vào cuối file
with open("app.log", "a", encoding="utf-8") as f:
    f.write("[2026-11-09 22:00] Server restarted\\n")""",
        "tips": "Nhớ rằng `w+` sẽ xóa sạch nội dung cũ ngay khi mở file! Nếu muốn đọc file và cập nhật một phần mà không làm mất dữ liệu cũ, hãy dùng `r+`."
    },
    {
        "id": 53,
        "category": "File Handling and Data Processing",
        "title_en": "How do you read and write data to a file in Python?",
        "title_vi": "Các phương thức đọc và ghi dữ liệu file hiệu quả trong Python?",
        "level": "Junior",
        "short_answer": "Để đọc: dùng `read()` (nạp toàn bộ), `readline()` (đọc 1 dòng), `readlines()` (đọc tất cả các dòng vào list), hoặc tốt nhất là duyệt lặp trực tiếp `for line in f:` (tiết kiệm bộ nhớ). Để ghi: dùng `write(str)` hoặc `writelines(list_of_strings)`.",
        "deep_dive": """Hiệu năng khi đọc file dung lượng lớn:
1. <b><code>f.read()</code> và <code>f.readlines()</code></b>:
   - Nạp toàn bộ dữ liệu vào RAM cùng lúc. Nếu file nặng 10GB, ứng dụng sẽ bị tràn bộ nhớ (Out Of Memory - OOM).
2. <b>Duyệt lặp <code>for line in f:</code> (Best Practice)</b>:
   - File object trong Python là một Iterable. Trình thông dịch sử dụng bộ đệm (internal buffer) tự động nạp từng chunk, giúp RAM duy trì cố định ở mức rất nhỏ.
3. <b>Thư viện hiện đại <code>pathlib.Path</code> (Từ Python 3.4+)</b>:
   - Hỗ trợ cú pháp hướng đối tượng thanh lịch: <code>Path('data.txt').read_text()</code> hoặc <code>Path('data.txt').write_text()</code>.""",
        "code_example": """from pathlib import Path

# Cách 1: Đọc stream từng dòng an toàn bộ nhớ
with open("large_access.log", "w", encoding="utf-8") as f:
    f.writelines([f"Request {i}\\n" for i in range(5)])

with open("large_access.log", "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        print(f"Dòng {line_num}: {line.strip()}")

# Cách 2: Dùng Pathlib cực kỳ ngắn gọn cho file nhỏ
p = Path("settings.env")
p.write_text("DEBUG=True\\nPORT=8000", encoding="utf-8")
print(p.read_text(encoding="utf-8"))""",
        "tips": "Luôn dùng `pathlib.Path` trong Python 3 thay vì các hàm cũ kỹ của `os.path`."
    },
    {
        "id": 54,
        "category": "File Handling and Data Processing",
        "title_en": "What is a CSV file and how do you read it in Python?",
        "title_vi": "File CSV là gì và các cách đọc/ghi CSV hiệu quả trong Python?",
        "level": "Junior",
        "short_answer": "CSV (Comma-Separated Values) là định dạng file văn bản thuần túy dùng dấu phẩy (hoặc tab/chấm phẩy) để phân tách các cột dữ liệu. Trong Python, ta có thể xử lý CSV bằng module tích hợp sẵn `csv` (`csv.reader`, `csv.DictReader`) hoặc dùng thư viện chuyên dụng `pandas`.",
        "deep_dive": """Module `csv` chuẩn của Python:
1. <b><code>csv.reader</code></b>: Đọc từng dòng thành một danh sách các chuỗi (list of strings).
2. <b><code>csv.DictReader</code> (Khuyên dùng)</b>:
   - Tự động lấy dòng đầu tiên làm tiêu đề (header) và trả về từng dòng dưới dạng Dictionary <code>{header: value}</code>, giúp truy xuất cột theo tên thay vì chỉ mục số.
3. <b>Tham số <code>newline=''</code> khi mở file</b>:
   - Khi ghi file CSV trên Windows, bắt buộc phải truyền <code>newline=''</code> vào hàm <code>open()</code> để tránh bị chèn thêm dòng trống thừa giữa các hàng.""",
        "code_example": """import csv

# Ghi file CSV với DictWriter
data = [
    {"name": "An", "age": 25, "role": "Backend Dev"},
    {"name": "Bình", "age": 28, "role": "DevOps"}
]

with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "role"])
    writer.writeheader()
    writer.writerows(data)

# Đọc file CSV bằng DictReader
with open("users.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"Nhân viên: {row['name']} | Vị trí: {row['role']}")""",
        "tips": "Khi làm việc với file CSV có dấu phẩy nằm bên trong giá trị chuỗi (ví dụ: `\"Hà Nội, Việt Nam\"`), module `csv` tự động xử lý dấu ngoặc kép an toàn, không bao giờ dùng `line.split(',')` thủ công."
    },
    {
        "id": 55,
        "category": "File Handling and Data Processing",
        "title_en": "What are JSON files and how does Python process them?",
        "title_vi": "File JSON là gì và cách làm việc với JSON trong Python?",
        "level": "Junior",
        "short_answer": "JSON (JavaScript Object Notation) là định dạng trao đổi dữ liệu dạng text phổ biến nhất trên web. Python xử lý JSON qua module tích hợp sẵn `json` với 4 phương thức chính: `dump` (ghi ra file), `dumps` (chuyển sang chuỗi), `load` (đọc từ file) và `loads` (phân tích từ chuỗi).",
        "deep_dive": """Bảng quy đổi kiểu dữ liệu giữa Python và JSON:
<table>
  <tr><th>Python Type</th><th>JSON Equivalent</th></tr>
  <tr><td><code>dict</code></td><td>object <code>{}</code></td></tr>
  <tr><td><code>list, tuple</code></td><td>array <code>[]</code></td></tr>
  <tr><td><code>str</code></td><td>string <code>""</code></td></tr>
  <tr><td><code>int, float</code></td><td>number</td></tr>
  <tr><td><code>True / False</code></td><td><code>true / false</code></td></tr>
  <tr><td><code>None</code></td><td><code>null</code></td></tr>
</table>
Các kỹ thuật nâng cao:
- Dùng <code>indent=2</code> để format JSON đẹp mắt (pretty print).
- Dùng <code>ensure_ascii=False</code> để giữ nguyên tiếng Việt có dấu.
- Dùng <code>default</code> serializer khi encode các object như <code>datetime</code> hoặc <code>UUID</code>.""",
        "code_example": """import json
from datetime import datetime

payload = {
    "title": "Cẩm nang phỏng vấn Python",
    "year": 2026,
    "tags": ["python", "backend"],
    "is_published": True
}

# 1. Chuyển Python Dict sang JSON String có format tiếng Việt đẹp:
json_str = json.dumps(payload, indent=2, ensure_ascii=False)
print("JSON String:\\n", json_str)

# 2. Parse ngược từ JSON String về Python Dict:
parsed_data = json.loads(json_str)
print("Lấy thẻ tags:", parsed_data["tags"])

# 3. Custom Serializer cho kiểu datetime
def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Unserializable object")

event = {"event": "Interview", "time": datetime.now()}
print(json.dumps(event, default=custom_encoder))""",
        "tips": "Nếu cần tốc độ serialize/deserialize JSON cực nhanh cho API tải cao, hãy nhắc đến thư viện bên thứ 3 viết bằng Rust/C như `orjson` hoặc `ujson` (nhanh gấp 5-10 lần module `json` chuẩn)."
    },
    {
        "id": 56,
        "category": "File Handling and Data Processing",
        "title_en": "How do you handle binary files in Python?",
        "title_vi": "Cách xử lý file nhị phân (Binary Files: ảnh, pdf, audio) trong Python?",
        "level": "Mid",
        "short_answer": "Để xử lý file nhị phân, ta thêm ký tự `'b'` vào mode khi mở file (`'rb'`, `'wb'`, `'ab'`). Khi đọc, dữ liệu trả về kiểu `bytes` thay vì `str`. Để giải mã cấu trúc nhị phân của C, ta dùng module `struct`, còn để tuần tự hóa object Python nhị phân, ta dùng `pickle`.",
        "deep_dive": """Các lưu ý quan trọng với dữ liệu nhị phân:
1. <b>Kiểu dữ liệu <code>bytes</code> và <code>bytearray</code></b>:
   - <code>bytes</code> là immutable, đại diện cho mảng các số nguyên từ 0 đến 255.
   - <code>bytearray</code> là mutable, cho phép chỉnh sửa từng byte trực tiếp in-place mà không cần copy bộ nhớ.
2. <b>Module <code>struct</code></b>:
   - Cho phép đóng gói và giải nén (pack/unpack) các kiểu dữ liệu C nguyên thủy (int 32-bit, float, double) từ chuỗi bytes.
3. <b>Cảnh báo bảo mật với <code>pickle</code></b>:
   - TUYỆT ĐỐI KHÔNG <code>pickle.load()</code> dữ liệu từ nguồn không tin cậy trên mạng vì có thể bị thực thi mã độc tùy ý (RCE).""",
        "code_example": """# 1. Sao chép một file ảnh nhị phân theo từng chunk
def copy_binary_file(src_path, dest_path, chunk_size=4096):
    with open(src_path, "rb") as src, open(dest_path, "wb") as dest:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dest.write(chunk)

# 2. Sử dụng struct để đóng gói dữ liệu nhị phân
import struct

# Đóng gói 1 số nguyên 32-bit (i) và 1 số thực 32-bit (f) theo thứ tự Little-Endian (<)
binary_packet = struct.pack("<if", 100, 3.14)
print("Dữ liệu nhị phân:", binary_packet)

# Mở gói dữ liệu
unpacked = struct.unpack("<if", binary_packet)
print("Giải mã:", unpacked)  # (100, 3.140000104904175)""",
        "tips": "Nếu được hỏi 'Pickle có an toàn để lưu session người dùng trong cookie không?', câu trả lời luôn là KHÔNG vì lỗ hổng Deserialization Attack có thể giúp hacker chiếm quyền điều khiển server."
    },
    {
        "id": 57,
        "category": "File Handling and Data Processing",
        "title_en": "What is the pandas library, and how is it used?",
        "title_vi": "Thư viện Pandas là gì và các cấu trúc dữ liệu cốt lõi của nó?",
        "level": "Junior",
        "short_answer": "Pandas là thư viện mã nguồn mở hàng đầu trong Python chuyên về phân tích, xử lý và làm sạch dữ liệu bảng (Tabular Data). Hai cấu trúc dữ liệu cốt lõi của Pandas là `Series` (mảng 1 chiều có gắn nhãn index) và `DataFrame` (bảng 2 chiều gồm nhiều dòng và cột).",
        "deep_dive": """Các tính năng mạnh mẽ nhất của Pandas:
1. <b>Đọc/Ghi đa định dạng</b>: <code>read_csv()</code>, <code>read_excel()</code>, <code>read_sql()</code>, <code>read_parquet()</code>.
2. <b>Căn chỉnh dữ liệu tự động (Automatic Alignment)</b>: Dựa trên nhãn Index.
3. <b>Xử lý dữ liệu khuyết thiếu (Missing Data)</b>: Nhận diện <code>NaN</code>, điền giá trị với <code>fillna()</code> hoặc loại bỏ với <code>dropna()</code>.
4. <b>Thao tác biến đổi dữ liệu mạnh mẽ</b>: Hỗ trợ Filter, GroupBy, Merge, Join, Pivot Table tương tự như câu lệnh SQL nhưng linh hoạt hơn nhiều.""",
        "code_example": """import pandas as pd

# Tạo DataFrame từ từ điển Python
raw_data = {
    "Tên": ["Lan", "Nam", "Huy", "An"],
    "Phòng_ban": ["IT", "Sales", "IT", "HR"],
    "Lương": [30_000_000, 20_000_000, 35_000_000, 18_000_000]
}

df = pd.DataFrame(raw_data)

# 1. Lọc nhân viên lương > 20 triệu
it_devs = df[df["Lương"] > 20_000_000]
print("Lương > 20tr:\\n", it_devs)

# 2. Tính lương trung bình theo từng phòng ban (GroupBy)
avg_salary = df.groupby("Phòng_ban")["Lương"].mean()
print("\\nLương trung bình phòng ban:\\n", avg_salary)""",
        "tips": "Khi làm việc với dữ liệu rất lớn (hơn 10GB), hãy cân nhắc nhắc đến `Polars` — thư viện thế hệ mới viết bằng Rust với API tương tự Pandas nhưng chạy nhanh hơn và tối ưu đa luồng tốt hơn nhiều."
    },
    {
        "id": 58,
        "category": "File Handling and Data Processing",
        "title_en": "How do you process data in chunks with pandas?",
        "title_vi": "Cách xử lý file dữ liệu khổng lồ bằng kỹ thuật Chunking trong Pandas?",
        "level": "Mid",
        "short_answer": "Để xử lý file CSV vượt quá dung lượng RAM, ta truyền tham số `chunksize=N` vào hàm `pd.read_csv()`. Hàm này sẽ trả về một TextFileReader (Iterator). Ta có thể dùng vòng lặp `for chunk in ...` để nạp và xử lý từng phần dữ liệu một mà không làm tràn bộ nhớ.",
        "deep_dive": """Quy trình Chunking chuẩn trong thực tế:
1. Khi file CSV có kích thước 20GB mà server chỉ có 8GB RAM, việc gọi <code>pd.read_csv('huge.csv')</code> sẽ gây lỗi Out of Memory ngay lập tức.
2. Dùng <code>chunksize=100_000</code>: Mỗi lần lặp sẽ trả về một DataFrame chứa 100,000 dòng.
3. Trong mỗi vòng lặp:
   - Làm sạch, lọc (filter) hoặc tính toán tổng hợp (aggregate) cục bộ.
   - Ghi kết quả tổng hợp ra DB hoặc gom vào một list kết quả nhỏ nhẹ.""",
        "code_example": """import pandas as pd

# Giả lập xử lý file giao dịch khổng lồ theo từng chunk 50,000 dòng
chunk_size = 50_000
total_revenue = 0

# chunk_reader là một Iterator trả về từng DataFrame nhỏ
for chunk in pd.read_csv("transactions_large.csv", chunksize=chunk_size):
    # Lọc các giao dịch thành công:
    valid_tx = chunk[chunk["status"] == "SUCCESS"]
    # Cộng dồn doanh thu:
    total_revenue += valid_tx["amount"].sum()

print(f"Tổng doanh thu tính toán thành công: {total_revenue:,} VND")""",
        "tips": "Có thể kết hợp `usecols=['col1', 'col2']` và `dtype={'col1': 'int32'}` khi dùng `pd.read_csv` để chỉ nạp các cột cần thiết và giảm kích thước kiểu dữ liệu trong RAM."
    },
    {
        "id": 59,
        "category": "File Handling and Data Processing",
        "title_en": "What are the advantages of using NumPy arrays over nested Python lists?",
        "title_vi": "Ưu điểm vượt trội của NumPy Array so với Python List lồng nhau?",
        "level": "Mid",
        "short_answer": "NumPy Array (`ndarray`) vượt trội hơn Python List ở 3 điểm: 1. **Hiệu năng**: Nhanh hơn gấp 50-100 lần nhờ tính toán được vector hóa viết bằng C/Fortran không cần vòng lặp for ở tầng Python, 2. **Bộ nhớ**: Lưu trữ mảng đồng nhất liên tục trong RAM không có overhead con trỏ đối tượng, 3. **Tiện ích**: Hỗ trợ Broadcasting và toán tử ma trận trực tiếp.",
        "deep_dive": """Bản chất bộ nhớ giữa List và ndarray:
1. <b>Python List of Lists</b>:
   - Là một mảng chứa các con trỏ trỏ tới các đối tượng <code>PyObject</code> rải rác trên RAM. Mỗi số nguyên int trong Python tốn 28 bytes. Thao tác duyệt mảng bị tình trạng CPU Cache Miss liên tục.
2. <b>NumPy ndarray</b>:
   - Dữ liệu được lưu trữ trong một khối bộ nhớ liền kề (Contiguous Memory Block), các phần tử cùng kiểu C nguyên thủy (ví dụ <code>int32</code> tốn đúng 4 bytes). CPU có thể nạp thẳng vào L1/L2 Cache và áp dụng tập chỉ lệnh SIMD (Single Instruction Multiple Data) để tính toán song song.""",
        "code_example": """import numpy as np
import time

size = 5_000_000

# 1. Đo thời gian với Python List thường
list_a = list(range(size))
list_b = list(range(size))
start = time.perf_counter()
result_list = [a + b for a, b in zip(list_a, list_b)]
print(f"Python List time: {time.perf_counter() - start:.4f}s")  # ~0.45s

# 2. Đo thời gian với NumPy Array (Vectorization)
arr_a = np.arange(size)
arr_b = np.arange(size)
start = time.perf_counter()
result_np = arr_a + arr_b  # Tính toán vector hóa
print(f"NumPy time:       {time.perf_counter() - start:.4f}s (Nhanh gấp 30 lần!)")  # ~0.015s""",
        "tips": "Từ khóa đắt giá cần nói trong phỏng vấn: 'Contiguous memory layout', 'Vectorization', 'SIMD instructions' và 'CPU Cache Locality'."
    },
    {
        "id": 60,
        "category": "File Handling and Data Processing",
        "title_en": "How do you use the os and sys modules for interacting with the operating system?",
        "title_vi": "Phân biệt và cách sử dụng module os và sys trong tương tác với hệ điều hành?",
        "level": "Junior",
        "short_answer": "Module `os` dùng để tương tác với các tính năng của Hệ điều hành (thao tác file, thư mục, biến môi trường, tiến trình). Module `sys` dùng để tương tác với chính Trình thông dịch Python (tham số dòng lệnh `sys.argv`, đường dẫn module `sys.path`, thoát chương trình `sys.exit()`, quản lý bộ nhớ `sys.getsizeof()`).",
        "deep_dive": """Phân loại chức năng chính giữa `os` và `sys`:
1. <b>Module <code>os</code> (Operating System)</b>:
   - Thao tác biến môi trường: <code>os.environ.get('SECRET_KEY')</code>.
   - Thao tác thư mục: <code>os.mkdir()</code>, <code>os.listdir()</code>, <code>os.walk()</code>.
   - Lấy PID hiện tại: <code>os.getpid()</code>.
2. <b>Module <code>sys</code> (Python Interpreter System)</b>:
   - Nhận đối số CLI: <code>sys.argv</code> (danh sách tham số khi chạy <code>python script.py arg1 arg2</code>).
   - Kiểm soát luồng I/O chuẩn: <code>sys.stdin</code>, <code>sys.stdout</code>, <code>sys.stderr</code>.
   - Thoát chương trình với mã trạng thái: <code>sys.exit(0)</code> (thành công) hoặc <code>sys.exit(1)</code> (lỗi).""",
        "code_example": """import os
import sys

# 1. Sử dụng sys: Đọc tham số dòng lệnh CLI
print("Tên script:", sys.argv[0])
print("Phiên bản Python:", sys.version_info.major, sys.version_info.minor)

# 2. Sử dụng os: Lấy biến môi trường an toàn
db_host = os.environ.get("DB_HOST", "localhost")
print(f"Kết nối DB tới: {db_host}")

# 3. Lấy đường dẫn thư mục hiện tại
current_dir = os.getcwd()
print("Thư mục hiện tại:", current_dir)""",
        "tips": "Để thao tác đường dẫn file/folder, thay vì dùng `os.path.join` kiểu cũ, hãy ưu tiên dùng `pathlib.Path` hiện đại hơn."
    },
    {
        "id": 61,
        "category": "Python Libraries and Frameworks",
        "title_en": "What are the key features of the Flask framework?",
        "title_vi": "Các đặc điểm nổi bật của Micro-framework Flask là gì?",
        "level": "Junior",
        "short_answer": "Flask là một micro-framework web nhẹ, đơn giản và linh hoạt. Đặc điểm chính: không áp đặt cấu trúc dự án cứng nhắc, dựa trên chuẩn WSGI (Werkzeug) và Jinja2 template engine, dễ mở rộng thông qua các extension (Flask-SQLAlchemy, Flask-Login, Flask-JWT-Extended), phù hợp cho microservices và ứng dụng nhỏ đến vừa.",
        "deep_dive": """Tại sao Flask được gọi là 'Micro-framework'?
1. <b>Triết lý tối giản (Minimalist Core)</b>:
   - Flask không tích hợp sẵn ORM (như Django ORM), không có Admin panel, không có hệ thống Authentication mặc định. Nó cho phép lập trình viên tự do lựa chọn công cụ tốt nhất cho từng bài toán.
2. <b>Cơ chế Application Context & Request Context</b>:
   - Dùng cơ chế Thread-local (hoặc ContextVar trong Python hiện đại) để cung cấp các biến toàn cục ảo như <code>request</code>, <code>g</code>, <code>session</code> một cách an toàn giữa các luồng.
3. <b>Flask Blueprints</b>:
   - Cho phép chia nhỏ ứng dụng lớn thành các module độc lập (tương tự như App trong Django).""",
        "code_example": """from flask import Flask, jsonify, request

app = Flask(__name__)

# Route đơn giản trả về JSON
@app.route("/api/v1/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "Bạn")
    return jsonify({"message": f"Xin chào, {name}!", "status": 200})

if __name__ == "__main__":
    app.run(debug=True, port=5000)""",
        "tips": "So sánh kinh điển: 'Khi nào dùng Flask, khi nào dùng Django, khi nào dùng FastAPI?'. Flask: linh hoạt cho microservices nhỏ; Django: đầy đủ tính năng cho monolith lớn; FastAPI: tối ưu hiệu năng cao cho REST API bất đồng bộ với Pydantic."
    },
    {
        "id": 62,
        "category": "Python Libraries and Frameworks",
        "title_en": "How do you build a REST API in Flask?",
        "title_vi": "Cách xây dựng một RESTful API chuẩn trong Flask?",
        "level": "Mid",
        "short_answer": "Xây dựng REST API trong Flask bằng cách định nghĩa các route tương ứng với các HTTP Methods chuẩn (GET, POST, PUT, DELETE), nhận request qua `request.get_json()`, trả về response chuẩn hóa bằng `jsonify()` kèm HTTP Status Code thích hợp (200, 201, 400, 404, 500). Trong dự án lớn, nên dùng Flask-RESTful hoặc Blueprints.",
        "deep_dive": """Các nguyên tắc thiết kế REST API chuẩn trong Flask:
1. <b>HTTP Verbs & Status Codes</b>:
   - <code>GET /items</code>: Lấy danh sách (200 OK).
   - <code>POST /items</code>: Tạo mới (201 Created).
   - <code>PUT /items/{id}</code>: Cập nhật toàn bộ (200 OK).
   - <code>DELETE /items/{id}</code>: Xóa (204 No Content).
   - <code>400 Bad Request</code> khi dữ liệu đầu vào không hợp lệ.
   - <code>404 Not Found</code> khi không tìm thấy tài nguyên.
2. <b>Xử lý lỗi tập trung</b>: Sử dụng <code>@app.errorhandler</code> để bắt lỗi và trả về JSON thống nhất.""",
        "code_example": """from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Giả lập Database trong bộ nhớ
TODOS = {1: {"id": 1, "task": "Ôn tập Python Core", "done": False}}

@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(list(TODOS.values())), 200

@app.route("/api/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Thiếu trường 'task'"}), 400
    
    new_id = max(TODOS.keys(), default=0) + 1
    new_item = {"id": new_id, "task": data["task"], "done": False}
    TODOS[new_id] = new_item
    return jsonify(new_item), 201

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    if todo_id not in TODOS:
        abort(404, description="Không tìm thấy việc cần làm")
    del TODOS[todo_id]
    return "", 204""",
        "tips": "Luôn trả về HTTP status code tường minh (`jsonify(...), 201`) thay vì dựa vào mã 200 mặc định."
    },
    {
        "id": 63,
        "category": "Python Libraries and Frameworks",
        "title_en": "What is Django and what is it used for?",
        "title_vi": "Django là gì và các ưu điểm lớn nhất của nó trong phát triển web?",
        "level": "Junior",
        "short_answer": "Django là một web framework bậc cao, đầy đủ tính năng ('batteries-included') theo mô hình MTV (Model-Template-View). Nó được thiết kế theo triết lý 'Don't Repeat Yourself' (DRY) và 'Rapid Development' (phát triển thần tốc), cung cấp sẵn Admin Panel, ORM, hệ thống Authentication, CSRF/XSS protection, và Migration.",
        "deep_dive": """Các thành phần 'Batteries-Included' làm nên thương hiệu Django:
1. <b>Django ORM</b>: Thao tác với cơ sở dữ liệu hoàn toàn bằng code Python, tự động sinh và quản lý Schema Migrations.
2. <b>Django Admin</b>: Giao diện quản trị CRUD dữ liệu tự động sinh chỉ với vài dòng cấu hình, tiết kiệm hàng tuần làm việc.
3. <b>Bảo mật tích hợp</b>: Chống mặc định các lỗ hổng OWASP Top 10 phổ biến như SQL Injection, Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF) và Clickjacking.
4. <b>Django REST Framework (DRF)</b>: Bộ công cụ mở rộng mạnh mẽ nhất để xây dựng Web APIs đẳng cấp enterprise.""",
        "code_example": """# Ví dụ định nghĩa một Model trong Django:
# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Truy vấn thông qua Django ORM cực kỳ dễ đọc:
# products = Product.objects.filter(stock__gt=0).order_by("-price")""",
        "tips": "Nhớ giải thích rõ: Django tuân theo kiến trúc MTV (Model - Template - View), trong đó View của Django tương đương với Controller trong mô hình MVC truyền thống."
    },
    {
        "id": 64,
        "category": "Python Libraries and Frameworks",
        "title_en": "How do you create a new Django project?",
        "title_vi": "Quy trình khởi tạo một dự án Django và ứng dụng mới chuẩn mực?",
        "level": "Junior",
        "short_answer": "Dự án Django được tạo bằng lệnh `django-admin startproject <project_name> .`, sau đó tạo ứng dụng con (app) chức năng bằng `python manage.py startapp <app_name>`. Sau khi tạo, cần khai báo tên app vào danh sách `INSTALLED_APPS` trong `settings.py` và chạy `python manage.py migrate`.",
        "deep_dive": """Phân biệt giữa Project và App trong Django:
1. <b>Django Project</b>: Là cấu hình tổng thể của toàn bộ hệ thống (chứa <code>settings.py</code>, <code>urls.py</code>, <code>wsgi.py/asgi.py</code>). Một project có thể chứa nhiều app.
2. <b>Django App</b>: Là một module tính năng độc lập, khép kín (ví dụ: app <code>users</code>, app <code>orders</code>, app <code>blog</code>). Một app được thiết kế tốt có thể tái sử dụng trên nhiều project khác nhau.
3. <b>Lệnh chạy server phát triển</b>: <code>python manage.py runserver</code>.""",
        "code_example": """# Các lệnh dòng lệnh chuẩn bị môi trường và tạo Django app:
# 1. Tạo virtual environment
# python3 -m venv .venv
# source .venv/bin/activate

# 2. Cài đặt Django và tạo project
# pip install django
# django-admin startproject my_ecommerce .

# 3. Tạo app chức năng sản phẩm
# python manage.py startapp products

# 4. Đăng ký app vào settings.py:
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     ...
#     'products.apps.ProductsConfig',  # Khai báo app mới tạo
# ]

# 5. Chạy migration và khởi động server:
# python manage.py migrate
# python manage.py runserver""",
        "tips": "Mẹo chuyên nghiệp: Thêm dấu chấm `.` ở cuối lệnh `startproject my_ecommerce .` để tạo project ngay tại thư mục hiện tại, tránh bị sinh thư mục lồng nhau thừa thãi."
    },
    {
        "id": 65,
        "category": "Python Libraries and Frameworks",
        "title_en": "What is an ORM, and how does Django use it?",
        "title_vi": "ORM là gì và cơ chế hoạt động của Django ORM?",
        "level": "Mid",
        "short_answer": "ORM (Object-Relational Mapping) là kỹ thuật ánh xạ các bảng trong cơ sở dữ liệu quan hệ thành các Class trong ngôn ngữ lập trình, và các dòng dữ liệu thành các Object. Django ORM cho phép lập trình viên thực hiện các thao tác CRUD và truy vấn quan hệ phức tạp hoàn toàn bằng Python mà không cần viết câu lệnh SQL thuần.",
        "deep_dive": """Cơ chế hoạt động của Django ORM:
1. <b>Lazy Evaluation (Đánh giá lười)</b>:
   - Một QuerySet trong Django KHÔNG hề thực thi câu lệnh SQL xuống database khi bạn mới khởi tạo nó (ví dụ: <code>q = User.objects.filter(active=True)</code>).
   - SQL chỉ thực sự được gửi xuống DB khi dữ liệu được đánh giá: duyệt vòng lặp <code>for</code>, lấy <code>len()</code>, gọi <code>list(q)</code>, hoặc slicing.
2. <b>Vấn đề N+1 Queries và cách khắc phục</b>:
   - Xảy ra khi truy vấn lặp trong quan hệ ForeignKey hoặc ManyToMany.
   - Giải pháp: Dùng <code>select_related()</code> (SQL INNER JOIN cho quan hệ 1-N / 1-1) và <code>prefetch_related()</code> (2 câu truy vấn riêng biệt rồi join trong Python cho quan hệ N-N).""",
        "code_example": """# Ví dụ giải quyết triệt để N+1 Queries trong Django:

# ❌ GÂY N+1 QUERIES (1 query lấy sách + N query lấy author):
# books = Book.objects.all()
# for b in books:
#     print(b.author.name)  # Mỗi vòng lặp bắn thêm 1 câu SELECT!

#  TỐI ƯU VỚI select_related (Chỉ 1 câu SQL JOIN duy nhất):
books = Book.objects.select_related("author").all()
for b in books:
    print(b.author.name)  # Tận dụng dữ liệu đã JOIN sẵn, 0 query phát sinh!""",
        "tips": "Câu hỏi số 1 trong mọi buổi phỏng vấn Django Backend: 'Phân biệt select_related và prefetch_related'. Hãy trả lời tự tin: select_related dùng SQL JOIN cho single-valued (ForeignKey, OneToOne); prefetch_related dùng Python join cho multi-valued (ManyToMany, Reverse ForeignKey)."
    },
    {
        "id": 66,
        "category": "Python Libraries and Frameworks",
        "title_en": "What is the purpose of the requests module?",
        "title_vi": "Mục đích và cách sử dụng thư viện requests trong Python?",
        "level": "Junior",
        "short_answer": "`requests` là thư viện HTTP client phổ biến nhất trong Python, được mệnh danh là 'HTTP for Humans'. Nó cung cấp API thanh lịch, trực quan để gửi các yêu cầu HTTP (GET, POST, PUT, DELETE, PATCH), tự động quản lý kết nối Keep-Alive, mã hóa tham số URL, xử lý JSON, và quản lý Cookie/Session.",
        "deep_dive": """Các tính năng cao cấp của requests:
1. <b><code>requests.Session()</code></b>:
   - Duy trì cookie giữa các request liên tiếp (rất quan trọng khi đăng nhập hoặc cào dữ liệu nhiều trang).
   - Tận dụng Connection Pooling (thông qua urllib3) để tái sử dụng kết nối TCP, tăng tốc độ gọi API gấp nhiều lần.
2. <b>Timeout bắt buộc</b>:
   - Mặc định <code>requests</code> không có timeout. Nếu server đích bị treo, thread của bạn sẽ bị block vĩnh viễn! Luôn luôn truyền tham số <code>timeout=(connect_timeout, read_timeout)</code>.
3. <b>Phương thức <code>raise_for_status()</code></b>: Tự động ném ngoại lệ <code>HTTPError</code> nếu status code là 4xx hoặc 5xx.""",
        "code_example": """import requests

# 1. Gọi GET API đơn giản có timeout
try:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=5.0  # Timeout sau 5 giây
    )
    response.raise_for_status()  # Ném lỗi nếu status >= 400
    data = response.json()
    print("Tiêu đề bài viết:", data["title"])
except requests.exceptions.RequestException as e:
    print(f"Lỗi mạng: {e}")

# 2. Sử dụng requests.Session để tối ưu Connection Pooling
with requests.Session() as session:
    session.headers.update({"Authorization": "Bearer MY_SECRET_TOKEN"})
    res1 = session.get("https://api.example.com/profile")
    res2 = session.get("https://api.example.com/orders")""",
        "tips": "Luôn nhắc đến việc cấu hình `timeout` và `Session()` khi viết crawler hoặc microservice giao tiếp nội bộ."
    },
    {
        "id": 67,
        "category": "Python Libraries and Frameworks",
        "title_en": "How do you visualize data in Python?",
        "title_vi": "Các thư viện trực quan hóa dữ liệu (Data Visualization) hàng đầu trong Python?",
        "level": "Junior",
        "short_answer": "Hệ sinh thái visualization của Python rất phong phú: 1. `Matplotlib` (thư viện nền tảng vẽ biểu đồ tĩnh chi tiết), 2. `Seaborn` (dựa trên Matplotlib, chuyên vẽ biểu đồ thống kê đẹp mắt), 3. `Plotly` (biểu đồ tương tác Web 2D/3D hiện đại), 4. `Bokeh` / `Streamlit` (xây dựng dashboard tương tác cho Data Science).",
        "deep_dive": """Khi nào chọn thư viện nào?
1. <b>Matplotlib</b>: Thích hợp cho các ấn phẩm nghiên cứu khoa học, báo cáo học thuật cần tùy biến pixel-perfect từng trục tọa độ.
2. <b>Seaborn</b>: Tuyệt vời cho giai đoạn Phân tích khám phá dữ liệu (EDA) với các biểu đồ phân phối: heatmap, boxplot, pairplot, violinplot.
3. <b>Plotly</b>: Thích hợp đưa vào Web application, Dashboard doanh nghiệp vì người dùng có thể rê chuột xem tooltip, zoom in/out và bật tắt legend trực tiếp trên trình duyệt.""",
        "code_example": """import matplotlib.pyplot as plt

# Vẽ biểu đồ đường đơn giản với Matplotlib
months = ["T1", "T2", "T3", "T4", "T5"]
revenue = [120, 150, 180, 220, 260]

plt.figure(figsize=(8, 4))
plt.plot(months, revenue, marker="o", color="#38bdf8", linewidth=2, label="Doanh thu (Triệu VND)")
plt.title("Biểu đồ tăng trưởng doanh thu 2026")
plt.xlabel("Tháng")
plt.ylabel("Doanh thu")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
# plt.savefig('revenue.png')  # Lưu file ảnh
plt.close()""",
        "tips": "Nếu làm ứng dụng dữ liệu tương tác nhanh cho sếp hoặc khách hàng xem trong 15 phút, hãy nhắc đến `Streamlit` — framework dựng dashboard nhanh nhất hiện nay."
    },
    {
        "id": 68,
        "category": "Python Libraries and Frameworks",
        "title_en": "What are some libraries you can use for machine learning in Python?",
        "title_vi": "Những thư viện Machine Learning và Deep Learning hàng đầu trong Python?",
        "level": "Junior",
        "short_answer": "Các thư viện chính gồm: 1. `Scikit-learn` (Machine Learning truyền thống: hồi quy, phân loại, phân cụm, PCA), 2. `PyTorch` và `TensorFlow/Keras` (Deep Learning, mạng nơ-ron sâu, LLM, Computer Vision), 3. `XGBoost` & `LightGBM` (Gradient Boosting cho dữ liệu dạng bảng), 4. `Hugging Face Transformers` (Mô hình ngôn ngữ lớn LLM và NLP).",
        "deep_dive": """Bản đồ hệ sinh thái AI/ML hiện đại:
1. <b>Scikit-learn</b>: Tiêu chuẩn vàng cho dữ liệu bảng vừa và nhỏ, cung cấp API <code>fit()</code>, <code>predict()</code>, <code>transform()</code> cực kỳ nhất quán.
2. <b>XGBoost / LightGBM / CatBoost</b>: Thống trị các cuộc thi Kaggle trên dữ liệu có cấu trúc (Tabular Data).
3. <b>PyTorch</b>: Thư viện Deep Learning số 1 trong nghiên cứu và công nghiệp hiện nay, tính toán Dynamic Computation Graph (Autograd) linh hoạt và hỗ trợ tăng tốc GPU qua CUDA.
4. <b>Hugging Face</b>: Trung tâm phát triển GenAI, LLM (Llama, Mistral, BERT) và AI Agents.""",
        "code_example": """# Ví dụ pipeline phân loại đơn giản với Scikit-learn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Tải dữ liệu mẫu
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Huấn luyện mô hình
clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X_train, y_train)

# 3. Đánh giá độ chính xác
preds = clf.predict(X_test)
print("Độ chính xác (Accuracy):", accuracy_score(y_test, preds))""",
        "tips": "Trong năm 2026, các buổi phỏng vấn Python ML/AI sẽ đánh giá rất cao nếu bạn biết dùng `PyTorch` kết hợp hệ sinh thái `Hugging Face` và kỹ thuật RAG/LangChain/LlamaIndex."
    },
    {
        "id": 69,
        "category": "Python Libraries and Frameworks",
        "title_en": "How do you schedule tasks in Python?",
        "title_vi": "Cách lập lịch chạy tác vụ định kỳ (Task Scheduling) trong Python?",
        "level": "Mid",
        "short_answer": "Tùy thuộc vào quy mô hệ thống: 1. Đơn giản trong script: Dùng module `schedule` hoặc `APScheduler`, 2. Hệ thống phân tán quy mô lớn (Enterprise): Dùng `Celery` kết hợp với Redis/RabbitMQ và `Celery Beat`, 3. Ở cấp độ hạ tầng OS: Dùng `Cron job` (Linux) hoặc `Kubernetes CronJob`.",
        "deep_dive": """So sánh các phương án lập lịch:
1. <b>Module <code>schedule</code></b>:
   - Cực kỳ thân thiện: <code>schedule.every().day.at('10:30').do(job)</code>. Chạy trong process Python hiện tại, nếu app restart thì lịch trình bị gián đoạn.
2. <b>APScheduler (Advanced Python Scheduler)</b>:
   - Hỗ trợ lưu trữ job vào Database (SQLAlchemy, MongoDB), tự động khôi phục lịch khi ứng dụng khởi động lại.
3. <b>Celery + Celery Beat (Chuẩn công nghiệp)</b>:
   - Tách biệt hoàn toàn phần lên lịch (Beat) và phần thực thi (Worker).
   - Tác vụ được đẩy vào Message Broker (Redis/RabbitMQ), các Worker phân tán trên nhiều server sẽ rút task về xử lý ngầm, đảm bảo không nghẽn Web request và có cơ chế Retry tự động khi lỗi.""",
        "code_example": """# Cách 1: Dùng thư viện 'schedule' cho script gọn nhẹ
import time

def send_daily_report():
    print(" Đang gửi báo cáo doanh thu ngày...")

# pip install schedule
try:
    import schedule
    schedule.every().day.at("08:00").do(send_daily_report)
    schedule.every(10).minutes.do(lambda: print("💓 Heartbeat check"))
    
    # Vòng lặp kiểm tra lịch (chỉ demo 1 nhịp)
    schedule.run_pending()
except ImportError:
    pass""",
        "tips": "Trong hệ thống web (Django/FastAPI), tuyệt đối không dùng `time.sleep()` trong luồng chính để hẹn giờ. Phải dùng background task queue như Celery hoặc RQ."
    },
    {
        "id": 70,
        "category": "Python Libraries and Frameworks",
        "title_en": "What is asyncio and how do you use it?",
        "title_vi": "Thư viện asyncio trong Python hoạt động như thế nào và cú pháp async/await?",
        "level": "Mid",
        "short_answer": "`asyncio` là thư viện tiêu chuẩn của Python dùng để viết code đơn luồng đồng thời (concurrent) bằng cú pháp `async/await`. Nó sử dụng kiến trúc Hướng sự kiện (Event Loop) để quản lý và luân chuyển giữa các tác vụ I/O non-blocking, cho phép xử lý hàng chục nghìn kết nối mạng đồng thời với chi phí RAM cực thấp.",
        "deep_dive": """3 khái niệm cốt lõi trong asyncio:
1. <b>Event Loop</b>: Trái tim của asyncio, là một vòng lặp liên tục theo dõi các sự kiện I/O và chuyển quyền điều khiển CPU cho coroutine sẵn sàng chạy.
2. <b>Coroutine</b>: Hàm khai báo với <code>async def</code>. Khi gọi, nó không chạy ngay mà trả về một Coroutine Object.
3. <b>Từ khóa <code>await</code></b>: Điểm nhường quyền điều khiển (yield control). Nó tạm dừng coroutine hiện tại và cho phép Event Loop chuyển sang làm việc khác cho đến khi tác vụ await hoàn tất.
4. <b>Chạy song song nhiều Coroutine</b>: Dùng <code>asyncio.gather(*tasks)</code> hoặc <code>asyncio.TaskGroup()</code> (từ Python 3.11+).""",
        "code_example": """import asyncio
import time

async def fetch_user(user_id):
    print(f"Bắt đầu tải user {user_id}...")
    await asyncio.sleep(1.0)  # Giả lập độ trễ mạng 1 giây
    print(f"Đã tải xong user {user_id}")
    return {"id": user_id, "name": f"User_{user_id}"}

async def main():
    start = time.perf_counter()
    # Chạy đồng thời 3 request, tổng thời gian chỉ mất ~1 giây thay vì 3 giây:
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )
    print("Kết quả:", results)
    print(f"Tổng thời gian: {time.perf_counter() - start:.2f}s")

asyncio.run(main())""",
        "tips": "Từ Python 3.11+, cú pháp chuẩn khuyến nghị để quản lý nhóm task là dùng `async with asyncio.TaskGroup() as tg:` để tự động xử lý exception an toàn hơn `asyncio.gather()`."
    },
    {
        "id": 71,
        "category": "Networking and Databases in Python",
        "title_en": "How do you implement socket programming in Python?",
        "title_vi": "Cách lập trình Socket TCP/IP cơ bản (Client - Server) trong Python?",
        "level": "Mid",
        "short_answer": "Sử dụng module tích hợp sẵn `socket`. Phía Server tạo socket `AF_INET` (IPv4) và `SOCK_STREAM` (TCP), sau đó gọi chuỗi hàm: `bind()` -> `listen()` -> `accept()` -> `recv()`/`send()`. Phía Client tạo socket và gọi: `connect()` -> `send()`/`recv()`.",
        "deep_dive": """Vòng đời kết nối TCP Socket:
1. <b>Server side</b>:
   - <code>bind((host, port))</code>: Ràng buộc socket với địa chỉ IP và cổng mạng.
   - <code>listen(backlog)</code>: Đưa socket vào trạng thái lắng nghe hàng đợi kết nối.
   - <code>conn, addr = server.accept()</code>: Lệnh chặn (blocking), chấp nhận kết nối từ client và trả về một socket kết nối mới riêng biệt.
2. <b>Client side</b>:
   - <code>client.connect((host, port))</code>: Bắt tay 3 bước TCP (Three-way handshake) với server.
3. <b>Gửi và nhận dữ liệu</b>: Dữ liệu truyền qua socket bắt buộc phải ở định dạng nhị phân <code>bytes</code> (cần <code>encode('utf-8')</code> khi gửi và <code>decode('utf-8')</code> khi nhận).""",
        "code_example": """import socket

# Minh họa Server TCP đơn giản:
def run_echo_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 9999))
    server.listen(1)
    print("Echo Server đang lắng nghe trên cổng 9999...")

    # client_conn, client_addr = server.accept()
    # data = client_conn.recv(1024)
    # client_conn.sendall(b"Echo: " + data)
    # client_conn.close()
    server.close()

# Minh họa Client TCP gửi tin nhắn:
def send_echo_message():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(('127.0.0.1', 9999))
    # client.sendall('Xin chào Server'.encode('utf-8'))
    # response = client.recv(1024).decode('utf-8')
    # print('Phản hồi:', response)
    client.close()""",
        "tips": "Nhớ tùy chọn `socket.SO_REUSEADDR` để tránh lỗi 'Address already in use' khi restart server mạng liên tục."
    },
    {
        "id": 72,
        "category": "Networking and Databases in Python",
        "title_en": "What are the steps to make a simple HTTP request in Python?",
        "title_vi": "Các bước thực hiện một HTTP Request trong Python (dùng thư viện chuẩn và requests)?",
        "level": "Junior",
        "short_answer": "Các bước chuẩn: 1. Chọn URL và HTTP method, 2. Chuẩn bị headers/params/payload, 3. Gửi request qua `requests.get()` hoặc `requests.post()`, 4. Kiểm tra Status Code (hoặc gọi `.raise_for_status()`), 5. Đọc nội dung trả về (qua `.json()` hoặc `.text`).",
        "deep_dive": """So sánh `urllib.request` (chuẩn) vs `requests` (bên ngoài):
1. <b>Thư viện chuẩn <code>urllib.request</code></b>:
   - Không cần cài thêm thư viện (hữu ích trong script hệ thống chỉ dùng standard lib).
   - Tuy nhiên cú pháp cồng kềnh, phải xử lý SSL context thủ công, tự decode bytes sang string.
2. <b>Thư viện <code>requests</code> hoặc <code>httpx</code></b>:
   - Code ngắn gọn, tự động encode params, parse JSON 1 dòng, hỗ trợ connection pooling.""",
        "code_example": """import requests

def fetch_weather(city: str):
    url = "https://api.example.com/weather"
    params = {"q": city, "units": "metric"}
    headers = {"User-Agent": "WeatherApp/1.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        # Kiểm tra nếu HTTP status code là 4xx hoặc 5xx thì ném lỗi
        response.raise_for_status()
        
        # Parse JSON tự động:
        data = response.json()
        return data
    except requests.exceptions.Timeout:
        print(" Quá thời gian chờ phản hồi (Timeout)")
    except requests.exceptions.RequestException as err:
        print(f" Lỗi gọi HTTP: {err}")""",
        "tips": "Nếu ứng dụng viết bằng `asyncio`, hãy thay thế `requests` bằng `httpx` hoặc `aiohttp` để tránh block Event Loop."
    },
    {
        "id": 73,
        "category": "Networking and Databases in Python",
        "title_en": "How do you connect to a SQL database in Python?",
        "title_vi": "Cách kết nối và làm việc với cơ sở dữ liệu SQL trong Python theo chuẩn DB-API 2.0?",
        "level": "Junior",
        "short_answer": "Python chuẩn hóa việc kết nối cơ sở dữ liệu qua đặc tả Python DB-API 2.0 (PEP 249). Quy trình gồm 4 bước: 1. Mở kết nối (`connect()`), 2. Tạo đối tượng con trỏ (`cursor()`), 3. Thực thi câu lệnh SQL (`cursor.execute()`), 4. Xác nhận thay đổi (`conn.commit()`) và đóng tài nguyên.",
        "deep_dive": """Các thư viện driver phổ biến theo từng hệ quản trị CSDL:
- <b>SQLite</b>: Module tích hợp sẵn <code>sqlite3</code> (không cần cài đặt).
- <b>PostgreSQL</b>: <code>psycopg2</code> hoặc <code>psycopg3</code> (phiên bản hiện đại hỗ trợ async).
- <b>MySQL / MariaDB</b>: <code>mysqlclient</code> hoặc <code>PyMySQL</code>.
- <b>Enterprise ORM</b>: <code>SQLAlchemy</code> hoặc <code>Django ORM</code> để quản lý Connection Pooling và trừu tượng hóa SQL.""",
        "code_example": """import sqlite3

# 1. Kết nối vào CSDL SQLite (Lưu trên file hoặc RAM ':memory:')
with sqlite3.connect("company.db") as conn:
    cursor = conn.cursor()

    # 2. Tạo bảng
    cursor.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            salary REAL
        )
    \"\"\")

    # 3. Thêm dữ liệu an toàn với Tham số hóa (Parameterized Query)
    cursor.execute(
        "INSERT INTO employees (name, salary) VALUES (?, ?)",
        ("Nguyễn Văn A", 25000000)
    )

    # 4. Commit tự động được thực hiện bởi context manager 'with conn:'
    print("Thêm nhân viên thành công!")""",
        "tips": "TUYỆT ĐỐI KHÔNG dùng f-string để nối chuỗi câu lệnh SQL: `f'SELECT * FROM users WHERE user = {username}'` vì sẽ tạo lỗ hổng SQL Injection chết người. Luôn dùng Parameterized Query với dấu `?` hoặc `%s`."
    },
    {
        "id": 74,
        "category": "Networking and Databases in Python",
        "title_en": "How do you execute a query in a database using Python?",
        "title_vi": "Cách thực thi truy vấn SELECT và lấy dữ liệu trong CSDL an toàn?",
        "level": "Junior",
        "short_answer": "Sau khi tạo con trỏ (`cursor`), ta gọi phương thức `cursor.execute(sql, params)`. Để lấy kết quả của câu lệnh SELECT, ta dùng: `cursor.fetchone()` (lấy 1 dòng), `cursor.fetchmany(size)` (lấy N dòng), hoặc `cursor.fetchall()` (lấy toàn bộ kết quả dạng danh sách các tuple).",
        "deep_dive": """So sánh các phương thức Fetch dữ liệu:
1. <b><code>cursor.fetchall()</code></b>:
   - Nạp toàn bộ kết quả vào bộ nhớ RAM của Python. Nếu bảng có hàng triệu dòng, sẽ gây nghẽn RAM!
2. <b><code>cursor.fetchone()</code> và Server-side Cursors</b>:
   - Lấy từng dòng một, rất tối ưu cho xử lý stream dữ liệu lớn.
3. <b>Dictionary Cursor (Row Factory)</b>:
   - Mặc định DB-API trả về Tuple, khó biết cột nào là trường nào.
   - Trong sqlite: <code>conn.row_factory = sqlite3.Row</code>.
   - Trong psycopg2: <code>cursor_factory=psycopg2.extras.DictCursor</code>, cho phép truy xuất <code>row['column_name']</code>.""",
        "code_example": """import sqlite3

conn = sqlite3.connect("company.db")
# Cấu hình Row Factory để truy xuất theo tên cột như Dict:
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Truy vấn có điều kiện an toàn chống SQL Injection:
min_salary = 20_000_000
cursor.execute("SELECT id, name, salary FROM employees WHERE salary >= ?", (min_salary,))

# Lấy tất cả kết quả
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row['id']} | Tên: {row['name']} | Lương: {row['salary']:,} VND")

conn.close()""",
        "tips": "Nếu bảng dữ liệu có 10 triệu bản ghi, câu trả lời của Senior là: 'Dùng Server-side Cursor (Named Cursor) kết hợp `fetchmany(1000)` để stream từng batch, không bao giờ dùng `fetchall()`'."
    },
    {
        "id": 75,
        "category": "Networking and Databases in Python",
        "title_en": "What is a NoSQL database and how would you interact with it in Python?",
        "title_vi": "Cơ sở dữ liệu NoSQL là gì và cách tương tác với MongoDB, Redis trong Python?",
        "level": "Mid",
        "short_answer": "NoSQL (Not Only SQL) là các hệ CSDL phi quan hệ, không yêu cầu schema cố định, tối ưu hóa cho khả năng mở rộng ngang (horizontal scaling) và tốc độ cao. Trong Python, các loại NoSQL phổ biến: 1. Document Store (MongoDB qua `pymongo` / `motor`), 2. Key-Value Store (Redis qua `redis-py`), 3. Column-family (Cassandra), 4. Graph (Neo4j).",
        "deep_dive": """Các trường hợp sử dụng NoSQL phổ biến:
1. <b>Redis (In-Memory Key-Value & Cache)</b>:
   - Dùng làm Caching layer, lưu trữ User Session, Rate Limiting, Pub/Sub và bảng xếp hạng Leaderboard (Sorted Sets).
2. <b>MongoDB (Document Store JSON/BSON)</b>:
   - Dùng khi cấu trúc dữ liệu thay đổi linh hoạt (Catalog sản phẩm thương mại điện tử, Blog, Log dữ liệu).
3. <b>Async Drivers cho hiệu năng cao</b>:
   - Dùng <code>motor</code> cho MongoDB async.
   - Dùng <code>redis.asyncio</code> cho Redis async.""",
        "code_example": """# 1. Tương tác với Redis (Key-Value & Cache với TTL)
# pip install redis
try:
    import redis
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    # Lưu key có thời hạn hết hạn 60 giây (TTL):
    # r.setex("otp:user_102", 60, "482910")
    # print("OTP:", r.get("otp:user_102"))
except ImportError:
    pass

# 2. Tương tác với MongoDB (Document Database)
# pip install pymongo
try:
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ecommerce_db"]
    users_col = db["users"]
    
    # Insert Document:
    # users_col.insert_one({"name": "Hải", "skills": ["Python", "Docker"]})
    # user = users_col.find_one({"name": "Hải"})
except ImportError:
    pass""",
        "tips": "Hãy giải thích rõ nguyên lý đánh đổi: Khi nào chọn SQL (cần ACID tuyệt đối, giao dịch tài chính, dữ liệu quan hệ chặt chẽ) vs khi nào chọn NoSQL (dữ liệu phi cấu trúc, tốc độ ghi siêu cao, scale ngang)."
    }
]
