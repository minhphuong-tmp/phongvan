# -*- coding: utf-8 -*-
# Part 4: Q76 to Q100 (Scripting & Automation, Regex, Environment & Config, Data Science, Machine Learning)

DATA_PART_4 = [
    {
        "id": 76,
        "category": "Python Scripting and Automation",
        "title_en": "How would you automate a repetitive task in Python?",
        "title_vi": "Cách tự động hóa các tác vụ lặp đi lặp lại bằng Python?",
        "level": "Junior",
        "short_answer": "Quy trình tự động hóa: 1. Xác định rõ các bước lặp lại thủ công, 2. Chọn thư viện phù hợp (vd: `shutil`/`os` cho file, `requests`/`BeautifulSoup`/`Playwright` cho web, `openpyxl` cho Excel, `smtplib` cho email), 3. Viết script xử lý ngoại lệ và logging, 4. Lên lịch chạy định kỳ bằng Cron, Task Scheduler hoặc module `schedule`.",
        "deep_dive": """Các lĩnh vực tự động hóa phổ biến nhất với Python:
1. <b>Tự động hóa File & Thư mục</b>: Đổi tên hàng loạt, nén file zip backup, dọn dẹp file tạm cũ hơn 30 ngày (dùng <code>pathlib</code>, <code>shutil</code>).
2. <b>Báo cáo Excel & Email</b>: Đọc dữ liệu từ DB, vẽ chart bằng <code>openpyxl</code> hoặc <code>pandas</code>, đính kèm file và gửi email báo cáo buổi sáng tự động qua <code>smtplib</code>.
3. <b>Tương tác API & RPA</b>: Tự động tải hóa đơn, đồng bộ số liệu giữa CRM và ERP.""",
        "code_example": """import shutil
from pathlib import Path
from datetime import datetime

def backup_logs(source_dir: str, backup_dir: str):
    \"\"\"Script tự động nén và backup log hàng ngày.\"\"\"
    src = Path(source_dir)
    dest = Path(backup_dir)
    dest.mkdir(parents=True, exist_ok=True)
    
    today_str = datetime.now().strftime('%Y_%m_%d')
    archive_name = dest / f"logs_backup_{today_str}"
    
    shutil.make_archive(str(archive_name), 'zip', src)
    print(f"✅ Đã tạo file backup thành công: {archive_name}.zip")""",
        "tips": "Luôn có cơ chế ghi log và gửi thông báo (Telegram/Slack webhook) khi script tự động hóa bị lỗi để người quản trị biết ngay lập tức."
    },
    {
        "id": 77,
        "category": "Python Scripting and Automation",
        "title_en": "How can Python scripts be used for system administration?",
        "title_vi": "Python được ứng dụng trong quản trị hệ thống (System Administration / DevOps) như thế nào?",
        "level": "Mid",
        "short_answer": "Python là ngôn ngữ số 1 cho SysAdmin/DevOps nhờ khả năng thay thế Bash script phức tạp: giám sát tài nguyên CPU/RAM/Disk (`psutil`), thực thi lệnh shell an toàn (`subprocess`), quản trị cấu hình từ xa qua SSH (`paramiko`, `fabric`, `Ansible`), và tương tác với Cloud API (AWS `boto3`, Docker SDK).",
        "deep_dive": """Các công cụ Python tiêu chuẩn cho DevOps/SysAdmin:
1. <b><code>subprocess.run()</code></b>: Thực thi lệnh hệ thống an toàn (thay thế hoàn toàn <code>os.system</code> cũ kỹ dễ bị shell injection).
2. <b><code>psutil</code></b>: Thư viện đa nền tảng lấy thông số phần cứng: % CPU, RAM sử dụng, dung lượng ổ đĩa, tiến trình đang chạy.
3. <b>Ansible</b>: Công cụ Configuration Management hàng đầu thế giới được viết 100% bằng Python.""",
        "code_example": """import subprocess

# Chạy lệnh hệ thống an toàn, bắt output và mã lỗi
def check_disk_space():
    result = subprocess.run(
        ["df", "-h"],
        capture_output=True,
        text=True,
        check=True
    )
    print("Thông tin dung lượng ổ đĩa:")
    print(result.stdout[:300])

check_disk_space()""",
        "tips": "Nhớ luôn truyền danh sách các tham số `['ls', '-la', path]` thay vì chuỗi `shell=True` để phòng ngừa lỗi bảo mật Command Injection."
    },
    {
        "id": 78,
        "category": "Python Scripting and Automation",
        "title_en": "What techniques can you use for parsing text files?",
        "title_vi": "Các kỹ thuật bóc tách và phân tích file văn bản (Text Parsing) trong Python?",
        "level": "Junior",
        "short_answer": "Các kỹ thuật từ đơn giản đến nâng cao gồm: 1. Các phương thức chuỗi có sẵn (`split()`, `strip()`, `partition()`, `startswith()`), 2. Biểu thức chính quy (`re`), 3. Định dạng có cấu trúc dùng parser chuyên dụng (`json`, `csv`, `yaml`, `xml.etree`), 4. Ngữ pháp phức tạp dùng `pyparsing` hoặc `lark`.",
        "deep_dive": """Nguyên tắc chọn kỹ thuật parsing tối ưu:
- Nếu chuỗi có cấu trúc phân cách cố định (vd tab, dấu phẩy): Dùng <code>str.split()</code> hoặc <code>str.partition()</code> nhanh hơn nhiều so với Regex.
- Nếu chuỗi có định dạng pattern thay đổi (vd email, IP, ngày tháng): Dùng <code>re.search()</code> hoặc <code>re.finditer()</code>.
- Nếu file văn bản khổng lồ: Kết hợp Generator để stream từng dòng trước khi parse.""",
        "code_example": """import re

log_line = '192.168.1.50 - - [09/Nov/2026:22:15:30] "GET /api/v1/users HTTP/1.1" 200 1420'

# Kỹ thuật dùng Regex có Named Groups để parse log rõ ràng:
log_pattern = re.compile(r'(?P<ip>\\S+) .* \\[(?P<time>.*?)\\] "(?P<method>\\S+) (?P<endpoint>\\S+) .*?" (?P<status>\\d+)')

match = log_pattern.match(log_line)
if match:
    data = match.groupdict()
    print("Parsed Log:", data)
    # {'ip': '192.168.1.50', 'method': 'GET', 'status': '200', ...}""",
        "tips": "Sử dụng Named Capture Groups `(?P<name>...)` trong Regex giúp code tự làm rõ nghĩa mà không cần nhớ chỉ số index số."
    },
    {
        "id": 79,
        "category": "Python Scripting and Automation",
        "title_en": "How do you manipulate CSV files using Python?",
        "title_vi": "Cách thao tác nâng cao (lọc, sắp xếp, cập nhật) file CSV trong Python?",
        "level": "Junior",
        "short_answer": "Có thể sử dụng module chuẩn `csv` với `DictReader`/`DictWriter` để thao tác từng dòng mà không cần cài thư viện ngoài, hoặc dùng `pandas` cho các phép biến đổi hàng loạt (lọc cột, merge nhiều file, group by, sort) chỉ với vài dòng code.",
        "deep_dive": """So sánh cách tiếp cận:
- <b>Module `csv` chuẩn</b>: Nhẹ, không tốn RAM, phù hợp cho kịch bản CLI nhẹ nhàng hoặc môi trường server không được cài thư viện ngoài.
- <b>Pandas</b>: Cực mạnh khi cần xử lý tính toán số học, loại bỏ dòng trùng lặp (`drop_duplicates`), xử lý giá trị rỗng (`fillna`), hoặc xuất ra định dạng Excel/Parquet.""",
        "code_example": """import csv

# Đọc file CSV, tăng lương 10% cho tất cả nhân viên và ghi ra file mới
input_file = "employees.csv"
output_file = "employees_updated.csv"

# Giả lập thao tác stream:
rows = [
    {"name": "Dũng", "salary": "20000000"},
    {"name": "Mai", "salary": "25000000"}
]

for r in rows:
    r["salary"] = str(int(float(r["salary"]) * 1.1))

print("Dữ liệu sau khi tăng lương:", rows)""",
        "tips": "Khi làm việc với các file CSV xuất từ Excel tiếng Việt, luôn chú ý kiểm tra mã hóa `utf-8-sig` để tự động xử lý ký tự Byte Order Mark (BOM)."
    },
    {
        "id": 80,
        "category": "Python Scripting and Automation",
        "title_en": "How do you automate web browsing using Python?",
        "title_vi": "Cách tự động hóa trình duyệt web (Web Automation & Testing) trong Python?",
        "level": "Mid",
        "short_answer": "Sử dụng các công cụ Headless Browser automation như `Playwright` hoặc `Selenium`. Hiện nay `Playwright for Python` được ưa chuộng hơn nhờ tốc độ nhanh, tự động chờ phần tử (auto-waiting), hỗ trợ async/await nguyên bản và dễ dàng xử lý các website Single Page Application (SPA) render bằng JavaScript.",
        "deep_dive": """So sánh Playwright vs Selenium:
1. <b>Selenium (Truyền thống)</b>: Dựa trên kiến trúc WebDriver HTTP JSON Wire Protocol, thường phải dùng các lệnh <code>sleep()</code> hoặc <code>WebDriverWait</code> thủ công để chờ DOM render.
2. <b>Playwright (Hiện đại)</b>: Kết nối trực tiếp qua giao thức WebSocket Chrome DevTools Protocol (CDP), tự động chờ element clickable trước khi click, hỗ trợ chụp ảnh màn hình, record video trace và bypass bot detection tốt hơn.""",
        "code_example": """# Ví dụ với Playwright (Async Python):
# pip install playwright && playwright install
import asyncio

async def run():
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://quotes.toscrape.com")
            title = await page.title()
            print("Tiêu đề trang:", title)
            await browser.close()
    except ImportError:
        print("Cần cài đặt: pip install playwright")

# asyncio.run(run())""",
        "tips": "Nếu chỉ cần cào dữ liệu tĩnh không có JavaScript, hãy dùng `requests` + `BeautifulSoup` hoặc `selectolax` để nhanh gấp 50 lần so với việc bật cả trình duyệt headless browser."
    },
    {
        "id": 81,
        "category": "Python Regular Expressions",
        "title_en": "What are regular expressions and how are they used?",
        "title_vi": "Regular Expressions (Regex) là gì và ứng dụng trong Python?",
        "level": "Junior",
        "short_answer": "Regular Expressions (Regex) là chuỗi các ký tự đặc biệt định nghĩa một mẫu tìm kiếm (search pattern). Trong Python, module `re` cung cấp các hàm để khớp mẫu, tìm kiếm, trích xuất và thay thế văn bản theo quy tắc.",
        "deep_dive": """Các hàm cốt lõi trong module `re`:
1. <code>re.match(pattern, string)</code>: Chỉ kiểm tra khớp từ NGAY ĐẦU chuỗi.
2. <code>re.search(pattern, string)</code>: Quét toàn bộ chuỗi để tìm vị trí khớp ĐẦU TIÊN.
3. <code>re.findall(pattern, string)</code>: Trả về danh sách TẤT CẢ các chuỗi con khớp mẫu.
4. <code>re.finditer(pattern, string)</code>: Trả về iterator các Match Object (tiết kiệm bộ nhớ).
5. <code>re.sub(pattern, repl, string)</code>: Thay thế chuỗi khớp mẫu.""",
        "code_example": """import re

text = "Liên hệ tuyển dụng qua email: hr@company.com hoặc tech.lead@dev.vn"

# Regex tìm kiếm địa chỉ email
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'

emails = re.findall(email_pattern, text)
print("Các email tìm thấy:", emails)
# Output: ['hr@company.com', 'tech.lead@dev.vn']""",
        "tips": "Luôn luôn dùng raw string (tiền tố `r'...'`) khi viết regex trong Python để tránh dấu gạch chéo ngược `\\` bị hiểu lầm là escape sequence của chuỗi."
    },
    {
        "id": 82,
        "category": "Python Regular Expressions",
        "title_en": "How do you compile a regular expression in Python?",
        "title_vi": "Tại sao và khi nào nên biên dịch trước Regular Expression bằng re.compile()?",
        "level": "Mid",
        "short_answer": "Sử dụng hàm `pattern = re.compile(r'regex_pattern', flags)`. Việc biên dịch trước pattern thành đối tượng Regex Object giúp tăng tốc độ thực thi đáng kể khi pattern đó được tái sử dụng nhiều lần trong các vòng lặp, đồng thời giúp code gọn gàng và dễ đọc hơn.",
        "deep_dive": """Cơ chế caching của module `re`:
1. Mặc dù các hàm như <code>re.search()</code> có cơ chế cache nội bộ khoảng 512 patterns gần nhất, việc dùng <code>re.compile()</code> ở cấp module giúp:
   - Tránh việc tra cứu cache liên tục.
   - Định nghĩa rõ ràng các cờ (flags) như <code>re.IGNORECASE</code> (không phân biệt hoa thường), <code>re.MULTILINE</code>, <code>re.VERBOSE</code> (cho phép comment giải thích regex).""",
        "code_example": """import re

# Biên dịch trước mẫu kiểm tra số điện thoại Việt Nam
PHONE_REGEX = re.compile(r'^(?:\\+84|0)(?:3|5|7|8|9)\\d{8}$')

def validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone.strip()))

print(validate_phone("0987654321"))  # True
print(validate_phone("+84912345678")) # True
print(validate_phone("123456"))        # False""",
        "tips": "Hãy nhắc đến cờ `re.VERBOSE` (hoặc `re.X`) — cờ này cho phép xuống dòng và viết comment bên trong chuỗi regex phức tạp, biến những regex khó đọc thành tài liệu cực kỳ dễ bảo trì."
    },
    {
        "id": 83,
        "category": "Python Regular Expressions",
        "title_en": "Give examples of commonly used regex patterns in Python.",
        "title_vi": "Các mẫu Regex phổ biến nhất trong thực tế (Email, Phone, Date, IP, Slug)?",
        "level": "Junior",
        "short_answer": "Các mẫu thông dụng: Email, Số điện thoại Việt Nam, Định dạng ngày `YYYY-MM-DD`, Địa chỉ IPv4, URL và Slug URL.",
        "deep_dive": """Bảng mẫu Regex thực chiến chuẩn:
- <b>Email</b>: <code>^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$</code>
- <b>Ngày YYYY-MM-DD</b>: <code>^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])$</code>
- <b>IPv4 Address</b>: <code>^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$</code>
- <b>Mật khẩu mạnh</b> (tối thiểu 8 ký tự, 1 chữ hoa, 1 chữ thường, 1 số, 1 ký tự đặc biệt): <code>^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$</code>""",
        "code_example": """import re

patterns = {
    "date": r"^\\d{4}-\\d{2}-\\d{2}$",
    "slug": r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
}

print(bool(re.match(patterns["date"], "2026-11-09")))  # True
print(bool(re.match(patterns["slug"], "hoc-python-nang-cao")))  # True""",
        "tips": "Cảnh báo bẫy: Đừng cố viết một regex phức tạp 500 ký tự để validate hoàn hảo chuẩn RFC 5322 của Email. Trong thực tế, chỉ cần regex cơ bản và gửi email kích hoạt xác thực."
    },
    {
        "id": 84,
        "category": "Python Regular Expressions",
        "title_en": "How do you replace text in a string using regular expressions?",
        "title_vi": "Cách thay thế văn bản bằng re.sub() và sử dụng hàm callback thay thế?",
        "level": "Mid",
        "short_answer": "Sử dụng hàm `re.sub(pattern, replacement, string)`. Phần thay thế (`replacement`) có thể là một chuỗi tĩnh, tham chiếu nhóm bắt (ví dụ `\\1`, `\\g<name>`), hoặc một hàm callback nhận vào một `Match Object` để tính toán giá trị thay thế động.",
        "deep_dive": """Sức mạnh của Callback Function trong `re.sub`:
1. Khi truyền một hàm làm đối số thứ hai của <code>re.sub</code>, Python sẽ gọi hàm này cho mỗi lần khớp.
2. Cho phép thực hiện các biến đổi phức tạp như: nhân đôi giá trị số tìm thấy, chuyển đổi tiền tệ, che giấu thông tin nhạy cảm (data masking / anonymization) cho thẻ tín dụng.""",
        "code_example": """import re

text = "Đơn hàng: Áo 200k, Quần 350k, Giày 800k"

# 1. Thay thế đơn giản: Đổi 'k' thành '000 VND'
result1 = re.sub(r'(\\d+)k', r'\\1,000 VND', text)
print(result1)
# Output: Đơn hàng: Áo 200,000 VND, Quần 350,000 VND, Giày 800,000 VND

# 2. Thay thế nâng cao dùng hàm callback: Giảm giá 50% tất cả món hàng
def apply_discount(match):
    original_price = int(match.group(1))
    discounted = original_price // 2
    return f"{discounted}k (Giảm 50%)"

result2 = re.sub(r'(\\d+)k', apply_discount, text)
print(result2)""",
        "tips": "Để giới hạn số lần thay thế, truyền thêm tham số `count=N` (mặc định count=0 là thay thế tất cả)."
    },
    {
        "id": 85,
        "category": "Python Regular Expressions",
        "title_en": "When should you use regular expressions and when should you avoid them?",
        "title_vi": "Khi nào nên dùng Regular Expressions và khi nào TUYỆT ĐỐI NÊN TRÁNH?",
        "level": "Senior",
        "short_answer": "Nên dùng Regex khi: cần tìm kiếm/khớp mẫu phức tạp (email, phone, ngày tháng, bóc tách log). Nên tránh Regex khi: các thao tác chuỗi đơn giản có thể giải quyết bằng hàm string built-in (`in`, `startswith`, `split`), khi parse HTML/XML (dùng `BeautifulSoup`), hoặc khi regex có nguy cơ gây tấn công từ chối dịch vụ ReDoS.",
        "deep_dive": """Tại sao không nên lạm dụng Regex?
1. <b>Hiệu năng</b>: Các phương thức chuỗi của Python (như <code>'abc' in text</code>) được viết bằng C cực kỳ tối ưu, nhanh hơn Regex từ 5 đến 20 lần.
2. <b>Khả năng bảo trì</b>: Câu châm ngôn nổi tiếng của Jamie Zawinski: <i>'Some people, when confronted with a problem, think: I know, I will use regular expressions. Now they have two problems.'</i>
3. <b>Lỗ hổng ReDoS (Regular Expression Denial of Service)</b>:
   - Các biểu thức Regex có cấu trúc lồng nhau (Catastrophic Backtracking, ví dụ: <code>(a+)+$</code>) có thể khiến CPU bị treo 100% khi nhận chuỗi đầu vào độc hại dài.""",
        "code_example": """# ❌ LẠM DỤNG REGEX:
# import re
# if re.match('^https://', url): pass

#  CHUẨN VÀ NHANH HƠN GẤP 10 LẦN:
url = "https://devinterview.io"
if url.startswith("https://"):
    print("Bảo mật HTTPS")

# ❌ TUYỆT ĐỐI KHÔNG DÙNG REGEX ĐỂ PARSE HTML!
# Dùng BeautifulSoup hoặc lxml thay thế""",
        "tips": "Trả lời phỏng vấn thông minh: 'Không dùng Regex để parse HTML/XML vì HTML là ngôn ngữ phi ngữ cảnh (Context-free grammar), Regex chỉ xử lý được ngôn ngữ chính quy (Regular language)'."
    },
    {
        "id": 86,
        "category": "Python Environment and Configuration",
        "title_en": "How do you manage Python environments using venv?",
        "title_vi": "Cách quản lý môi trường ảo bằng module venv chuẩn của Python?",
        "level": "Junior",
        "short_answer": "Dùng module tích hợp `venv`: 1. Tạo môi trường: `python3 -m venv .venv`, 2. Kích hoạt: `source .venv/bin/activate` (macOS/Linux) hoặc `.venv\\Scripts\\activate` (Windows), 3. Cài đặt thư viện: `pip install <pkg>`, 4. Hủy kích hoạt: `deactivate`.",
        "deep_dive": """Cơ chế hoạt động của virtual environment:
1. Thư mục <code>.venv</code> chứa một bản copy (hoặc symlink) của trình thông dịch Python và thư mục <code>site-packages</code> riêng biệt.
2. Khi kích hoạt môi trường, biến môi trường <code>PATH</code> của shell được cập nhật để trỏ tới <code>.venv/bin</code> trước các thư mục hệ thống. Khi gõ <code>python</code> hoặc <code>pip</code>, OS sẽ ưu tiên dùng phiên bản cô lập trong <code>.venv</code>.""",
        "code_example": """# Các lệnh dòng lệnh chuẩn (Terminal Commands):
# 1. Tạo môi trường ảo tên .venv
# python3 -m venv .venv

# 2. Kích hoạt trên macOS / Linux:
# source .venv/bin/activate

# 3. Kiểm tra đường dẫn python đang dùng:
# which python
# -> /Users/macos/myproject/.venv/bin/python

# 4. Thoát khỏi môi trường ảo:
# deactivate""",
        "tips": "Luôn thêm `.venv/` vào file `.gitignore` để tránh commit hàng nghìn file thư viện vào git repository."
    },
    {
        "id": 87,
        "category": "Python Environment and Configuration",
        "title_en": "What is a virtual environment and when should you use one?",
        "title_vi": "Môi trường ảo (Virtual Environment) là gì và tại sao bắt buộc phải sử dụng?",
        "level": "Junior",
        "short_answer": "Môi trường ảo là một không gian độc lập khép kín chứa trình thông dịch Python và các package thư viện riêng biệt cho từng dự án. Bắt buộc sử dụng để ngăn chặn xung đột phiên bản (Dependency Hell) giữa các dự án khác nhau và bảo vệ môi trường Python của hệ điều hành gốc.",
        "deep_dive": """Tại sao cài package toàn cục (Global) là thảm họa?
1. Dự án A cần <code>Django 3.2</code> để bảo trì hệ thống cũ. Dự án B cần <code>Django 5.0</code> cho tính năng mới. Nếu không có môi trường ảo, bạn không thể chạy đồng thời 2 dự án trên cùng một máy!
2. Trên các hệ điều hành hiện đại (macOS Sonoma, Ubuntu 24.04+), lệnh <code>pip install</code> ở cấp hệ thống bị khóa mặc định với lỗi <code>externally-managed-environment</code> (PEP 668) để tránh làm hỏng các công cụ của hệ điều hành.""",
        "code_example": """# Minh họa xung đột nếu không dùng venv:
# Project_A: yêu cầu urllib3 == 1.26.15
# Project_B: yêu cầu urllib3 >= 2.0.0
# => Giải pháp: Mỗi project tạo 1 .venv riêng biệt.""",
        "tips": "Nêu rõ tiêu chuẩn PEP 668: Môi trường hệ thống được bảo vệ, mọi thao tác cài đặt thư viện phải diễn ra bên trong virtual environment."
    },
    {
        "id": 88,
        "category": "Python Environment and Configuration",
        "title_en": "How do you install Python packages?",
        "title_vi": "Các cách cài đặt Python package qua pip và các công cụ hiện đại?",
        "level": "Junior",
        "short_answer": "Cách thông dụng nhất là dùng trình quản lý gói `pip`: `pip install package_name` (tải từ kho lưu trữ PyPI). Có thể cài theo phiên bản cụ thể (`pip install django==5.0.2`), cài từ file (`pip install -r requirements.txt`), hoặc cài từ Git repository.",
        "deep_dive": """Các công cụ quản lý package thế hệ mới (2026):
1. <b>pip & wheel</b>: Cài đặt các gói nhị phân <code>.whl</code> đã biên dịch sẵn mà không cần cài trình biên dịch C trên máy.
2. <b>uv (Viết bằng Rust)</b>: Công cụ cài đặt package nhanh nhất thế giới hiện nay, nhanh gấp 10-100 lần <code>pip</code>.
3. <b>Poetry & PDM</b>: Quản lý dependency theo chuẩn <code>pyproject.toml</code> (PEP 518/621), hỗ trợ giải quyết xung đột dependency và tạo file lock tự động.""",
        "code_example": """# 1. Cài đặt package cơ bản
# pip install requests

# 2. Cài đặt theo phiên bản chính xác
# pip install fastapi==0.110.0

# 3. Cài đặt chế độ phát triển (Editable Mode) từ mã nguồn local:
# pip install -e .

# 4. Cài đặt siêu tốc với công cụ uv hiện đại:
# uv pip install -r requirements.txt""",
        "tips": "Luôn dùng lệnh `python -m pip install <pkg>` thay vì chỉ gõ `pip install <pkg>` để đảm bảo thư viện được cài đúng vào phiên bản Python hiện tại đang chạy."
    },
    {
        "id": 89,
        "category": "Python Environment and Configuration",
        "title_en": "How do you manage dependencies in Python projects?",
        "title_vi": "Cách quản lý Dependencies trong dự án Python chuyên nghiệp?",
        "level": "Mid",
        "short_answer": "Cách truyền thống là dùng `requirements.txt` kết hợp `pip freeze`. Cách tiêu chuẩn công nghiệp hiện đại là sử dụng file `pyproject.toml` kết hợp với các công cụ quản lý khóa phụ thuộc (Lockfile) như `Poetry`, `Pipenv`, hoặc `uv` để đảm bảo môi trường phát triển và production đồng nhất 100% (deterministic builds).",
        "deep_dive": """Tại sao `requirements.txt` không đủ cho Production?
1. <b>Vấn đề Sub-dependencies trôi nổi</b>: Nếu bạn chỉ ghi <code>requests==2.31.0</code>, thì các thư viện con của nó (như <code>urllib3</code>, <code>certifi</code>) có thể bị nâng cấp ngầm lên phiên bản mới hơn khi deploy, dẫn đến lỗi bất ngờ ở production.
2. <b>Giải pháp Lockfile (<code>poetry.lock</code> / <code>requirements.lock</code>)</b>:
   - Ghi lại chính xác SHA-256 hash và phiên bản của TẤT CẢ các thư viện chính và thư viện con.
3. <b>Tách biệt môi trường Development và Production</b>:
   - Không cài các thư viện test (pytest, black, flake8) lên server production.""",
        "code_example": """# Cấu trúc file pyproject.toml chuẩn PEP 621:
# [project]
# name = "my-awesome-api"
# version = "1.0.0"
# dependencies = [
#     "fastapi>=0.100.0",
#     "uvicorn[standard]>=0.28.0",
#     "pydantic>=2.0.0",
# ]

# [project.optional-dependencies]
# dev = [
#     "pytest>=8.0.0",
#     "ruff>=0.3.0",
# ]""",
        "tips": "Nếu phỏng vấn hỏi về quản lý dependency hiện đại, hãy nhắc đến `Poetry` hoặc công cụ mới nhất `uv` (Astral) với file `uv.lock`."
    },
    {
        "id": 90,
        "category": "Python Environment and Configuration",
        "title_en": "What is Docker and how do you use it with Python?",
        "title_vi": "Docker là gì và các Best Practices khi đóng gói ứng dụng Python vào Docker container?",
        "level": "Mid",
        "short_answer": "Docker là nền tảng ảo hóa cấp hệ điều hành (Containerization) cho phép đóng gói ứng dụng Python cùng toàn bộ thư viện, môi trường và cấu hình hệ thống vào một Container độc lập. Nó giải quyết triệt để vấn đề kinh điển: 'Nó chạy được trên máy tôi nhưng không chạy được trên server!'.",
        "deep_dive": """Các Best Practices tối quan trọng khi viết Dockerfile cho Python:
1. <b>Sử dụng Base Image nhẹ</b>: Dùng <code>python:3.12-slim</code> thay vì image đầy đủ (giảm kích thước từ 1GB xuống dưới 150MB).
2. <b>Tận dụng Docker Layer Caching</b>: Copy file <code>requirements.txt</code> và chạy <code>pip install</code> TRƯỚC KHI copy toàn bộ mã nguồn. Khi bạn sửa code Python, Docker không cần phải tải lại thư viện.
3. <b>Tạo Non-root User</b>: Tuyệt đối không chạy ứng dụng dưới quyền <code>root</code> bên trong container vì lý do an toàn bảo mật.
4. <b>Cấu hình cờ Python</b>:
   - <code>PYTHONDONTWRITEBYTECODE=1</code>: Không sinh file .pyc.
   - <code>PYTHONUNBUFFERED=1</code>: Đẩy log ra stdout ngay lập tức không bị đệm.""",
        "code_example": """# Dockerfile chuẩn Production cho Python Web App:
FROM python:3.12-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Tận dụng Docker Cache cho dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy mã nguồn ứng dụng
COPY . .

# 3. Tạo user không có quyền root vì bảo mật
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]""",
        "tips": "Nhớ thêm `.dockerignore` để loại trừ `__pycache__`, `.venv`, `.git` nhằm giảm dung lượng build context của Docker."
    },
    {
        "id": 91,
        "category": "Python and Data Science",
        "title_en": "What is data science and how is Python used in it?",
        "title_vi": "Khoa học dữ liệu (Data Science) là gì và tại sao Python là ngôn ngữ số 1 trong ngành này?",
        "level": "Junior",
        "short_answer": "Data Science là lĩnh vực liên ngành kết hợp thống kê, toán học, lập trình và nghiệp vụ để trích xuất tri thức từ dữ liệu. Python là ngôn ngữ số 1 nhờ cú pháp trực quan, cộng đồng khổng lồ và hệ sinh thái thư viện hoàn chỉnh từ thu thập dữ liệu, làm sạch, phân tích, trực quan hóa đến triển khai Machine Learning/AI.",
        "deep_dive": """Các chặng trong quy trình Data Science chuẩn với Python:
1. <b>Thu thập dữ liệu (Data Ingestion)</b>: <code>requests</code>, <code>BeautifulSoup</code>, <code>SQLAlchemy</code>.
2. <b>Làm sạch & Biến đổi (Data Wrangling)</b>: <code>Pandas</code>, <code>NumPy</code>.
3. <b>Phân tích khám phá (EDA & Visualization)</b>: <code>Matplotlib</code>, <code>Seaborn</code>, <code>Plotly</code>.
4. <b>Xây dựng mô hình (Modeling)</b>: <code>Scikit-learn</code>, <code>Statsmodels</code>.
5. <b>Deep Learning & GenAI</b>: <code>PyTorch</code>, <code>TensorFlow</code>, <code>Transformers</code>.
6. <b>Triển khai API (Deployment)</b>: <code>FastAPI</code>, <code>Flask</code>, <code>Docker</code>.""",
        "code_example": """# Ví dụ pipeline Data Science thu nhỏ trong 4 dòng:
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Nạp và tiền xử lý
df = pd.DataFrame({"dien_tich": [50, 60, 80, 100], "gia": [1.5, 1.8, 2.5, 3.2]})

# 2. Huấn luyện mô hình hồi quy dự đoán giá nhà
model = LinearRegression().fit(df[["dien_tich"]], df["gia"])

# 3. Dự đoán cho căn nhà 75m2
predicted_price = model.predict([[75]])
print(f"Giá dự đoán căn 75m2: {predicted_price[0]:.2f} tỷ VND")""",
        "tips": "Khi được hỏi so sánh Python và R: R mạnh về thống kê học thuật thuần túy, nhưng Python vượt trội hoàn toàn về khả năng tích hợp hệ thống production và kỹ thuật phần mềm."
    },
    {
        "id": 92,
        "category": "Python and Data Science",
        "title_en": "How do you clean and preprocess data in Python?",
        "title_vi": "Quy trình làm sạch và tiền xử lý dữ liệu (Data Preprocessing) trong Python?",
        "level": "Mid",
        "short_answer": "Quy trình làm sạch dữ liệu chuẩn gồm 5 bước: 1. Xử lý giá trị bị thiếu (Missing values), 2. Xóa bỏ hoặc xử lý dữ liệu trùng lặp (Duplicates), 3. Chuẩn hóa kiểu dữ liệu (Type casting), 4. Xử lý giá trị ngoại lai (Outliers), 5. Chuẩn hóa thang đo (Scaling/Normalization) và mã hóa biến phân loại (Encoding).",
        "deep_dive": """Các kỹ thuật tiền xử lý chi tiết với Pandas & Scikit-learn:
1. <b>Xử lý Missing Data</b>:
   - Điền giá trị trung vị (Median) cho dữ liệu số bị lệch, hoặc Mode cho dữ liệu phân loại.
2. <b>Mã hóa biến phân loại (Categorical Encoding)</b>:
   - <i>One-Hot Encoding</i>: Dùng <code>pd.get_dummies()</code> hoặc <code>OneHotEncoder</code> cho biến không có thứ bậc (vd: Đỏ, Xanh).
   - <i>Label/Ordinal Encoding</i>: Cho biến có thứ bậc (vd: Tiểu học, Trung học, Đại học).
3. <b>Feature Scaling</b>:
   - <code>StandardScaler</code>: Chuẩn hóa về mean=0, std=1.
   - <code>MinMaxScaler</code>: Đưa về thang đo [0, 1].""",
        "code_example": """import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({
    "tuoi": [25, None, 30, 22, 200],  # 200 là outlier, None là missing
    "thanh_pho": ["HN", "HCM", "HN", "DN", "HN"]
})

# 1. Điền giá trị thiếu bằng trung vị
df["tuoi"] = df["tuoi"].fillna(df["tuoi"].median())

# 2. Xử lý Outlier (Cắt ngưỡng tuổi > 100)
df = df[df["tuoi"] < 100]

# 3. One-hot encoding cột 'thanh_pho'
df_processed = pd.get_dummies(df, columns=["thanh_pho"], drop_first=True)
print("Dữ liệu sau khi làm sạch:\\n", df_processed)""",
        "tips": "Luôn nhớ: Fit scaler trên tập Train rồi mới dùng để transform tập Test/Validation để tránh rò rỉ dữ liệu (Data Leakage)."
    },
    {
        "id": 93,
        "category": "Python and Data Science",
        "title_en": "What is a DataFrame in pandas?",
        "title_vi": "Pandas DataFrame là gì và cách truy xuất dữ liệu với loc và iloc?",
        "level": "Junior",
        "short_answer": "DataFrame là cấu trúc dữ liệu bảng 2 chiều có kích thước thay đổi được, gồm các hàng (rows) và cột (columns) có gắn nhãn. Để truy xuất dữ liệu: `loc` dùng nhãn tên (Label-based indexing), còn `iloc` dùng chỉ số nguyên vị trí (Integer position-based indexing).",
        "deep_dive": """So sánh chi tiết `loc` vs `iloc`:
1. <b><code>df.loc[row_label, col_label]</code></b>:
   - Truy xuất bằng tên của hàng và tên của cột.
   - Khi cắt lát (slicing) <code>df.loc['a':'c']</code>: Bao gồm CẢ điểm kết thúc (inclusive).
2. <b><code>df.iloc[row_idx, col_idx]</code></b>:
   - Truy xuất hoàn toàn bằng số nguyên từ 0 đến N-1.
   - Khi cắt lát <code>df.iloc[0:3]</code>: KHÔNG bao gồm điểm kết thúc (exclusive), giống hệt slicing trong Python List thông thường.""",
        "code_example": """import pandas as pd

df = pd.DataFrame(
    {"diem_toan": [8.5, 9.0, 7.5], "diem_van": [7.0, 8.0, 6.5]},
    index=["hoc_sinh_A", "hoc_sinh_B", "hoc_sinh_C"]
)

# 1. Dùng loc: Truy xuất theo TÊN nhãn
print("Điểm toán học sinh B (loc):", df.loc["hoc_sinh_B", "diem_toan"])  # 9.0

# 2. Dùng iloc: Truy xuất theo VỊ TRÍ chỉ số số nguyên
print("Hàng 0, Cột 1 (iloc):", df.iloc[0, 1])  # 7.0

# 3. Lọc theo điều kiện boolean
gioi_toan = df[df["diem_toan"] >= 8.5]
print("Học sinh giỏi toán:\\n", gioi_toan)""",
        "tips": "Đừng bao giờ dùng `df['col'][row]` để gán giá trị vì sẽ bị cảnh báo `SettingWithCopyWarning`. Luôn dùng `df.loc[row, 'col'] = val`."
    },
    {
        "id": 94,
        "category": "Python and Data Science",
        "title_en": "How do you handle missing data with pandas?",
        "title_vi": "Cách phát hiện và xử lý dữ liệu khuyết thiếu (Missing Data / NaN) trong Pandas?",
        "level": "Junior",
        "short_answer": "Trong Pandas: 1. Phát hiện: `df.isna()` hoặc `df.isnull()`, 2. Thống kê: `df.isna().sum()`, 3. Loại bỏ: `df.dropna()`, 4. Điền giá trị: `df.fillna(value)` hoặc nội suy dữ liệu chuỗi thời gian bằng `df.interpolate()`.",
        "deep_dive": """Chiến lược xử lý missing data thông minh:
1. <b>Khi nào nên Drop (`dropna`)?</b>
   - Khi tỷ lệ missing của dòng đó rất nhỏ (< 2%) hoặc missing ở cột mục tiêu nhãn (target variable).
   - Nếu một cột bị mất > 60% dữ liệu: Cân nhắc xóa bỏ cả cột đó.
2. <b>Khi nào nên Impute (`fillna`)?</b>
   - Dữ liệu số liên tục: Điền bằng <code>mean()</code> (nếu phân phối chuẩn) hoặc <code>median()</code> (nếu có outlier lệch).
   - Dữ liệu chuỗi thời gian (Time-series): Điền giá trị của ngày trước đó (<code>method='ffill'</code> - forward fill).
   - Dữ liệu phân loại: Điền giá trị xuất hiện nhiều nhất (<code>mode()[0]</code>) hoặc điền nhãn 'Unknown'.""",
        "code_example": """import pandas as pd
import numpy as np

df = pd.DataFrame({
    "san_pham": ["Laptop", "Chuột", "Bàn phím", None],
    "gia": [20_000_000, np.nan, 1_500_000, 500_000]
})

# 1. Thống kê số lượng rỗng theo từng cột:
print("Thống kê missing:\\n", df.isna().sum())

# 2. Điền giá trị thiếu của cột 'gia' bằng trung vị:
df["gia"] = df["gia"].fillna(df["gia"].median())

# 3. Loại bỏ các dòng mà tên 'san_pham' bị rỗng:
df_clean = df.dropna(subset=["san_pham"])
print("\\nDataFrame sau khi xử lý missing:\\n", df_clean)""",
        "tips": "Lưu ý rằng trong Python `np.nan == np.nan` sẽ trả về `False`! Vì vậy không thể kiểm tra missing bằng `if val == np.nan`, mà phải dùng `np.isnan(val)` hoặc `pd.isna(val)`."
    },
    {
        "id": 95,
        "category": "Python and Data Science",
        "title_en": "How can you perform data aggregation in pandas?",
        "title_vi": "Cách thực hiện nhóm và tổng hợp dữ liệu (GroupBy & Aggregation) trong Pandas?",
        "level": "Mid",
        "short_answer": "Sử dụng mô hình 'Split-Apply-Combine' thông qua phương thức `df.groupby('column').agg()`. Ta có thể áp dụng các hàm tính toán tích hợp (`mean`, `sum`, `count`, `std`, `min`, `max`) hoặc truyền hàm custom lambda cho từng cột riêng biệt.",
        "deep_dive": """Mô hình Split-Apply-Combine:
1. <b>Split</b>: Chia DataFrame thành các nhóm nhỏ dựa trên giá trị của một hoặc nhiều cột.
2. <b>Apply</b>: Áp dụng các hàm tính toán thống kê độc lập trên từng nhóm.
3. <b>Combine</b>: Gom các kết quả lại thành một DataFrame mới.
4. <b>Phương thức <code>.agg()</code> nâng cao</b>:
   - Cho phép tính nhiều chỉ số thống kê cùng lúc trên nhiều cột với cú pháp Dictionary: <code>{'gia': ['mean', 'max'], 'so_luong': 'sum'}</code>.""",
        "code_example": """import pandas as pd

orders = pd.DataFrame({
    "khu_vuc": ["Miền Bắc", "Miền Nam", "Miền Bắc", "Miền Trung", "Miền Nam"],
    "doanh_thu": [100, 250, 150, 80, 300],
    "don_hang": [1, 2, 1, 1, 3]
})

# Tổng hợp nhiều chỉ số cùng lúc theo khu vực:
report = orders.groupby("khu_vuc").agg(
    tong_doanh_thu=("doanh_thu", "sum"),
    trung_binh_don=("doanh_thu", "mean"),
    tong_so_don=("don_hang", "sum")
)

print(report)""",
        "tips": "Nếu muốn giữ nguyên số lượng hàng ban đầu sau khi tính toán theo nhóm, hãy dùng `.transform()` thay vì `.agg()`."
    },
    {
        "id": 96,
        "category": "Python and Machine Learning",
        "title_en": "What is scikit-learn and how do you use it?",
        "title_vi": "Scikit-learn là gì và thiết kế API chuẩn mực (Estimator - Transformer - Predictor)?",
        "level": "Junior",
        "short_answer": "Scikit-learn là thư viện Machine Learning mã nguồn mở hàng đầu trong Python cho các thuật toán học máy cổ điển. Thiết kế API của nó cực kỳ nhất quán xoay quanh 3 phương thức chuẩn: `fit()` (huấn luyện mô hình), `transform()` (biến đổi dữ liệu), và `predict()` (dự đoán nhãn mới).",
        "deep_dive": """3 giao diện cốt lõi (Core Interfaces) của Scikit-learn:
1. <b>Estimator</b>: Bất kỳ đối tượng nào học từ dữ liệu thông qua phương thức <code>fit(X, y)</code>.
2. <b>Transformer</b>: Dùng để tiền xử lý và kỹ nghệ đặc trưng (Feature Engineering), hỗ trợ <code>transform(X)</code> hoặc gộp <code>fit_transform(X)</code>.
3. <b>Predictor</b>: Dự đoán kết quả trên dữ liệu mới bằng <code>predict(X)</code> hoặc xác suất bằng <code>predict_proba(X)</code>.
4. <b>Pipeline (<code>sklearn.pipeline.Pipeline</code>)</b>:
   - Ghép nối các bước tiền xử lý và mô hình thành một khối duy nhất, chống rò rỉ dữ liệu (data leakage) khi cross-validation.""",
        "code_example": """from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

# 1. Tạo dữ liệu mẫu
X, y = make_classification(n_samples=500, n_features=4, random_state=42)

# 2. Xây dựng Pipeline chuẩn mực (Scaler -> Model)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression())
])

# 3. Huấn luyện toàn bộ pipeline với 1 lệnh duy nhất
pipeline.fit(X, y)

# 4. Dự đoán trên dữ liệu mới
sample = [[0.5, -1.2, 0.8, -0.4]]
print("Nhãn dự đoán:", pipeline.predict(sample))""",
        "tips": "Luôn khuyến khích sử dụng `sklearn.pipeline.Pipeline` trong bài phỏng vấn để thể hiện tư duy viết code ML sạch, có khả năng tái sử dụng và deploy tốt."
    },
    {
        "id": 97,
        "category": "Python and Machine Learning",
        "title_en": "How do you handle feature selection in Python?",
        "title_vi": "Các phương pháp lựa chọn đặc trưng (Feature Selection) trong Machine Learning?",
        "level": "Mid",
        "short_answer": "Lựa chọn đặc trưng giúp giảm chiều dữ liệu, tránh overfitting và tăng tốc độ huấn luyện. Có 3 nhóm phương pháp chính: 1. Filter Methods (dựa trên tương quan Pearson, ANOVA, Mutual Information), 2. Wrapper Methods (RFE - Recursive Feature Elimination), 3. Embedded/Intrinsic Methods (Lasso L1 Regularization, Feature Importance từ Random Forest/XGBoost).",
        "deep_dive": """So sánh 3 nhóm phương pháp:
1. <b>Filter Methods</b> (Nhanh nhất):
   - Đánh giá từng biến độc lập với mô hình. Dùng <code>SelectKBest</code> với <code>f_classif</code> hoặc <code>chi2</code>.
2. <b>Wrapper Methods</b> (Chính xác nhưng tốn CPU):
   - Huấn luyện mô hình lặp đi lặp lại để tìm tập đặc trưng tối ưu. Ví dụ: <code>RFE(estimator=RandomForestClassifier())</code>.
3. <b>Embedded Methods</b> (Tối ưu cân bằng):
   - Quá trình chọn đặc trưng diễn ra ngay trong lúc model huấn luyện.
   - Hồi quy Lasso (L1) ép trọng số của các biến không quan trọng về đúng bằng 0.""",
        "code_example": """from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
print("Số đặc trưng ban đầu:", X.shape[1])  # 4

# Chọn 2 đặc trưng quan trọng nhất bằng ANOVA F-test
selector = SelectKBest(score_func=f_classif, k=2)
X_selected = selector.fit_transform(X, y)

print("Số đặc trưng sau khi lọc:", X_selected.shape[1])  # 2
print("Điểm số của từng đặc trưng:", selector.scores_)""",
        "tips": "Nếu dữ liệu có nhiều biến phân loại bị tương quan cao (Multicollinearity), hãy nhắc đến việc kiểm tra ma trận tương quan (Correlation Matrix) và chỉ số VIF (Variance Inflation Factor)."
    },
    {
        "id": 98,
        "category": "Python and Machine Learning",
        "title_en": "What is cross-validation and how do you perform it in Python?",
        "title_vi": "K-Fold Cross-Validation là gì và cách triển khai trong Scikit-learn?",
        "level": "Junior",
        "short_answer": "Cross-Validation (Kiểm định chéo) là kỹ thuật đánh giá hiệu năng mô hình một cách khách quan, tránh phụ thuộc vào một lần chia Train/Test ngẫu nhiên may rủi. Trong K-Fold, dữ liệu được chia thành K phần bằng nhau: mô hình được huấn luyện trên K-1 phần và kiểm thử trên 1 phần còn lại, lặp lại K lần rồi lấy điểm trung bình.",
        "deep_dive": """Các biến thể Cross-Validation quan trọng:
1. <b>K-Fold</b>: Chia ngẫu nhiên $K$ phần (thường $K=5$ hoặc $K=10$).
2. <b>Stratified K-Fold (Bắt buộc cho Imbalanced Classification)</b>:
   - Đảm bảo tỷ lệ các lớp (class distribution) ở mỗi fold con đều giống hệt tỷ lệ trên toàn bộ tập dữ liệu gốc.
3. <b>Time Series Split</b>:
   - Dành cho dữ liệu chuỗi thời gian, không được xáo trộn ngẫu nhiên mà phải train trên quá khứ và test trên tương lai.""",
        "code_example": """from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
model = LogisticRegression(max_iter=200)

# Thực hiện 5-Fold Stratified Cross-Validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")

print("Điểm từng fold:", scores)
print(f"Độ chính xác trung bình: {scores.mean():.4f} (+/- {scores.std():.4f})")""",
        "tips": "Nếu dữ liệu mất cân bằng nghiêm trọng (ví dụ phát hiện gian lận: 99% sạch, 1% gian lận), KHÔNG BAO GIỜ dùng K-Fold thường và không dùng metric accuracy! Phải dùng `StratifiedKFold` và metric `f1-score` hoặc `roc_auc`."
    },
    {
        "id": 99,
        "category": "Python and Machine Learning",
        "title_en": "How do you save a trained machine learning model with Python?",
        "title_vi": "Cách lưu và tải mô hình Machine Learning đã huấn luyện (Model Persistence)?",
        "level": "Junior",
        "short_answer": "Có 2 cách thông dụng nhất: 1. Sử dụng thư viện `joblib` (tối ưu nhất cho các mô hình Scikit-learn chứa nhiều mảng số lớn NumPy), 2. Sử dụng module tích hợp sẵn `pickle`. Đối với Deep Learning, dùng `torch.save()` (PyTorch) hoặc `model.save()` (Keras/HDF5/SavedModel).",
        "deep_dive": """Tại sao nên ưu tiên `joblib` hơn `pickle` cho Scikit-learn?
1. <code>joblib.dump()</code> được thiết kế chuyên biệt để nén và ghi các mảng dữ liệu lớn của NumPy cực kỳ nhanh và tốn ít dung lượng ổ đĩa hơn pickle thuần.
2. <b>Định dạng hiện đại ONNX (Open Neural Network Exchange)</b>:
   - Nếu cần triển khai mô hình đa nền tảng (chạy trên C++, C#, Java hoặc mobile) với tốc độ suy luận (inference) tối đa, lưu mô hình sang định dạng <code>.onnx</code> là giải pháp chuẩn doanh nghiệp hiện nay.""",
        "code_example": """import joblib
from sklearn.ensemble import RandomForestClassifier

# 1. Huấn luyện mô hình mẫu
clf = RandomForestClassifier(n_estimators=10)
clf.fit([[1, 2], [3, 4]], [0, 1])

# 2. Lưu mô hình ra đĩa
model_path = "rf_model.joblib"
joblib.dump(clf, model_path)
print("Đã lưu model vào:", model_path)

# 3. Tải lại model trong môi trường production / API:
loaded_model = joblib.load(model_path)
prediction = loaded_model.predict([[1, 2]])
print("Dự đoán từ model đã tải:", prediction)""",
        "tips": "Cảnh báo tương thích phiên bản: File joblib/pickle phụ thuộc vào phiên bản thư viện! Nếu train bằng `scikit-learn 1.4` nhưng server deploy dùng `1.2`, có thể văng lỗi UnpicklingError. Hãy cố định chính xác version trong Docker."
    },
    {
        "id": 100,
        "category": "Python and Machine Learning",
        "title_en": "What are the steps involved in training a machine learning model with Python?",
        "title_vi": "Toàn bộ quy trình từ đầu đến cuối (End-to-End Pipeline) huấn luyện mô hình Machine Learning?",
        "level": "Senior",
        "short_answer": "Quy trình End-to-End gồm 7 bước cốt lõi: 1. Định nghĩa bài toán kinh doanh (Problem Definition), 2. Thu thập & Khám phá dữ liệu (Data Ingestion & EDA), 3. Tiền xử lý & Kỹ nghệ đặc trưng (Preprocessing & Feature Engineering), 4. Huấn luyện mô hình (Model Training & Hyperparameter Tuning), 5. Đánh giá kiểm định (Evaluation & Validation), 6. Đóng gói & Triển khai (Deployment / MLOps), 7. Giám sát độ trôi dữ liệu (Monitoring & Drift Detection).",
        "deep_dive": """Chi tiết 7 bước chuẩn công nghiệp:
1. <b>Hiểu bài toán</b>: Xác định loại bài toán (Supervised: Classification, Regression; Unsupervised: Clustering) và metric đánh giá kinh doanh (Accuracy, Precision, Recall, F1, ROC-AUC, RMSE).
2. <b>EDA & Data Cleaning</b>: Trực quan hóa tương quan, xử lý missing values, ngoại lai.
3. <b>Feature Engineering</b>: Mã hóa, scaling, tạo biến mới từ domain knowledge. Đóng gói vào <code>Pipeline</code>.
4. <b>Train & Tuning</b>: Dùng <code>GridSearchCV</code> hoặc <code>Optuna</code> để tối ưu siêu tham số.
5. <b>Đánh giá trên tập Test độc lập</b>: Tránh hoàn toàn Overfitting.
6. <b>Triển khai MLOps</b>: Đóng gói API với FastAPI, Container hóa bằng Docker, quản lý vòng đời mô hình với MLflow.
7. <b>Giám sát Production</b>: Theo dõi Model Drift và Data Drift để kích hoạt retrain tự động.""",
        "code_example": """# Quy trình End-to-End mẫu với Pipeline + Hyperparameter Tuning:
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# 1. Dữ liệu
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Xây dựng Pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", GradientBoostingClassifier(random_state=42))
])

# 3. Tinh chỉnh siêu tham số
param_grid = {"model__n_estimators": [50, 100], "model__learning_rate": [0.05, 0.1]}
grid = GridSearchCV(pipe, param_grid, cv=3, scoring="f1")
grid.fit(X_train, y_train)

# 4. Đánh giá chất lượng
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
print("Báo cáo đánh giá mô hình:\\n", classification_report(y_test, y_pred))""",
        "tips": "Ứng viên Senior luôn nói về MLOps: Sau khi mô hình có accuracy cao trên máy dev, làm sao để đóng gói, kiểm thử tự động CI/CD, theo dõi model drift trên production và tự động tái huấn luyện."
    }
]
