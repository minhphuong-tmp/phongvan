# -*- coding: utf-8 -*-
# Part 2: Q26 to Q50 (Advanced Concepts Part 2, OOP, Debugging & Testing)

DATA_PART_2 = [
    {
        "id": 26,
        "category": "Python Advanced Concepts",
        "title_en": "What is the Global Interpreter Lock (GIL)?",
        "title_vi": "Global Interpreter Lock (GIL) trong Python là gì và ảnh hưởng thế nào đến hiệu năng?",
        "level": "Senior",
        "short_answer": "GIL là cơ chế khóa mutex được sử dụng trong CPython để đảm bảo tại một thời điểm chỉ có duy nhất MỘT luồng (thread) được quyền thực thi bytecode Python. GIL ngăn chặn race condition trong cơ chế đếm tham chiếu (Reference Counting) của bộ nhớ CPython, nhưng khiến các tác vụ CPU-bound không thể tận dụng đa nhân CPU khi dùng đa luồng.",
        "deep_dive": """Phân tích chuyên sâu về GIL:
1. <b>Tại sao CPython cần GIL?</b>
   - Cơ chế quản lý bộ nhớ của CPython dựa vào <code>ob_refcnt</code>. Nếu không có GIL, khi nhiều luồng cùng tăng/giảm refcount sẽ dẫn đến Memory Leak hoặc Crash do giải phóng bộ nhớ sai thời điểm. Dùng 1 khóa toàn cục GIL đơn giản và nhanh hơn nhiều so với việc đặt lock trên từng object riêng lẻ.
2. <b>Tác động tới 2 loại tác vụ</b>:
   - <b>I/O-Bound</b> (gọi API, đọc file, DB): GIL KHÔNG PHẢI VẤN ĐỀ! Khi một thread chờ I/O, nó sẽ tự động nhả GIL cho thread khác chạy.
   - <b>CPU-Bound</b> (tính toán, xử lý ảnh, nén dữ liệu): GIL khiến việc thêm luồng thậm chí còn CHẬM HƠN chạy đơn luồng do overhead tranh chấp và chuyển đổi GIL (GIL contention).
3. <b>Cách vượt qua GIL</b>:
   - Dùng <code>multiprocessing</code> (mỗi process có 1 GIL riêng).
   - Đẩy tính toán xuống C/C++ Extension hoặc thư viện NumPy, Cython (các thư viện này tự nhả GIL khi chạy mã C).
   - Python 3.13+ bắt đầu hỗ trợ bản thử nghiệm Free-threaded Python (PEP 703: No-GIL).""",
        "code_example": """import time
from threading import Thread
from multiprocessing import Process

def cpu_task(n):
    count = 0
    for i in range(n):
        count += i
    return count

N = 20_000_000

# 1. Chạy đa luồng (Bị GIL cản trở, không nhanh hơn đơn luồng)
t1 = Thread(target=cpu_task, args=(N,))
t2 = Thread(target=cpu_task, args=(N,))
start = time.perf_counter()
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Threading time: {time.perf_counter() - start:.2f}s")

# 2. Chạy đa tiến trình (Vượt qua GIL, tận dụng 2 nhân CPU thật)
if __name__ == "__main__":
    p1 = Process(target=cpu_task, args=(N,))
    p2 = Process(target=cpu_task, args=(N,))
    start = time.perf_counter()
    p1.start(); p2.start()
    p1.join(); p2.join()
    print(f"Multiprocessing time: {time.perf_counter() - start:.2f}s (Nhanh gấp đôi!)")""",
        "tips": "Nếu nhà tuyển dụng hỏi 'Python 3.13 có gì mới về GIL?', hãy tự tin nhắc tới PEP 703 (Making the Global Interpreter Lock Optional in CPython - No-GIL build)."
    },
    {
        "id": 27,
        "category": "Python Advanced Concepts",
        "title_en": "How would you optimize the performance of a Python application?",
        "title_vi": "Bạn sẽ tối ưu hóa hiệu năng của một ứng dụng Python như thế nào trong thực tế?",
        "level": "Senior",
        "short_answer": "Quy trình tối ưu chuẩn gồm 5 bước: 1. Đo lường (Profiling) để tìm đúng điểm nghẽn (bottleneck), 2. Tối ưu thuật toán & cấu trúc dữ liệu, 3. Tận dụng Caching & Lazy Evaluation, 4. Áp dụng Concurrency/Parallelism (AsyncIO cho I/O, Multiprocessing cho CPU), 5. Dùng thư viện C cấp thấp (NumPy, Cython, Polars) hoặc chuyển sang JIT (PyPy).",
        "deep_dive": """Các chiến lược tối ưu hóa chuyên sâu:
1. <b>Profiling trước khi tối ưu (Never Guess)</b>:
   - Dùng <code>cProfile</code>, <code>line_profiler</code> để đo thời gian từng dòng code.
   - Dùng <code>memory_profiler</code> hoặc <code>tracemalloc</code> để đo mức tiêu thụ RAM.
2. <b>Cấu trúc dữ liệu & Thuật toán</b>:
   - Đổi phép tìm kiếm từ $O(n)$ trên List sang $O(1)$ trên Set hoặc Dict.
   - Dùng <code>collections.deque</code> cho thao tác thêm/bớt ở đầu mảng thay vì <code>list.pop(0)</code> ($O(1)$ vs $O(n)$).
   - Dùng <code>__slots__</code> cho các class tạo hàng triệu instance.
3. <b>Caching thông minh</b>:
   - Dùng <code>@functools.lru_cache</code> cho các hàm thuần túy (pure functions).
   - Dùng Redis cho cache phân tán tầng backend/database.
4. <b>Tối ưu truy vấn Database</b>:
   - Tránh triệt để N+1 queries bằng eager loading (Django: <code>select_related</code>, SQLAlchemy: <code>joinedload</code>).
   - Đánh Index đúng trên các cột hay WHERE / JOIN.""",
        "code_example": """import cProfile
from functools import lru_cache

# 1. Caching với LRU Cache: Tăng tốc từ hàm đệ quy O(2^n) lên O(n)
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Fibonacci(100):", fibonacci(100))

# 2. Chạy cProfile để tìm bottleneck của hàm
def test_performance():
    # Giả lập logic xử lý
    data = [x for x in range(100_000)]
    lookup_set = set(data)
    found = 99_999 in lookup_set  # O(1) tra cứu siêu tốc

cProfile.run("test_performance()")""",
        "tips": "Hãy luôn trích dẫn câu nói kinh điển của Donald Knuth: 'Premature optimization is the root of all evil'. Luôn profile để biết chắc chắn điểm nghẽn nằm ở CPU, RAM, Network hay Database trước khi sửa code."
    },
    {
        "id": 28,
        "category": "Python Advanced Concepts",
        "title_en": "What is a context manager and the with statement in Python?",
        "title_vi": "Context Manager và câu lệnh with trong Python là gì?",
        "level": "Mid",
        "short_answer": "Context Manager là cơ chế quản lý tài nguyên (mở file, kết nối DB, khóa lock), đảm bảo tài nguyên được cấp phát và giải phóng an toàn thông qua câu lệnh `with`. Nó hoạt động dựa trên 2 phương thức đặc biệt: `__enter__()` (chạy khi bắt đầu) và `__exit__()` (luôn chạy khi kết thúc hoặc có lỗi).",
        "deep_dive": """Cơ chế hoạt động bên dưới của `with`:
1. Khi chạy câu lệnh: <code>with ContextExpression() as target:</code>
   - Gọi phương thức <code>__enter__()</code>, giá trị trả về được gán cho biến <code>target</code> (nếu có <code>as</code>).
   - Thực thi khối lệnh bên trong <code>with</code>.
   - Khi thoát khỏi khối lệnh (dù hoàn thành bình thường hay bị exception ném ra), Python luôn tự động gọi <code>__exit__(exc_type, exc_val, exc_tb)</code>.
2. <b>Xử lý ngoại lệ trong `__exit__`</b>:
   - Nếu phương thức <code>__exit__</code> trả về <code>True</code>, ngoại lệ xảy ra bên trong khối <code>with</code> sẽ bị chặn lại (suppressed). Nếu trả về <code>False</code> (mặc định), ngoại lệ sẽ tiếp tục nổi lên (re-raised).
3. <b>Viết Context Manager nhanh</b>: Dùng decorator <code>@contextlib.contextmanager</code> kết hợp với <code>yield</code>.""",
        "code_example": """from contextlib import contextmanager
import time

# Cách 1: Tạo Context Manager bằng Class (OOP)
class DatabaseConnection:
    def __enter__(self):
        print("🔌 1. Mở kết nối Database")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("🔒 3. Đóng kết nối Database an toàn")
        if exc_type:
            print(f"⚠️ Phát hiện lỗi: {exc_val}")
        return False  # Cho phép lỗi nổi lên nếu có

# Cách 2: Tạo bằng Decorator @contextmanager (Ngắn gọn)
@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"⏱️ [{label}] Mất {time.perf_counter() - start:.4f}s")

# Sử dụng thực tế:
with timer("Xử lý dữ liệu"):
    with DatabaseConnection():
        print("  ⚡ 2. Đang thực thi truy vấn SQL...")""",
        "tips": "Nếu cần tự động dọn dẹp nhiều tài nguyên cùng lúc, từ Python 3.10+ bạn có thể dùng cú pháp dấu ngoặc đơn: `with (open('a.txt') as a, open('b.txt') as b):`."
    },
    {
        "id": 29,
        "category": "Python Advanced Concepts",
        "title_en": "What strategies can be employed to optimize memory usage in Python applications?",
        "title_vi": "Các chiến lược tối ưu hóa dung lượng bộ nhớ (RAM) trong ứng dụng Python?",
        "level": "Senior",
        "short_answer": "Các chiến lược chính gồm: 1. Dùng `__slots__` trong class để loại bỏ overhead của `__dict__`, 2. Dùng Generator/Iterator thay vì nạp toàn bộ List vào RAM, 3. Sử dụng cấu trúc dữ liệu chuyên biệt (`array`, `NumPy`, `Polars`), 4. Kích hoạt bộ thu gom rác thủ công (`gc.collect()`), 5. Dùng kiểu dữ liệu nhỏ gọn hơn hoặc slotting memoryview.",
        "deep_dive": """Phân tích các kỹ thuật giảm RAM triệt để:
1. <b>Sức mạnh của `__slots__`</b>:
   - Mặc định mỗi class instance trong Python dùng một Dictionary (<code>__dict__</code>) để lưu trữ thuộc tính động. Một dict tốn từ 100 - 300+ bytes overhead.
   - Khai báo <code>__slots__ = ('name', 'age')</code> sẽ thay thế <code>__dict__</code> bằng một mảng con trỏ C cố định, giảm hơn 60% RAM cho mỗi instance khi tạo hàng triệu object.
2. <b>Xử lý Stream bằng Generator</b>:
   - Xử lý file/log/bản ghi DB hàng GB bằng cách đọc từng dòng hoặc từng batch nhỏ (chunks), RAM duy trì ở mức phẳng $O(1)$.
3. <b>Dùng `sys.intern()` cho String lặp lại</b>:
   - Nếu có hàng trăm nghìn bản ghi chứa chuỗi trùng nhau (ví dụ: 'active', 'pending'), intern chúng để tất cả cùng trỏ về 1 địa chỉ ô nhớ.
4. <b>Thư viện `weakref`</b>: Tránh giữ tham chiếu mạnh làm cản trở Garbage Collector thu hồi vùng nhớ.""",
        "code_example": """import sys

# 1. So sánh Class thông thường vs Class dùng __slots__
class RegularUser:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class SlottedUser:
    __slots__ = ("name", "age")
    def __init__(self, name, age):
        self.name = name
        self.age = age

u1 = RegularUser("Tuấn", 25)
u2 = SlottedUser("Tuấn", 25)

# SlottedUser không có __dict__ -> Tiết kiệm bộ nhớ vượt trội
print("Regular User RAM:", sys.getsizeof(u1) + sys.getsizeof(u1.__dict__))  # ~152 bytes
print("Slotted User RAM:", sys.getsizeof(u2))                              # ~48 bytes (Giảm 68%!)

# 2. Đo kiểm rò rỉ bộ nhớ với tracemalloc
import tracemalloc
tracemalloc.start()
# ... chạy tác vụ nghi vấn ...
current, peak = tracemalloc.get_traced_memory()
print(f"RAM hiện tại: {current / 1024:.1f} KB; Đỉnh điểm: {peak / 1024:.1f} KB")
tracemalloc.stop()""",
        "tips": "Nếu làm việc với dữ liệu số dạng bảng lớn, luôn nhắc đến `numpy.ndarray` hoặc `pandas.Categorical` để nén các cột string lặp lại thành integer mapping."
    },
    {
        "id": 30,
        "category": "Python Advanced Concepts",
        "title_en": "What is monkey patching in Python?",
        "title_vi": "Monkey Patching trong Python là gì, ưu và nhược điểm?",
        "level": "Mid",
        "short_answer": "Monkey Patching là kỹ thuật ghi đè hoặc bổ sung thuộc tính, hàm, hoặc phương thức của một module hoặc class tại thời điểm runtime mà không cần sửa đổi mã nguồn gốc của file đó. Nó cực kỳ hữu ích khi viết Unit Test (mocking) hoặc vá nóng lỗi thư viện bên thứ 3, nhưng có thể gây lỗi khó lường nếu lạm dụng.",
        "deep_dive": """Cơ chế hoạt động và rủi ro:
1. <b>Bản chất</b>: Trong Python, class và module đều là các đối tượng khả biến (mutable objects). Vì thế ta có thể gán lại thuộc tính của chúng: <code>math.sin = my_custom_sin</code>.
2. <b>Ưu điểm (Use Cases tốt)</b>:
   - <b>Testing & Mocking</b>: Thư viện <code>unittest.mock.patch</code> sử dụng monkey patching để thay thế các hàm gọi mạng/database bằng mock object.
   - <b>Hotfix thư viện bên thứ ba</b>: Khi thư viện bên ngoài có lỗi mà tác giả chưa kịp release bản vá, bạn có thể monkey patch hàm đó ngay khi khởi động ứng dụng.
   - Thư viện <code>gevent</code> monkey patch socket của thư viện chuẩn sang non-blocking.
3. <b>Nhược điểm (Rủi ro)</b>:
   - Khó debug: Code chạy một đường nhưng hành vi lại bị đổi ở runtime.
   - Phá vỡ tính tương thích khi thư viện gốc nâng cấp phiên bản.""",
        "code_example": """import math

# Giả sử cần log lại mỗi khi hàm tính căn bậc 2 được gọi
original_sqrt = math.sqrt

def logged_sqrt(x):
    print(f"🔍 [Log] Tính căn bậc 2 của số: {x}")
    return original_sqrt(x)

# Thực hiện Monkey Patching:
math.sqrt = logged_sqrt

# Gọi hàm bình thường:
print("Kết quả:", math.sqrt(25))
# Output:
# 🔍 [Log] Tính căn bậc 2 của số: 25
# Kết quả: 5.0

# Khôi phục lại hàm gốc sau khi dùng xong:
math.sqrt = original_sqrt""",
        "tips": "Nhấn mạnh với interviewer: Trong dự án production, chỉ nên dùng monkey patching trong môi trường Testing (thông qua `mock.patch`) hoặc khi bắt buộc phải hotfix tạm thời thư viện ngoài, tránh dùng bừa bãi trong logic nghiệp vụ chính."
    },
    {
        "id": 31,
        "category": "Python Object-oriented Programming",
        "title_en": "What are classes in Python?",
        "title_vi": "Class trong Python là gì và cấu trúc của một Class chuẩn?",
        "level": "Junior",
        "short_answer": "Class (Lớp) là một bản thiết kế (blueprint) hoặc khuôn mẫu định nghĩa các thuộc tính (dữ liệu) và phương thức (hành vi) mà các đối tượng (Object / Instance) được tạo ra từ nó sẽ sở hữu.",
        "deep_dive": """Cấu trúc cốt lõi của Class trong Python:
1. <b>Phương thức khởi tạo <code>__init__</code></b>: Được tự động gọi khi tạo mới một instance để thiết lập giá trị ban đầu cho các thuộc tính.
2. <b>Tham số <code>self</code></b>: Đại diện cho chính instance đang gọi phương thức. Giúp phân biệt thuộc tính của từng đối tượng cụ thể trong RAM.
3. <b>Class Attribute vs Instance Attribute</b>:
   - <i>Class Attribute</i>: Thuộc tính gắn liền với class, được chia sẻ chung bởi TẤT CẢ các instances.
   - <i>Instance Attribute</i>: Thuộc tính riêng biệt của từng đối tượng (gán qua <code>self.attr</code>).
4. Mọi class trong Python 3 đều tự động kế thừa từ class cơ sở <code>object</code>.""",
        "code_example": """class BankAccount:
    # Class Attribute (Chia sẻ chung cho mọi tài khoản)
    bank_name = "Techcombank"
    interest_rate = 0.05

    def __init__(self, owner: str, balance: float = 0.0):
        # Instance Attributes (Dữ liệu riêng biệt của từng đối tượng)
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            print(f"Đã nạp {amount:,} VND. Số dư mới: {self.balance:,} VND")

acc1 = BankAccount("Huy", 10_000_000)
acc2 = BankAccount("Lan", 5_000_000)

print(acc1.bank_name)  # Techcombank
acc1.deposit(2_000_000)""",
        "tips": "Bẫy phỏng vấn: Nếu gán một mutable object (như list) làm Class Attribute, mọi instance sẽ cùng sửa chung một danh sách đó!"
    },
    {
        "id": 32,
        "category": "Python Object-oriented Programming",
        "title_en": "How does Python support object-oriented programming?",
        "title_vi": "Python hỗ trợ 4 tính chất cốt lõi của lập trình hướng đối tượng (OOP) như thế nào?",
        "level": "Mid",
        "short_answer": "Python hỗ trợ đầy đủ 4 trụ cột OOP: 1. Đóng gói (Encapsulation - qua quy ước private `_` và `__`), 2. Kế thừa (Inheritance - hỗ trợ cả đơn kế thừa và đa kế thừa), 3. Đa hình (Polymorphism - thông qua Duck Typing và Method Overriding), 4. Trừu tượng (Abstraction - thông qua module `abc` và decorator `@abstractmethod`).",
        "deep_dive": """Triển khai 4 tính chất trong Python:
1. <b>Encapsulation</b>:
   - Dùng tiền tố <code>_name</code> (protected quy ước) và <code>__name</code> (private qua Name Mangling).
   - Dùng <code>@property</code> để tạo getter/setter tinh tế.
2. <b>Inheritance</b>:
   - Cú pháp: <code>class Dog(Animal):</code>. Hỗ trợ đa kế thừa với giải thuật C3 Linearization (MRO).
3. <b>Polymorphism & Duck Typing</b>:
   - <i>'Nếu nó đi như con vịt và kêu như con vịt, nó là con vịt'</i>. Không cần chung class cha, chỉ cần các class cùng cài đặt phương thức có cùng tên là có thể dùng thay thế cho nhau.
4. <b>Abstraction</b>:
   - Kế thừa từ <code>abc.ABC</code> và đánh dấu <code>@abstractmethod</code> để ép buộc các class con phải override.""",
        "code_example": """from abc import ABC, abstractmethod

# 1. Abstraction (Tính trừu tượng)
class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

# 2. Inheritance & Polymorphism (Kế thừa và Đa hình)
class MomoPayment(PaymentGateway):
    def pay(self, amount: float) -> bool:
        print(f" Thanh toán {amount:,} VND qua MoMo")
        return True

class VNPAYPayment(PaymentGateway):
    def pay(self, amount: float) -> bool:
        print(f" Thanh toán {amount:,} VND qua VNPAY QR")
        return True

# Hàm thanh toán đa hình nhận bất kỳ gateway nào:
def process_checkout(gateway: PaymentGateway, total: float):
    gateway.pay(total)

process_checkout(MomoPayment(), 500_000)
process_checkout(VNPAYPayment(), 1_200_000)""",
        "tips": "Hãy tự hào nhắc đến 'Duck Typing' — nét đặc trưng quyến rũ nhất của tính Đa hình trong Python so với Java hay C++."
    },
    {
        "id": 33,
        "category": "Python Object-oriented Programming",
        "title_en": "What is inheritance and give an example in Python?",
        "title_vi": "Kế thừa (Inheritance) trong Python là gì? Nêu ví dụ đơn kế thừa và đa kế thừa.",
        "level": "Junior",
        "short_answer": "Kế thừa cho phép một class con (subclass/derived class) tiếp nhận các thuộc tính và phương thức từ một hoặc nhiều class cha (base/parent class), giúp tái sử dụng mã nguồn và mở rộng tính năng mà không cần viết lại.",
        "deep_dive": """Các loại kế thừa trong Python:
1. <b>Đơn kế thừa (Single Inheritance)</b>: Class con kế thừa từ đúng 1 class cha. Dùng <code>super().__init__()</code> để khởi tạo phần của cha.
2. <b>Đa kế thừa (Multiple Inheritance)</b>: Một class con kế thừa cùng lúc từ 2 hoặc nhiều class cha (ví dụ: <code>class Smartphone(Camera, Phone):</code>).
3. <b>Vấn đề Kim cương (Diamond Problem)</b>:
   - Khi A là cha của B và C, còn D kế thừa từ cả B và C.
   - Python giải quyết triệt để vấn đề này bằng thuật toán <b>C3 Linearization</b> để xác định thứ tự ưu tiên (MRO).""",
        "code_example": """# Đơn kế thừa
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def get_role(self) -> str:
        return "Nhân viên chung"

class Developer(Employee):
    def __init__(self, name: str, salary: float, programming_language: str):
        # Gọi constructor của class cha:
        super().__init__(name, salary)
        self.programming_language = programming_language

    # Ghi đè phương thức (Method Overriding):
    def get_role(self) -> str:
        return f"Lập trình viên {self.programming_language}"

dev = Developer("Nam", 30_000_000, "Python")
print(dev.name, "-", dev.get_role())  # Nam - Lập trình viên Python""",
        "tips": "Luôn dùng hàm `super()` thay vì gọi trực tiếp tên class cha như `Employee.__init__(self, ...)`. `super()` đảm bảo toàn bộ chuỗi MRO được gọi chính xác trong đa kế thừa."
    },
    {
        "id": 34,
        "category": "Python Object-oriented Programming",
        "title_en": "How do you achieve encapsulation in Python?",
        "title_vi": "Cách thực hiện tính Đóng gói (Encapsulation) trong Python?",
        "level": "Mid",
        "short_answer": "Python không có các từ khóa `private` hay `protected` nghiêm ngặt như Java/C++. Thay vào đó, tính đóng gói được thực hiện thông qua quy ước đặt tên (Naming Conventions: `_single_underscore` và `__double_underscore`) kết hợp với decorator `@property` để kiểm soát quyền đọc/ghi dữ liệu.",
        "deep_dive": """3 cấp độ truy cập thuộc tính trong Python:
1. <b>Public (Công khai)</b>: <code>self.name</code> — Có thể truy xuất và sửa đổi tự do từ bất kỳ đâu.
2. <b>Protected (Bảo vệ theo quy ước)</b>: <code>self._balance</code> — Dấu gạch dưới đơn báo hiệu cho lập trình viên biết đây là biến nội bộ, chỉ nên dùng trong class và các subclass. Python KHÔNG cấm truy xuất từ bên ngoài.
3. <b>Private (Riêng tư & Name Mangling)</b>: <code>self.__password</code> — Tiền tố hai dấu gạch dưới kích hoạt cơ chế <i>Name Mangling</i>. Python tự đổi tên biến thành <code>_ClassName__password</code> để tránh bị class con vô tình ghi đè.
4. <b>Property Decorators</b>: Dùng <code>@property</code> để tạo getter và <code>@name.setter</code> để validate dữ liệu khi gán.""",
        "code_example": """class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self._account_type = "Checking"  # Protected (quy ước)
        self.__balance = balance         # Private (Name Mangling)

    # Getter: Đọc dữ liệu có kiểm soát
    @property
    def balance(self) -> float:
        return self.__balance

    # Setter: Validate dữ liệu trước khi cho phép gán
    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Số dư không được là số âm!")
        self.__balance = value

acc = BankAccount("Hải", 1_000_000)
print("Số dư:", acc.balance)   # 1,000,000
acc.balance = 2_000_000       # Gán hợp lệ

# Kiểm tra cơ chế Name Mangling:
print(acc._BankAccount__balance)  # Vẫn truy xuất được qua tên đã bị mangle!""",
        "tips": "Hãy trả lời phỏng vấn theo tinh thần văn hóa Python: 'We are all consenting adults here' — Python tin tưởng lập trình viên biết tự chịu trách nhiệm nên không tạo rào cản tuyệt đối."
    },
    {
        "id": 35,
        "category": "Python Object-oriented Programming",
        "title_en": "What are class methods, static methods, and instance methods?",
        "title_vi": "Phân biệt Instance Method, Class Method và Static Method trong Python.",
        "level": "Junior",
        "short_answer": "Instance method nhận `self` và thao tác trên trạng thái của đối tượng cụ thể. Class method nhận `cls` qua decorator `@classmethod` và thao tác trên trạng thái của Class (thường dùng làm Factory constructor). Static method dùng `@staticmethod`, không nhận `self` hay `cls`, hoạt động như một hàm tiện ích thông thường gắn vào namespace của class.",
        "deep_dive": """Bảng so sánh chi tiết:
<table>
  <tr><th>Tiêu chí</th><th>Instance Method</th><th>Class Method (<code>@classmethod</code>)</th><th>Static Method (<code>@staticmethod</code>)</th></tr>
  <tr><td><b>Tham số đầu tiên</b></td><td><code>self</code> (trỏ tới đối tượng hiện tại)</td><td><code>cls</code> (trỏ tới chính class)</td><td>Không có tham số bắt buộc</td></tr>
  <tr><td><b>Truy cập dữ liệu</b></td><td>Truy cập cả instance & class attributes</td><td>Chỉ truy cập class attributes</td><td>Không truy cập được thuộc tính class/instance</td></tr>
  <tr><td><b>Use case phổ biến</b></td><td>Hành vi thông thường của đối tượng</td><td>Factory method (tạo object từ chuỗi JSON, date, file)</td><td>Hàm tiện ích (Utility/Helper function) độc lập</td></tr>
</table>""",
        "code_example": """class DateUtils:
    def __init__(self, day: int, month: int, year: int):
        self.day = day
        self.month = month
        self.year = year

    # 1. Instance Method: In định dạng của ngày cụ thể
    def display(self) -> str:
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

    # 2. Class Method: Factory constructor tạo object từ chuỗi 'YYYY-MM-DD'
    @classmethod
    def from_string(cls, date_str: str):
        year, month, day = map(int, date_str.split("-"))
        return cls(day, month, year)

    # 3. Static Method: Kiểm tra năm nhuận độc lập
    @staticmethod
    def is_leap_year(year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

d1 = DateUtils(9, 11, 2026)
d2 = DateUtils.from_string("2026-11-09")  # Gọi qua class method
print(d2.display())                     # 09/11/2026
print(DateUtils.is_leap_year(2024))     # True""",
        "tips": "Khi được hỏi 'Tại sao không viết hàm static ra ngoài module mà phải đưa vào class?', trả lời: Để đóng gói logic helper liên quan chặt chẽ vào chung namespace của class, giúp code gọn gàng."
    },
    {
        "id": 36,
        "category": "Python Object-oriented Programming",
        "title_en": "What is polymorphism in Python?",
        "title_vi": "Tính đa hình (Polymorphism) và Duck Typing trong Python được thể hiện ra sao?",
        "level": "Mid",
        "short_answer": "Tính đa hình cho phép các đối tượng thuộc các class khác nhau phản hồi theo cách riêng biệt của chúng đối với cùng một lời gọi phương thức. Trong Python, đa hình được phát huy tối đa nhờ nguyên lý Duck Typing: chỉ cần đối tượng có phương thức tương ứng, không bắt buộc chúng phải có quan hệ kế thừa cùng một lớp cha.",
        "deep_dive": """2 hình thức đa hình chính trong Python:
1. <b>Method Overriding (Đa hình qua kế thừa)</b>:
   - Các class con kế thừa từ cùng 1 class cha và ghi đè phương thức để có hành vi riêng.
2. <b>Duck Typing (Đa hình không cần kế thừa)</b>:
   - Cụm từ nổi tiếng của Alex Martelli: <i>'If it walks like a duck and quacks like a duck, it's a duck'</i>.
   - Ví dụ: Bất kỳ object nào có cài đặt phương thức <code>__len__()</code> thì đều có thể truyền vào hàm <code>len(obj)</code> (chuỗi, list, tuple, dict, custom class).
3. <b>Operator Overloading (Nạp chồng toán tử)</b>:
   - Toán tử <code>+</code> thực hiện phép cộng số nguyên, nhưng với chuỗi là nối chuỗi, với list là gộp list nhờ phương thức ma thuật <code>__add__()</code>.""",
        "code_example": """class PDFExporter:
    def export(self, data):
        return f" Xuất file PDF với nội dung: {data}"

class ExcelExporter:
    def export(self, data):
        return f"📊 Xuất file Excel với nội dung: {data}"

# Hàm xử lý báo cáo không quan tâm exporter là class nào,
# miễn là nó có phương thức .export() (Duck Typing)
def generate_report(exporter, content):
    print(exporter.export(content))

generate_report(PDFExporter(), "Báo cáo doanh thu Q4")
generate_report(ExcelExporter(), "Danh sách đơn hàng 2026")""",
        "tips": "Nếu muốn kiểm tra interface lúc type checking mà vẫn giữ tinh thần Duck Typing, hãy dùng `typing.Protocol` (Structural Subtyping theo PEP 544)."
    },
    {
        "id": 37,
        "category": "Python Object-oriented Programming",
        "title_en": "Explain the use of the super() function.",
        "title_vi": "Giải thích tác dụng của hàm super() và tại sao nó đặc biệt quan trọng trong đa kế thừa?",
        "level": "Senior",
        "short_answer": "Hàm `super()` trả về một đối tượng proxy đại diện cho class cha kế tiếp trong chuỗi thứ tự phân giải phương thức (Method Resolution Order - MRO). Nó giúp gọi các phương thức của lớp cha một cách linh hoạt, tránh gọi tên cứng class cha và ngăn chặn việc gọi lặp lại một phương thức trong mô hình đa kế thừa hình kim cương.",
        "deep_dive": """Tại sao `super()` lại vượt trội hơn `BaseClass.__init__(self)`?
1. <b>Hợp tác trong đa kế thừa (Cooperative Multiple Inheritance)</b>:
   - Trong mô hình Diamond (A -> B, C -> D): Nếu dùng <code>A.__init__(self)</code> trong cả B và C, thì khi khởi tạo D, constructor của A sẽ bị gọi 2 lần!
   - Sử dụng <code>super()</code> sẽ tuân thủ nghiêm ngặt danh sách MRO: Mỗi class trong cây kế thừa được gọi ĐÚNG MỘT LẦN duy nhất theo thứ tự tuyến tính hóa C3.
2. <b>Dễ bảo trì</b>: Nếu bạn đổi tên class cha hoặc thay đổi cấu trúc phân cấp, code trong class con dùng <code>super()</code> không cần phải sửa đổi.""",
        "code_example": """class A:
    def __init__(self):
        print("-> Khởi tạo A")

class B(A):
    def __init__(self):
        super().__init__()
        print("-> Khởi tạo B")

class C(A):
    def __init__(self):
        super().__init__()
        print("-> Khởi tạo C")

class D(B, C):
    def __init__(self):
        super().__init__()
        print("-> Khởi tạo D")

d = D()
# Thứ tự thực thi nhờ super() và MRO:
# -> Khởi tạo A
# -> Khởi tạo C
# -> Khởi tạo B
# -> Khởi tạo D
print("MRO của D:", [cls.__name__ for cls in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']""",
        "tips": "Trong Python 3, chỉ cần gọi `super().__init__()` mà không cần truyền `super(CurrentClass, self)` như thời Python 2."
    },
    {
        "id": 38,
        "category": "Python Object-oriented Programming",
        "title_en": "What is method resolution order (MRO) in Python?",
        "title_vi": "Method Resolution Order (MRO) là gì và thuật toán C3 Linearization hoạt động thế nào?",
        "level": "Senior",
        "short_answer": "MRO (Method Resolution Order) là thứ tự tuyến tính mà Python duyệt qua các class để tìm kiếm một phương thức hoặc thuộc tính khi được gọi trên một đối tượng. Python sử dụng thuật toán C3 Linearization để đảm bảo tính đơn điệu (monotonicity) và tôn trọng thứ tự khai báo cha-con.",
        "deep_dive": """Nguyên tắc vàng của thuật toán C3 Linearization:
1. <b>Class con luôn được duyệt trước class cha</b>.
2. <b>Nếu có nhiều class cha (đa kế thừa)</b>: Thứ tự duyệt tuân theo đúng thứ tự được liệt kê trong tuple kế thừa từ trái sang phải: <code>class Child(Parent1, Parent2):</code> -> duyệt Parent1 trước Parent2.
3. <b>Bảo toàn tính đơn điệu</b>: Nếu một class xuất hiện trước một class khác trong MRO của class cha, thứ tự đó phải được giữ nguyên trong MRO của class con.
4. Cách xem MRO:
   - Thuộc tính <code>ClassName.__mro__</code>
   - Phương thức <code>ClassName.mro()</code>""",
        "code_example": """class X: pass
class Y: pass
class A(X, Y): pass
class B(Y): pass
class C(A, B): pass

# In thứ tự MRO của class C
print("C3 MRO Order:")
for idx, cls in enumerate(C.__mro__):
    print(f"  {idx + 1}. {cls.__name__}")

# Output:
# 1. C
# 2. A
# 3. X
# 4. B
# 5. Y
# 6. object""",
        "tips": "Nếu cấu trúc kế thừa tạo ra xung đột không thể giải quyết thứ tự tuyến tính hợp lệ, Python sẽ ném lỗi ngay lúc định nghĩa class: `TypeError: Cannot create a consistent method resolution order (MRO)`."
    },
    {
        "id": 39,
        "category": "Python Object-oriented Programming",
        "title_en": "What are magic methods in Python?",
        "title_vi": "Magic Methods (Dunder Methods) trong Python là gì và các ứng dụng phổ biến?",
        "level": "Mid",
        "short_answer": "Magic Methods (hay Dunder Methods - Double Underscore) là các phương thức đặc biệt có hai dấu gạch dưới ở đầu và cuối (như `__init__`, `__str__`, `__len__`, `__getitem__`). Chúng được Python tự động gọi ngầm định khi đối tượng tham gia vào các hành vi cú pháp tích hợp (như in ra chuỗi, phép cộng, duyệt for, truy xuất chỉ mục).",
        "deep_dive": """Các nhóm Dunder Methods thông dụng nhất:
1. <b>Khởi tạo & Đại diện chuỗi</b>:
   - <code>__init__</code>: Khởi tạo giá trị.
   - <code>__str__</code>: Chuỗi hiển thị thân thiện cho người dùng (khi gọi <code>print(obj)</code> hoặc <code>str(obj)</code>).
   - <code>__repr__</code>: Chuỗi chi tiết rõ ràng phục vụ debug cho dev (khi inspect trong log/REPL).
2. <b>Nạp chồng toán tử (Operator Overloading)</b>:
   - <code>__add__ (+)</code>, <code>__sub__ (-)</code>, <code>__mul__ (*)</code>, <code>__eq__ (==)</code>, <code>__lt__ (<)</code>.
3. <b>Collection Protocol & Container</b>:
   - <code>__len__</code>: Trả về độ dài khi gọi <code>len(obj)</code>.
   - <code>__getitem__</code>: Truy xuất phần tử dạng <code>obj[key]</code>.
   - <code>__setitem__</code>: Gán phần tử <code>obj[key] = val</code>.
4. <b>Callable Object</b>:
   - <code>__call__</code>: Cho phép gọi instance của class như một function: <code>obj()</code>.""",
        "code_example": """class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Nạp chồng toán tử cộng (+)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # Hiển thị đẹp mắt khi print()
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    # So sánh bằng (==)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector(2, 4)
v2 = Vector(3, 1)
v3 = v1 + v2           # Tự động gọi v1.__add__(v2)

print(v3)              # Vector(5, 5)
print(v3 == Vector(5, 5))  # True""",
        "tips": "Quy tắc vàng: Nếu chỉ cài đặt 1 phương thức đại diện, hãy luôn chọn `__repr__` vì nếu không có `__str__`, Python sẽ tự động fallback về `__repr__`."
    },
    {
        "id": 40,
        "category": "Python Object-oriented Programming",
        "title_en": "How do you prevent a class from being inherited?",
        "title_vi": "Làm thế nào để ngăn chặn một Class bị kế thừa trong Python (Final Class)?",
        "level": "Mid",
        "short_answer": "Cách chuẩn mực và hiện đại nhất từ Python 3.8+ là sử dụng decorator `@final` từ module `typing`. Ngoài ra, ở mức runtime, ta có thể dùng phương thức `__init_subclass__` để ném ngoại lệ nếu có class nào cố tình kế thừa nó.",
        "deep_dive": """2 phương pháp ngăn chặn kế thừa:
1. <b>Dùng <code>@final</code> (Static Type Checker)</b>:
   - Đạt chuẩn PEP 591. Các công cụ kiểm tra kiểu tĩnh (Mypy, Pyright, VSCode Pylance) sẽ báo lỗi ngay khi bạn viết code kế thừa class có <code>@final</code>.
2. <b>Dùng <code>__init_subclass__</code> (Enforce lúc Runtime)</b>:
   - Phương thức này được tự động gọi trên class cha bất cứ khi nào có một class con kế thừa nó. Ta chỉ cần ném ra <code>TypeError</code> để chặn hoàn toàn việc kế thừa lúc chạy ứng dụng.""",
        "code_example": """from typing import final

# Cách 1: Chuẩn PEP 591 với @final (Báo lỗi linter)
@final
class SecureVault:
    pass

# Cách 2: Khóa chặt 100% ở Runtime với __init_subclass__
class ImmutableBase:
    def __init_subclass__(cls, **kwargs):
        raise TypeError(f"Class '{cls.__name__}' không được phép kế thừa từ '{ImmutableBase.__name__}'!")

# Thử nghiệm kế thừa:
try:
    class HackerVault(ImmutableBase):
        pass
except TypeError as e:
    print(f" Đã chặn kế thừa thành công: {e}")""",
        "tips": "Cách dùng `__init_subclass__` ra đời từ Python 3.6, thanh lịch và sạch sẽ hơn rất nhiều so với cách dùng Metaclass truyền thống ngày xưa."
    },
    {
        "id": 41,
        "category": "Python Debugging and Testing",
        "title_en": "How do you debug a Python program?",
        "title_vi": "Các phương pháp và chiến lược debug một chương trình Python hiệu quả?",
        "level": "Junior",
        "short_answer": "Các phương pháp debug từ cơ bản đến nâng cao: 1. Sử dụng hàm `breakpoint()` tích hợp sẵn (mở trình gỡ lỗi PDB), 2. Sử dụng logging thay vì print rải rác, 3. Dùng GUI Debugger trong IDE (VS Code, PyCharm), 4. Phân tích Traceback và ngoại lệ, 5. Sử dụng Post-mortem debugging khi chương trình bị crash.",
        "deep_dive": """Quy trình debug chuyên nghiệp trong dự án thực tế:
1. <b>Sử dụng <code>breakpoint()</code> (từ Python 3.7+)</b>:
   - Chèn dòng <code>breakpoint()</code> tại vị trí nghi vấn, chương trình sẽ tạm dừng và mở terminal tương tác PDB.
   - Các lệnh PDB cơ bản: <code>n</code> (next line), <code>s</code> (step into), <code>c</code> (continue), <code>p variable</code> (print value), <code>q</code> (quit).
2. <b>Thay thế <code>print()</code> bằng Module <code>logging</code></b>:
   - Có timestamp, level (DEBUG, INFO, WARNING, ERROR), và tên module. Dễ dàng tắt bật trong production mà không cần xóa code.
3. <b>Thư viện hỗ trợ nâng cao</b>:
   - <code>icecream (ic())</code>: In biến kèm biểu thức và tên file tự động.
   - <code>pudb</code>: Trình debug toàn màn hình dạng terminal UI.""",
        "code_example": """def calculate_discount(price, percent):
    # Đặt điểm dừng để kiểm tra giá trị biến lúc chạy
    # breakpoint()  # Bỏ comment khi cần nhảy vào PDB
    discount_amount = price * (percent / 100)
    final_price = price - discount_amount
    return final_price

result = calculate_discount(200_000, 15)
print("Giá sau giảm:", result)""",
        "tips": "Tuyệt đối không để sót các dòng `print()` debug khi tạo Pull Request. Hãy tập thói quen dùng `breakpoint()` và `logging.debug()`."
    },
    {
        "id": 42,
        "category": "Python Debugging and Testing",
        "title_en": "What are some popular debugging tools for Python?",
        "title_vi": "Những công cụ debugging phổ biến và mạnh mẽ nhất cho Python là gì?",
        "level": "Mid",
        "short_answer": "Các công cụ debug phổ biến gồm: pdb/ipdb (CLI debugger tích hợp và nâng cao), VS Code / PyCharm Debugger (giao diện đồ họa), IceCream (thay thế print thông minh), Sentry (theo dõi lỗi phân tán trên production), và Py-Spy / Memray (profiler không xâm lấn).",
        "deep_dive": """Chi tiết các công cụ hàng đầu:
1. <b>PDB & IPDB</b>:
   - <code>ipdb</code> bổ sung màu sắc cú pháp, tab completion từ IPython vào PDB truyền thống.
2. <b>Py-Spy</b>:
   - Sampling profiler cực kỳ ấn tượng: có thể đính kèm vào một process Python đang chạy trên Production để vẽ Flame Graph mà không làm chậm ứng dụng.
3. <b>Memray</b>:
   - Công cụ chuyên dụng của Bloomberg để phát hiện rò rỉ bộ nhớ (memory leak) cả ở tầng Python và C extension.
4. <b>Sentry</b>:
   - Bắt tự động các Unhandled Exceptions, gửi thông báo kèm toàn bộ biến local và stack trace về dashboard.""",
        "code_example": """# Cài đặt và sử dụng IceCream thay cho print():
# pip install icecream
try:
    from icecream import ic
    user = {"id": 42, "name": "Bình"}
    ic(user["name"])  # Output: ic| user['name']: 'Bình' (Kèm dòng code & file)
except ImportError:
    pass""",
        "tips": "Nếu ứng dụng đang chạy production bị treo (hang/freeze), nhắc đến lệnh `py-spy dump --pid <PID>` để lấy call stack tức thì của tất cả các luồng mà không cần restart server."
    },
    {
        "id": 43,
        "category": "Python Debugging and Testing",
        "title_en": "What is unit testing in Python?",
        "title_vi": "Unit Testing trong Python là gì và các nguyên tắc viết test tốt?",
        "level": "Junior",
        "short_answer": "Unit Testing là phương pháp kiểm thử phần mềm ở cấp độ nhỏ nhất — kiểm tra tính đúng đắn của từng đơn vị mã nguồn riêng lẻ (thường là một hàm hoặc một phương thức class). Trong Python, ta có thể dùng thư viện tích hợp `unittest` hoặc framework phổ biến `pytest`.",
        "deep_dive": """Các nguyên tắc viết Unit Test chuẩn:
1. <b>Mô hình FIRST</b>:
   - <b>F</b>ast (Chạy nhanh)
   - <b>I</b>ndependent (Độc lập, không phụ thuộc thứ tự chạy)
   - <b>R</b>epeatable (Lặp lại kết quả nhất quán ở mọi môi trường)
   - <b>S</b>elf-validating (Tự động pass/fail)
   - <b>T</b>imely (Viết kịp thời, theo hướng TDD)
2. <b>Cấu trúc AAA (Arrange - Act - Assert)</b>:
   - <i>Arrange</i>: Chuẩn bị dữ liệu và mock.
   - <i>Act</i>: Gọi hàm cần kiểm thử.
   - <i>Assert</i>: Xác minh kết quả trả về đúng như kỳ vọng.""",
        "code_example": """# Giả sử có hàm cần test:
def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]

# Viết test bằng unittest:
import unittest

class TestEmailValidation(unittest.TestCase):
    def test_valid_email(self):
        # Arrange & Act & Assert
        self.assertTrue(is_valid_email("contact@gmail.com"))

    def test_invalid_email_without_at(self):
        self.assertFalse(is_valid_email("contact.gmail.com"))

if __name__ == "__main__":
    unittest.main()""",
        "tips": "Unit test tốt là test KHÔNG chạm vào database thật, không gọi mạng thật và không đọc ghi ổ cứng thật — mọi phụ thuộc bên ngoài phải được mock."
    },
    {
        "id": 44,
        "category": "Python Debugging and Testing",
        "title_en": "How do you write a basic test case in Python using unittest?",
        "title_vi": "Cách viết một Test Case cơ bản với module unittest có sẵn của Python?",
        "level": "Junior",
        "short_answer": "Tạo một class kế thừa từ `unittest.TestCase`, viết các phương thức kiểm thử bắt đầu bằng tiền tố `test_`, và sử dụng các phương thức assertion có sẵn như `assertEqual`, `assertTrue`, `assertRaises` để xác nhận kết quả.",
        "deep_dive": """Vòng đời của TestCase trong `unittest`:
1. <code>setUp()</code>: Chạy trước MỖI phương thức test để chuẩn bị dữ liệu mới sạch sẽ.
2. <code>tearDown()</code>: Chạy sau MỖI phương thức test để dọn dẹp tài nguyên.
3. <code>setUpClass()</code> & <code>tearDownClass()</code>: Chạy đúng 1 lần cho toàn bộ class test (dùng decorator <code>@classmethod</code>).
4. Kiểm tra ném ngoại lệ: Dùng context manager <code>with self.assertRaises(ValueError):</code>.""",
        "code_example": """import unittest

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Không thể chia cho số 0!")
    return a / b

class TestMathOperations(unittest.TestCase):
    def setUp(self):
        self.default_a = 10.0

    def test_divide_success(self):
        result = divide(self.default_a, 2.0)
        self.assertEqual(result, 5.0)

    def test_divide_by_zero_raises_error(self):
        with self.assertRaises(ZeroDivisionError):
            divide(self.default_a, 0)

if __name__ == "__main__":
    unittest.main()""",
        "tips": "Bắt buộc tên phương thức test phải bắt đầu bằng chữ `test_`, nếu không `unittest` runner sẽ bỏ qua phương thức đó."
    },
    {
        "id": 45,
        "category": "Python Debugging and Testing",
        "title_en": "What is pytest and how is it used?",
        "title_vi": "Pytest là gì và tại sao nó lại được ưa chuộng hơn unittest trong các dự án hiện đại?",
        "level": "Mid",
        "short_answer": "`pytest` là framework kiểm thử phổ biến nhất hiện nay trong hệ sinh thái Python. Nó được ưa chuộng vượt trội vì: cú pháp ngắn gọn (dùng hàm thường thay vì phải kế thừa class), dùng lệnh `assert` thuần túy của Python, hệ thống Fixtures mạnh mẽ tái sử dụng cao, và hệ sinh thái plugin đồ sộ (pytest-cov, pytest-asyncio, pytest-xdist).",
        "deep_dive": """Tại sao Pytest đánh bại Unittest?
1. <b>Assert thuần túy</b>: Thay vì phải nhớ hàng chục hàm như <code>self.assertEqual()</code>, <code>self.assertIn()</code>, Pytest chỉ cần câu lệnh <code>assert a == b</code> và tự động hiển thị chi tiết giá trị khác biệt (assertion introspection) cực kỳ rõ ràng khi fail.
2. <b>Pytest Fixtures (<code>@pytest.fixture</code>)</b>:
   - Quản lý phụ thuộc theo phong cách Dependency Injection.
   - Hỗ trợ các scope linh hoạt: function, class, module, session.
3. <b>Parametrized Testing (<code>@pytest.mark.parametrize</code>)</b>:
   - Chạy cùng một test logic với hàng chục bộ input/output khác nhau chỉ với 1 decorator.""",
        "code_example": """# File: test_calculator.py (Chạy lệnh: pytest)
import pytest

def add(a, b):
    return a + b

# 1. Test đơn giản với assert chuẩn Python
def test_add_simple():
    assert add(2, 3) == 5

# 2. Parametrize: Chạy test với nhiều bộ dữ liệu đầu vào
@pytest.mark.parametrize("x, y, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300)
])
def test_add_multiple_cases(x, y, expected):
    assert add(x, y) == expected""",
        "tips": "Trong hầu hết các dự án tuyển dụng hiện nay, nếu bạn nhắc đến `pytest` kết hợp `pytest-mock` và `pytest-cov` để đo test coverage, bạn sẽ được đánh giá cao hơn nhiều so với việc chỉ biết `unittest`."
    },
    {
        "id": 46,
        "category": "Python Debugging and Testing",
        "title_en": "How do you test a Python function with side effects?",
        "title_vi": "Cách kiểm thử một hàm có tác dụng phụ (Side Effects: gửi email, gọi API, ghi DB)?",
        "level": "Senior",
        "short_answer": "Ta sử dụng kỹ thuật Mocking thông qua thư viện `unittest.mock` (hoặc `pytest-mock`). Bằng cách dùng `Mock`, `MagicMock` hoặc decorator `@patch`, ta thay thế các thành phần phụ thuộc bên ngoài bằng các đối tượng giả lập, sau đó xác minh (assert) xem các hàm đó đã được gọi với đúng tham số hay chưa.",
        "deep_dive": """Kỹ thuật Mocking với `@patch`:
1. <b>Nguyên tắc 'Patch where an object is LOOKED UP, not where it is defined'</b>:
   - Nếu trong file <code>order_service.py</code> bạn viết <code>import requests</code>, bạn phải patch <code>order_service.requests.post</code> chứ không phải <code>requests.post</code>.
2. <b>MagicMock vs Mock</b>:
   - <code>MagicMock</code> cài đặt sẵn hầu hết các dunder methods (như <code>__iter__</code>, <code>__enter__</code>, <code>__exit__</code>), rất phù hợp khi mock file hoặc context manager.
3. <b>Các phương thức kiểm tra cuộc gọi</b>:
   - <code>mock.assert_called_once()</code>
   - <code>mock.assert_called_with(*args, **kwargs)</code>""",
        "code_example": """from unittest.mock import patch, MagicMock

# Hàm cần kiểm thử có side-effect gọi API thanh toán bên thứ 3
def charge_customer(api_url, user_id, amount):
    import requests
    response = requests.post(api_url, json={"user": user_id, "amount": amount})
    if response.status_code == 200:
        return "SUCCESS"
    return "FAILED"

# Viết test cô lập hoàn toàn, không gọi mạng thật:
@patch("requests.post")
def test_charge_customer_success(mock_post):
    # Giả lập response trả về mã 200:
    mock_post.return_value.status_code = 200

    result = charge_customer("https://api.stripe.com/charge", "U123", 500)

    # 1. Kiểm tra kết quả trả về
    assert result == "SUCCESS"
    # 2. Xác minh hàm requests.post đã được gọi đúng 1 lần với đúng payload:
    mock_post.assert_called_once_with(
        "https://api.stripe.com/charge",
        json={"user": "U123", "amount": 500}
    )""",
        "tips": "Nhớ nhấn mạnh quy tắc 'Patch where it's used' — 80% developer mới làm quen với mock đều bị lỗi test không hoạt động do patch sai đường dẫn module."
    },
    {
        "id": 47,
        "category": "Python Debugging and Testing",
        "title_en": "What is a breakpoint and how do you use it?",
        "title_vi": "Breakpoint là gì và cách sử dụng hàm breakpoint() trong Python 3.7+?",
        "level": "Junior",
        "short_answer": "Breakpoint là một điểm dừng được đặt có chủ đích trong mã nguồn. Khi chương trình chạy đến vị trí này, quá trình thực thi sẽ tạm dừng để lập trình viên có thể kiểm tra giá trị các biến, xem xét stack frame và thực thi từng dòng lệnh để tìm nguyên nhân gây lỗi.",
        "deep_dive": """Cơ chế hàm `breakpoint()` tích hợp từ PEP 553:
1. Trước Python 3.7, bạn phải viết: <code>import pdb; pdb.set_trace()</code>.
2. Từ Python 3.7+, chỉ cần gõ <code>breakpoint()</code>.
3. <b>Tùy biến qua biến môi trường <code>PYTHONBREAKPOINT</code></b>:
   - Tắt toàn bộ breakpoints khi deploy mà không cần xóa code: <code>PYTHONBREAKPOINT=0 python app.py</code>
   - Đổi trình debugger sang ipdb: <code>PYTHONBREAKPOINT=ipdb.set_trace python app.py</code>
4. <b>Các lệnh điều khiển PDB cốt lõi</b>:
   - <code>l</code> (list code xung quanh)
   - <code>p var</code> hoặc <code>pp var</code> (pretty print biến)
   - <code>n</code> (next - sang dòng kế tiếp)
   - <code>s</code> (step in - nhảy vào trong thân hàm)
   - <code>c</code> (continue - chạy tiếp đến breakpoint sau)""",
        "code_example": """def process_order(items, discount):
    subtotal = sum(item["price"] for item in items)
    # breakpoint()  # Chương trình sẽ dừng tại đây để dev inspect 'subtotal'
    total = subtotal - (subtotal * discount)
    return total

cart = [{"name": "Sách", "price": 100}, {"name": "Bút", "price": 20}]
print("Tổng tiền:", process_order(cart, 0.1))""",
        "tips": "Điểm cộng lớn khi phỏng vấn: Hãy nhắc tới biến môi trường `PYTHONBREAKPOINT=0` giúp vô hiệu hóa toàn bộ breakpoint khi chạy production hoặc CI/CD pipeline."
    },
    {
        "id": 48,
        "category": "Python Debugging and Testing",
        "title_en": "How do you log messages in Python?",
        "title_vi": "Cách ghi log chuẩn mực trong Python với module logging?",
        "level": "Mid",
        "short_answer": "Sử dụng module chuẩn `logging`. Module này hỗ trợ 5 mức độ nghiêm trọng (DEBUG, INFO, WARNING, ERROR, CRITICAL), định dạng thông điệp chi tiết (timestamp, thread, file, line number), và định tuyến log ra nhiều đích đến (Console, File, Logstash, Sentry).",
        "deep_dive": """Kiến trúc hệ thống Logging trong Python:
1. <b>Logger</b>: Điểm vào tiếp nhận thông điệp log từ ứng dụng (tạo qua <code>logging.getLogger(__name__)</code>).
2. <b>Handler</b>: Quyết định nơi log được gửi đến:
   - <code>StreamHandler</code>: Đẩy ra màn hình Console (stdout/stderr).
   - <code>RotatingFileHandler</code> / <code>TimedRotatingFileHandler</code>: Ghi ra file và tự động chia nhỏ file khi đạt dung lượng tối đa để tránh đầy ổ cứng.
3. <b>Formatter</b>: Quy định cấu trúc dòng log (ví dụ JSON format cho Kubernetes/ELK Stack).
4. <b>Filter</b>: Lọc các bản ghi log nâng cao.""",
        "code_example": """import logging

# Thiết lập cấu hình cơ bản cho Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s:%(lineno)d) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("PaymentService")

def transfer(from_user, to_user, amount):
    logger.debug("Bắt đầu xác thực tài khoản...")  # Mức DEBUG (ẩn nếu level=INFO)
    logger.info(f"Chuyển {amount:,} VND từ {from_user} sang {to_user}")
    
    try:
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
    except ValueError as err:
        # Ghi log kèm toàn bộ stack trace tự động với exc_info=True
        logger.error(f"Giao dịch thất bại: {err}", exc_info=True)

transfer("Nam", "An", -50000)""",
        "tips": "Luôn dùng `logging.getLogger(__name__)` thay vì `logging.info(...)` trực tiếp từ root logger để dễ dàng lọc và quản lý log theo từng module trong dự án lớn."
    },
    {
        "id": 49,
        "category": "Python Debugging and Testing",
        "title_en": "How do you use assertions in Python?",
        "title_vi": "Cách sử dụng câu lệnh assert trong Python và khi nào KHÔNG ĐƯỢC DÙNG nó?",
        "level": "Mid",
        "short_answer": "Câu lệnh `assert condition, 'Thông báo lỗi'` dùng để kiểm tra các giả định nội bộ của lập trình viên. Nếu điều kiện trả về `False`, Python sẽ ném ngoại lệ `AssertionError`. Assert CHỈ NÊN DÙNG để debug và viết test case; TUYỆT ĐỐI KHÔNG DÙNG assert để xác thực dữ liệu người dùng (input validation) hay kiểm tra phân quyền trong production.",
        "deep_dive": """Tại sao không dùng assert cho Data Validation?
1. <b>Cờ tối ưu <code>-O</code> (Optimize Flag)</b>:
   - Khi chạy Python với cờ tối ưu hóa (<code>python -O app.py</code>), toàn bộ các câu lệnh <code>assert</code> sẽ BỊ BỎ QUA HOÀN TOÀN (stripped out) khỏi bytecode!
   - Nếu bạn viết <code>assert user.is_admin, 'Forbidden'</code>, khi chạy với <code>-O</code>, bất kỳ ai cũng có thể vượt qua quyền admin!
2. <b>Cách dùng đúng</b>:
   - Dùng <code>if not condition: raise ValueError(...)</code> cho logic nghiệp vụ và input validation.
   - Dùng <code>assert</code> để bắt các trạng thái 'bất khả thi' (Invariants) mà nếu xảy ra nghĩa là code có bug.""",
        "code_example": """# ❌ SAI LẦM NGUY HIỂM: Dùng assert để validate input người dùng
def buy_ticket(age):
    # Nếu chạy 'python -O', dòng này bị xóa bỏ hoàn toàn!
    assert age >= 18, "Phải từ 18 tuổi trở lên!"
    print("Mua vé thành công!")

#  CÁCH LÀM CHUẨN MỰC TRONG PRODUCTION:
def buy_ticket_safe(age):
    if age < 18:
        raise ValueError("Yêu cầu độ tuổi tối thiểu là 18!")
    print("Mua vé thành công!")""",
        "tips": "Câu hỏi bẫy 'Điều gì xảy ra khi chạy python với cờ -O?' là một câu hỏi phân loại ứng viên cực kỳ phổ biến. Câu trả lời chính xác: Bytecode compiler sẽ loại bỏ toàn bộ lệnh `assert`."
    },
    {
        "id": 50,
        "category": "Python Debugging and Testing",
        "title_en": "What is a traceback, and how do you analyze it?",
        "title_vi": "Traceback trong Python là gì và cách đọc hiểu để định vị lỗi nhanh nhất?",
        "level": "Junior",
        "short_answer": "Traceback (hay Stack Trace) là bản báo cáo chi tiết các khung ngăn xếp (stack frames) của hàm tại thời điểm xảy ra ngoại lệ chưa được xử lý. Để phân tích nhanh nhất, hãy đọc từ DƯỚI LÊN TRÊN: dòng cuối cùng cho biết loại lỗi và thông điệp lỗi, các dòng ngay phía trên chỉ ra file và số dòng code trong dự án của bạn gây ra lỗi.",
        "deep_dive": """Cách đọc một Traceback chuẩn:
1. <b>Dòng dưới cùng (Bottom line)</b>: Loại ngoại lệ (Exception Class) và thông điệp mô tả (ví dụ: <code>KeyError: 'user_id'</code> hoặc <code>IndexError: list index out of range</code>).
2. <b>Duyệt ngược từ dưới lên</b>:
   - Bỏ qua các file thuộc thư viện ngoài (trong <code>site-packages</code>).
   - Dừng lại ở file đầu tiên thuộc mã nguồn dự án của bạn. Đó chính là dòng code đã trực tiếp gọi hoặc gây ra lỗi.
3. <b>Exception Chaining (Từ Python 3)</b>:
   - Nếu một exception xảy ra trong quá trình xử lý exception khác, bạn sẽ thấy thông báo: <i>'During handling of the above exception, another exception occurred'</i> hoặc <i>'The above exception was the direct cause of the following exception'</i> (dùng cú pháp <code>raise NewError from original_err</code>).""",
        "code_example": """# File: order.py
def calculate_tax(price):
    return price * 0.1

def process_item(item):
    # Dòng gây lỗi: Truy xuất key không tồn tại trong dict
    return calculate_tax(item["price"])

data = {"title": "Tai nghe"}
process_item(data)

# Traceback mẫu khi chạy:
# Traceback (most recent call last):
#   File "order.py", line 9, in <module>
#     process_item(data)
#   File "order.py", line 6, in process_item
#     return calculate_tax(item["price"])
# KeyError: 'price'  <-- Đọc dòng này đầu tiên!""",
        "tips": "Từ Python 3.11+, CPython bổ sung tính năng Enhanced Error Locations: Traceback in ra các dấu `^^^^` gạch chân chính xác biểu thức con bị lỗi trên dòng, giúp phát hiện lỗi như `a[b][c]` ngay lập tức."
    }
]
