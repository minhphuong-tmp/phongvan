# 🎯 Bộ Cẩm Nang Câu Hỏi Phỏng Vấn Chuyên Sâu (Interview Master Guides)

Tổng hợp hơn **428+ câu hỏi và câu trả lời phỏng vấn chuyên sâu** kèm code ví dụ thực tế, phân tích cơ chế hoạt động (under the hood), và các điểm cộng/bẫy phỏng vấn cấp độ Senior dành cho Software Engineers.

---

## 📚 Danh Sách Các Bộ Cẩm Nang Phỏng Vấn (Interactive HTML Guides)

Toàn bộ các file HTML đều được thiết kế độc lập (Self-contained), có thể mở và sử dụng **hoàn toàn Offline** trên bất kỳ trình duyệt nào (Chrome, Safari, Firefox, Edge) mà không cần cài đặt thêm server hay phụ thuộc internet.

| Công nghệ | Thư mục | Số câu hỏi | File giao diện tương tác |
| :--- | :--- | :---: | :--- |
| **Python** | `python/` | **100** | [devinterview_python_100_answers.html](python/devinterview_python_100_answers.html) |
| **Django** | `python/` | **70** | [django_interview_answers.html](python/django_interview_answers.html) |
| **Node.js** | `nodejs/` | **100** | [nodejs_interview_answers.html](nodejs/nodejs_interview_answers.html) |
| **Express.js** | `nodejs/` | **58** | [expressjs_interview_answers.html](nodejs/expressjs_interview_answers.html) |
| **Vue.js** | `python/` | **100** | [vuejs_interview_answers.html](python/vuejs_interview_answers.html) |

*(Tại thư mục gốc cũng có sẵn bản mirror của 5 file HTML trên để truy cập nhanh chóng).*

---

## 🌟 Điểm Nổi Bật Của Hệ Thống Cẩm Nang

Mỗi câu hỏi trong bộ tài liệu được cấu trúc bài bản theo chuẩn phỏng vấn kỹ thuật quốc tế:

1. 🎯 **Tóm Tắt Trọng Tâm (30s Pitch)**: Câu trả lời súc tích, trực diện dành cho 30 giây đầu tiên trả lời nhà tuyển dụng.
2. 🔍 **Giải Thích Chuyên Sâu & Cơ Chế Hoạt Động**: Đi sâu vào bản chất kiến trúc (libuv event loop, streams backpressure, V8 heap, Vue 3 Proxy reactivity, Django MTV architecture, Python GIL & memory management...).
3. 💻 **Code Ví Dụ Thực Tế & Output**: Minh họa cú pháp chuẩn mực, xử lý ngoại lệ và best practices. Tích hợp nút **📋 Sao chép 1-click** với thông báo toast.
4. 💡 **Điểm Cộng & Bẫy Phỏng Vấn (Gotchas / Senior Tips)**: Các sai lầm phổ biến ứng viên hay mắc phải và mẹo ghi điểm tuyệt đối trong mắt Tech Lead / Hiring Manager.

### 🛠️ Bộ Công Cụ Tương Tác Trên Giao Diện:
- **Live Search**: Tìm kiếm tức thì theo từ khóa, tên hàm, module, thuật ngữ kỹ thuật.
- **Level Filters**: Lọc câu hỏi theo cấp độ mong muốn: `Junior`, `Mid-level`, `Senior`.
- **Sidebar Navigation**: Menu phân loại theo từng nhóm chủ đề với số lượng câu hỏi và liên kết nhảy nhanh.
- **Expand / Collapse All**: Nút thu gọn hoặc mở rộng toàn bộ câu hỏi linh hoạt.
- **Dark Mode Design System**: Phối màu tối chuyên nghiệp, dịu mắt, tối ưu cho lập trình viên.

---

## 📁 Cấu Trúc Thư Mục Repository

```text
phongvan/
├── README.md                                # Tài liệu tổng quan kho lưu trữ
├── devinterview_python_100_answers.html     # Mirror cẩm nang Python 100 Qs
├── django_interview_answers.html            # Mirror cẩm nang Django 70 Qs
├── nodejs_interview_answers.html            # Mirror cẩm nang Node.js 100 Qs
├── expressjs_interview_answers.html         # Mirror cẩm nang Express.js 58 Qs
├── vuejs_interview_answers.html             # Mirror cẩm nang Vue.js 100 Qs
│
├── python/
│   ├── devinterview_python_100_answers.html # Bản chính thức Python 100 Qs
│   ├── django_interview_answers.html        # Bản chính thức Django 70 Qs
│   └── vuejs_interview_answers.html         # Bản chính thức Vue.js 100 Qs
│
└── nodejs/
    ├── nodejs_interview_answers.html        # Bản chính thức Node.js 100 Qs
    └── expressjs_interview_answers.html     # Bản chính thức Express.js 58 Qs
```
