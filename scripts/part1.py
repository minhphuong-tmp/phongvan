# -*- coding: utf-8 -*-
# Part 1: Q1 to Q25 (Python Fundamentals, Functions & Modules, Advanced Concepts Part 1)

DATA_PART_1 = [
    {
        "id": 1,
        "category": "Python Fundamentals",
        "title_en": "What are the key features of Python?",
        "title_vi": "Các đặc điểm chính nổi bật của Python là gì?",
        "level": "Junior",
        "short_answer": "Python là ngôn ngữ lập trình bậc cao, thông dịch (interpreted), đa mô hình (multi-paradigm: OOP, hàm, thủ tục), định kiểu động (dynamically typed) nhưng có tính định kiểu mạnh (strongly typed), và có cú pháp rõ ràng, dễ đọc.",
        "deep_dive": """Các đặc điểm cốt lõi làm nên sức mạnh của Python:
1. <b>Cú pháp rõ ràng (Readability & PEP 8)</b>: Sử dụng khoảng trắng/thụt lề (indentation) thay cho dấu ngoặc nhọn <code>{}</code>, giúp code sạch và chuẩn hóa giữa các dev.
2. <b>Định kiểu động nhưng mạnh (Dynamically & Strongly Typed)</b>: Không cần khai báo kiểu dữ liệu cho biến khi viết code (dynamic), nhưng Python không tự ý ép kiểu ngầm giữa các kiểu dữ liệu không tương thích (ví dụ: <code>'5' + 5</code> sẽ ném <code>TypeError</code> chứ không ra <code>'55'</code> như JS).
3. <b>Thông dịch & Tương tác (Interpreted & REPL)</b>: Mã nguồn được biên dịch thành bytecode (<code>.pyc</code>) rồi thực thi trên máy ảo Python Virtual Machine (PVM).
4. <b>Quản lý bộ nhớ tự động</b>: Sử dụng cơ chế Reference Counting kết hợp với bộ gom rác tuần hoàn (Generational Cyclic Garbage Collector).
5. <b>Hệ sinh thái 'Batteries Included'</b>: Thư viện tiêu chuẩn phong phú (os, sys, itertools, asyncio, math...) và kho package PyPI khổng lồ với hơn 500,000 thư viện.""",
        "code_example": """# 1. Cú pháp thụt lề rõ ràng & Dynamically Typed
x = 10          # x là int
x = "Python 3"  # x chuyển thành str hợp lệ (Dynamically typed)

# 2. Strongly Typed: Không tự ép kiểu ngầm gây lỗi tiềm ẩn
try:
    result = "Tuổi: " + 25
except TypeError as e:
    print(f"Lỗi: {e}")  # can only concatenate str to str

# Cách viết chuẩn Pythonic
result = f"Tuổi: {25}"
print(result)  # Output: Tuổi: 25""",
        "tips": "Nhà tuyển dụng rất thích nghe bạn phân biệt rõ: 'Dynamic typing' (biến gán kiểu lúc runtime) khác với 'Strong typing' (không tự ép kiểu ngầm). Đừng nhầm lẫn Python là 'weakly typed'!"
    },
    {
        "id": 2,
        "category": "Python Fundamentals",
        "title_en": "How is Python executed?",
        "title_vi": "Python được thực thi như thế nào (Quá trình thực thi mã nguồn)?",
        "level": "Mid",
        "short_answer": "Python là ngôn ngữ thông dịch kết hợp biên dịch bytecode. Quá trình gồm 2 bước: Trình biên dịch CPython dịch mã nguồn `.py` thành bytecode trung gian (`.pyc` trong thư mục `__pycache__`), sau đó Python Virtual Machine (PVM) thông dịch từng chỉ lệnh bytecode thành mã máy của CPU.",
        "deep_dive": """Quy trình thực thi chi tiết trong CPython:
1. <b>Lexing & Parsing</b>: Mã nguồn Python được tách thành token và chuyển thành cây cú pháp trừu tượng (Abstract Syntax Tree - AST).
2. <b>Bytecode Compilation</b>: Trình biên dịch chuyển AST thành bytecode — chuỗi chỉ lệnh nhị phân cấp thấp độc lập nền tảng (nằm trong file <code>.pyc</code> lưu tại <code>__pycache__</code> để cache lần chạy sau).
3. <b>PVM (Python Virtual Machine) Loop</b>: PVM là một stack-based virtual machine viết bằng C, duyệt qua từng opcode (như <code>LOAD_CONST</code>, <code>BINARY_OP</code>, <code>STORE_NAME</code>) và gọi các hàm C tương ứng để CPU thực thi.
4. <b>Các implementation khác</b>:
   - <b>CPython</b>: Bản chuẩn bằng C.
   - <b>PyPy</b>: Dùng JIT (Just-In-Time) compiler, nhanh hơn 4-7 lần cho tác vụ tính toán.
   - <b>Jython / IronPython</b>: Chạy trên JVM / .NET CLR.""",
        "code_example": """import dis

def add(a, b):
    return a + b

# Dùng module 'dis' (Disassembler) để xem trực tiếp Bytecode mà PVM thực thi:
print("--- Bytecode của hàm add ---")
dis.dis(add)

# Output bytecode mẫu:
#   2           0 RESUME                   0
#   3           2 LOAD_FAST                0 (a)
#               4 LOAD_FAST                1 (b)
#               6 BINARY_OP                0 (+)
#              10 RETURN_VALUE""",
        "tips": "Nếu phỏng vấn hỏi 'Python là interpreted hay compiled?', câu trả lời chuẩn Senior là: 'Python kết hợp cả hai: Biên dịch trước thành Bytecode (.pyc) rồi mới thông dịch qua PVM'."
    },
    {
        "id": 3,
        "category": "Python Fundamentals",
        "title_en": "What is PEP 8 and why is it important?",
        "title_vi": "PEP 8 là gì và tại sao nó lại quan trọng trong dự án Python?",
        "level": "Junior",
        "short_answer": "PEP 8 (Python Enhancement Proposal 8) là bộ quy chuẩn hướng dẫn phong cách viết code (Style Guide) chính thức của Python. Nó quan trọng vì giúp code nhất quán, dễ đọc, dễ bảo trì và giảm thiểu lỗi trong làm việc nhóm.",
        "deep_dive": """Các quy tắc PEP 8 quan trọng nhất cần thuộc nằm lòng:
1. <b>Thụt lề (Indentation)</b>: Dùng 4 dấu cách (spaces) cho mỗi cấp thụt lề, KHÔNG BAO GIỜ dùng phím Tab hoặc trộn lẫn Tab và Space.
2. <b>Độ dài dòng tối đa</b>: Giới hạn tối đa 79 ký tự cho code và 72 ký tự cho docstring/comment.
3. <b>Quy ước đặt tên (Naming Conventions)</b>:
   - Biến và hàm: <code>snake_case</code> (ví dụ: <code>calculate_total_price()</code>)
   - Lớp (Class): <code>PascalCase / CapWords</code> (ví dụ: <code>UserProfileService</code>)
   - Hằng số: <code>UPPER_SNAKE_CASE</code> (ví dụ: <code>MAX_RETRIES = 5</code>)
   - Thuộc tính private: Tiền tố dấu gạch dưới <code>_internal_method</code> hoặc <code>__mangled_var</code>
4. <b>Khoảng trắng (Whitespace)</b>:
   - Dùng 1 khoảng trắng quanh các toán tử gán, so sánh: <code>x = a + b</code>
   - Không có khoảng trắng ngay sau dấu ngoặc: <code>spam(ham[1], {eggs: 2})</code>
5. <b>Công cụ tự động hóa</b>: Dự án thực tế thường dùng <code>black</code>, <code>ruff</code>, <code>flake8</code> để tự động format code theo PEP 8.""",
        "code_example": """# ❌ Vi phạm PEP 8:
class user_profile:
    def __init__(self,Name,Age):
        self.Name=Name; self.Age=Age
    def GetInfo( self ):
        return self.Name+': '+str(self.Age)

#  Chuẩn PEP 8:
class UserProfile:
    \"\"\"Đại diện cho thông tin người dùng tuân thủ PEP 8.\"\"\"

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def get_info(self) -> str:
        return f"{self.name}: {self.age}" """,
        "tips": "Hãy đề cập thêm việc bạn tích hợp linter/formatter như `ruff` hoặc `pre-commit hook` vào CI/CD pipeline để đảm bảo toàn đội ngũ luôn tuân thủ PEP 8."
    },
    {
        "id": 4,
        "category": "Python Fundamentals",
        "title_en": "How is memory allocation and garbage collection handled in Python?",
        "title_vi": "Quản lý cấp phát bộ nhớ và gom rác (Garbage Collection) hoạt động như thế nào trong Python?",
        "level": "Senior",
        "short_answer": "CPython quản lý bộ nhớ thông qua cơ chế đếm tham chiếu (Reference Counting) làm tuyến phòng thủ đầu tiên. Khi số tham chiếu về 0, vùng nhớ được giải phóng ngay lập tức. Để giải quyết vấn đề tham chiếu vòng (cyclic references), Python bổ sung bộ Generational Garbage Collector chia làm 3 thế hệ (Gen 0, 1, 2).",
        "deep_dive": """Kiến trúc bộ nhớ trong CPython gồm 2 tầng chính:
1. <b>Python Memory Manager & PyMalloc</b>:
   - Python quản lý một vùng heap riêng biệt (Private Heap). Dưới 512 bytes, Python dùng <code>PyMalloc</code> với cơ chế chia nhỏ thành Arenas (256KB), Pools (4KB), và Blocks để tránh phân mảnh bộ nhớ khi cấp phát cho hàng triệu object nhỏ.
2. <b>Reference Counting (Bộ đếm tham chiếu)</b>:
   - Mỗi PyObject đều có trường <code>ob_refcnt</code>. Khi object được gán, truyền vào hàm, hoặc thêm vào list -> <code>ob_refcnt += 1</code>. Khi ra khỏi scope hoặc bị <code>del</code> -> <code>ob_refcnt -= 1</code>. Về 0 -> thu hồi ngay.
3. <b>Generational Cyclic Garbage Collector</b>:
   - Reference Counting bất lực trước tham chiếu vòng: <code>A.child = B</code> và <code>B.parent = A</code>.
   - Module <code>gc</code> chia các object có khả năng chứa tham chiếu khác (container: list, dict, class instance) thành 3 thế hệ:
     - <b>Generation 0</b>: Các object mới tạo. Được quét thường xuyên nhất.
     - <b>Generation 1</b>: Các object sống sót qua đợt quét Gen 0.
     - <b>Generation 2</b>: Các object sống lâu năm (long-lived). Quét ít thường xuyên nhất.""",
        "code_example": """import sys
import gc

# 1. Minh họa Reference Counting
a = [1, 2, 3]
print(sys.getrefcount(a))  # Thường là 2 (a + biến tạm truyền vào getrefcount)

b = a
print(sys.getrefcount(a))  # Tăng lên 3 vì b tham chiếu tới a

# 2. Minh họa Tham chiếu vòng (Cyclic Reference)
class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

node1 = Node("A")
node2 = Node("B")
node1.ref = node2
node2.ref = node1  # Tham chiếu vòng: node1 -> node2 -> node1

del node1
del node2  # refcount không về 0, nhưng không còn biến nào trỏ tới!

# Kích hoạt Cyclic GC thủ công:
unreachable = gc.collect()
print(f"Số object rác thu gom được: {unreachable}")""",
        "tips": "Điểm cộng lớn khi phỏng vấn: Nhớ nhắc đến `__slots__` để giảm thiểu overhead bộ nhớ của dict `__dict__` và module `tracemalloc` hoặc `objgraph` để debug memory leak trong production."
    },
    {
        "id": 5,
        "category": "Python Fundamentals",
        "title_en": "What are the built-in data types in Python?",
        "title_vi": "Các kiểu dữ liệu tích hợp sẵn (Built-in Data Types) trong Python là gì?",
        "level": "Junior",
        "short_answer": "Python cung cấp các kiểu dữ liệu tích hợp chính: Kiểu số (int, float, complex), Kiểu chuỗi/dãy (str, list, tuple, range), Kiểu ánh xạ (dict), Kiểu tập hợp (set, frozenset), Kiểu Boolean (bool), Kiểu nhị phân (bytes, bytearray, memoryview) và Kiểu đặc biệt (NoneType).",
        "deep_dive": """Phân loại chuẩn theo đặc tính:
1. <b>Numeric Types</b>:
   - <code>int</code>: Số nguyên có độ chính xác vô hạn (arbitrary precision, không bị overflow như C/Java 32-bit/64-bit).
   - <code>float</code>: Số thực dấu phẩy động 64-bit theo chuẩn IEEE 754.
   - <code>complex</code>: Số phức với phần ảo <code>j</code> (ví dụ: <code>3 + 4j</code>).
2. <b>Sequence Types</b>:
   - <code>str</code>: Chuỗi ký tự Unicode, immutable.
   - <code>list</code>: Mảng động, mutable, cho phép phần tử trùng lặp và đa kiểu.
   - <code>tuple</code>: Dãy cố định, immutable, tiết kiệm bộ nhớ và hashable.
   - <code>range</code>: Tạo dãy số lười (lazy sequence), tiết kiệm RAM $O(1)$.
3. <b>Mapping Type</b>:
   - <code>dict</code>: Bảng băm key-value, từ Python 3.7+ bảo đảm thứ tự chèn (insertion order).
4. <b>Set Types</b>:
   - <code>set</code> (mutable) và <code>frozenset</code> (immutable): Chứa các phần tử duy nhất, hashable, tối ưu tra cứu $O(1)$.
5. <b>Special</b>:
   - <code>NoneType</code>: Đại diện cho giá trị rỗng/vắng mặt, là một Singleton (<code>None</code>).""",
        "code_example": """# Kiểm tra kiểu dữ liệu và thuộc tính
num = 10**50               # int độ chính xác vô hạn
text = "Hello Python"      # str
numbers = [1, 2.5, "ba"]   # list đa kiểu
coords = (10.5, 20.8)      # tuple
unique_ids = {101, 102}    # set
user_map = {"id": 1}       # dict
is_active = True           # bool (subclass của int)
empty_val = None           # NoneType

print(type(num), type(unique_ids), type(empty_val))
# <class 'int'> <class 'set'> <class 'NoneType'>""",
        "tips": "Cần nhấn mạnh rằng trong Python `bool` thực chất là subclass của `int` (với `True == 1` và `False == 0`). Kiểm tra type nên dùng `isinstance(x, int)` thay vì `type(x) == int` để hỗ trợ đa hình."
    },
    {
        "id": 6,
        "category": "Python Fundamentals",
        "title_en": "Explain the difference between a mutable and immutable object.",
        "title_vi": "Giải thích sự khác biệt giữa Mutable Object và Immutable Object?",
        "level": "Junior",
        "short_answer": "Mutable object (đối tượng khả biến) có thể thay đổi trạng thái hoặc nội dung ngay tại địa chỉ bộ nhớ ban đầu sau khi tạo (ví dụ: list, dict, set). Immutable object (đối tượng bất biến) không thể thay đổi nội dung sau khi khởi tạo; mọi thao tác chỉnh sửa đều tạo ra một đối tượng mới ở địa chỉ bộ nhớ khác (ví dụ: int, float, str, tuple, frozenset).",
        "deep_dive": """Bản chất bộ nhớ và tác động:
1. <b>Cơ chế `id()` và Memory Address</b>:
   - Với Immutable (như <code>str</code>, <code>int</code>): Thao tác cộng chuỗi hoặc cộng dồn <code>s += 'a'</code> sẽ cấp phát một object mới và trỏ biến sang <code>id</code> mới.
   - Với Mutable (như <code>list</code>): <code>lst.append(5)</code> sửa trực tiếp trên mảng buffer hiện tại, giữ nguyên <code>id</code>.
2. <b>Tính chất Hashable & Dict Key</b>:
   - Chỉ các object <b>Immutable</b> mới có thể tính toán được hash code ổn định (<code>hash()</code>) -> do đó chỉ có immutable objects (str, int, tuple chứa toàn immutable) mới được dùng làm <b>Key của dict</b> hoặc phần tử của <b>Set</b>.
   - List, dict, set không hashable (sẽ văng <code>TypeError: unhashable type: 'list'</code>).
3. <b>Bẫy tham số mặc định (Default Argument Trap)</b>:
   - Dùng mutable object làm default argument trong hàm sẽ bị lưu giữ trạng thái giữa các lần gọi hàm.""",
        "code_example": """# 1. Immutable minh họa:
x = 100
old_id = id(x)
x += 1
print(id(x) == old_id)  # False: Đối tượng mới đã được sinh ra!

# 2. Mutable minh họa:
arr = [1, 2]
old_arr_id = id(arr)
arr.append(3)
print(id(arr) == old_arr_id)  # True: Thay đổi nội dung in-place!

# 3. Bẫy kinh điển: Mutable Default Argument
def add_item(item, target_list=[]):  # ❌ KHÔNG NÊN DÙNG!
    target_list.append(item)
    return target_list

print(add_item("A"))  # ['A']
print(add_item("B"))  # ['A', 'B'] -> target_list bị dùng chung giữa các lần gọi!

# Cách sửa đúng:
def add_item_fixed(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list""",
        "tips": "90% phỏng vấn Python sẽ hỏi về Mutable Default Argument trap. Hãy chủ động phân tích bài toán `def func(val, lst=None)` để thể hiện sự vững vàng."
    },
    {
        "id": 7,
        "category": "Python Fundamentals",
        "title_en": "How do you handle exceptions in Python?",
        "title_vi": "Xử lý ngoại lệ (Exception Handling) trong Python được thực hiện như thế nào?",
        "level": "Junior",
        "short_answer": "Python sử dụng khối `try - except - else - finally` để bắt và xử lý lỗi. Khối `try` chứa mã có thể gây lỗi, `except` xử lý lỗi cụ thể, `else` chạy khi không có ngoại lệ nào xảy ra, và `finally` luôn luôn thực thi bất kể có lỗi hay không (thường dùng để dọn dẹp tài nguyên).",
        "deep_dive": """Cấu trúc đầy đủ và triết lý EAFP của Python:
1. <b>EAFP vs LBYL</b>:
   - Python chuộng triết lý <b>EAFP</b>: <i>'Easier to Ask for Forgiveness than Permission'</i> (Cứ thử chạy trong <code>try-except</code>, nếu lỗi thì xử lý), thay vì <b>LBYL</b>: <i>'Look Before You Leap'</i> (Kiểm tra <code>if-else</code> kiểm tra từng điều kiện trước khi thực hiện).
2. <b>Thứ tự khối</b>:
   - <code>try</code>: Chạy mã chính.
   - <code>except SpecificError as e</code>: Bắt lỗi cụ thể. Có thể có nhiều khối <code>except</code> từ cụ thể đến tổng quát.
   - <code>else</code>: Chỉ chạy nếu <code>try</code> kết thúc thành công mỹ mãn không bị lỗi. Tách bạch logic xử lý kết quả khỏi khối bắt lỗi.
   - <code>finally</code>: Đảm bảo tài nguyên (file handle, socket, DB connection) luôn được giải phóng kể cả khi hàm return giữa chừng.
3. <b>Custom Exception</b>: Tạo class kế thừa từ <code>Exception</code>.""",
        "code_example": """class InsufficientFundsError(Exception):
    \"\"\"Custom exception khi số dư tài khoản không đủ.\"\"\"
    pass

def withdraw(balance: float, amount: float) -> float:
    if amount > balance:
        raise InsufficientFundsError(f"Cần rút {amount} nhưng số dư chỉ còn {balance}!")
    return balance - amount

try:
    current_balance = 1000
    current_balance = withdraw(current_balance, 1500)
except InsufficientFundsError as err:
    print(f"Xử lý nghiệp vụ: {err}")
except Exception as unexpected:
    print(f"Lỗi không mong muốn: {unexpected}")
else:
    print(f"Rút tiền thành công! Số dư mới: {current_balance}")
finally:
    print("Giao dịch kết thúc, đóng kết nối ATM an toàn.")""",
        "tips": "Tuyệt đối tránh `except: pass` hoặc `except Exception: pass` (bắt lỗi mù quáng / bare except) vì nó sẽ nuốt luôn cả `KeyboardInterrupt` hoặc `SystemExit`, gây khó khăn cực lớn cho việc debug hệ thống."
    },
    {
        "id": 8,
        "category": "Python Fundamentals",
        "title_en": "What is the difference between list and tuple?",
        "title_vi": "Sự khác biệt giữa List và Tuple trong Python là gì?",
        "level": "Junior",
        "short_answer": "List là cấu trúc dữ liệu mutable (có thể thêm, sửa, xóa phần tử in-place), dùng cú pháp ngoặc vuông `[]`. Tuple là immutable (cố định kích thước và giá trị sau khi tạo), dùng cú pháp ngoặc tròn `()`. Do tính bất biến, Tuple an toàn dữ liệu hơn, tiết kiệm RAM hơn, chạy nhanh hơn và có thể dùng làm key trong Dictionary.",
        "deep_dive": """Bảng so sánh chi tiết giữa List và Tuple:
<table>
  <tr><th>Tiêu chí</th><th>List (<code>[]</code>)</th><th>Tuple (<code>()</code>)</th></tr>
  <tr><td><b>Mutability</b></td><td>Mutable (thay đổi được)</td><td>Immutable (bất biến)</td></tr>
  <tr><td><b>Kích thước bộ nhớ</b></td><td>Lớn hơn (có over-allocation buffer để resize mảng nhanh)</td><td>Nhỏ hơn (vừa khít số phần tử, tối ưu hóa C struct)</td></tr>
  <tr><td><b>Hiệu năng tạo</b></td><td>Chậm hơn</td><td>Nhanh hơn gấp 2-5 lần (do CPython cache lại các tuple nhỏ)</td></tr>
  <tr><td><b>Khả năng băm (Hashable)</b></td><td>Không (Unhashable, không làm dict key được)</td><td>Có (nếu mọi phần tử bên trong đều hashable)</td></tr>
  <tr><td><b>Mục đích sử dụng</b></td><td>Tập hợp các phần tử đồng nhất có thể thay đổi</td><td>Bản ghi dữ liệu (Records/Heterogeneous), tọa độ, cấu hình</td></tr>
</table>""",
        "code_example": """import sys

# 1. So sánh dung lượng bộ nhớ
lst = [1, 2, 3, 4, 5]
tup = (1, 2, 3, 4, 5)

print(f"Dung lượng List:  {sys.getsizeof(lst)} bytes")  # ~104 bytes
print(f"Dung lượng Tuple: {sys.getsizeof(tup)} bytes")  # ~80 bytes

# 2. Tuple làm key trong Dict (List sẽ ném lỗi TypeError)
location_cache = {}
point = (21.0285, 105.8542)  # Tọa độ Hà Nội
location_cache[point] = "Hà Nội"

print(location_cache[point])  # Output: Hà Nội""",
        "tips": "Nếu bạn có một tập dữ liệu cố định không thay đổi xuyên suốt chương trình, hãy luôn ưu tiên dùng Tuple thay vì List để bảo vệ dữ liệu khỏi side-effects và tối ưu hóa bộ nhớ."
    },
    {
        "id": 9,
        "category": "Python Fundamentals",
        "title_en": "How do you create a dictionary in Python?",
        "title_vi": "Cách tạo Dictionary trong Python và các phương thức phổ biến?",
        "level": "Junior",
        "short_answer": "Dictionary được tạo bằng cách sử dụng dấu ngoặc nhọn `{key: value}`, hàm khởi tạo `dict()`, phương thức `dict.fromkeys()`, hoặc Dictionary Comprehension `{k: v for ...}`.",
        "deep_dive": """Các cách khởi tạo Dictionary chuyên nghiệp:
1. <b>Cú pháp ngoặc nhọn trực tiếp</b>: <code>user = {'id': 1, 'role': 'admin'}</code>
2. <b>Dùng constructor <code>dict()</code></b>:
   - Keyword args: <code>dict(name='Alice', age=25)</code>
   - List of tuples: <code>dict([('a', 1), ('b', 2)])</code>
   - Ghép 2 list bằng <code>zip</code>: <code>dict(zip(keys, values))</code>
3. <b>Dictionary Comprehension</b>: <code>{x: x**2 for x in range(5)}</code>
4. <b>Defaultdict & Counter (module collections)</b>: Tối ưu khi xử lý key vắng mặt tránh <code>KeyError</code>.
5. <b>Bản chất bên dưới (CPython Dict)</b>:
   - Từ Python 3.6+, dict sử dụng cấu trúc Compact Hash Table (mảng hash indices kết hợp mảng entries) giúp tiết kiệm 20-25% RAM và bảo toàn thứ tự chèn (insertion order).""",
        "code_example": """# 1. Các cách khởi tạo
d1 = {"a": 1, "b": 2}
d2 = dict(a=1, b=2)
d3 = dict(zip(["a", "b"], [1, 2]))
d4 = {x: x * 2 for x in range(3)}  # {0: 0, 1: 2, 2: 4}

# 2. Truy xuất an toàn với .get() và .setdefault()
user = {"name": "Tuấn"}
age = user.get("age", 18)  # Trả về 18 nếu không có key 'age' thay vì crash

# 3. Gộp 2 dictionary (Merge operator | từ Python 3.9+)
dict_a = {"x": 1, "y": 2}
dict_b = {"y": 99, "z": 3}
merged = dict_a | dict_b   # {'x': 1, 'y': 99, 'z': 3}
print("Merged:", merged)""",
        "tips": "Nhớ nhắc đến toán tử gộp `|` và `|=` được giới thiệu từ Python 3.9 (PEP 584) — đây là câu hỏi ghi điểm cập nhật phiên bản mới."
    },
    {
        "id": 10,
        "category": "Python Fundamentals",
        "title_en": "What is the difference between == and is operator in Python?",
        "title_vi": "Sự khác biệt giữa toán tử == và is trong Python là gì?",
        "level": "Junior",
        "short_answer": "Toán tử `==` so sánh giá trị (Value Equality) của hai đối tượng (gọi hàm `__eq__`). Trong khi toán tử `is` so sánh danh tính bộ nhớ (Reference/Identity Equality) — kiểm tra xem hai biến có cùng trỏ tới một địa chỉ ô nhớ trong RAM hay không (`id(a) == id(b)`).",
        "deep_dive": """Cơ chế so sánh và hiện tượng Integer/String Caching:
1. <b>Bản chất</b>:
   - <code>a == b</code>: Hai object có chứa dữ liệu bằng nhau không?
   - <code>a is b</code>: Chúng có phải là ĐÚNG MỘT đối tượng duy nhất trong RAM không?
2. <b>Cơ chế Small Integer Caching (Số nguyên nhỏ từ -5 đến 256)</b>:
   - CPython tự động cache trước một mảng các số nguyên từ <code>-5</code> đến <code>256</code> khi khởi động. Mọi biến gán giá trị trong khoảng này đều trỏ chung vào 1 singleton C struct.
   - Ngoài khoảng này (ví dụ: 1000), mỗi lần khai báo ở scope khác nhau sẽ tạo 1 object mới trong RAM.
3. <b>String Interning</b>:
   - Các chuỗi ngắn không có khoảng trắng thường được interning để tiết kiệm RAM và tăng tốc độ so sánh bằng con trỏ.""",
        "code_example": """# 1. So sánh List
list_a = [1, 2, 3]
list_b = [1, 2, 3]

print(list_a == list_b)  # True  (Cùng giá trị phần tử)
print(list_a is list_b)  # False (Nằm ở 2 vùng nhớ RAM độc lập)

# 2. Quy tắc vàng khi so sánh với None
val = None
print(val is None)      #  Chuẩn Pythonic: So sánh danh tính với singleton None
print(val == None)      # ⚠️ Không nên dùng (có thể bị class custom ghi đè __eq__)

# 3. Integer Caching Gotcha
x = 256
y = 256
print(x is y)  # True (Nằm trong khoảng cache -5 đến 256)

m = 1000
n = 1000
# Trong terminal tương tác REPL có thể ra False, trong cùng file/code object có thể optimize ra True""",
        "tips": "Luôn luôn dùng `is None` hoặc `is not None` khi kiểm tra giá trị None, không bao giờ dùng `== None`."
    },
    {
        "id": 11,
        "category": "Python Functions and Modules",
        "title_en": "How does a Python function work?",
        "title_vi": "Hàm (Function) trong Python hoạt động như thế nào (First-class citizen)?",
        "level": "Mid",
        "short_answer": "Trong Python, hàm là 'Công dân hạng nhất' (First-class citizen). Điều này có nghĩa là hàm cũng là đối tượng (object kế thừa từ `object`), có thể được gán cho biến, lưu trong danh sách, truyền vào hàm khác như tham số, và được trả về từ hàm khác.",
        "deep_dive": """Các cơ chế chuyên sâu của hàm trong Python:
1. <b>First-Class Objects</b>: Mọi hàm tạo bằng <code>def</code> đều là một instance của class <code>function</code>, sở hữu các thuộc tính nội tại như <code>__name__</code>, <code>__doc__</code>, <code>__code__</code>, <code>__annotations__</code>.
2. <b>Cơ chế truyền tham số: 'Pass-by-assignment' (hoặc Pass-by-object-reference)</b>:
   - Nếu truyền <i>immutable object</i> (int, str): Hàm không thể sửa đổi giá trị của biến gốc bên ngoài (giống pass-by-value).
   - Nếu truyền <i>mutable object</i> (list, dict): Các thao tác sửa đổi in-place bên trong hàm sẽ làm thay đổi object gốc bên ngoài (giống pass-by-reference).
3. <b>Scope & LEGB Rule</b>: Khi tìm kiếm biến, hàm tra cứu theo thứ tự: Local -> Enclosing -> Global -> Built-in.""",
        "code_example": """# 1. Hàm là First-class citizen (Gán biến, truyền đối số)
def shout(text):
    return text.upper() + "!"

def apply_func(func, val):
    return func(val)

print(apply_func(shout, "xin chào"))  # Output: XIN CHÀO!

# 2. Cơ chế Pass-by-object-reference
def modify(numbers, val):
    numbers.append(val)  # Sửa đổi trực tiếp object mutable ngoài hàm
    val = 99             # Gán lại biến local, không ảnh hưởng số gốc

my_list = [1, 2]
my_num = 10
modify(my_list, my_num)

print(my_list)  # [1, 2, 99] -> BỊ THAY ĐỔI
print(my_num)   # 10         -> KHÔNG ĐỔI""",
        "tips": "Khi được hỏi 'Python là pass-by-value hay pass-by-reference?', đừng chọn 1 trong 2! Hãy khẳng định: 'Python là Pass-by-assignment (hay Pass-by-object-reference)' và giải thích trường hợp mutable vs immutable."
    },
    {
        "id": 12,
        "category": "Python Functions and Modules",
        "title_en": "What is a lambda function, and where would you use it?",
        "title_vi": "Lambda function là gì và khi nào nên sử dụng nó?",
        "level": "Junior",
        "short_answer": "Lambda function là hàm ẩn danh (anonymous function) được định nghĩa bằng từ khóa `lambda`. Nó chỉ được phép chứa một biểu thức đơn lẻ (single expression) và tự động trả về kết quả của biểu thức đó mà không cần lệnh `return`.",
        "deep_dive": """Đặc điểm và ứng dụng thực tế:
1. <b>Cú pháp</b>: <code>lambda arguments: expression</code>
2. <b>Giới hạn của Lambda</b>:
   - Không chứa câu lệnh gán (statements), không chứa vòng lặp <code>for/while</code>, không có <code>try-except</code>.
   - Thích hợp cho các hàm nhỏ, dùng 1 lần (throw-away functions).
3. <b>Trường hợp sử dụng thực tế (Use Cases)</b>:
   - Dùng làm <code>key</code> trong các hàm sắp xếp: <code>sorted()</code>, <code>list.sort()</code>, <code>min()</code>, <code>max()</code>.
   - Dùng trong các hàm lập trình hàm (Functional Programming): <code>map()</code>, <code>filter()</code>.
   - Dùng làm handler ngắn gọn trong GUI (Tkinter, PyQt) hoặc callback pipeline.""",
        "code_example": """# 1. Sắp xếp danh sách tuple/dict theo trường cụ thể
students = [("Huy", 8.5), ("An", 9.2), ("Bình", 7.0)]
# Sắp xếp theo điểm số tăng dần:
sorted_students = sorted(students, key=lambda s: s[1])
print(sorted_students)  # [('Bình', 7.0), ('Huy', 8.5), ('An', 9.2)]

# 2. Kết hợp với filter để lấy số chẵn
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4, 6]

# 3. PEP 8 khuyến cáo: Không nên gán lambda cho một tên biến
# ❌ Không khuyến khích: add = lambda x, y: x + y
#  Khuyến khích: def add(x, y): return x + y""",
        "tips": "PEP 8 khuyên rằng nếu bạn định đặt tên cho một hàm (ví dụ `f = lambda x: ...`), hãy dùng `def f(x):` bình thường để có stack trace và docstring rõ ràng."
    },
    {
        "id": 13,
        "category": "Python Functions and Modules",
        "title_en": "Explain *args and **kwargs in Python.",
        "title_vi": "Giải thích *args và **kwargs trong Python.",
        "level": "Junior",
        "short_answer": "`*args` cho phép hàm nhận một số lượng tùy ý các đối số vị trí (positional arguments) dưới dạng một `tuple`. `**kwargs` cho phép hàm nhận một số lượng tùy ý các đối số từ khóa (keyword arguments) dưới dạng một `dict`.",
        "deep_dive": """Cơ chế đóng gói (Packing) và mở gói (Unpacking):
1. <b>Dấu sao <code>*</code> và <code>**</code> mới là cú pháp cốt lõi</b>, tên <code>args</code> và <code>kwargs</code> chỉ là quy ước cộng đồng.
2. <b>Thứ tự định nghĩa tham số trong hàm chuẩn</b>:
   - <code>def func(standard_args, *args, keyword_only_args, **kwargs):</code>
3. <b>Unpacking khi gọi hàm</b>:
   - <code>func(*[1, 2])</code> sẽ rải các phần tử của list vào các tham số vị trí.
   - <code>func(**{'a': 1, 'b': 2})</code> sẽ rải key-value vào các tham số từ khóa.
4. <b>Ứng dụng thực tế</b>:
   - Viết Decorator bao bọc các hàm có chữ ký (signature) bất kỳ.
   - Ghi đè phương thức con gọi <code>super().__init__(*args, **kwargs)</code>.""",
        "code_example": """def log_transaction(user_id, *items, **metadata):
    print(f"User: {user_id}")
    print(f"Items (Tuple): {items}")
    print(f"Metadata (Dict): {metadata}")

# Gọi hàm với số lượng đối số linh hoạt
log_transaction(
    "U102",
    "Laptop", "Chuột không dây", "Bàn phím",
    ip="192.168.1.1", discount_code="SUMMER2026"
)

# Unpacking list và dict vào hàm
extra_items = ["Tai nghe", "Lót chuột"]
config = {"status": "pending", "payment": "credit_card"}
log_transaction("U103", *extra_items, **config)""",
        "tips": "Hãy đề cập keyword-only arguments (ví dụ: `def func(*, timeout=30)` bắt buộc caller phải truyền `func(timeout=30)` chứ không được truyền theo vị trí), tính năng rất phổ biến trong Python hiện đại."
    },
    {
        "id": 14,
        "category": "Python Functions and Modules",
        "title_en": "What are decorators in Python?",
        "title_vi": "Decorator trong Python là gì và hoạt động như thế nào?",
        "level": "Mid",
        "short_answer": "Decorator là một Design Pattern cho phép bổ sung hoặc thay đổi hành vi của một hàm hoặc class mà không cần sửa đổi mã nguồn gốc của nó. Về bản chất, Decorator là một Higher-order function nhận vào một hàm làm đối số và trả về một hàm bao bọc (wrapper function) mới.",
        "deep_dive": """Bản chất cú pháp `@decorator`:
1. Viết <code>@my_decorator</code> ngay trước định nghĩa hàm <code>def my_func(): ...</code> tương đương hoàn toàn với phép gán:
   <code>my_func = my_decorator(my_func)</code>
2. <b>Sử dụng <code>functools.wraps</code></b>:
   - Khi bọc hàm, metadata của hàm gốc (<code>__name__</code>, <code>__doc__</code>) sẽ bị ghi đè bởi wrapper. Dùng <code>@wraps(func)</code> để bảo tồn thông tin gốc.
3. <b>Decorator có đối số (Decorator Factory)</b>:
   - Cần thêm 1 tầng hàm bên ngoài (3 tầng hàm lồng nhau): tầng nhận tham số cấu hình -> tầng nhận hàm -> wrapper.
4. <b>Ứng dụng thực tế</b>:
   - Đo thời gian thực thi (Benchmarking/Profiling).
   - Xác thực & Phân quyền (Authentication/Authorization trong Django/Flask).
   - Caching (ví dụ: <code>@functools.lru_cache</code>).
   - Rate limiting, retry logic khi gọi API bên thứ 3.""",
        "code_example": """import time
from functools import wraps

def time_tracker(func):
    \"\"\"Decorator đo thời gian chạy của hàm.\"\"\"
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"⏱️ Hàm '{func.__name__}' thực thi trong {duration:.4f} giây")
        return result
    return wrapper

@time_tracker
def heavy_calculation(n):
    return sum(i * i for i in range(n))

res = heavy_calculation(1_000_000)
# Output:
# ⏱️ Hàm 'heavy_calculation' thực thi trong 0.0482 giây""",
        "tips": "Luôn luôn dùng `@functools.wraps(func)` trong wrapper. Nếu phỏng vấn hỏi 'Tại sao cần `@wraps`?', trả lời: để tránh làm mất `__name__` và docstring của hàm gốc, giúp debug và sinh tài liệu Swagger/Sphinx chính xác."
    },
    {
        "id": 15,
        "category": "Python Functions and Modules",
        "title_en": "How can you create a module in Python?",
        "title_vi": "Cách tạo và sử dụng Module trong Python?",
        "level": "Junior",
        "short_answer": "Một module trong Python đơn giản là bất kỳ file mã nguồn nào có phần mở rộng `.py` (chứa các định nghĩa biến, hàm, class). Để sử dụng, ta dùng từ khóa `import module_name` hoặc `from module_name import something`.",
        "deep_dive": """Nguyên lý nạp module trong CPython:
1. Khi câu lệnh <code>import math</code> được gọi:
   - Python kiểm tra cache <code>sys.modules</code> xem module đã được load chưa.
   - Nếu chưa, Python tìm kiếm file theo danh sách thư mục trong <code>sys.path</code>.
   - Biên dịch file sang bytecode (lưu cache trong <code>__pycache__</code>).
   - Thực thi mã từ trên xuống dưới trong một namespace riêng và lưu vào <code>sys.modules</code>.
2. <b>Tránh import vòng tròn (Circular Import)</b>:
   - Xảy ra khi file A import file B, và file B lại import file A.
   - Cách khắc phục: Tái cấu trúc tách logic dùng chung ra module C, hoặc import bên trong hàm (local import).""",
        "code_example": """# File 1: utils.py
def format_currency(amount: float) -> str:
    return f"{amount:,.0f} VND"

APP_VERSION = "2.5.0"

# File 2: main.py
import utils
from utils import format_currency

print(utils.APP_VERSION)            # 2.5.0
print(format_currency(5000000))     # 5,000,000 VND""",
        "tips": "Tránh dùng `from module import *` (wildcard import) vì nó gây ô nhiễm namespace toàn cục, khó biết hàm nào đến từ đâu và dễ bị ghi đè tên biến bất ngờ."
    },
    {
        "id": 16,
        "category": "Python Functions and Modules",
        "title_en": "How do you share global variables across modules?",
        "title_vi": "Cách chia sẻ biến toàn cục (Global Variables) an toàn giữa các module?",
        "level": "Mid",
        "short_answer": "Cách chuẩn mực nhất trong Python là tạo một module cấu hình riêng biệt (ví dụ: `config.py` hoặc `shared_state.py`). Tất cả các module khác đều import module này và truy xuất/cập nhật thông qua thuộc tính của nó (`config.variable`).",
        "deep_dive": """Tại sao không nên dùng `from config import my_var` để chia sẻ trạng thái thay đổi?
1. <b>Bản chất gán tham chiếu</b>:
   - Khi làm <code>from config import my_var</code>, module hiện tại tạo một biến cục bộ trỏ tới object đó. Nếu gán lại <code>my_var = new_val</code>, chỉ có biến cục bộ bị thay đổi, file <code>config.py</code> gốc không hề thay đổi!
2. <b>Cách tiếp cận đúng (Canonical Pattern)</b>:
   - Luôn dùng <code>import config</code> rồi truy xuất <code>config.my_var = new_val</code>. Vì <code>config</code> được cache là một đối tượng duy nhất trong <code>sys.modules</code>, mọi file import <code>config</code> sẽ cùng nhìn thấy giá trị mới nhất.
3. <b>Mô hình Singleton / Config Class</b>:
   - Trong ứng dụng lớn, nên bọc cấu hình trong một class hoặc dùng Pydantic BaseSettings.""",
        "code_example": """# File: config.py (Module lưu trữ trạng thái chia sẻ)
database_url = "sqlite:///app.db"
active_users_count = 0

# File: service.py
import config

def user_login():
    config.active_users_count += 1
    print(f"User đăng nhập. Tổng online: {config.active_users_count}")

# File: main.py
import config
import service

print("Ban đầu:", config.active_users_count)  # 0
service.user_login()                         # 1
print("Sau khi login:", config.active_users_count)  # 1""",
        "tips": "Tuyệt đối không lạm dụng `builtins` (gán vào `__builtins__`) để tạo biến global vì sẽ phá vỡ tính đóng gói và gây ác mộng khi viết Unit Test."
    },
    {
        "id": 17,
        "category": "Python Functions and Modules",
        "title_en": "What is the use of if __name__ == '__main__':?",
        "title_vi": "Ý nghĩa và tác dụng của câu lệnh if __name__ == '__main__':?",
        "level": "Junior",
        "short_answer": "Câu lệnh này dùng để kiểm tra xem file Python hiện tại đang được thực thi trực tiếp từ dòng lệnh (như chương trình chính) hay đang được import như một thư viện vào file khác. Mã bên trong khối `if` sẽ CHỈ chạy khi file được chạy trực tiếp.",
        "deep_dive": """Biến đặc biệt `__name__` hoạt động ra sao:
1. Mỗi khi Python nạp một file mã nguồn, PVM tự động gán giá trị cho biến ẩn <code>__name__</code>:
   - Nếu file được chạy trực tiếp (ví dụ: <code>python app.py</code>): <code>__name__</code> được gán bằng chuỗi <code>'__main__'</code>.
   - Nếu file được import vào file khác (ví dụ: <code>import app</code>): <code>__name__</code> sẽ mang giá trị là tên của module (<code>'app'</code>).
2. <b>Lợi ích cốt lõi</b>:
   - Cho phép viết code kiểm thử, demo mẫu hoặc chạy script độc lập mà không sợ code đó tự động chạy khi người khác import module của bạn.""",
        "code_example": """# File: math_helper.py
def square(n):
    return n * n

# Khối này chỉ chạy khi gõ: python math_helper.py
# Sẽ KHÔNG chạy nếu ai đó viết: from math_helper import square
if __name__ == "__main__":
    print("Đang chạy ở chế độ kiểm thử nội bộ:")
    assert square(4) == 16
    print("Test passed: square(4) == 16")""",
        "tips": "Đây là câu hỏi kinh điển dành cho Junior/Fresher để đánh giá xem ứng viên có hiểu cách module hoạt động hay chỉ copy-paste code theo thói quen."
    },
    {
        "id": 18,
        "category": "Python Functions and Modules",
        "title_en": "What are Python namespaces?",
        "title_vi": "Namespace (Không gian tên) trong Python là gì?",
        "level": "Mid",
        "short_answer": "Namespace là một bảng ánh xạ (dictionary) từ tên định danh (tên biến, hàm, class) sang các đối tượng thực tế trong bộ nhớ RAM. Nó đảm bảo các tên biến không bị xung đột dù trùng tên ở các phạm vi (scopes) khác nhau.",
        "deep_dive": """3 loại Namespace chính trong Python và vòng đời:
1. <b>Built-in Namespace</b>:
   - Chứa các hàm/hằng số tích hợp sẵn như <code>print</code>, <code>len</code>, <code>int</code>, <code>ValueError</code>.
   - Được tạo khi trình thông dịch Python khởi động và tồn tại vĩnh viễn cho đến khi tắt.
2. <b>Global Namespace</b>:
   - Được tạo riêng cho mỗi module khi file được nạp vào. Chứa các biến, hàm, class cấp cao nhất của module đó.
3. <b>Local Namespace</b>:
   - Được tạo khi một hàm được gọi. Chứa các tham số và biến cục bộ bên trong hàm. Bị hủy bỏ ngay khi hàm thực thi xong hoặc gặp exception.
4. <b>Quy tắc LEGB (Scope Lookup Order)</b>:
   - <b>L</b>ocal -> <b>E</b>nclosing (hàm bao ngoài) -> <b>G</b>lobal -> <b>B</b>uilt-in.""",
        "code_example": """x = "Global x"

def outer():
    x = "Enclosing x"
    
    def inner():
        x = "Local x"
        print("Trong inner:", x)       # Local x
        print("Xem locals():", locals())  # {'x': 'Local x'}
        
    inner()
    print("Trong outer:", x)          # Enclosing x

outer()
print("Toàn cục:", x)                 # Global x""",
        "tips": "Nếu muốn thay đổi biến ở Enclosing scope, dùng từ khóa `nonlocal`. Nếu muốn thay đổi biến ở Global scope, dùng từ khóa `global`."
    },
    {
        "id": 19,
        "category": "Python Functions and Modules",
        "title_en": "How does a Python module search path work?",
        "title_vi": "Cách thức tìm kiếm Module (Module Search Path) trong Python hoạt động như thế nào?",
        "level": "Mid",
        "short_answer": "Khi có lệnh `import abc`, Python sẽ duyệt qua danh sách các thư mục được lưu trong `sys.path`. Thứ tự tìm kiếm là: 1. Thư mục hiện tại chứa script đang chạy, 2. Biến môi trường `PYTHONPATH`, 3. Thư viện tiêu chuẩn (Standard Library), 4. Các package cài đặt ngoài (`site-packages`).",
        "deep_dive": """Chi tiết thứ tự ưu tiên trong `sys.path`:
1. <b>Thư mục hiện tại</b>: Thư mục chứa script đầu vào hoặc thư mục làm việc hiện tại (Current Working Directory).
   - <i>Cảnh báo bẫy</i>: Nếu bạn tạo file tên là <code>math.py</code> hoặc <code>json.py</code> ngay trong thư mục dự án, nó sẽ che khuất (shadow) thư viện chuẩn của Python!
2. <b>Biến môi trường <code>PYTHONPATH</code></b>: Danh sách các đường dẫn bổ sung do lập trình viên cấu hình.
3. <b>Standard Library</b>: Các module có sẵn đi kèm với bản cài đặt Python.
4. <b>Site-packages</b>: Nơi <code>pip</code> cài các thư viện bên thứ 3 (trong virtualenv hoặc global).
5. Nếu duyệt hết mà không thấy file hoặc thư mục hợp lệ -> Ném ngoại lệ <code>ModuleNotFoundError</code>.""",
        "code_example": """import sys
from pathlib import Path

# In ra các đường dẫn tìm kiếm module
for idx, path in enumerate(sys.path):
    print(f"{idx}: {path}")

# Thêm một thư mục tùy biến vào search path khi chạy runtime
custom_lib_dir = Path(__file__).resolve().parent / "custom_libs"
if str(custom_lib_dir) not in sys.path:
    sys.path.insert(0, str(custom_lib_dir))  # Ưu tiên tìm kiếm đầu tiên""",
        "tips": "Bẫy phỏng vấn: 'Tại sao `import random` bỗng dưng báo lỗi attribute missing?'. Khả năng cao là ai đó đã vô tình tạo một file tên là `random.py` trong cùng thư mục."
    },
    {
        "id": 20,
        "category": "Python Functions and Modules",
        "title_en": "What is a Python package?",
        "title_vi": "Package trong Python là gì và vai trò của file __init__.py?",
        "level": "Junior",
        "short_answer": "Package là một thư mục chứa nhiều module (file `.py`) và có thể chứa các sub-package khác, giúp phân cấp và tổ chức cấu trúc dự án rõ ràng. Kể từ Python 3.3 (PEP 420), file `__init__.py` không còn bắt buộc (gọi là Namespace Package), nhưng vẫn thường được dùng để khởi tạo package và kiểm soát API công khai.",
        "deep_dive": """Vai trò và kỹ thuật với `__init__.py`:
1. <b>Khởi tạo Package</b>: Code trong <code>__init__.py</code> sẽ tự động thực thi khi package được import lần đầu.
2. <b>Đơn giản hóa Import API</b>: Thay vì bắt user gõ <code>from my_package.auth.oauth import login</code>, trong <code>__init__.py</code> ta có thể expose trực tiếp <code>from .auth.oauth import login</code> để user chỉ cần gọi <code>from my_package import login</code>.
3. <b>Biến <code>__all__</code></b>: Định nghĩa danh sách các module/hàm sẽ được import khi người dùng dùng cú pháp <code>from package import *</code>.""",
        "code_example": """# Cấu trúc thư mục:
# my_ecommerce/
# ├── __init__.py
# ├── orders.py
# └── payments.py

# Nội dung file: my_ecommerce/__init__.py:
\"\"\"Khởi tạo package và public API gọn gàng.\"\"\"
from .orders import create_order
from .payments import process_payment

__all__ = ["create_order", "process_payment"]

# File main.py bên ngoài:
# Người dùng có thể import cực kỳ ngắn gọn:
from my_ecommerce import create_order, process_payment""",
        "tips": "Hãy đề cập sự khác biệt giữa Regular Package (có `__init__.py`) và Namespace Package (từ PEP 420 cho phép chia sẻ 1 package name trên nhiều thư mục/repository khác nhau)."
    },
    {
        "id": 21,
        "category": "Python Advanced Concepts",
        "title_en": "What is list comprehension? Give an example.",
        "title_vi": "List Comprehension là gì? Nêu ví dụ và so sánh với vòng lặp thường.",
        "level": "Junior",
        "short_answer": "List comprehension là một cú pháp ngắn gọn, mang tính biểu cảm cao để tạo ra một danh sách mới từ một iterable có sẵn. Nó nhanh hơn vòng lặp `for` truyền thống vì được tối ưu hóa ở tầng C bytecode mà không cần liên tục gọi hàm `list.append()`.",
        "deep_dive": """Cú pháp và cơ chế tối ưu:
1. <b>Cú pháp chuẩn</b>: <code>[expression for item in iterable if condition]</code>
2. <b>Tại sao List Comprehension nhanh hơn?</b>
   - Trong vòng lặp <code>for</code> thường: Mỗi vòng lặp đều phải tra cứu thuộc tính (attribute lookup) <code>append</code> và thực thi hàm gọi.
   - List comprehension sử dụng opcode chuyên biệt cấp thấp của CPython (<code>LIST_APPEND</code>), thực hiện cấp phát và chèn trực tiếp trên C array.
3. <b>Khi nào KHÔNG NÊN dùng?</b>
   - Khi logic quá phức tạp với nhiều điều kiện if-else lồng nhau (làm giảm độ dễ đọc).
   - Khi dữ liệu cực lớn (hàng triệu phần tử) -> nên dùng Generator Expression <code>(x for x in ...)</code> để tránh tốn RAM.""",
        "code_example": """# Tạo danh sách bình phương các số chẵn từ 0 đến 9

# Cách 1: Dùng vòng lặp for truyền thống
squares_loop = []
for x in range(10):
    if x % 2 == 0:
        squares_loop.append(x ** 2)

# Cách 2: Dùng List Comprehension (Pythonic & Nhanh hơn)
squares_comp = [x ** 2 for x in range(10) if x % 2 == 0]

print("Kết quả:", squares_comp)  # [0, 4, 16, 36, 64]

# Biểu thức if-else (Ternary) bên trong List Comprehension:
labels = ["Chẵn" if n % 2 == 0 else "Lẻ" for n in range(5)]
print(labels)  # ['Chẵn', 'Lẻ', 'Chẵn', 'Lẻ', 'Chẵn']""",
        "tips": "Cần phân biệt rõ: `if` ở cuối `[x for x in ... if cond]` dùng để lọc (filtering), còn `if-else` ở đầu `[x if cond else y for x in ...]` dùng để biến đổi giá trị (mapping)."
    },
    {
        "id": 22,
        "category": "Python Advanced Concepts",
        "title_en": "Explain dictionary comprehension.",
        "title_vi": "Giải thích Dictionary Comprehension trong Python.",
        "level": "Junior",
        "short_answer": "Dictionary Comprehension là cú pháp ngắn gọn để tạo mới một từ điển (Dictionary) từ một hoặc nhiều iterable, tuân theo cấu trúc `{key_expr: value_expr for item in iterable if condition}`.",
        "deep_dive": """Các trường hợp ứng dụng thực tế phổ biến:
1. <b>Đảo ngược Key và Value</b>: Đổi chỗ từ <code>{k: v}</code> sang <code>{v: k}</code> (với điều kiện value là duy nhất và hashable).
2. <b>Lọc dữ liệu từ điển cũ</b>: Giữ lại các key/value thỏa mãn điều kiện nhất định.
3. <b>Chuẩn hóa dữ liệu</b>: Ví dụ chuyển toàn bộ key sang chữ thường (lowercase) hoặc strip khoảng trắng thừa.
4. <b>Chuyển đổi từ danh sách object sang map/index</b>: Tra cứu theo ID với độ phức tạp $O(1)$.""",
        "code_example": """# 1. Tạo dict bình phương
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 2. Đảo ngược key-value trong từ điển
original = {"admin": 1, "editor": 2, "viewer": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)  # {1: 'admin', 2: 'editor', 3: 'viewer'}

# 3. Lọc danh sách nhân viên có lương > 20 triệu
salaries = {"Tuấn": 25, "Lan": 18, "Hải": 30, "Nam": 15}
high_earners = {k: v for k, v in salaries.items() if v >= 20}
print(high_earners)  # {'Tuấn': 25, 'Hải': 30}""",
        "tips": "Nếu trong quá trình đảo ngược key-value mà value ban đầu bị trùng lặp, các key trùng phía sau sẽ ghi đè lên key phía trước mà không báo lỗi."
    },
    {
        "id": 23,
        "category": "Python Advanced Concepts",
        "title_en": "What are generators in Python, and how do you use them?",
        "title_vi": "Generator trong Python là gì và tại sao chúng lại tối ưu bộ nhớ?",
        "level": "Mid",
        "short_answer": "Generator là một loại hàm đặc biệt trả về một Iterator lười (Lazy Iterator). Thay vì lưu toàn bộ kết quả vào bộ nhớ cùng lúc như List, Generator tạo ra từng phần tử một tại thời điểm được yêu cầu (on-the-fly) bằng từ khóa `yield`. Nhờ đó mức tiêu thụ bộ nhớ luôn duy trì ở mức tối ưu $O(1)$.",
        "deep_dive": """Cơ chế hoạt động của Generator:
1. <b>Từ khóa <code>yield</code> vs <code>return</code></b>:
   - <code>return</code> trả về giá trị và giải phóng toàn bộ stack frame của hàm.
   - <code>yield</code> tạm dừng (pause) việc thực thi hàm, ghi nhớ toàn bộ trạng thái cục bộ (local variables, instruction pointer) và nhả giá trị ra ngoài. Lần gọi <code>next()</code> tiếp theo, hàm tiếp tục chạy ngay từ điểm tạm dừng.
2. <b>Generator Object Protocol</b>:
   - Một generator object cài đặt 2 phương thức: <code>__iter__()</code> và <code>__next__()</code>. Khi hết dữ liệu, nó ném ngoại lệ <code>StopIteration</code>.
3. <b>Generator Expressions</b>: Dùng cú pháp ngoặc đơn <code>(x for x in iterable)</code>.""",
        "code_example": """import sys

# 1. Generator Function đọc file log dung lượng hàng chục GB
def read_large_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()

# 2. So sánh bộ nhớ: List Comprehension vs Generator Expression
size = 1_000_000
list_data = [x for x in range(size)]       # Tốn ~8 MB RAM
gen_data  = (x for x in range(size))       # Chỉ tốn 104 bytes!

print(f"RAM của List:      {sys.getsizeof(list_data):,} bytes")
print(f"RAM của Generator: {sys.getsizeof(gen_data):,} bytes")

# Duyệt từng phần tử của Generator
print(next(gen_data))  # 0
print(next(gen_data))  # 1""",
        "tips": "Câu hỏi thực tế rất hay gặp: 'Làm sao đọc và xử lý 1 file CSV 50GB trên máy chỉ có 8GB RAM?'. Đáp án chuẩn là: 'Dùng Generator để stream từng dòng hoặc đọc theo chunk, không bao giờ dùng `readlines()` hay nạp cả file'."
    },
    {
        "id": 24,
        "category": "Python Advanced Concepts",
        "title_en": "How do you implement concurrency in Python?",
        "title_vi": "Các phương pháp triển khai Concurrency (Đồng thời) trong Python và khi nào dùng cái nào?",
        "level": "Senior",
        "short_answer": "Python hỗ trợ 3 mô hình xử lý đồng thời chính: 1. `threading` (Đa luồng - tối ưu cho I/O-bound), 2. `multiprocessing` (Đa tiến trình - tối ưu cho CPU-bound để vượt qua GIL), 3. `asyncio` (Bất đồng bộ đơn luồng dựa trên Event Loop - tối ưu cho kết nối mạng quy mô lớn/Web sockets).",
        "deep_dive": """Bảng phân biệt chọn mô hình Concurrency chuẩn:
<table>
  <tr><th>Mô hình</th><th>Cơ chế</th><th>Tối ưu cho</th><th>Ảnh hưởng bởi GIL?</th></tr>
  <tr><td><b>threading</b> (Preemptive multitasking)</td><td>Nhiều thread trong 1 process, chung bộ nhớ</td><td>I/O-bound (gọi HTTP API, đọc ghi file, truy vấn DB)</td><td>Có (GIL khóa luồng chạy mã Python)</td></tr>
  <tr><td><b>multiprocessing</b> (True Parallelism)</td><td>Mỗi process có Python interpreter & bộ nhớ riêng</td><td>CPU-bound (xử lý ảnh, mã hóa, tính toán ma trận, AI)</td><td>Không (mỗi process có 1 GIL riêng)</td></tr>
  <tr><td><b>asyncio</b> (Cooperative multitasking)</td><td>Đơn luồng, chuyển đổi ngữ cảnh tự nguyện qua coroutine</td><td>Cực nhiều kết nối I/O đồng thời (10,000+ websockets/microservices)</td><td>Không bị xung đột race conditions luồng</td></tr>
</table>""",
        "code_example": """import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 1. Ví dụ AsyncIO cho I/O-bound
async def fetch_data(task_id, delay):
    await asyncio.sleep(delay)
    return f"Task {task_id} done"

async def main_async():
    results = await asyncio.gather(fetch_data(1, 0.5), fetch_data(2, 0.5))
    print("AsyncIO results:", results)

# 2. Ví dụ ProcessPoolExecutor cho CPU-bound
def cpu_heavy_task(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    asyncio.run(main_async())
    
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(cpu_heavy_task, 10_000_000) for _ in range(4)]
        print("Multiprocessing hoàn thành:", len(futures))""",
        "tips": "Nguyên tắc vàng: Nhiệm vụ tính toán nặng CPU -> `multiprocessing`. Nhiệm vụ chờ mạng/I/O thông thường -> `threading` hoặc `asyncio`."
    },
    {
        "id": 25,
        "category": "Python Advanced Concepts",
        "title_en": "What are coroutines and how do they differ from threads?",
        "title_vi": "Coroutine là gì và chúng khác biệt như thế nào so với Thread?",
        "level": "Senior",
        "short_answer": "Coroutine là một hàm đặc biệt có thể tạm dừng (suspend) và tiếp tục thực thi sau đó (resume) tại các điểm `await` mà không làm nghẽn luồng. Coroutine hoạt động theo cơ chế hợp tác (Cooperative multitasking) do ứng dụng kiểm soát, trong khi Thread do Hệ điều hành lên lịch ép buộc (Preemptive multitasking) và tốn tài nguyên chuyển ngữ cảnh hơn nhiều.",
        "deep_dive": """So sánh Coroutine vs OS Thread:
1. <b>Chi phí tài nguyên (Overhead)</b>:
   - <b>Thread</b>: Mỗi OS thread tốn khoảng 8MB bộ nhớ stack và việc chuyển đổi ngữ cảnh (Context Switching) phải gọi xuống kernel của hệ điều hành. Tạo 10,000 threads có thể làm sập hệ thống.
   - <b>Coroutine</b>: Chỉ là một object Python trong heap (vài KB). Ta có thể chạy hàng trăm nghìn coroutines trên 1 thread duy nhất.
2. <b>Cơ chế chuyển đổi (Switching)</b>:
   - <b>Thread</b>: Bị HĐH ngắt bất kỳ lúc nào (Preemptive) -> Rất dễ bị Race Condition, cần dùng Lock, Semaphore, Mutex để đồng bộ.
   - <b>Coroutine</b>: Chỉ nhường quyền điều khiển khi gặp từ khóa <code>await</code> (Cooperative) -> Không sợ race condition giữa 2 bước tính toán liên tiếp trên cùng 1 luồng.""",
        "code_example": """import asyncio

# Định nghĩa Coroutine bằng 'async def'
async def simulate_api_call(service_name, delay):
    print(f"➡️ Gọi {service_name}...")
    await asyncio.sleep(delay)  # Tạm dừng tại đây, nhường CPU cho coroutine khác
    print(f"⬅️ Nhận phản hồi từ {service_name}")
    return {"service": service_name, "status": "success"}

async def main():
    # Chạy 3 coroutines đồng thời trên cùng 1 thread duy nhất:
    results = await asyncio.gather(
        simulate_api_call("Service Auth", 1.0),
        simulate_api_call("Service Payment", 0.5),
        simulate_api_call("Service Notification", 0.8)
    )
    print("Tất cả đã xong:", results)

asyncio.run(main())""",
        "tips": "Nếu trong một hàm `async def` bạn vô tình gọi một hàm chặn (blocking) như `time.sleep()` hoặc `requests.get()`, toàn bộ Event Loop sẽ bị 'đóng băng'. Phải dùng thư viện async tương ứng (`asyncio.sleep()`, `httpx`, `aiohttp`)."
    }
]
