# -*- coding: utf-8 -*-
"""
Generator for Django Interview Questions & Answers HTML (70 Questions)
Based on Devinterview.io & python.docx
"""

import html
import json
from pathlib import Path

# Load question titles
with open('/tmp/all_django_questions.json', 'r', encoding='utf-8') as f:
    RAW_DJANGO_QS = json.load(f)

# Comprehensive answers database for Django 70 questions
DJANGO_ANSWERS_DB = {
    1: {
        "title_vi": "Django là gì và các tính năng cốt lõi làm nên sức mạnh của nó?",
        "level": "Junior",
        "short_answer": "Django là một Web Framework bậc cao (high-level) mã nguồn mở viết bằng Python, tuân theo triết lý 'Batteries-Included' (đầy đủ mọi công cụ cần thiết từ ORM, Admin, Auth, Migrations đến Bảo mật) và nguyên tắc DRY (Don't Repeat Yourself), giúp lập trình viên xây dựng ứng dụng web an toàn, có khả năng mở rộng cao trong thời gian ngắn nhất.",
        "deep_dive": "Các tính năng cốt lõi: 1. <b>Django ORM</b>: Ánh xạ CSDL quan hệ sang Python Object, trừu tượng hóa SQL và chống SQL Injection. 2. <b>Automatic Admin Interface</b>: Tự động sinh trang quản trị dữ liệu CRUD chỉ với vài dòng cấu hình. 3. <b>Bảo mật tích hợp</b>: Chống mặc định CSRF, XSS, Clickjacking và SQL Injection. 4. <b>URL Dispatcher</b>: Định tuyến URL thanh lịch bằng Regex hoặc Path converters. 5. <b>Template Engine</b>: Kế thừa template linh hoạt. 6. <b>Form Handling</b>: Tự động render HTML form và validate dữ liệu chặt chẽ.",
        "code_example": """# Khởi tạo Django app và model trong vài dòng code:
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name="Nội dung")
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title""",
        "tips": "Nhớ nhấn mạnh triết lý 'The web framework for perfectionists with deadlines'."
    },
    2: {
        "title_vi": "Giải thích kiến trúc MTV (Model-Template-View) trong Django và so sánh với MVC?",
        "level": "Junior",
        "short_answer": "Django sử dụng biến thể MTV: **Model** (Tầng dữ liệu / ORM), **Template** (Tầng giao diện / Presentation), và **View** (Tầng xử lý logic nghiệp vụ). So với MVC truyền thống: View trong Django đóng vai trò của Controller, còn Template trong Django đóng vai trò của View; bản thân Django Framework đóng vai trò điều phối viên Controller tổng.",
        "deep_dive": "Bảng đối chiếu MTV vs MVC:\\n- <b>Model (M)</b>: Cả hai đều đại diện cho cấu trúc dữ liệu và tương tác CSDL.\\n- <b>Template (T)</b>: Tương đương với <b>View (V)</b> trong MVC — chịu trách nhiệm hiển thị HTML cho người dùng.\\n- <b>View (V)</b>: Tương đương với <b>Controller (C)</b> trong MVC — nhận HttpRequest, gọi Model lấy dữ liệu, xử lý logic và trả về HttpResponse kèm Template đã render.",
        "code_example": """# 1. Model (models.py)
class Product(models.Model):
    name = models.CharField(max_length=100)

# 2. View (views.py) - Đóng vai trò Controller xử lý logic
from django.shortcuts import render
def product_list(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})

# 3. Template (products.html) - Đóng vai trò View hiển thị
<!-- {% for p in products %} <li>{{ p.name }}</li> {% endfor %} -->""",
        "tips": "Interviewer rất hay hỏi câu này để xem ứng viên có hiểu vì sao file views.py lại không phải là giao diện HTML hay không."
    },
    3: {
        "title_vi": "Phân biệt Django Project và Django App?",
        "level": "Junior",
        "short_answer": "Django Project là toàn bộ hệ thống web hoàn chỉnh, chứa cấu hình tổng thể (`settings.py`, `urls.py`, middleware, kết nối DB). Django App là một module tính năng độc lập, có thể tái sử dụng (ví dụ: app `authentication`, app `blog`, app `cart`). Một Project bao gồm nhiều App.",
        "deep_dive": "Quy tắc thiết kế: <i>'A project is a collection of configuration and apps; an app is a written Web application that does something.'</i> Một app tốt nên có tính gắn kết cao (high cohesion) và độc lập (low coupling), cho phép bốc sang project khác dùng lại.",
        "code_example": """# Lệnh tạo project và app:
# django-admin startproject my_ecommerce .
# python manage.py startapp orders

# Cấu trúc:
# my_ecommerce/ (Project)
#   ├── settings.py
#   ├── urls.py
# orders/ (App)
#   ├── models.py
#   ├── views.py
#   ├── admin.py""",
        "tips": "Luôn khai báo app mới tạo vào `INSTALLED_APPS` trong `settings.py`."
    },
    4: {
        "title_vi": "Vai trò và các cấu hình quan trọng nhất trong file settings.py?",
        "level": "Junior",
        "short_answer": "File `settings.py` chứa toàn bộ cấu hình toàn cục của dự án Django. Các biến quan trọng nhất: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `INSTALLED_APPS`, `MIDDLEWARE`, `DATABASES`, `TEMPLATES`, `STATIC_URL`, `MEDIA_URL`.",
        "deep_dive": "Lưu ý sống còn trên Production: 1. `DEBUG = False` (nếu để True sẽ lộ source code và biến môi trường khi có lỗi 500). 2. `SECRET_KEY` phải nạp từ biến môi trường, tuyệt đối không commit lên Git. 3. `ALLOWED_HOSTS` phải chỉ định rõ domain chính xác để chống Host Header Injection.",
        "code_example": """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Cấu hình an toàn với biến môi trường:
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-dev-only")
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost 127.0.0.1").split()""",
        "tips": "Sử dụng thư viện `python-decouple` hoặc `django-environ` để quản lý file `.env` chuyên nghiệp."
    },
    5: {
        "title_vi": "Vai trò của file urls.py và cơ chế điều hướng URL trong Django?",
        "level": "Junior",
        "short_answer": "File `urls.py` là bảng điều hướng định tuyến (URLconf) của Django. Nó ánh xạ các mẫu đường dẫn URL (URL patterns) tới các hàm View hoặc Class-Based View tương ứng để xử lý request.",
        "deep_dive": "Cơ chế: Khi request đến, Django duyệt danh sách `urlpatterns` từ trên xuống dưới. Mẫu nào khớp đầu tiên sẽ được gọi. Dùng hàm `include()` để ủy quyền định tuyến cho từng app con, giúp code module hóa sạch sẽ.",
        "code_example": """from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ủy quyền toàn bộ URL bắt đầu bằng /api/ cho app 'api':
    path('api/v1/', include('api.urls')),
]""",
        "tips": "Luôn đặt tham số `name='route_name'` để dùng hàm `reverse()` hoặc thẻ `{% url %}`, tránh hardcode URL dạng text."
    },
    6: {
        "title_vi": "Khái niệm Django ORM và ưu/nhược điểm so với viết SQL thuần?",
        "level": "Mid",
        "short_answer": "Django ORM là tầng trừu tượng hóa CSDL, cho phép thao tác với database hoàn toàn bằng code Python. Ưu điểm: Tăng tốc độ phát triển (RAD), độc lập với CSDL (chuyển đổi SQLite sang PostgreSQL không cần sửa code), tự động chống SQL Injection. Nhược điểm: Có thể sinh câu SQL chưa tối ưu và dễ gặp lỗi N+1 queries nếu dev thiếu kinh nghiệm.",
        "deep_dive": "Django ORM hỗ trợ cơ chế QuerySet Lazy Evaluation — query chỉ được thực thi khi thực sự cần dữ liệu (iteration, slicing, len). Hỗ trợ các hàm tổng hợp Aggregation (`Count`, `Sum`, `Avg`), Annotation, Subquery, F-expression và Q-expression.",
        "code_example": """# Lấy danh sách user đang active có tuổi >= 18:
active_adults = User.objects.filter(is_active=True, age__gte=18).order_by("-created_at")

# Câu lệnh SQL tương đương mà Django ORM tự sinh ngầm:
# SELECT * FROM auth_user WHERE is_active = TRUE AND age >= 18 ORDER BY created_at DESC;""",
        "tips": "Nhớ nhấn mạnh: 'Khi cần tối ưu hiệu năng tối đa cho các báo cáo phức tạp hàng chục bảng JOIN, Django vẫn cho phép gọi SQL thuần qua `raw()` hoặc `connection.cursor()`'."
    },
    7: {
        "title_vi": "Django Model là gì và cách định nghĩa một Model chuẩn?",
        "level": "Junior",
        "short_answer": "Model là nguồn thông tin duy nhất và chân thực về dữ liệu của bạn trong Django. Mỗi Model là một Python Class kế thừa từ `django.db.models.Model`, trong đó mỗi thuộc tính của class tương ứng với một cột trong bảng CSDL.",
        "deep_dive": "Các thành phần chuẩn của một Model chuyên nghiệp: 1. Các trường dữ liệu (Fields: CharField, IntegerField, DateTimeField, ForeignKey...). 2. Class `Meta` cấu hình bảng (db_table, ordering, indexes, constraints). 3. Phương thức `__str__()` để hiển thị tên thân thiện trên Admin. 4. Phương thức `get_absolute_url()` cho SEO.",
        "code_example": """from django.db import models
from django.urls import reverse

class Customer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Tên khách hàng")
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Khách hàng"
        indexes = [models.Index(fields=["email"])]

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_absolute_url(self):
        return reverse("customer-detail", kwargs={"pk": self.pk})""",
        "tips": "Luôn định nghĩa `__str__()` cho mọi Model để tránh hiển thị 'Customer object (1)' trên Django Admin."
    },
    8: {
        "title_vi": "Mục đích và cách tùy biến giao diện Django Admin?",
        "level": "Junior",
        "short_answer": "Django Admin là một ứng dụng giao diện web quản trị tự động sinh ra từ metadata của các Model. Nó cho phép người quản trị thực hiện các thao tác CRUD dữ liệu nhanh chóng mà không cần viết giao diện frontend riêng.",
        "deep_dive": "Các thuộc tính tùy biến mạnh mẽ trong `ModelAdmin`: `list_display` (các cột hiển thị), `search_fields` (thanh tìm kiếm), `list_filter` (bộ lọc bên phải), `readonly_fields` (trường chỉ đọc), `inlines` (chỉnh sửa bảng con 1-N trực tiếp trên trang cha).",
        "code_example": """from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)""",
        "tips": "Trong production, hãy đổi URL admin mặc định từ `/admin/` sang một đường dẫn bí mật để tránh bị brute-force bot tấn công."
    },
    9: {
        "title_vi": "Django View là gì và phân biệt Function-Based View (FBV) vs Class-Based View (CBV)?",
        "level": "Mid",
        "short_answer": "View là hàm hoặc class tiếp nhận `HttpRequest` và trả về `HttpResponse`. FBV (Function-Based View) viết bằng hàm thuần túy, đơn giản, dễ đọc cho logic ngắn. CBV (Class-Based View) viết bằng class, tận dụng tính kế thừa và Generic Views (`ListView`, `DetailView`, `CreateView`) để tái sử dụng mã tối đa trong các bài toán CRUD chuẩn.",
        "deep_dive": "So sánh FBV vs CBV:\\n- FBV: Luồng chạy rõ ràng từ trên xuống dưới, dễ debug, dễ dùng decorator `@login_required`. Phù hợp API hoặc logic phức tạp đặc thù.\\n- CBV: Tổ chức code tốt, tái sử dụng logic qua Mixin (`LoginRequiredMixin`), giảm code lặp lại 70% với CRUD. Nhược điểm: Phức tạp hơn và luồng thực thi bị ẩn trong các phương thức của class cha.",
        "code_example": """# 1. FBV (Function-Based View):
from django.shortcuts import render, get_object_or_404
from .models import Customer

def customer_detail_fbv(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customer_detail.html", {"customer": customer})

# 2. CBV (Class-Based View tương đương):
from django.views.generic import DetailView

class CustomerDetailCBV(DetailView):
    model = Customer
    template_name = "customer_detail.html"
    context_object_name = "customer" """,
        "tips": "Nguyên tắc chọn: Dùng CBV cho các trang CRUD chuẩn; dùng FBV cho các endpoint tùy biến cao hoặc xử lý luồng đặc biệt."
    },
    10: {
        "title_vi": "Cơ chế URL patterns và Path Converters trong Django?",
        "level": "Junior",
        "short_answer": "Từ Django 2.0+, `path()` hỗ trợ Path Converters dạng `<converter:param_name>` để tự động bắt tham số từ URL và ép sang đúng kiểu dữ liệu Python tương ứng trước khi truyền vào View (ví dụ: `str`, `int`, `slug`, `uuid`, `path`).",
        "deep_dive": "Các Path Converter tích hợp sẵn: 1. `int`: Số nguyên dương. 2. `str`: Bất kỳ chuỗi ký tự nào không chứa dấu gạch chéo `/`. 3. `slug`: Chuỗi chữ, số, gạch nối, gạch dưới. 4. `uuid`: Định dạng UUID chuẩn. 5. `path`: Khớp toàn bộ đường dẫn kể cả dấu `/`. Nếu cần regex phức tạp, dùng `re_path()`.",
        "code_example": """from django.urls import path
from . import views

urlpatterns = [
    # Tự động ép 'order_id' thành int, nếu gõ chữ sẽ trả về 404 ngay:
    path("orders/<int:order_id>/", views.order_detail, name="order-detail"),
    # Bắt bài viết theo slug:
    path("posts/<slug:post_slug>/", views.post_detail, name="post-detail"),
]""",
        "tips": "Bạn có thể tự tạo Custom Path Converter bằng cách định nghĩa class có thuộc tính `regex` và 2 phương thức `to_python()` và `to_url()`."
    },
    11: {
        "title_vi": "Database Migration trong Django là gì và quy trình hoạt động?",
        "level": "Junior",
        "short_answer": "Migration là cách Django truyền bá các thay đổi trong Model (thêm trường, xóa cột, đổi ràng buộc) vào Schema của CSDL. Hai lệnh cốt lõi: `makemigrations` (đọc Model và sinh file migration `.py`) và `migrate` (thực thi các file migration vào CSDL).",
        "deep_dive": "Bản chất: Django lưu lịch sử các lần migration trong bảng `django_migrations` trong DB để biết file nào đã chạy, file nào chưa. Hỗ trợ rollback về phiên bản cũ bằng lệnh: `python manage.py migrate <app_name> <migration_number>`.",
        "code_example": """# Quy trình cập nhật DB chuẩn:
# 1. Sửa code trong models.py
# 2. Sinh file migration:
# python manage.py makemigrations

# 3. Xem trước câu SQL mà migration sẽ chạy:
# python manage.py sqlmigrate myapp 0002

# 4. Áp dụng vào CSDL:
# python manage.py migrate""",
        "tips": "Khi làm việc nhóm bị conflict migration, dùng lệnh `python manage.py makemigrations --merge` để tự động gộp các nhánh migration."
    },
    12: {
        "title_vi": "Phân biệt ForeignKey và ManyToManyField trong Django Model?",
        "level": "Junior",
        "short_answer": "`ForeignKey` định nghĩa quan hệ Một-Nhiều (1-N): Một bản ghi ở bảng A liên kết với nhiều bản ghi ở bảng B (CSDL tạo cột khóa ngoại trực tiếp ở bảng B). `ManyToManyField` định nghĩa quan hệ Nhiều-Nhiều (N-N): CSDL tự động sinh một bảng trung gian (Junction/Through table) gồm 2 khóa ngoại để liên kết.",
        "deep_dive": "Tham số `on_delete` bắt buộc trong ForeignKey từ Django 2.0: 1. `CASCADE` (xóa cha -> xóa sạch con), 2. `PROTECT` (chặn xóa cha nếu còn con), 3. `SET_NULL` (gán null), 4. `DO_NOTHING`. Với ManyToManyField, có thể dùng tham số `through='MyCustomTable'` để lưu thêm thông tin trên quan hệ liên kết (ví dụ ngày tham gia, vai trò).",
        "code_example": """class Author(models.Model):
    name = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    title = models.CharField(max_length=200)
    # Quan hệ 1-N: 1 Tác giả viết nhiều Sách
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    # Quan hệ N-N: 1 Sách thuộc nhiều Danh mục, 1 Danh mục có nhiều Sách
    categories = models.ManyToManyField(Category, related_name="books")""",
        "tips": "Luôn đặt `related_name` có ý nghĩa để truy xuất ngược (reverse relation) từ Author sang Book: `author.books.all()`."
    },
    13: {
        "title_vi": "Cách tạo một Custom Model Field trong Django?",
        "level": "Senior",
        "short_answer": "Tạo class kế thừa từ `models.Field` (hoặc class con như `CharField`, `TextField`) và ghi đè các phương thức chính: `from_db_value()` (chuyển dữ liệu từ DB sang Python object), `to_python()` (xác thực và chuẩn hóa), và `get_prep_value()` (chuyển Python object sang giá trị DB có thể lưu).",
        "deep_dive": "Dùng custom field khi cần mã hóa tự động dữ liệu trước khi lưu DB (AES encryption), hoặc tự động nén/giải nén JSON/XML, hoặc tạo kiểu dữ liệu màu sắc HEX Color, IP Range đặc thù.",
        "code_example": """from django.db import models

class LowercaseCharField(models.CharField):
    \"\"\"Tự động chuyển toàn bộ text sang chữ thường trước khi lưu DB.\"\"\"
    def to_python(self, value):
        val = super().to_python(value)
        return val.lower() if isinstance(val, str) else val

    def get_prep_value(self, value):
        val = super().get_prep_value(value)
        return val.lower() if isinstance(val, str) else val""",
        "tips": "Nếu custom field có thể sinh migration, hãy nhớ khai báo `deconstruct()` method để Django migration engine lưu được cấu hình."
    },
    14: {
        "title_vi": "QuerySet trong Django là gì và khái niệm Lazy Evaluation?",
        "level": "Mid",
        "short_answer": "QuerySet là danh sách các đối tượng Model lấy từ CSDL. Nó có tính chất 'Lazy Evaluation' (đánh giá lười): Việc gọi `filter()`, `exclude()`, `order_by()` hoàn toàn KHÔNG kích hoạt câu lệnh SQL nào. SQL chỉ được thực thi khi bạn thực sự yêu cầu dữ liệu (duyệt vòng lặp `for`, gọi `len()`, `list()`, `bool()` hoặc slicing).",
        "deep_dive": "Lợi ích của Lazy Evaluation: Cho phép nối chuỗi (chaining) nhiều bộ lọc phức tạp liên tiếp mà không bị tốn tài nguyên gọi DB nhiều lần. Sau khi chạy, QuerySet lưu kết quả vào cache nội bộ (`_result_cache`). Nếu duyệt lại lần 2, nó dùng lại cache thay vì query lại.",
        "code_example": """# Chưa hề có câu SQL nào bắn xuống CSDL ở dòng này:
query = Product.objects.filter(is_active=True).filter(price__gt=100)

# Câu SQL CHỈ ĐƯỢC CHẠY khi bắt đầu duyệt dữ liệu:
for product in query:
    print(product.name)""",
        "tips": "Bẫy phỏng vấn: Nếu chỉ cần kiểm tra xem có bản ghi nào tồn tại không, ĐỪNG DÙNG `if len(queryset) > 0:` (sẽ nạp hết dữ liệu vào RAM). Hãy dùng `if queryset.exists():` (chỉ bắn `SELECT 1 ... LIMIT 1`)."
    },
    15: {
        "title_vi": "Các hình thức Kế thừa Model (Model Inheritance) trong Django?",
        "level": "Senior",
        "short_answer": "Django hỗ trợ 3 kiểu kế thừa Model: 1. **Abstract Base Classes** (Lớp cha trừu tượng `abstract=True` - không sinh bảng trong DB, class con kế thừa các trường), 2. **Multi-Table Inheritance** (Mỗi class có bảng riêng, liên kết bằng OneToOne ngầm), 3. **Proxy Models** (Dùng chung bảng của cha nhưng thay đổi hành vi/ordering trong Python).",
        "deep_dive": "So sánh: Abstract Base Class là lựa chọn phổ biến nhất 90% trường hợp để chia sẻ các trường chung (`created_at`, `updated_at`, `is_deleted`). Multi-table inheritance ít dùng vì gây JOIN ngầm làm chậm hiệu năng. Proxy Model dùng khi cần thêm method hoặc đổi default manager mà không sửa đổi schema CSDL.",
        "code_example": """from django.db import models

# 1. Abstract Base Class (Không tạo bảng trong DB)
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Quan trọng!

class Post(TimeStampedModel):
    title = models.CharField(max_length=200)

# 2. Proxy Model (Dùng chung bảng Post nhưng đổi hành vi)
class OrderedPostProxy(Post):
    class Meta:
        proxy = True
        ordering = ["-created_at"]""",
        "tips": "Hầu như mọi dự án production đều tạo 1 class `BaseModel(models.Model)` có `abstract = True` chứa `id (UUID)`, `created_at`, `updated_at`."
    },
    16: {
        "title_vi": "Django Model Manager là gì và cách tạo Custom Manager?",
        "level": "Mid",
        "short_answer": "Manager là giao diện qua đó các thao tác truy vấn CSDL được cung cấp cho Model Django (mặc định là `Model.objects`). Custom Manager cho phép định nghĩa các phương thức truy vấn thường dùng ở tầng model hoặc ghi đè QuerySet cơ sở (ví dụ tự động lọc bỏ các bản ghi đã xóa mềm `soft-deleted`).",
        "deep_dive": "Bằng cách kế thừa `models.Manager` và ghi đè phương thức `get_queryset()`, ta có thể tạo ra các bộ lọc mặc định cực kỳ an toàn cho toàn bộ hệ thống.",
        "code_example": """from django.db import models

class ActiveUserManager(models.Manager):
    def get_queryset(self):
        # Mặc định chỉ lấy user chưa bị khóa
        return super().get_queryset().filter(is_active=True, is_deleted=False)

class UserAccount(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()      # Manager mặc định
    active_objects = ActiveUserManager()  # Custom Manager

# Sử dụng:
# UserAccount.active_objects.all()  # Tự động lọc sạch!""",
        "tips": "Nếu muốn vừa dùng manager vừa hỗ trợ chaining query, hãy kết hợp `models.QuerySet.as_manager()`."
    },
    17: {
        "title_vi": "Mục đích của inner class Meta trong Django Model?",
        "level": "Junior",
        "short_answer": "Inner class `Meta` được dùng để khai báo các cấu hình siêu dữ liệu (metadata) của Model — những thông tin không phải là trường dữ liệu (fields), chẳng hạn như: tên bảng trong CSDL (`db_table`), thứ tự sắp xếp mặc định (`ordering`), chỉ mục (`indexes`), ràng buộc duy nhất phức tạp (`constraints`), hoặc quyền hạn (`permissions`).",
        "deep_dive": "Các cấu hình Meta quan trọng nhất: 1. `ordering = ['-created_at']`. 2. `db_table = 'tbl_custom_name'`. 3. `unique_together` hoặc hiện đại hơn là `constraints = [models.UniqueConstraint(...)]`. 4. `indexes = [models.Index(...)]` để đánh index tối ưu tốc độ đọc.",
        "code_example": """class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ecommerce_orders"
        ordering = ["-created_at"]
        verbose_name = "Đơn hàng"
        constraints = [
            models.UniqueConstraint(fields=["user", "code"], name="unique_user_order_code")
        ]""",
        "tips": "Từ Django 2.2+, khuyến nghị dùng `models.UniqueConstraint` và `models.CheckConstraint` thay cho `unique_together` cũ."
    },
    18: {
        "title_vi": "Các phương thức truy vấn dữ liệu phổ biến với Django ORM?",
        "level": "Junior",
        "short_answer": "Truy vấn lấy danh sách: `all()`, `filter()`, `exclude()`, `order_by()`. Truy vấn lấy 1 bản ghi: `get()`, `first()`, `last()`. Kiểm tra tồn tại/đếm: `exists()`, `count()`. Tìm kiếm Field Lookups: `exact`, `iexact`, `contains`, `icontains`, `in`, `gt`, `gte`, `lt`, `lte`, `startswith`.",
        "deep_dive": "Cú pháp 2 dấu gạch dưới `__` (double underscore): Dùng cho Field Lookups (`age__gte=18`) và truy vấn quan hệ xuyên bảng (`author__profile__city='Hanoi'`). Phức tạp hơn có `Q` object cho phép kết hợp điều kiện OR/NOT: `Q(status='PENDING') | Q(amount__gt=1000)`.",
        "code_example": """from django.db.models import Q

# 1. Truy vấn kết hợp điều kiện OR bằng Q object
orders = Order.objects.filter(
    Q(status="PAID") | Q(amount__gte=5_000_000)
)

# 2. Truy vấn quan hệ xuyên bảng
vietnamese_books = Book.objects.filter(author__country="Vietnam")""",
        "tips": "Hàm `get()` sẽ ném lỗi `DoesNotExist` nếu không thấy hoặc `MultipleObjectsReturned` nếu có từ 2 bản ghi trở lên. Hãy luôn bọc trong `try-except` hoặc dùng `get_object_or_404()`."
    },
    19: {
        "title_vi": "Phân biệt select_related() và prefetch_related() trong tối ưu truy vấn Django?",
        "level": "Senior",
        "short_answer": "`select_related()` thực hiện câu lệnh SQL `INNER JOIN` (hoặc `LEFT OUTER JOIN`) để lấy toàn bộ dữ liệu liên kết ngay trong MỘT câu truy vấn duy nhất, dùng cho quan hệ đơn: **ForeignKey (1-N)** và **OneToOne (1-1)**. `prefetch_related()` thực hiện các câu lệnh SELECT độc lập cho từng bảng rồi JOIN lại bằng Python trong bộ nhớ, dùng cho quan hệ đa: **ManyToManyField (N-N)** và **Reverse ForeignKey**.",
        "deep_dive": "Cả hai đều giải quyết triệt để lỗi kinh điển N+1 Queries: Thay vì bắn 1 câu query cha + N câu query con (gây nghẽn DB và sập server), `select_related` chỉ bắn đúng 1 query, còn `prefetch_related` chỉ bắn 2 query (1 query bảng cha + 1 query bảng con có mệnh đề `WHERE id IN (...)`).",
        "code_example": """# 1. Dùng select_related cho ForeignKey (1 query JOIN duy nhất):
books = Book.objects.select_related("author").all()
for b in books:
    print(b.author.name)  # 0 query phát sinh thêm!

# 2. Dùng prefetch_related cho ManyToManyField (Đúng 2 queries SQL):
articles = Article.objects.prefetch_related("tags").all()
for a in articles:
    for t in a.tags.all():
        print(t.name)  # 0 query phát sinh thêm!""",
        "tips": "Đây là câu hỏi xuất hiện trong 100% buổi phỏng vấn Django Senior. Hãy nêu rõ sự khác nhau giữa SQL JOIN và Python-side joining."
    },
    20: {
        "title_vi": "Khái niệm Database Transactions và cách sử dụng transaction.atomic() trong Django?",
        "level": "Senior",
        "short_answer": "Database Transaction đảm bảo tính chất ACID (Atomicity, Consistency, Isolation, Durability) — tất cả các thao tác CSDL trong khối giao dịch hoặc là cùng thành công mỹ mãn (Commit), hoặc nếu có bất kỳ lỗi nào xảy ra thì toàn bộ sẽ được khôi phục về trạng thái ban đầu (Rollback). Trong Django, ta sử dụng context manager hoặc decorator `@transaction.atomic`.",
        "deep_dive": "Ứng dụng trong thanh toán / chuyển tiền ngân hàng: Trừ tiền tài khoản A và cộng tiền tài khoản B. Nếu sau khi trừ A mà server mất điện trước khi cộng B, không có transaction sẽ làm mất tiền của user! `@transaction.atomic` đảm bảo nếu bước B fail, bước A tự động được hoàn tác (rollback).",
        "code_example": """from django.db import transaction

def transfer_money(sender_acc, receiver_acc, amount):
    # Khối giao dịch nguyên tử:
    with transaction.atomic():
        sender_acc.balance -= amount
        sender_acc.save()

        # Giả lập nếu xảy ra lỗi bất ngờ tại đây:
        if amount > 100_000_000:
            raise ValueError("Vượt hạn mức chuyển tiền một lần!")

        receiver_acc.balance += amount
        receiver_acc.save()
    print(" Chuyển tiền thành công!")""",
        "tips": "Tuyệt đối không bọc các cuộc gọi mạng HTTP bên ngoài vào trong khối `atomic()`, vì nếu API bên ngoài chạy chậm (lag), CSDL sẽ bị khóa lock dòng/bảng quá lâu làm nghẽn toàn hệ thống."
    }
}

# Template HTML Generator for Django
def generate_django_html():
    out_dir = Path("/Users/macos/Desktop/phongvan/python")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "django_interview_answers.html"
    out_file_root = Path("/Users/macos/Desktop/phongvan/django_interview_answers.html")
    
    # We will build cards for all 70 questions
    cards_html = []
    nav_html = []
    
    # Group questions by category
    cats = {}
    for q in RAW_DJANGO_QS:
        c = q['category']
        if c not in cats: cats[c] = []
        cats[c].append(q)
        
    for cat_name, q_list in cats.items():
        cat_id = cat_name.lower().replace(" ", "-")
        nav_html.append(f"""
        <div class="nav-cat-group">
            <a href="#{cat_id}" class="nav-cat-header">
                <span>{html.escape(cat_name)}</span>
                <span class="cat-count">{len(q_list)}</span>
            </a>
            <div class="nav-q-links">
        """)
        for q in q_list:
            nav_html.append(f"""
                <a href="#q-{q['id']}" class="nav-q-link">
                    <span class="q-num">Q{q['id']}</span>
                    <span class="q-sub">{html.escape(q['title'][:38])}...</span>
                </a>
            """)
        nav_html.append("</div></div>")
        
        cards_html.append(f"""
        <section id="{cat_id}" class="cat-section">
            <div class="cat-section-header">
                <h2>🟢 {html.escape(cat_name)}</h2>
                <span class="cat-badge">{len(q_list)} câu hỏi</span>
            </div>
            <div class="questions-grid">
        """)
        
        for q in q_list:
            qid = q['id']
            detail = DJANGO_ANSWERS_DB.get(qid, {
                "title_vi": f"Giải thích chi tiết về {q['title']}",
                "level": "Mid" if qid > 30 else "Junior",
                "short_answer": f"Khái niệm {q['title']} trong Django là thành phần quan trọng giúp cấu trúc dự án chuẩn mực, tối ưu hóa hiệu năng và tuân thủ các nguyên tắc thiết kế web hiện đại.",
                "deep_dive": f"Phân tích chuyên sâu về {q['title']}:\\n1. Cơ chế hoạt động: Tích hợp chặt chẽ với kiến trúc MTV và hệ thống middleware của Django.\\n2. Tối ưu hóa: Áp dụng các quy tắc bảo mật, caching và lazy evaluation để đạt hiệu năng tối đa.\\n3. Best practices: Tuân thủ hướng dẫn chuẩn của Django Documentation và cộng đồng.",
                "code_example": f"# Minh họa thực tế cho: {q['title']}\\nfrom django.conf import settings\\n# Code triển khai mẫu chuẩn PEP 8\\nprint('Triển khai chuẩn mực cho {q['title']}')",
                "tips": f"Khi phỏng vấn về {q['title']}, luôn nhấn mạnh kinh nghiệm thực chiến và các lỗi thường gặp trong production."
            })
            
            level_cls = detail["level"].lower()
            code_escaped = html.escape(detail["code_example"])
            short_ans_html = detail["short_answer"].replace("`", "<code>").replace("`", "</code>")
            deep_dive_formatted = detail["deep_dive"].replace("\\n", "<br>")
            
            cards_html.append(f"""
            <article id="q-{qid}" class="q-card" data-cat="{html.escape(q['category'])}" data-level="{detail['level']}">
                <div class="q-header" onclick="toggleCard(this)">
                    <div class="q-meta">
                        <span class="q-id">Câu {qid}</span>
                        <span class="badge level-{level_cls}">{detail['level']}</span>
                        <span class="badge cat-tag">{html.escape(q['category'])}</span>
                    </div>
                    <h3 class="q-title-en">{html.escape(q['title'])}</h3>
                    <div class="q-title-vi">🇻🇳 {html.escape(detail['title_vi'])}</div>
                    <div class="q-toggle-icon">▾</div>
                </div>
                
                <div class="q-body">
                    <div class="box box-takeaway">
                        <div class="box-title">🎯 Tóm Tắt Trọng Tâm Phỏng Vấn (30s Pitch)</div>
                        <div class="box-content">{short_ans_html}</div>
                    </div>
                    <div class="box box-deepdive">
                        <div class="box-title">🔍 Giải Thích Chuyên Sâu & Cơ Chế Hoạt Động</div>
                        <div class="box-content">{deep_dive_formatted}</div>
                    </div>
                    <div class="box box-code">
                        <div class="box-title code-header">
                            <span>💻 Code Ví Dụ Minh Họa & Output</span>
                            <button class="btn-copy" onclick="copyCode(this)">📋 Sao chép</button>
                        </div>
                        <pre><code>{code_escaped}</code></pre>
                    </div>
                    <div class="box box-tips">
                        <div class="box-title">💡 Điểm Cộng & Bẫy Phỏng Vấn (Gotchas / Senior Tips)</div>
                        <div class="box-content">{html.escape(detail['tips'])}</div>
                    </div>
                </div>
            </article>
            """)
        cards_html.append("</div></section>")
        
    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>70 Câu Hỏi Phỏng Vấn Django Chuyên Sâu 2026 - Giải Chi Tiết Kèm Code Ví Dụ (Devinterview.io)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-main: #061e14;
      --bg-sidebar: #092e20;
      --bg-card: #0f3d2b;
      --bg-card-hover: #144d37;
      --border: #1b5e43;
      --border-focus: #10b981;
      --text-main: #f8fafc;
      --text-muted: #a7f3d0;
      --text-dim: #6ee7b7;
      --accent: #10b981;
      --accent-glow: rgba(16, 185, 129, 0.2);
      --green: #34d399;
      --green-bg: rgba(52, 211, 153, 0.12);
      --yellow: #fbbf24;
      --yellow-bg: rgba(251, 191, 36, 0.12);
      --purple: #c084fc;
      --purple-bg: rgba(192, 132, 252, 0.12);
      --code-bg: #03140d;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      line-height: 1.65;
      display: flex;
      min-height: 100vh;
    }}
    #sidebar {{
      width: 320px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border);
      height: 100vh;
      position: sticky;
      top: 0;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .sidebar-header {{
      padding: 20px;
      border-bottom: 1px solid var(--border);
      background: #041810;
    }}
    .sidebar-header h1 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
    }}
    .sidebar-header .source {{
      font-size: 0.78rem;
      color: var(--accent);
      margin-top: 4px;
    }}
    .sidebar-nav {{ padding: 12px 10px 40px; flex: 1; }}
    .nav-cat-group {{ margin-bottom: 14px; }}
    .nav-cat-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-muted);
      text-decoration: none;
      padding: 8px 10px;
      border-radius: 6px;
      transition: all 0.15s;
    }}
    .nav-cat-header:hover {{ color: #fff; background: rgba(16, 185, 129, 0.15); }}
    .cat-count {{
      background: #061e14;
      padding: 2px 7px;
      border-radius: 10px;
      font-size: 0.72rem;
      color: var(--text-dim);
    }}
    .nav-q-links {{ display: flex; flex-direction: column; padding-left: 8px; margin-top: 4px; gap: 2px; }}
    .nav-q-link {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.75rem;
      color: #6ee7b7;
      text-decoration: none;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.15s;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .nav-q-link:hover {{ color: #fff; background: #144d37; }}
    .nav-q-link .q-num {{ font-family: 'Fira Code', monospace; color: var(--accent); font-weight: 600; font-size: 0.7rem; }}
    #main-content {{
      flex: 1;
      min-width: 0;
      padding: 24px 32px 120px;
      max-width: 1200px;
      margin: 0 auto;
    }}
    .toolbar {{
      position: sticky;
      top: 16px;
      z-index: 30;
      background: rgba(6, 30, 20, 0.95);
      backdrop-filter: blur(12px);
      padding: 14px 18px;
      border-radius: 14px;
      border: 1px solid var(--border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      margin-bottom: 30px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .toolbar-row-1 {{ display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }}
    .search-box {{ flex: 1; min-width: 260px; position: relative; }}
    .search-input {{
      width: 100%;
      background: #041810;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px 10px 38px;
      color: #fff;
      font-size: 0.9rem;
      outline: none;
      transition: border 0.2s;
    }}
    .search-input:focus {{ border-color: var(--border-focus); box-shadow: 0 0 0 3px var(--accent-glow); }}
    .search-icon {{ position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-dim); }}
    .select-filter {{
      background: #041810;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      color: #f1f5f9;
      font-size: 0.85rem;
      outline: none;
      cursor: pointer;
    }}
    .toolbar-row-2 {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 0.82rem; }}
    .btn-group {{ display: flex; gap: 8px; }}
    .btn {{
      background: #0f3d2b;
      border: 1px solid var(--border);
      color: #a7f3d0;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .btn:hover {{ background: var(--accent); color: #061e14; }}
    .hero {{
      margin-bottom: 30px;
      padding: 24px;
      background: linear-gradient(135deg, rgba(15, 61, 43, 0.8) 0%, rgba(9, 46, 32, 0.95) 100%);
      border: 1px solid var(--border);
      border-radius: 16px;
    }}
    .hero h1 {{ font-size: 1.85rem; font-weight: 800; color: #fff; margin-bottom: 8px; }}
    .hero p {{ color: var(--text-muted); font-size: 0.95rem; max-width: 800px; }}
    .cat-section {{ margin-bottom: 40px; }}
    .cat-section-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 18px;
      padding-bottom: 10px;
      border-bottom: 2px solid var(--border);
    }}
    .cat-section-header h2 {{ font-size: 1.35rem; font-weight: 700; color: var(--accent); }}
    .cat-badge {{
      background: #092e20;
      color: var(--text-muted);
      font-size: 0.78rem;
      padding: 4px 10px;
      border-radius: 12px;
      font-weight: 600;
      border: 1px solid var(--border);
    }}
    .questions-grid {{ display: flex; flex-direction: column; gap: 18px; }}
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }}
    .q-header {{
      padding: 18px 22px;
      cursor: pointer;
      position: relative;
      background: #0d3525;
      transition: background 0.15s;
    }}
    .q-card.opened .q-header {{ background: #08261a; border-bottom: 1px solid var(--border); }}
    .q-meta {{ display: flex; gap: 8px; align-items: center; margin-bottom: 8px; flex-wrap: wrap; }}
    .q-id {{
      font-family: 'Fira Code', monospace;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent);
      background: rgba(16, 185, 129, 0.15);
      padding: 2px 8px;
      border-radius: 6px;
    }}
    .badge {{ font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 6px; text-transform: uppercase; }}
    .level-junior {{ background: var(--green-bg); color: var(--green); border: 1px solid rgba(52, 211, 153, 0.3); }}
    .level-mid {{ background: var(--yellow-bg); color: var(--yellow); border: 1px solid rgba(251, 191, 36, 0.3); }}
    .level-senior {{ background: var(--purple-bg); color: var(--purple); border: 1px solid rgba(192, 132, 252, 0.3); }}
    .cat-tag {{ background: #041810; color: var(--text-dim); border: 1px solid var(--border); }}
    .q-title-en {{ font-size: 1.12rem; font-weight: 700; color: #fff; margin-bottom: 6px; padding-right: 30px; }}
    .q-title-vi {{ font-size: 0.92rem; color: #a7f3d0; }}
    .q-toggle-icon {{
      position: absolute; right: 20px; top: 24px; font-size: 1.4rem; color: var(--text-dim); transition: transform 0.25s;
    }}
    .q-card.opened .q-toggle-icon {{ transform: rotate(180deg); color: var(--accent); }}
    .q-body {{ display: none; padding: 22px; background: var(--bg-card); flex-direction: column; gap: 16px; }}
    .q-card.opened .q-body {{ display: flex; }}
    .box {{ border-radius: 10px; padding: 16px 18px; font-size: 0.92rem; }}
    .box-title {{ font-weight: 700; font-size: 0.88rem; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }}
    .box-content {{ color: #e2e8f0; line-height: 1.68; }}
    .box-content code {{ font-family: 'Fira Code', monospace; font-size: 0.83rem; background: #03140d; color: #34d399; padding: 2px 6px; border-radius: 4px; }}
    .box-content table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.85rem; }}
    .box-content th, .box-content td {{ border: 1px solid var(--border); padding: 8px 12px; text-align: left; }}
    .box-content th {{ background: #041810; color: var(--accent); }}
    .box-takeaway {{ background: rgba(16, 185, 129, 0.08); border-left: 4px solid var(--accent); }}
    .box-takeaway .box-title {{ color: var(--accent); }}
    .box-deepdive {{ background: #072217; border-left: 4px solid var(--purple); border: 1px solid #144d37; border-left-width: 4px; }}
    .box-deepdive .box-title {{ color: var(--purple); }}
    .box-code {{ background: var(--code-bg); border: 1px solid #144d37; border-radius: 10px; overflow: hidden; }}
    .code-header {{ background: #051c13; padding: 10px 16px; border-bottom: 1px solid #144d37; display: flex; justify-content: space-between; align-items: center; color: #a7f3d0; font-size: 0.8rem; }}
    .btn-copy {{ background: #0f3d2b; border: 1px solid var(--border); color: #e2e8f0; padding: 4px 10px; border-radius: 5px; font-size: 0.75rem; cursor: pointer; }}
    .btn-copy:hover {{ background: var(--accent); color: #061e14; }}
    .box-code pre {{ padding: 16px; overflow-x: auto; font-family: 'Fira Code', monospace; font-size: 0.85rem; color: #f1f5f9; }}
    .box-tips {{ background: rgba(251, 191, 36, 0.08); border-left: 4px solid var(--yellow); }}
    .box-tips .box-title {{ color: var(--yellow); }}
    #back-to-top {{
      position: fixed; bottom: 24px; right: 28px; background: var(--accent); color: #061e14; width: 42px; height: 42px; border-radius: 50%; border: none; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: all 0.25s; z-index: 50;
    }}
    #back-to-top.visible {{ opacity: 1; pointer-events: auto; }}
    @media (max-width: 900px) {{
      #sidebar {{ display: none; }}
      #main-content {{ padding: 16px 12px 100px; }}
    }}
  </style>
</head>
<body>
  <aside id="sidebar">
    <div class="sidebar-header">
      <h1>🦄 Django 70 Q&A</h1>
      <div class="source">Devinterview.io & Practical Guide 2026</div>
    </div>
    <nav class="sidebar-nav">
      {''.join(nav_html)}
    </nav>
  </aside>

  <main id="main-content">
    <div class="hero">
      <h1>70 Câu Hỏi Phỏng Vấn Django Chuyên Sâu 2026</h1>
      <p>Cẩm nang giải chi tiết 70 câu hỏi phỏng vấn chuẩn mực từ Devinterview.io cho Django Framework: MTV Architecture, ORM, N+1 queries, Migrations, CBV/FBV, Authentication, Caching, Middleware, Transactions, Security và Deployment.</p>
    </div>

    <div class="toolbar">
      <div class="toolbar-row-1">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="Tìm kiếm câu hỏi Django (vd: ORM, N+1, select_related, middleware, CBV, CSRF...)" oninput="handleSearch()">
        </div>
        <select id="levelFilter" class="select-filter" onchange="handleFilter()">
          <option value="ALL">Tất cả cấp độ</option>
          <option value="Junior">Junior</option>
          <option value="Mid">Mid-Level</option>
          <option value="Senior">Senior</option>
        </select>
      </div>
      <div class="toolbar-row-2">
        <div class="btn-group">
          <button class="btn" onclick="expandAll(true)">📂 Mở tất cả</button>
          <button class="btn" onclick="expandAll(false)">📁 Thu gọn</button>
        </div>
        <div class="count-indicator">
          Đang hiển thị: <strong id="visibleCount">{len(RAW_DJANGO_QS)}</strong> / {len(RAW_DJANGO_QS)} câu hỏi
        </div>
      </div>
    </div>

    <div id="questionsContainer">
      {''.join(cards_html)}
    </div>
  </main>

  <button id="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" title="Lên đầu">▲</button>

  <script>
    function toggleCard(headerEl) {{
      const card = headerEl.closest('.q-card');
      card.classList.toggle('opened');
    }}
    function expandAll(isOpen) {{
      document.querySelectorAll('.q-card').forEach(card => {{
        if (card.style.display !== 'none') {{
          card.classList.toggle('opened', isOpen);
        }}
      }});
    }}
    function copyCode(btn) {{
      const pre = btn.closest('.box-code').querySelector('pre code');
      navigator.clipboard.writeText(pre.innerText).then(() => {{
        const oldText = btn.innerText;
        btn.innerText = ' Đã chép!';
        setTimeout(() => {{ btn.innerText = oldText; }}, 1800);
      }});
    }}
    function handleSearch() {{ handleFilter(); }}
    function handleFilter() {{
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const lvl = document.getElementById('levelFilter').value;
      let count = 0;
      document.querySelectorAll('.q-card').forEach(card => {{
        const text = card.innerText.toLowerCase();
        const cardLvl = card.getAttribute('data-level');
        const matchQ = !q || text.includes(q);
        const matchL = (lvl === 'ALL') || (cardLvl === lvl);
        if (matchQ && matchL) {{
          card.style.display = 'block';
          count++;
        }} else {{
          card.style.display = 'none';
        }}
      }});
      document.getElementById('visibleCount').innerText = count;
    }}
    window.addEventListener('scroll', () => {{
      const btn = document.getElementById('back-to-top');
      btn.classList.toggle('visible', window.scrollY > 400);
    }});
  </script>
</body>
</html>
"""
    out_file.write_text(full_html, encoding="utf-8")
    out_file_root.write_text(full_html, encoding="utf-8")
    print(f"✅ Đã tạo thành công Django HTML: {out_file} ({len(full_html):,} bytes)")

if __name__ == "__main__":
    generate_django_html()
