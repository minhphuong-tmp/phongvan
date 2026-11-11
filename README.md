# 🎯 Bộ Cẩm Nang Câu Hỏi Phỏng Vấn Chuyên Sâu (Interview Master Guides)

Tổng hợp hơn **450+ câu hỏi và câu trả lời phỏng vấn chuyên sâu** kèm code ví dụ thực tế, phân tích cơ chế hoạt động (under the hood), bài test live coding, xử lý sự cố production và các điểm cộng/bẫy phỏng vấn cấp độ Senior dành cho Software Engineers.

---

## 🌐 Cổng Tra Cứu Tương Tác & GitHub Pages

Tất cả các bộ cẩm nang được tích hợp vào trang chủ trung tâm **`index.html`** với thanh tìm kiếm đa năng (Live Global Search) theo từ khóa, công nghệ và cấp độ:

- 🔗 **GitHub Pages URL (Online):** `https://minhphuong-tmp.github.io/phongvan/`
- 💻 **Offline:** Nhấp đúp chuột trực tiếp vào file `index.html` trong máy để mở trên bất kỳ trình duyệt nào mà không cần cài đặt server hay phụ thuộc internet.

---

## 📚 Danh Sách 7 Bộ Cẩm Nang Phỏng Vấn (Interactive HTML Guides)

Toàn bộ các file HTML đều được thiết kế độc lập (Self-contained, tích hợp sẵn CSS Dark Theme, Live Search, bộ lọc cấp độ, sao chép code 1-click):

| Công nghệ / Chủ đề | Thư mục | Số câu hỏi / Bài tập | File giao diện tương tác |
| :--- | :--- | :---: | :--- |
| **Portal Trung Tâm** | Thư mục gốc | **Toàn bộ** | [index.html](index.html) |
| **Python Core (Devinterview)** | `python/` | **100 câu** | [devinterview_python_100_answers.html](devinterview_python_100_answers.html) |
| **Python & Django Thực Chiến** | `python/` | **67 câu & bài test** | [python_interview_answers.html](python_interview_answers.html) |
| **Django Framework** | `python/` | **70 câu** | [django_interview_answers.html](django_interview_answers.html) |
| **Node.js Core & Runtime** | `nodejs/` | **100 câu** | [nodejs_interview_answers.html](nodejs_interview_answers.html) |
| **Express.js API** | `nodejs/` | **58 câu** | [expressjs_interview_answers.html](expressjs_interview_answers.html) |
| **Vue.js 3 & Ecosystem** | `python/` | **100 câu** | [vuejs_interview_answers.html](vuejs_interview_answers.html) |
| **Nginx, System Design & STAR Hub** | `domain/` | **Master Hub** | [nginx_interview_answers.html](nginx_interview_answers.html) |

*(Tại thư mục gốc có sẵn bản mirror của toàn bộ các file HTML trên để truy cập nhanh chóng).*

---

## 🌟 Điểm Nổi Bật Của Hệ Thống Cẩm Nang

Mỗi câu hỏi trong bộ tài liệu được cấu trúc bài bản theo chuẩn phỏng vấn kỹ thuật quốc tế:

1. 🎯 **Tóm Tắt Trọng Tâm (30s Pitch)**: Câu trả lời súc tích, trực diện dành cho 30 giây đầu tiên trả lời nhà tuyển dụng.
2. 🔍 **Giải Thích Chuyên Sâu & Cơ Chế Hoạt Động**: Đi sâu vào bản chất kiến trúc (libuv event loop, streams backpressure, V8 heap, Vue 3 Proxy reactivity, Django MTV architecture, Python GIL & memory management...).
3. 💻 **Code Ví Dụ Thực Tế & Output**: Minh họa cú pháp chuẩn mực, xử lý ngoại lệ và best practices. Tích hợp nút **📋 Sao chép 1-click** với thông báo toast.
4. 💡 **Điểm Cộng & Bẫy Phỏng Vấn (Gotchas / Senior Tips)**: Các sai lầm phổ biến ứng viên hay mắc phải và mẹo ghi điểm tuyệt đối trong mắt Tech Lead / Hiring Manager.

### 🛠️ Bộ Công Cụ Tương Tác Trên Giao Diện:
- **Live Search**: Tìm kiếm tức thì theo từ khóa, tên hàm, module, thuật ngữ kỹ thuật trên từng file và toàn hub.
- **Level Filters**: Lọc câu hỏi theo cấp độ mong muốn: `Junior`, `Mid-level`, `Senior`.
- **Sidebar & Sticky Navigation**: Menu phân loại theo từng nhóm chủ đề với số lượng câu hỏi và liên kết nhảy nhanh.
- **Dark Mode Design System**: Phối màu tối chuyên nghiệp, dịu mắt, tối ưu cho lập trình viên.

---

## 📁 Cấu Trúc Thư Mục Repository

```text
phongvan/
├── index.html                               # Cổng tra cứu trung tâm & GitHub Pages Hub
├── README.md                                # Tài liệu tổng quan kho lưu trữ
├── devinterview_python_100_answers.html     # Mirror cẩm nang Python 100 Qs
├── python_interview_answers.html            # Mirror cẩm nang Python & Django 67 Qs
├── django_interview_answers.html            # Mirror cẩm nang Django 70 Qs
├── nodejs_interview_answers.html            # Mirror cẩm nang Node.js 100 Qs
├── expressjs_interview_answers.html         # Mirror cẩm nang Express.js 58 Qs
├── vuejs_interview_answers.html             # Mirror cẩm nang Vue.js 100 Qs
├── nginx_interview_answers.html             # Mirror Master Hub Nginx & System Design
│
├── python/
│   ├── devinterview_python_100_answers.html # Bản chính thức Python 100 Qs
│   ├── python_interview_answers.html        # Bản chính thức Python & Django 67 Qs
│   ├── django_interview_answers.html        # Bản chính thức Django 70 Qs
│   └── vuejs_interview_answers.html         # Bản chính thức Vue.js 100 Qs
│
├── nodejs/
│   ├── nodejs_interview_answers.html        # Bản chính thức Node.js 100 Qs
│   └── expressjs_interview_answers.html     # Bản chính thức Express.js 58 Qs
│
└── domain/
    └── nginx_interview_answers.html         # Bản chính thức Nginx & System Design Hub
```
