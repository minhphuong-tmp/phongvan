"""Express.js Interview Questions & Answers Database (58 Questions)"""

EXPRESS_ANSWERS_DB = {
    1: {
        "title_vi": "Express.js là gì và mối quan hệ của nó với Node.js?",
        "level": "Junior",
        "short_answer": "Express.js là framework ứng dụng web tối giản, linh hoạt và phổ biến nhất được xây dựng trên nền tảng Node.js. Trong khi Node.js cung cấp môi trường runtime và module `http` ở tầng thấp, Express.js cung cấp một lớp trừu tượng (abstraction layer) cấp cao bao gồm hệ thống định tuyến (Routing), chuỗi xử lý Middleware, phân tích dữ liệu yêu cầu và xử lý phản hồi HTTP trực quan.",
        "deep_dive": """1. Mối quan hệ: Node.js là Engine/Runtime; Express.js là Framework/Thư viện chạy bên trong runtime đó.
2. Tại sao không dùng `http` thuần: Khi dùng `http` thuần, lập trình viên phải tự parse URL, tự gom buffer dữ liệu `req.on('data')`, tự map method và path bằng nhiều khối `if/else`, tự cấu hình header MIME types. Express đóng gói tất cả các thao tác này vào các API trực quan như `app.get()`, `req.body`, `res.json()`.
3. Triết lý Unopinionated: Express không áp đặt cấu trúc thư mục, kiến trúc MVC hay bất kỳ ORM nào.""",
        "code_example": """const express = require('express');
const app = express();

// Express trừu tượng hóa toàn bộ việc xử lý HTTP của Node.js
app.get('/api/welcome', (req, res) => {
  res.status(200).json({
    framework: 'Express.js',
    runtime: 'Node.js',
    message: 'Chào mừng bạn đến với REST API tối giản!'
  });
});

app.listen(3000, () => console.log('Server chạy tại port 3000'));""",
        "tips": "Nhớ nhấn mạnh: 'Express không thay thế Node.js mà là một tiện ích bổ trợ xây dựng trực tiếp trên core module http của Node.js'."
    },

    2: {
        "title_vi": "Khái niệm Middleware trong Express.js hoạt động như thế nào?",
        "level": "Junior",
        "short_answer": "Middleware là các hàm trung gian nằm trong chu trình Request-Response (Vòng đời từ khi client gửi request đến khi server trả response). Một middleware có quyền truy cập vào 3 tham số: `req` (Request object), `res` (Response object), và `next` (hàm kích hoạt middleware tiếp theo trong chuỗi).",
        "deep_dive": """1. Bốn nhiệm vụ của Middleware:
   - Thực thi bất kỳ đoạn mã nào (ví dụ logging, kiểm tra bảo mật).
   - Biến đổi hoặc gắn thêm thuộc tính vào `req` và `res` (ví dụ `req.user = decodedToken`).
   - Kết thúc chu trình request-response (gọi `res.send()`, `res.json()`).
   - Gọi `next()` để chuyển quyền thực thi cho middleware kế tiếp.
2. Nguy cơ treo request: Nếu middleware không kết thúc response và cũng không gọi `next()`, request sẽ bị đứng yên mãi mãi dẫn đến timeout.""",
        "code_example": """const express = require('express');
const app = express();

// Middleware ghi nhật ký request
const requestLogger = (req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`);
  next(); // BẮT BUỘC gọi next() để tiếp tục luồng!
};

app.use(requestLogger);

app.get('/hello', (req, res) => {
  res.send('Xin chào!');
});""",
        "tips": "Luôn nhớ: Thứ tự khai báo middleware (`app.use`) trong Express cực kỳ quan trọng! Middleware nào khai báo trước sẽ chạy trước."
    },

    3: {
        "title_vi": "Cách thiết lập một ứng dụng Express.js cơ bản từ đầu?",
        "level": "Junior",
        "short_answer": "Thiết lập ứng dụng gồm 4 bước cơ bản: (1) Khởi tạo dự án bằng `npm init -y`, (2) Cài đặt package `npm install express`, (3) Tạo file `index.js`, import Express, khởi tạo instance `const app = express()`, định nghĩa route mẫu, và (4) Gọi `app.listen(PORT)` để lắng nghe kết nối.",
        "deep_dive": """1. Cấu hình Scripts: Thêm `\"start\": \"node index.js\"` và `\"dev\": \"nodemon index.js\"` vào `package.json`.
2. Kiểm tra Health Endpoint: Luôn tạo route `/health` để hệ thống giám sát (Load Balancer, Kubernetes) kiểm tra xem server có đang sống không.""",
        "code_example": """const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware parse JSON
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'UP', timestamp: new Date() });
});

app.listen(PORT, () => {
  console.log(`Express application đang chạy tại http://localhost:${PORT}`);
});""",
        "tips": "Luôn dùng `process.env.PORT || 3000` thay vì fix cứng cổng 3000 để server có thể chạy linh hoạt khi deploy lên Heroku, AWS, hoặc Docker."
    },

    4: {
        "title_vi": "Mục đích và cơ chế của hàm `app.use()` trong Express?",
        "level": "Junior",
        "short_answer": "`app.use()` là hàm dùng để đăng ký một hoặc nhiều middleware vào pipeline xử lý của ứng dụng Express. Nó có thể áp dụng cho toàn bộ ứng dụng (Application-level) hoặc giới hạn cho một tiền tố đường dẫn cụ thể (ví dụ: `app.use('/api', apiRouter)`).",
        "deep_dive": """1. Khác biệt với `app.get()` / `app.post()`: `app.use()` khớp với MỌI HTTP Method (GET, POST, PUT, DELETE, OPTIONS...) và khớp với tiền tố đường dẫn (Prefix matching).
2. Ví dụ: `app.use('/users', ...)` sẽ tự động khớp với `/users`, `/users/123`, `/users/profile/edit`.""",
        "code_example": """const express = require('express');
const app = express();

// 1. Áp dụng toàn cục cho tất cả mọi request
app.use(express.json());

// 2. Chỉ áp dụng cho các route bắt đầu bằng /admin
app.use('/admin', (req, res, next) => {
  console.log('Truy cập khu vực quản trị Admin!');
  next();
});""",
        "tips": "Thứ tự đặt `app.use()` quyết định luồng chạy. Nếu đặt `app.use(express.json())` sau các route handlers, `req.body` trong các route đó sẽ bị `undefined`!"
    },

    5: {
        "title_vi": "Cách phục vụ các file tĩnh (Static Files: CSS, JS, hình ảnh) trong Express?",
        "level": "Junior",
        "short_answer": "Express cung cấp sẵn built-in middleware `express.static(root, [options])`. Bạn chỉ cần chỉ định thư mục chứa file tĩnh (ví dụ thư mục `public`), Express sẽ tự động phục vụ các file đó với đúng MIME type và ETag header.",
        "deep_dive": """1. Tuyệt đối dùng `path.join`: Luôn kết hợp với `path.join(__dirname, 'public')` để đảm bảo đường dẫn chính xác khi chạy script từ các thư mục khác nhau.
2. Tiền tố ảo (Virtual Path Prefix): Có thể gắn mount path: `app.use('/static', express.static('public'))` để truy cập file qua URL `/static/images/logo.png`.
3. Caching: Cấu hình `maxAge` để trình duyệt lưu cache, giảm tải cho server.""",
        "code_example": """const path = require('node:path');
const express = require('express');
const app = express();

// Phục vụ file tĩnh từ thư mục 'public' với cache 1 ngày
app.use('/assets', express.static(path.join(__dirname, 'public'), {
  maxAge: '1d',
  etag: true
}));

// Khi đó file /public/css/style.css sẽ truy cập qua:
// http://localhost:3000/assets/css/style.css""",
        "tips": "Trong môi trường Production lớn, hãy để Nginx hoặc AWS CloudFront/S3 phục vụ file tĩnh thay vì để Express gánh, giúp tiết kiệm CPU cho Node.js."
    },

    6: {
        "title_vi": "Sự khác biệt giữa `app.get()` và `app.post()` trong Express.js?",
        "level": "Junior",
        "short_answer": "`app.get()` dùng để định nghĩa handler cho HTTP GET Request (dùng để tìm nạp / truy vấn dữ liệu từ server mà không làm thay đổi trạng thái hệ thống). `app.post()` dùng để định nghĩa handler cho HTTP POST Request (dùng để gửi dữ liệu từ client lên server để tạo mới tài nguyên hoặc kích hoạt tác vụ).",
        "deep_dive": """1. Vị trí truyền dữ liệu:
   - GET: Dữ liệu gửi qua URL Query string (`req.query`), hiển thị rõ ràng trên thanh địa chỉ trình duyệt, có giới hạn độ dài URL (~2048 ký tự), có thể bị lưu vào Browser History và Cache.
   - POST: Dữ liệu gửi ẩn trong Message Body (`req.body`), không giới hạn độ dài khắt khe, không bị browser cache tự ý.
2. Tính lũy thoái (Idempotence): GET là Safe & Idempotent (gọi nhiều lần kết quả không đổi, không gây side-effect). POST là Non-idempotent (gọi 2 lần sẽ tạo ra 2 đơn hàng khác nhau).""",
        "code_example": """const express = require('express');
const app = express();
app.use(express.json());

// GET: Đọc dữ liệu (Query params)
app.get('/api/search', (req, res) => {
  const keyword = req.query.q;
  res.json({ results: [`Kết quả cho: ${keyword}`] });
});

// POST: Ghi dữ liệu (Request Body)
app.post('/api/orders', (req, res) => {
  const { productId, quantity } = req.body;
  res.status(201).json({ success: true, orderId: 999 });
});""",
        "tips": "Tuyệt đối không bao giờ dùng `GET` để thực hiện các thao tác nhạy cảm như xóa dữ liệu hoặc đăng nhập (vì mật khẩu sẽ bị lộ trên URL và Access Logs)."
    },

    7: {
        "title_vi": "Cách lấy các tham số URL (Route Parameters) trong Express?",
        "level": "Junior",
        "short_answer": "Sử dụng dấu hai chấm `:` khi định nghĩa đường dẫn route (ví dụ: `/users/:userId/posts/:postId`). Trong route handler, các giá trị này sẽ tự động được Express trích xuất và lưu dưới dạng đối tượng khóa-giá trị trong `req.params`.",
        "deep_dive": """1. Kiểu dữ liệu: Tất cả các giá trị trong `req.params` mặc định đều là kiểu Chuỗi (`string`). Nếu cần tính toán hoặc so sánh ID số nguyên, bạn phải tự ép kiểu bằng `parseInt(req.params.id, 10)` hoặc `Number()`.
2. Tham số tùy chọn: Thêm dấu chấm hỏi sau tên param: `/users/:userId?` (userId có thể có hoặc không).
3. Regex trong params: Cho phép ràng buộc định dạng ngay trên route: `app.get('/users/:id(\\\\d+)', ...)` (chỉ khớp nếu id là các chữ số).""",
        "code_example": """const express = require('express');
const app = express();

// Định nghĩa route có 2 route parameters
app.get('/api/users/:userId/orders/:orderId', (req, res) => {
  const { userId, orderId } = req.params;
  
  res.json({
    userId: parseInt(userId, 10),
    orderId: orderId,
    timestamp: Date.now()
  });
});""",
        "tips": "Phân biệt rõ: `req.params` là phần động của URL path (`/users/:id`), còn `req.query` là các tham số sau dấu hỏi chấm (`/users?role=admin`)."
    },

    8: {
        "title_vi": "Route Handlers trong Express là gì và cách triển khai linh hoạt?",
        "level": "Junior",
        "short_answer": "Route Handler là hàm hoặc một mảng các hàm được thực thi khi một HTTP request khớp với đường dẫn (path) và phương thức (method) cụ thể. Express cho phép truyền nhiều hàm xử lý kế tiếp nhau cho cùng một route bằng cách sử dụng `next()`.",
        "deep_dive": """1. Chuỗi Handler (Chaining Handlers): Bạn có thể truyền 1 hàm, nhiều hàm phân cách bằng dấu phẩy, hoặc 1 mảng các hàm.
2. `next('route')`: Một tính năng đặc biệt! Nếu bạn gọi `next('route')`, Express sẽ bỏ qua tất cả các handler còn lại trong cụm route hiện tại và nhảy sang route tiếp theo khớp đường dẫn.""",
        "code_example": """const express = require('express');
const app = express();

const checkPermission = (req, res, next) => {
  req.isAdmin = true;
  next();
};

const validatePayload = (req, res, next) => {
  console.log('Payload hợp lệ');
  next();
};

// Truyền chuỗi nhiều handlers cho 1 route
app.post('/api/products', checkPermission, validatePayload, (req, res) => {
  res.send('Sản phẩm đã được tạo bởi Admin!');
});""",
        "tips": "Áp dụng mẫu thiết kế này để chia nhỏ việc kiểm tra quyền (Authorization), validate dữ liệu và business logic thành các hàm riêng biệt, dễ viết unit test."
    },

    9: {
        "title_vi": "Cách kích hoạt và cấu hình CORS (Cross-Origin Resource Sharing) trong Express?",
        "level": "Junior",
        "short_answer": "CORS là cơ chế an ninh của trình duyệt ngăn chặn các trang web ở domain này gọi API sang domain khác. Trong Express, cách chuẩn mực nhất là sử dụng package `cors`. Ta có thể cho phép tất cả các domain hoặc chỉ định danh sách Whitelist các domain tin cậy.",
        "deep_dive": """1. Preflight Request: Với các method như PUT, DELETE hoặc khi có custom headers, trình duyệt tự động gửi một request `OPTIONS` trước để thăm dò server có cho phép không. Middleware `cors` tự động phản hồi status 204 cho preflight này.
2. Credentials: Nếu frontend gửi Cookie hoặc Authorization header, phải cấu hình `credentials: true` và `origin` không được phép là `'*'`. Khách hàng phải là domain cụ thể.""",
        "code_example": """const express = require('express');
const cors = require('cors');
const app = express();

const whitelist = ['https://myfrontend.com', 'http://localhost:5173'];
const corsOptions = {
  origin: function (origin, callback) {
    // Cho phép các tool như Postman (origin undefined) hoặc domain trong whitelist
    if (!origin || whitelist.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Bị chặn bởi chính sách bảo mật CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE']
};

app.use(cors(corsOptions));""",
        "tips": "Lỗi CORS là lỗi của TRÌNH DUYỆT, không phải lỗi của Node server. Postman hoặc curl không bao giờ bị lỗi CORS vì chúng không áp dụng chính sách Same-Origin Policy."
    },

    10: {
        "title_vi": "Giải thích vai trò của hàm `next()` trong Middleware của Express?",
        "level": "Junior",
        "short_answer": "`next()` là hàm điều phối cốt lõi của Express. Khi được gọi, nó chuyển quyền điều khiển sang middleware tiếp theo trong ngăn xếp (middleware stack). Nếu không gọi `next()` (và cũng không gửi response về cho client), request sẽ bị treo vĩnh viễn.",
        "deep_dive": """1. Chuyển tiếp lỗi: Nếu truyền bất kỳ tham số nào vào `next(err)` (ngoại trừ chuỗi `'route'`), Express sẽ coi đó là một LỖI và ngay lập tức bỏ qua toàn bộ các middleware thông thường còn lại để nhảy thẳng đến Error-handling Middleware gần nhất!
2. `next('router')`: Bỏ qua instance Router hiện tại.""",
        "code_example": """const express = require('express');
const app = express();

app.use((req, res, next) => {
  const authHeader = req.headers['authorization'];
  if (!authHeader) {
    // ⚠️ Truyền Error vào next() để nhảy thẳng đến Error Handler
    return next(new Error('Thiếu Authorization Header'));
  }
  next(); // Không có lỗi, đi tiếp bình thường
});

// Error-handling middleware tiếp nhận lỗi
app.use((err, req, res, next) => {
  res.status(401).json({ error: err.message });
});""",
        "tips": "Luôn nhớ từ khóa `return`: Viết `return next();` để đảm bảo code bên dưới không tiếp tục thực thi sau khi đã chuyển quyền điều khiển."
    },

    11: {
        "title_vi": "Vai trò của lớp `express.Router` và cách module hóa ứng dụng lớn?",
        "level": "Mid",
        "short_answer": "`express.Router` hoạt động như một 'ứng dụng Express mini' (mini-app). Nó có đầy đủ khả năng định tuyến và gắn middleware riêng, giúp chia nhỏ một ứng dụng lớn thành nhiều module độc lập theo nghiệp vụ (ví dụ: `authRouter`, `userRouter`, `productRouter`) rồi gắn chúng vào app chính.",
        "deep_dive": """1. Độc lập & Tái sử dụng: Mỗi router có thể có middleware riêng (như auth check riêng cho adminRouter) mà không ảnh hưởng đến các router công khai khác.
2. Tùy chọn `mergeParams: true`: Mặc định, router con không truy cập được `req.params` của router cha. Cần bật `express.Router({ mergeParams: true })` khi viết Nested Routes (ví dụ `/users/:userId/posts/:postId`).""",
        "code_example": """// === routes/user.routes.js ===
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => res.json({ users: [] }));
router.get('/:id', (req, res) => res.json({ id: req.params.id }));

module.exports = router;

// === server.js ===
const app = express();
const userRouter = require('./routes/user.routes');

// Gắn router vào tiền tố /api/users
app.use('/api/users', userRouter);""",
        "tips": "Senior Tip: Luôn cấu hình cấu trúc thư mục dạng Module: mỗi domain có một folder chứa `*.routes.js`, `*.controller.js`, `*.service.js` riêng biệt."
    },

    12: {
        "title_vi": "Cách xử lý lỗi 404 (Route Not Found) chuẩn mực trong Express?",
        "level": "Junior",
        "short_answer": "Trong Express, 404 không được coi là một ngoại lệ (exception) hay lỗi ném ra. 404 đơn giản là không có bất kỳ route handler nào khớp với đường dẫn URL được yêu cầu. Cách xử lý chuẩn là đặt một middleware ở CUỐI CÙNG của file định tuyến (sau tất cả các routes khác).",
        "deep_dive": """1. Nguyên tắc Fallthrough: Express kiểm tra route từ trên xuống dưới. Nếu đi hết tất cả các `app.get()` và `app.post()` mà không có cái nào khớp và trả response, request sẽ rơi xuống middleware cuối cùng này.
2. Định dạng phản hồi: Trả về JSON cho API hoặc trang HTML 404 đẹp mắt cho người dùng web.""",
        "code_example": """const express = require('express');
const app = express();

// Các routes hợp lệ của bạn
app.get('/api/users', (req, res) => res.send('Users list'));

// ✅ Middleware bắt 404 (BẮT BUỘC ĐẶT Ở CUỐI CÙNG)
app.use((req, res, next) => {
  res.status(404).json({
    success: false,
    statusCode: 404,
    message: `Không tìm thấy endpoint: ${req.method} ${req.originalUrl}`
  });
});""",
        "tips": "Bẫy phỏng vấn: Đặt middleware 404 lên trên đầu các route sẽ khiến 100% requests đều bị trả về 404!"
    },

    13: {
        "title_vi": "Sự khác biệt giữa `req.query` và `req.params` trong Express?",
        "level": "Junior",
        "short_answer": "`req.params` chứa các giá trị định danh được nhúng trực tiếp trong cấu trúc đường dẫn route (ví dụ `/users/:id` -> `req.params.id`). Trong khi đó, `req.query` chứa các tham số truy vấn nằm sau dấu chấm hỏi `?` trên URL (ví dụ `/users?sort=asc&limit=10` -> `req.query.sort`).",
        "deep_dive": """1. Mục đích sử dụng:
   - `req.params`: Dùng để xác định một TÀI NGUYÊN CỤ THỂ (Resource Identification - ví dụ User ID, Order Code).
   - `req.query`: Dùng để LỌC (Filter), SẮP XẾP (Sort), TÌM KIẾM (Search) hoặc PHÂN TRANG (Pagination) tập hợp tài nguyên.
2. Khả năng tùy chọn: Query parameters luôn là tùy chọn (optional), còn Route params thường là bắt buộc đối với route đó.""",
        "code_example": """const express = require('express');
const app = express();

// URL: /api/categories/electronics/products?page=2&sort=price_desc
app.get('/api/categories/:categoryName/products', (req, res) => {
  const category = req.params.categoryName; // 'electronics'
  const { page, sort } = req.query;         // page='2', sort='price_desc'
  
  res.json({ category, page, sort });
});""",
        "tips": "Cả hai đối tượng này đều chứa giá trị kiểu `string`. Luôn nhớ parse sang `Number` hoặc validate bằng Zod trước khi dùng trong database query."
    },

    14: {
        "title_vi": "Mục đích của `req.body` và cách cấu hình để truy cập dữ liệu body?",
        "level": "Junior",
        "short_answer": "`req.body` chứa dữ liệu (payload) được client gửi lên trong thân của HTTP request (thường dùng trong POST, PUT, PATCH). Mặc định trong Express, `req.body` là `undefined`. Để truy cập được dữ liệu này, bạn BẮT BUỘC phải đăng ký các middleware phân tích cú pháp (body parser) như `express.json()` hoặc `express.urlencoded()`.",
        "deep_dive": """1. Lịch sử: Trong Express 3, body-parser được tích hợp sẵn. Express 4 tách riêng ra package ngoài. Từ Express 4.16+, `express.json()` và `express.urlencoded()` đã được tích hợp lại vào core.
2. Content-Type Matching:
   - Client gửi `Content-Type: application/json` -> Cần `app.use(express.json())`.
   - Client gửi form HTML `Content-Type: application/x-www-form-urlencoded` -> Cần `app.use(express.urlencoded({ extended: true }))`.
   - Client gửi form upload file `multipart/form-data` -> Cần dùng `multer`.""",
        "code_example": """const express = require('express');
const app = express();

// Kích hoạt body parser
app.use(express.json({ limit: '1mb' })); // Giới hạn kích thước tránh tấn công DoS
app.use(express.urlencoded({ extended: true }));

app.post('/api/register', (req, res) => {
  // Bây giờ req.body đã sẵn sàng để sử dụng
  const { email, password } = req.body;
  res.status(201).json({ message: `Đã tạo tài khoản cho: ${email}` });
});""",
        "tips": "Nếu gửi POST request từ Postman mà `req.body` vẫn rỗng `{}`: Kiểm tra xem trên Postman đã chọn tab Body -> `raw` -> chọn format là `JSON` chưa (chưa chọn JSON thì header Content-Type sẽ sai)."
    },

    15: {
        "title_vi": "Cách viết một Custom Middleware ghi lại Method, URL và thời gian thực thi của mỗi request?",
        "level": "Junior",
        "short_answer": "Tạo một hàm nhận `(req, res, next)`. Lưu lại mốc thời gian bắt đầu `const start = Date.now()`. Lắng nghe sự kiện `'finish'` trên đối tượng `res` để tính toán thời gian phản hồi khi response đã được gửi hoàn tất, sau đó in ra console.",
        "deep_dive": """1. Tại sao lắng nghe `res.on('finish')`: Vì middleware chạy trước route handler, nếu đo ngay lúc đó bạn chỉ đo được thời gian vào. Khi response thực sự được gửi xong tới client, sự kiện `'finish'` mới phát ra.
2. Thư viện thay thế: Trong production, người ta thường dùng thư viện chuẩn `morgan` hoặc logger chuyên dụng như `pino-http`.""",
        "code_example": """const express = require('express');
const app = express();

// Custom Request Logger Middleware
app.use((req, res, next) => {
  const start = Date.now();
  const { method, originalUrl } = req;

  // Lắng nghe khi response được gửi hoàn tất
  res.on('finish', () => {
    const duration = Date.now() - start;
    const statusCode = res.statusCode;
    console.log(`[HTTP] ${method} ${originalUrl} -> Status: ${statusCode} (${duration}ms)`);
  });

  next(); // Cho phép request đi tiếp
});""",
        "tips": "Trong phỏng vấn, giải thích việc dùng `res.on('finish')` cho thấy bạn hiểu rất sâu về Node.js Writable Stream bên dưới Express Response."
    },

    16: {
        "title_vi": "Cách triển khai Nested Routes (Định tuyến lồng nhau) trong Express?",
        "level": "Mid",
        "short_answer": "Nested Routes (ví dụ `/users/:userId/posts/:postId`) được triển khai bằng cách tạo một Router con cho resource bên trong (ví dụ `postRouter`), sau đó gắn router con này vào router cha thông qua `userRouter.use('/:userId/posts', postRouter)`. Đặc biệt, BẮT BUỘC phải bật tùy chọn `{ mergeParams: true }` trên router con.",
        "deep_dive": """1. Vấn đề `mergeParams`: Mặc định, mỗi Router có phạm vi `req.params` độc lập. Nếu không có `mergeParams: true`, bên trong `postRouter` bạn sẽ chỉ lấy được `:postId` mà `:userId` sẽ bị `undefined`!
2. Cấu trúc RESTful chuẩn: Phản ánh quan hệ 1-N (Một User có nhiều Bài viết).""",
        "code_example": """const express = require('express');

// Router cha: Quản lý Users
const userRouter = express.Router();

// Router con: Quản lý Posts (BẮT BUỘC mergeParams: true)
const postRouter = express.Router({ mergeParams: true });

postRouter.get('/:postId', (req, res) => {
  // Lấy được CẢ HAI tham số từ cả cha lẫn con!
  const { userId, postId } = req.params;
  res.json({ message: `Lấy bài viết ${postId} của người dùng ${userId}` });
});

// Gắn router con vào router cha
userRouter.use('/:userId/posts', postRouter);

const app = express();
app.use('/api/users', userRouter);""",
        "tips": "Đây là câu hỏi phân loại ứng viên Mid cực kỳ phổ biến: 'Tại sao trong router con tôi không đọc được param của router cha?' Đáp án: Thiếu `{ mergeParams: true }` khi gọi `express.Router()`."
    },

    17: {
        "title_vi": "Cách bắt và phản hồi các tham số URL với tiền tố/hậu tố đặc biệt?",
        "level": "Mid",
        "short_answer": "Express hỗ trợ Regular Expressions (biểu thức chính quy) hoặc các ký tự đại diện (wildcards) ngay bên trong định nghĩa chuỗi route. Bạn có thể sử dụng dấu gạch ngang, dấu chấm hoặc regex trong dấu ngoặc đơn để trích xuất dữ liệu chi tiết.",
        "deep_dive": """1. Dấu gạch ngang và chấm: `/flights/:from-:to` hoặc `/files/:filename.:ext` được Express tự động phân tích thành các params độc lập.
2. Ràng buộc kiểu dữ liệu: `/users/:id(\\\\d+)` đảm bảo route chỉ được kích hoạt nếu `:id` hoàn toàn là các chữ số.""",
        "code_example": """const express = require('express');
const app = express();

// 1. Phân tách bằng dấu gạch ngang
// URL: /flights/HAN-SGN
app.get('/flights/:from-:to', (req, res) => {
  res.json({ from: req.params.from, to: req.params.to });
});

// 2. Phân tách tên file và đuôi mở rộng
// URL: /download/document.pdf
app.get('/download/:file.:ext', (req, res) => {
  res.json({ file: req.params.file, extension: req.params.ext });
});""",
        "tips": "Kỹ thuật này rất hay dùng khi viết các endpoint tải file hoặc tra cứu vé máy bay, chuyến bay."
    },

    18: {
        "title_vi": "Cách phục vụ nhiều định dạng nội dung khác nhau (JSON, HTML, Text) dựa trên Header của Client?",
        "level": "Mid",
        "short_answer": "Sử dụng hàm `res.format()` của Express. Hàm này tự động kiểm tra header `Accept` được gửi từ client trong request và thực thi hàm callback tương ứng để trả về định dạng phù hợp (Content Negotiation). Nếu client yêu cầu định dạng không được hỗ trợ, Express sẽ trả về lỗi `406 Not Acceptable`.",
        "deep_dive": """1. Content Negotiation (Thương lượng nội dung): Giúp một endpoint duy nhất có thể phục vụ cả trình duyệt web (cần HTML) lẫn ứng dụng Mobile / API client (cần JSON) hoặc script console (cần Plain Text).""",
        "code_example": """const express = require('express');
const app = express();

app.get('/api/users/profile', (req, res) => {
  const user = { name: 'Alex', role: 'Admin' };

  res.format({
    'text/plain': () => {
      res.send(`User: ${user.name} - Role: ${user.role}`);
    },
    'text/html': () => {
      res.send(`<h1>${user.name}</h1><p>Role: ${user.role}</p>`);
    },
    'application/json': () => {
      res.json(user);
    },
    default: () => {
      res.status(406).send('Định dạng không được hỗ trợ');
    }
  });
});""",
        "tips": "Nhắc đến thuật ngữ chuẩn quốc tế 'Content Negotiation' và HTTP header 'Accept'."
    },

    19: {
        "title_vi": "Các thực hành tốt nhất (Best Practices) để tổ chức cấu trúc một ứng dụng Express lớn?",
        "level": "Senior",
        "short_answer": "Trong dự án Express quy mô lớn: (1) Áp dụng kiến trúc phân tầng (Layered Architecture) hoặc theo Module tính năng (Feature-based), (2) Tách biệt tuyệt đối giữa Routing, Business Logic (Services) và Truy vấn dữ liệu (Repositories/Models), (3) Quản lý lỗi tập trung qua Custom Error classes và Global Error Middleware, (4) Validate toàn bộ đầu vào bằng Zod/Joi trước khi vào controller, và (5) Tách file cấu hình môi trường an toàn.",
        "deep_dive": """1. Nguyên tắc Single Responsibility (Trách nhiệm duy nhất):
   - Controller: Chỉ nhận request, validate cú pháp, gọi Service, và trả HTTP response. Không viết query DB trong controller!
   - Service: Chứa 100% logic nghiệp vụ (tính thuế, gọi cổng thanh toán, gửi email). Không chạm vào đối tượng `req` hay `res`.
   - Repository: Chứa các câu lệnh SQL/Prisma/Mongoose thao tác với cơ sở dữ liệu.""",
        "code_example": """// Cấu trúc thư mục chuẩn Senior cho Express:
// src/
// ├── config/            # Cấu hình DB, Redis, biến môi trường
// ├── modules/
// │   ├── auth/          # Gom theo feature module
// │   │   ├── auth.controller.js
// │   │   ├── auth.service.js
// │   │   ├── auth.routes.js
// │   │   └── auth.validation.js
// │   └── order/
// ├── middlewares/       # errorHandler, authGuard, rateLimiter
// ├── utils/             # AppError, logger
// └── app.js             # Setup express pipelines (không listen)
// └── server.js          # Khởi động app.listen và DB connect""",
        "tips": "Luôn tách `app.js` và `server.js`! Điều này giúp bạn kiểm thử API bằng Supertest cực kỳ dễ dàng mà không làm mở cổng mạng thực tế."
    },

    20: {
        "title_vi": "Các Built-in Middleware có sẵn trong Express.js là gì?",
        "level": "Junior",
        "short_answer": "Từ phiên bản Express 4.16+, Express tích hợp sẵn 3 built-in middleware cốt lõi: (1) `express.json()` (phân tích JSON payload), (2) `express.urlencoded()` (phân tích form data), và (3) `express.static()` (phục vụ file tĩnh). Ngoài ra còn có `express.raw()` và `express.text()`.",
        "deep_dive": """1. `express.raw()`: Phân tích payload thành đối tượng `Buffer` nhị phân (rất quan trọng khi xử lý Stripe Webhook để xác thực chữ ký cryptographic signature).
2. `express.text()`: Đọc payload thành chuỗi ký tự thuần túy.""",
        "code_example": """const express = require('express');
const app = express();

app.use(express.json());                          // Parse application/json
app.use(express.urlencoded({ extended: true }));  // Parse application/x-www-form-urlencoded
app.use('/static', express.static('public'));     // Phục vụ file tĩnh
app.use('/webhook/stripe', express.raw({ type: 'application/json' })); // Nhận raw buffer cho Webhooks""",
        "tips": "Nhớ nhấn mạnh: 'Trước Express 4.16, ta phải cài riêng thư viện body-parser qua npm. Hiện nay nó đã được tích hợp trực tiếp vào Express core'."
    },

    21: {
        "title_vi": "Cách viết Custom Middleware tái sử dụng trong Express?",
        "level": "Junior",
        "short_answer": "Một Custom Middleware là một hàm nhận `(req, res, next)`. Nếu muốn truyền thêm tham số cấu hình cho middleware, ta viết theo mẫu Factory Function (hàm trả về một hàm middleware).",
        "deep_dive": """1. Factory Pattern cho Middleware: Cho phép truyền các tham số linh hoạt (ví dụ: danh sách các quyền được phép truy cập `requireRole(['admin', 'editor'])`).""",
        "code_example": """const express = require('express');
const app = express();

// Middleware Factory: Cho phép truyền tham số cấu hình
function requireRole(allowedRoles) {
  return (req, res, next) => {
    // Giả sử user đã được gắn từ middleware auth trước đó
    const userRole = req.user ? req.user.role : 'guest';

    if (!allowedRoles.includes(userRole)) {
      return res.status(403).json({
        error: 'Quyền truy cập bị từ chối: Bạn không có quyền thực hiện thao tác này'
      });
    }

    next(); // Hợp lệ, cho phép đi tiếp
  };
}

// Sử dụng linh hoạt cho từng route
app.delete('/api/users/:id', requireRole(['superadmin']), (req, res) => {
  res.send('Đã xóa người dùng thành công.');
});""",
        "tips": "Sử dụng Factory Function là cách chuyên nghiệp nhất để viết các middleware bảo mật, xác thực quyền hạn và rate limiting."
    },

    22: {
        "title_vi": "Cách xử lý File Uploads trong Express sử dụng thư viện `multer`?",
        "level": "Mid",
        "short_answer": "`multer` là middleware tiêu chuẩn cho Express chuyên xử lý dữ liệu biểu mẫu dạng `multipart/form-data`. Nó cung cấp các phương thức như `upload.single('fieldName')` (1 file), `upload.array('fieldName', maxCount)` (nhiều file cùng trường), hoặc `upload.fields()` (nhiều file khác trường).",
        "deep_dive": """1. Storage Engines:
   - `multer.memoryStorage()`: Lưu file trực tiếp vào RAM dưới dạng `Buffer` (thích hợp khi cần đẩy ngay lên AWS S3 hoặc resize ảnh với `sharp`).
   - `multer.diskStorage()`: Lưu file trực tiếp ra ổ đĩa của server.
2. Bảo mật: Luôn cấu hình `limits.fileSize` và hàm `fileFilter` để chặn các file thực thi nguy hiểm.""",
        "code_example": """const express = require('express');
const multer = require('multer');
const path = require('node:path');
const app = express();

// Cấu hình lưu trữ an toàn trên Disk
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename: (req, file, cb) => {
    // Đổi tên file ngẫu nhiên tránh trùng lặp và ghi đè
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 2 * 1024 * 1024 }, // Giới hạn 2MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) cb(null, true);
    else cb(new Error('Chỉ cho phép tải lên hình ảnh!'), false);
  }
});

app.post('/api/upload-avatar', upload.single('avatar'), (req, res) => {
  res.json({ message: 'Upload ảnh thành công!', file: req.file });
});""",
        "tips": "Nếu lưu file trên ổ cứng server, đừng bao giờ giữ nguyên tên file gốc của người dùng (`file.originalname`) vì có thể dính lỗi Path Traversal (`../../etc/passwd`)."
    },

    23: {
        "title_vi": "`express-session` là gì và cách sử dụng quản lý trạng thái đăng nhập?",
        "level": "Mid",
        "short_answer": "`express-session` là middleware quản lý phiên làm việc của người dùng phía server. Khi người dùng truy cập, nó tự động cấp một Session ID ngẫu nhiên, lưu session ID đó trong một cookie an toàn ở trình duyệt, và lưu trữ dữ liệu phiên (ví dụ `req.session.userId`) ở phía backend.",
        "deep_dive": """1. Nguy cơ MemoryStore: Mặc định `express-session` lưu trong RAM. Điều này bị cấm ngặt trên Production vì sẽ rò rỉ bộ nhớ và mất session khi restart server.
2. Cấu hình Production: BẮT BUỘC dùng Redis hoặc cơ sở dữ liệu làm session store (`connect-redis`).
3. Cookie Security: Thiết lập `httpOnly: true`, `secure: true` (chỉ chạy HTTPS) và `sameSite: 'lax'`.""",
        "code_example": """const session = require('express-session');
const express = require('express');
const app = express();

app.use(session({
  secret: 'my-super-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: 1000 * 60 * 60 * 24, // 1 ngày
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production'
  }
}));

app.post('/login', (req, res) => {
  // Đăng nhập thành công, lưu thông tin vào session
  req.session.userId = 'user_99';
  req.session.role = 'admin';
  res.send('Đăng nhập thành công!');
});

app.get('/dashboard', (req, res) => {
  if (!req.session.userId) return res.status(401).send('Chưa đăng nhập');
  res.send(`Xin chào User: ${req.session.userId}`);
});""",
        "tips": "So sánh Session vs JWT: Session dễ thu hồi (chỉ cần xóa trên Redis), nhưng tốn tài nguyên DB. JWT hoàn toàn stateless, nhưng khó thu hồi token trước hạn."
    },

    24: {
        "title_vi": "Cách định nghĩa Error-Handling Middleware trong Express?",
        "level": "Junior",
        "short_answer": "Error-handling middleware trong Express là một hàm ĐẶC BIỆT nhận chính xác 4 THAM SỐ: `(err, req, res, next)`. Nếu khai báo thiếu tham số `err` (chỉ có 3 tham số), Express sẽ coi đó là middleware thông thường và không bao giờ bắt được lỗi.",
        "deep_dive": """1. Cơ chế nhận diện của Express: Express kiểm tra thuộc tính độ dài tham số của hàm: `fn.length === 4`.
2. Vị trí đặt: BẮT BUỘC phải đặt ở DƯỚI CÙNG của tất cả các `app.use()` và routes khác.
3. Chuyển tiếp lỗi bất đồng bộ: Trong Express 4, với các hàm async, nếu xảy ra lỗi trong `await`, bạn phải dùng `try/catch` và gọi `next(err)` hoặc bọc bằng wrapper `express-async-errors`. (Từ Express 5, các promise rejection được tự động bắt).""",
        "code_example": """const express = require('express');
const app = express();

app.get('/api/error-test', (req, res, next) => {
  const err = new Error('Không tìm thấy tài nguyên theo yêu cầu');
  err.statusCode = 404;
  next(err); // Ném lỗi vào Error Middleware
});

// ✅ Error-Handling Middleware chuẩn mực (ĐỦ 4 THAM SỐ)
app.use((err, req, res, next) => {
  console.error('[Error Logger]:', err.stack);

  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    success: false,
    error: {
      message: err.message || 'Lỗi hệ thống nội bộ',
      statusCode: statusCode,
      // Chỉ hiện stacktrace khi ở môi trường Development
      stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
    }
  });
});""",
        "tips": "Luôn nhớ: Không bao giờ xóa tham số `next` dù không dùng đến trong error handler, vì nếu chỉ để `(err, req, res)` thì `fn.length` sẽ bằng 3 và Express không nhận diện được!"
    },

    25: {
        "title_vi": "Ví dụ và cách sử dụng Third-Party Middleware như `morgan`?",
        "level": "Junior",
        "short_answer": "`morgan` là một middleware HTTP request logger chuẩn cho Node.js/Express. Nó tự động ghi lại chi tiết mọi request gửi đến máy chủ (phương thức, đường dẫn, mã trạng thái HTTP, thời gian xử lý, độ dài gói tin) theo các định dạng định sẵn như `'dev'`, `'combined'`, `'tiny'`.",
        "deep_dive": """1. Tự động hóa log: Giúp phát hiện ngay lập tức các request bị lỗi 500 hoặc các endpoint chạy chậm (> 1000ms).
2. Tích hợp ghi file log: Có thể chuyển hướng output của morgan vào một `fs.createWriteStream` để lưu log xoay vòng (rotating file logs) trên máy chủ.""",
        "code_example": """const express = require('express');
const morgan = require('morgan');
const app = express();

// Sử dụng format 'dev' có màu sắc trực quan trong quá trình phát triển
app.use(morgan('dev'));

app.get('/api/items', (req, res) => {
  res.json(['Item 1', 'Item 2']);
});

// Output trên Terminal khi có request:
// GET /api/items 200 4.123 ms - 23""",
        "tips": "Trên Production, hãy dùng format `morgan('combined')` (chuẩn Apache Combined Log) để dễ dàng tích hợp và nạp vào hệ thống phân tích log ELK hoặc Datadog."
    },

    26: {
        "title_vi": "Cách bảo vệ ứng dụng Express khỏi SQL Injection và NoSQL Injection?",
        "level": "Senior",
        "short_answer": "Để bảo vệ cơ sở dữ liệu: (1) Với SQL Database: LUÔN LUÔN dùng Parameterized Queries (Truy vấn có tham số) hoặc ORM chuẩn (Prisma/TypeORM/Sequelize), tuyệt đối KHÔNG ghép chuỗi câu lệnh SQL, (2) Với MongoDB: Sử dụng thư viện `express-mongo-sanitize` để loại bỏ các toán tử độc hại như `$gt`, `$ne` trong payload người dùng, và (3) Validate chặt chẽ Schema đầu vào bằng Zod.",
        "deep_dive": """1. NoSQL Injection hoạt động ra sao: Nếu người dùng gửi body `{ \"username\": \"admin\", \"password\": { \"$ne\": null } }`, câu lệnh `User.findOne(req.body)` của MongoDB sẽ tìm thấy admin ngay lập tức mà không cần biết mật khẩu thật!
2. Biện pháp triệt để: Sử dụng `express-mongo-sanitize` để tước bỏ tất cả các keys bắt đầu bằng dấu `$` hoặc chứa dấu chấm `.`.""",
        "code_example": """const mongoSanitize = require('express-mongo-sanitize');
const express = require('express');
const app = express();

app.use(express.json());

// ✅ Tự động làm sạch dữ liệu chống NoSQL Injection
app.use(mongoSanitize());

// Với SQL: Luôn dùng Prepared Statements an toàn tuyệt đối
// const query = 'SELECT * FROM users WHERE email = ? AND status = ?';
// await db.query(query, [userEmail, 'active']);""",
        "tips": "Khắc cốt ghi tâm: 'Không bao giờ tin tưởng dữ liệu từ client gửi lên'. Bất kể dữ liệu từ params, query hay body đều phải được sanitize và validate."
    },

    27: {
        "title_vi": "Cách triển khai cơ chế Caching trong ứng dụng Express.js?",
        "level": "Senior",
        "short_answer": "Caching trong Express được triển khai ở nhiều tầng: (1) HTTP Client Caching (gửi header `Cache-Control` và `ETag`), (2) In-Memory Caching phía server (dùng Redis hoặc NodeCache cho các kết quả tính toán đắt đỏ), và (3) Reverse Proxy / CDN Caching (Cloudflare, Nginx lưu trữ cache HTML/JSON ở rìa mạng).",
        "deep_dive": """1. Redis Cache Middleware Pattern:
   - Khi có request GET đến: Lấy URL làm cache key, kiểm tra Redis.
   - Nếu Cache Hit: Trả về dữ liệu từ Redis ngay trong 1ms!
   - Nếu Cache Miss: Chuyển sang route handler thực thi query DB, lưu kết quả vào Redis với thời gian sống TTL (Time-To-Live), sau đó trả về cho client.
2. Cache Invalidation: Bắt buộc xóa cache tương ứng trong Redis mỗi khi có request POST, PUT, DELETE làm thay đổi dữ liệu.""",
        "code_example": """const { createClient } = require('redis');
const redisClient = createClient();
redisClient.connect();

// Middleware Caching tự động cho Express
function cacheMiddleware(ttlSeconds = 60) {
  return async (req, res, next) => {
    if (req.method !== 'GET') return next();

    const key = `cache:${req.originalUrl}`;
    const cachedData = await redisClient.get(key);

    if (cachedData) {
      res.setHeader('X-Cache', 'HIT');
      return res.json(JSON.parse(cachedData));
    }

    res.setHeader('X-Cache', 'MISS');
    // Ghi đè hàm res.json để tự động lưu cache trước khi trả kết quả
    const originalJson = res.json.bind(res);
    res.json = (body) => {
      redisClient.setEx(key, ttlSeconds, JSON.stringify(body));
      return originalJson(body);
    };

    next();
  };
}

app.get('/api/products', cacheMiddleware(300), async (req, res) => {
  // Query DB tốn 500ms...
  res.json({ products: [] });
});""",
        "tips": "Hai điều khó nhất trong khoa học máy tính: 'Đặt tên biến và Hủy bộ nhớ đệm (Cache Invalidation)'. Hãy chuẩn bị sẵn chiến lược xóa cache khi dữ liệu thay đổi."
    },

    28: {
        "title_vi": "Cách thiết lập và đọc Cookies trong Express sử dụng `cookie-parser`?",
        "level": "Junior",
        "short_answer": "Sử dụng thư viện `cookie-parser` để đọc cookie từ request qua `req.cookies`. Để thiết lập cookie trả về cho client, sử dụng hàm `res.cookie(name, value, [options])`. Để xóa cookie, sử dụng `res.clearCookie(name)`.",
        "deep_dive": """1. Các cờ bảo mật quan trọng nhất của Cookie:
   - `httpOnly: true`: Ngăn chặn JavaScript trình duyệt đọc cookie qua `document.cookie` (chống XSS đánh cắp session).
   - `secure: true`: Chỉ cho phép truyền cookie qua kết nối HTTPS đã mã hóa.
   - `sameSite: 'strict'` hoặc `'lax'`: Chống tấn công CSRF (Cross-Site Request Forgery).
   - `signed: true`: Ký cookie bằng secret key để phát hiện client cố tình sửa đổi giá trị cookie trái phép.""",
        "code_example": """const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

// Khởi tạo cookie-parser với secret key để ký signed cookies
app.use(cookieParser('my-cookie-signing-secret'));

app.get('/set-cookie', (req, res) => {
  res.cookie('userSession', 'token_12345', {
    maxAge: 900000, // 15 phút
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    signed: true // Ký bảo vệ chống giả mạo
  });
  res.send('Cookie bảo mật đã được thiết lập!');
});

app.get('/get-cookie', (req, res) => {
  // Đọc signed cookie đã được xác thực chữ ký
  const sessionToken = req.signedCookies.userSession;
  res.json({ sessionToken });
});""",
        "tips": "Nhớ: Để đọc signed cookie, phải truy cập qua `req.signedCookies` chứ không phải `req.cookies`."
    },

    29: {
        "title_vi": "Các cách tối ưu hóa hiệu năng (Performance Optimization) cho ứng dụng Express?",
        "level": "Senior",
        "short_answer": "Tối ưu hóa Express toàn diện bao gồm: (1) Luôn đặt `NODE_ENV=production` để kích hoạt bộ nhớ đệm nội bộ, (2) Bật nén Gzip/Brotli bằng middleware `compression`, (3) Sử dụng kết nối Database Connection Pooling, (4) Áp dụng In-memory Caching với Redis, (5) Chạy ở chế độ Cluster (PM2) tận dụng đa nhân CPU, và (6) Tránh hoàn toàn các hàm đồng bộ (`*Sync`) làm nghẽn Event Loop.",
        "deep_dive": """1. Middleware `compression`: Tự động nén các payload JSON/HTML lớn trước khi gửi qua mạng, giảm kích thước truyền tải lên đến 70%, giúp tăng tốc độ tải trang đáng kể.
2. Bỏ các middleware không cần thiết: Tránh gắn các middleware nặng vào toàn bộ ứng dụng (`app.use`) nếu chúng chỉ cần thiết cho 1-2 route.""",
        "code_example": """const express = require('express');
const compression = require('compression');
const helmet = require('helmet');

const app = express();

// 1. Tự động nén phản hồi JSON/HTML
app.use(compression());

// 2. Tắt header tiết lộ công nghệ
app.disable('x-powered-by');

// 3. Cache tĩnh
app.use('/static', express.static('public', { maxAge: '7d' }));""",
        "tips": "Điểm cộng phỏng vấn: Đề xuất benchmark định kỳ bằng `autocannon` để phát hiện sự suy giảm hiệu năng trước khi đưa code lên production."
    },

    30: {
        "title_vi": "Cách cấu hình ứng dụng Express khi chạy phía sau một Reverse Proxy (như Nginx)?",
        "level": "Mid",
        "short_answer": "Khi đứng sau Reverse Proxy, địa chỉ IP kết nối trực tiếp vào Node.js là IP của chính Nginx (`127.0.0.1`), không phải IP của người dùng thật. Để Express nhận diện đúng IP thật và giao thức HTTPS của người dùng, bạn BẮT BUỘC phải bật thiết lập: `app.set('trust proxy', 1)` hoặc `app.enable('trust proxy')`.",
        "deep_dive": """1. Tại sao cần thiết:
   - `req.ip`: Sẽ đọc từ header `X-Forwarded-For` do Nginx truyền vào thay vì IP loopback.
   - `req.secure` / `req.protocol`: Sẽ nhận biết chính xác request gốc là `https` nhờ header `X-Forwarded-Proto`.
   - Cookie `secure: true`: Sẽ hoạt động đúng. Nếu không có `trust proxy`, Express tưởng kết nối là HTTP thường và sẽ từ chối gửi cookie `secure`!""",
        "code_example": """const express = require('express');
const app = express();

// ✅ BẬT TRUST PROXY KHI CHẠY SAU NGINX / CLOUDFLARE / AWS ALB
app.set('trust proxy', 1); // 1 = Tin tưởng 1 tầng proxy đầu tiên

app.get('/api/client-info', (req, res) => {
  res.json({
    realClientIp: req.ip,           // Lấy đúng IP thật của người dùng
    protocol: req.protocol,         // 'https'
    isSecure: req.secure            // true
  });
});""",
        "tips": "Nếu không cấu hình `trust proxy`, các thư viện Rate Limiting (như `express-rate-limit`) sẽ coi tất cả người dùng trên thế giới có chung 1 IP là `127.0.0.1`, dẫn đến việc 1 người spam thì cả triệu người khác bị khóa chung!"
    },

    31: {
        "title_vi": "Mục đích của Template Engines và cách tích hợp với Express?",
        "level": "Junior",
        "short_answer": "Template Engine (như EJS, Pug, Handlebars) cho phép nhúng mã JavaScript động vào các file HTML tĩnh trên server. Khi có request, Express kết hợp dữ liệu từ cơ sở dữ liệu với template để biên dịch thành một file HTML hoàn chỉnh gửi về cho trình duyệt. Tích hợp bằng cách dùng `app.set('view engine', 'ejs')` và gọi `res.render('templateName', data)`.",
        "deep_dive": """1. Phân biệt:
   - EJS: Cú pháp HTML thuần túy kết hợp thẻ `<%= variable %>`, rất dễ học.
   - Pug (trước là Jade): Cú pháp thụt đầu dòng tối giản, không cần đóng thẻ HTML.
2. Vị trí lưu trữ: Mặc định Express tìm kiếm template trong thư mục `views/` (có thể đổi qua `app.set('views', path)`).""",
        "code_example": """const express = require('express');
const path = require('node:path');
const app = express();

// Cấu hình View Engine là EJS
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.get('/profile', (req, res) => {
  // Render file views/profile.ejs với dữ liệu truyền vào
  res.render('profile', {
    user: { name: 'Nguyễn Văn A', email: 'vana@gmail.com' },
    title: 'Trang cá nhân'
  });
});""",
        "tips": "Trong thế giới web hiện đại, các ứng dụng lớn thường tách biệt hoàn toàn Frontend (React/Vue) và Backend (Express REST API). Template engine hiện nay chủ yếu dùng cho việc render email template hoặc các trang web nhỏ cần SEO đơn giản."
    },

    32: {
        "title_vi": "Cách kiểm thử (Testing) một ứng dụng Express với Supertest và Jest?",
        "level": "Mid",
        "short_answer": "Sử dụng thư viện `supertest` kết hợp với `jest`. Supertest cho phép gửi các HTTP request giả lập trực tiếp đến đối tượng `app` của Express mà không cần chạy `app.listen()`, sau đó kiểm tra Status Code, Response Headers và cấu trúc dữ liệu JSON trả về.",
        "deep_dive": """1. Kiến trúc tách file:
   - `src/app.js`: Chỉ chứa cấu hình Express, middleware và routes (`module.exports = app`).
   - `src/server.js`: Import `app` và gọi `app.listen(PORT)`.
   - File test sẽ import trực tiếp `app.js` để test siêu nhanh mà không bị xung đột port mạng.""",
        "code_example": """// tests/user.test.js
const request = require('supertest');
const app = require('../src/app');

describe('API Users Integration Tests', () => {
  it('GET /api/users phải trả về danh sách có status 200', async () => {
    const res = await request(app)
      .get('/api/users')
      .expect('Content-Type', /json/)
      .expect(200);

    expect(Array.isArray(res.body.data)).toBe(true);
  });

  it('POST /api/users phải trả về 400 nếu thiếu email', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Test User' }) // Thiếu email
      .expect(400);

    expect(res.body.error).toBeDefined();
  });
});""",
        "tips": "Luôn nhớ quy tắc tách `app.js` khỏi `server.js` khi được hỏi về testing trong Express."
    },

    33: {
        "title_vi": "Các kỹ thuật Debugging thông dụng cho ứng dụng Express?",
        "level": "Junior",
        "short_answer": "Các kỹ thuật debugging bao gồm: (1) Sử dụng module `debug` tích hợp sẵn của Express bằng biến môi trường `DEBUG=express:* node app.js`, (2) Sử dụng cờ `--inspect` để kết nối với Chrome DevTools hoặc VS Code Debugger, (3) Thêm middleware ghi log chi tiết cho từng request, và (4) Bắt các biến thể lỗi bằng custom error handling.",
        "deep_dive": """1. Biến môi trường DEBUG: Express tích hợp sẵn thư viện `debug`. Khi bạn bật `DEBUG=express:router`, Express sẽ in ra từng route được khớp, từng middleware được duyệt qua trên terminal, cực kỳ trực quan để phát hiện vì sao request không vào route mong muốn.""",
        "code_example": """# Bật toàn bộ log nội bộ của Express để xem luồng routing:
DEBUG=express:* node server.js

# Hoặc chỉ xem router:
DEBUG=express:router node server.js

# Chạy với Node Debugger để gắn Breakpoints trong VS Code:
node --inspect server.js""",
        "tips": "Lệnh `DEBUG=express:*` là vũ khí bí mật giúp bạn hiểu chính xác Express đang làm gì bên dưới mỗi khi có request tới."
    },

    34: {
        "title_vi": "Vai trò của Biến môi trường trong ứng dụng Express?",
        "level": "Junior",
        "short_answer": "Biến môi trường giúp tách biệt hoàn toàn mã nguồn (Code) khỏi cấu hình hạ tầng (Configuration) theo nguyên tắc 12-Factor App. Chúng được dùng để lưu trữ các giá trị thay đổi tùy theo môi trường triển khai (cổng mạng `PORT`, chuỗi kết nối Database `DATABASE_URL`, khóa bí mật `JWT_SECRET`, và cờ môi trường `NODE_ENV`).",
        "deep_dive": """1. Tầm quan trọng của `NODE_ENV`:
   - Khi `NODE_ENV === 'production'`: Express tự động cache view templates, ẩn các thông tin stacktrace lỗi nhạy cảm, và kích hoạt tối ưu hóa hiệu năng nội bộ.
   - Khi `development`: Express in chi tiết lỗi ra màn hình để lập trình viên sửa bug.""",
        "code_example": """// config/env.js
require('dotenv').config();

module.exports = {
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  dbUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  isProd: process.env.NODE_ENV === 'production'
};""",
        "tips": "Tuyệt đối không commit file `.env` lên GitHub để tránh bị hacker quét bot lấy cắp API keys."
    },

    35: {
        "title_vi": "Cách sử dụng VS Code Debugger với ứng dụng Express?",
        "level": "Junior",
        "short_answer": "Tạo file cấu hình `.vscode/launch.json` trong thư mục dự án với loại môi trường `pwa-node`. Cấu hình file khởi động trỏ tới file server chính. Sau đó nhấn phím `F5` trên bàn phím để kích hoạt debugger, đặt Breakpoints bằng cách click vào lề trái của dòng code để dừng chương trình và soi giá trị của `req`, `res` khi có request.",
        "deep_dive": """1. Auto Attach: Tính năng thông minh của VS Code. Chỉ cần mở terminal trong VS Code và gõ `node --watch server.js`, VS Code tự động gắn debugger vào mà không cần tạo file cấu hình.""",
        "code_example": """// .vscode/launch.json
{
  \"version\": \"0.2.0\",
  \"configurations\": [
    {
      \"type\": \"pwa-node\",
      \"request\": \"launch\",
      \"name\": \"Khởi chạy Debug Express\",
      \"skipFiles\": [\"<node_internals>/**\"],
      \"program\": \"${workspaceFolder}/src/server.js\",
      \"restart\": true,
      \"envFile\": \"${workspaceFolder}/.env\"
    }
  ]
}""",
        "tips": "Sử dụng Breakpoints thay vì chèn hàng chục câu lệnh `console.log` bừa bãi vào mã nguồn."
    },

    36: {
        "title_vi": "Cách kết nối cơ sở dữ liệu MongoDB với Express bằng Mongoose?",
        "level": "Mid",
        "short_answer": "Sử dụng thư viện `mongoose`. Tạo một file kết nối riêng gọi `mongoose.connect(URI)`. Trong ứng dụng Express, kết nối DB thành công trước khi bắt đầu `app.listen()`. Định nghĩa Schema, Model và gọi các hàm bất đồng bộ trong controller.",
        "deep_dive": """1. Kết nối trước khi mở Server: Đảm bảo server chỉ nhận request khi đã kết nối DB thành công.
2. Tối ưu hóa đọc với `.lean()`: Giúp tăng tốc độ truy vấn đọc dữ liệu gấp nhiều lần trong route handlers.""",
        "code_example": """const mongoose = require('mongoose');
const express = require('express');
const app = express();
app.use(express.json());

async function startServer() {
  try {
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/shop');
    console.log('✅ Đã kết nối cơ sở dữ liệu MongoDB');

    app.listen(3000, () => console.log('Server chạy tại port 3000'));
  } catch (err) {
    console.error('❌ Lỗi kết nối MongoDB:', err);
    process.exit(1);
  }
}

startServer();""",
        "tips": "Luôn bao bọc hàm khởi động trong khối `try/catch` và gọi `process.exit(1)` nếu không kết nối được database lúc khởi động."
    },

    37: {
        "title_vi": "Cách tích hợp ORM như Sequelize hoặc Prisma vào Express?",
        "level": "Mid",
        "short_answer": "Khởi tạo một instance singleton của ORM Client (ví dụ `const prisma = new PrismaClient()`). Trong các Controllers của Express, import client này để thực hiện các thao tác CRUD bất đồng bộ bên trong khối `try/catch` hoặc async handler.",
        "deep_dive": """1. Singleton Client: Bắt buộc chỉ tạo DUY NHẤT một instance của ORM client trong suốt vòng đời của ứng dụng để tránh việc tạo ra quá nhiều connection pools làm cạn kiệt kết nối của Database server.
2. Tách biệt tầng Repository: Không nên gọi trực tiếp ORM trong route file. Hãy đóng gói vào Service hoặc Repository layer.""",
        "code_example": """// lib/prisma.js (Singleton)
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();
module.exports = prisma;

// controllers/user.controller.js
const prisma = require('../lib/prisma');

exports.getUsers = async (req, res, next) => {
  try {
    const users = await prisma.user.findMany({
      select: { id: true, email: true, name: true }
    });
    res.json(users);
  } catch (error) {
    next(error);
  }
};""",
        "tips": "Prisma hiện nay là giải pháp ORM được ưa chuộng hàng đầu cho Node.js/Express nhờ khả năng sinh Type-safe tự động tuyệt đối."
    },

    38: {
        "title_vi": "Cách xử lý lỗi cơ sở dữ liệu (Database Errors) trong Express?",
        "level": "Mid",
        "short_answer": "Xử lý lỗi cơ sở dữ liệu đòi hỏi việc phân loại mã lỗi (Error Codes) của hệ quản trị cơ sở dữ liệu (ví dụ mã `23505` của PostgreSQL hay `E11000` của MongoDB cho lỗi trùng lặp khóa duy nhất). Sau đó chuyển đổi các lỗi kỹ thuật tầng thấp này thành các thông báo lỗi HTTP thân thiện với người dùng (như `409 Conflict` hoặc `400 Bad Request`).",
        "deep_dive": """1. Không lộ thông tin Database nội bộ: Tránh ném nguyên xi câu query lỗi chứa tên bảng và tên cột ra cho client. Kẻ tấn công có thể lợi dụng thông tin này để khai thác lỗ hổng.
2. Centralized Error Mapping: Đặt logic chuyển đổi mã lỗi DB ngay bên trong Global Error-Handling Middleware.""",
        "code_example": """// Middleware chuẩn hóa lỗi Database
app.use((err, req, res, next) => {
  // Bắt lỗi trùng Unique Key của MongoDB (E11000)
  if (err.code === 11000) {
    const field = Object.keys(err.keyValue)[0];
    return res.status(409).json({
      error: `Giá trị của trường '${field}' đã tồn tại trong hệ thống.`
    });
  }

  // Bắt lỗi Validation của Mongoose
  if (err.name === 'ValidationError') {
    const errors = Object.values(err.errors).map(el => el.message);
    return res.status(400).json({ error: 'Dữ liệu không hợp lệ', details: errors });
  }

  res.status(500).json({ error: 'Lỗi cơ sở dữ liệu nội bộ' });
});""",
        "tips": "Xử lý chuẩn mã lỗi trùng lặp (Duplicate Key) với HTTP status 409 Conflict là câu trả lời ghi điểm tuyệt đối trong mắt nhà tuyển dụng."
    },

    39: {
        "title_vi": "Ưu điểm của cơ chế Connection Pooling khi kết nối Database trong Express?",
        "level": "Senior",
        "short_answer": "Connection Pooling duy trì một nhóm các kết nối TCP tới Database đã được mở sẵn và giữ ở trạng thái nhàn rỗi. Khi có request cần truy vấn, nó mượn một kết nối từ pool, thực thi xong trả lại pool cho request khác tái sử dụng. Ưu điểm: (1) Loại bỏ chi phí đắt đỏ của quá trình bắt tay TCP và chứng thực mỗi lần truy vấn, (2) Giảm đáng kể độ trễ (latency), và (3) Giới hạn số lượng kết nối tối đa để bảo vệ Database không bị quá tải sập nguồn.",
        "deep_dive": """1. Chi phí bắt tay: Mở một kết nối TCP/TLS và xác thực mật khẩu với Postgres mất từ 30ms đến 100ms. Dùng pool giúp thời gian lấy kết nối giảm xuống chỉ còn < 1ms!
2. Cấu hình tối ưu: Thiết lập `max: 20` (số kết nối tối đa) và `idleTimeoutMillis: 30000`.""",
        "code_example": """const { Pool } = require('pg');

// Khởi tạo Connection Pool cho PostgreSQL trong Express
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Tối đa 20 kết nối đồng thời
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

app.get('/api/data', async (req, res, next) => {
  try {
    // Mượn connection từ pool, query xong tự động trả lại
    const result = await pool.query('SELECT NOW()');
    res.json(result.rows[0]);
  } catch (err) {
    next(err);
  }
});""",
        "tips": "Nếu không dùng Connection Pool mà tạo mới kết nối trên mỗi request, server của bạn sẽ lập tức nhận lỗi `Too many connections` của MySQL/Postgres khi có đợt tăng tải đột biến."
    },

    40: {
        "title_vi": "Cách triển khai xác thực người dùng (Authentication) với JWT trong Express?",
        "level": "Mid",
        "short_answer": "Xác thực với JWT (JSON Web Token) bao gồm 2 phần: (1) Endpoint Đăng nhập: Kiểm tra mật khẩu (so khớp hash bằng `bcrypt`), nếu đúng thì ký tạo token `jwt.sign({ userId }, SECRET, { expiresIn: '1h' })` và trả về client, và (2) Auth Middleware: Đọc token từ header `Authorization: Bearer <token>`, giải mã bằng `jwt.verify()`, gắn thông tin `req.user` và cho phép đi tiếp.",
        "deep_dive": """1. Lưu trữ an toàn: Khuyên dùng gửi JWT qua Cookie `httpOnly` thay vì lưu trong localStorage của trình duyệt để chống tấn công XSS.
2. Refresh Token Pattern: Sử dụng Access Token có hạn ngắn (15 phút) và Refresh Token có hạn dài (7 ngày) lưu trong database để cấp lại token mới khi hết hạn mà người dùng không phải đăng nhập lại.""",
        "code_example": """const jwt = require('jsonwebtoken');

// Middleware xác thực JWT
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Định dạng: Bearer <TOKEN>

  if (!token) {
    return res.status(401).json({ error: 'Yêu cầu token xác thực để truy cập' });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Token đã hết hạn hoặc không hợp lệ' });
    }
    req.user = user; // Gắn thông tin người dùng vào request
    next();
  });
};

app.get('/api/protected/profile', authenticateToken, (req, res) => {
  res.json({ message: 'Dữ liệu bảo mật', user: req.user });
});""",
        "tips": "Luôn phân biệt rõ: Status `401 Unauthorized` (chưa cung cấp token hoặc token sai) và `403 Forbidden` (token đúng nhưng không có quyền truy cập tài nguyên)."
    },

    41: {
        "title_vi": "Cách quản lý phiên (Sessions) trong Express và so sánh với JWT?",
        "level": "Mid",
        "short_answer": "Session-based Authentication lưu trữ trạng thái người dùng ở phía Server (thường là trong Redis) và chỉ gửi một Cookie chứa Session ID về cho client. Trong khi đó, JWT là Token-based hoàn toàn Stateless, toàn bộ thông tin người dùng được mã hóa ký điện tử nằm ngay bên trong token ở phía Client.",
        "deep_dive": """So sánh chi tiết:
1. Thu hồi (Revocation): Session thắng tuyệt đối! Nếu muốn đá user ra khỏi hệ thống, server chỉ cần xóa key session trên Redis. JWT rất khó thu hồi ngay lập tức trước khi nó hết hạn.
2. Khả năng mở rộng (Scalability): JWT thắng vì server không tốn tài nguyên lưu trữ và truy vấn DB trên mỗi request.
3. Dung lượng: Session Cookie rất nhẹ (~32 ký tự). JWT mang theo payload nên kích thước lớn hơn (~300 - 500 bytes) gửi kèm trong mỗi HTTP request.""",
        "code_example": """// Minh họa thu hồi Session ngay lập tức:
app.post('/api/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) return res.status(500).send('Không thể đăng xuất');
    res.clearCookie('connect.sid');
    res.json({ message: 'Đã hủy phiên làm việc thành công' });
  });
});""",
        "tips": "Xu hướng hiện đại: Kết hợp cả hai - Dùng Access Token JWT ngắn hạn (15 phút) kết hợp Refresh Token quản lý trong cơ sở dữ liệu/Redis."
    },

    42: {
        "title_vi": "Cách xử lý phân quyền và vai trò người dùng (RBAC - Role-Based Access Control) trong Express?",
        "level": "Mid",
        "short_answer": "RBAC được triển khai bằng một middleware phân quyền chạy ngay sau middleware xác thực (Auth). Middleware này nhận danh sách các vai trò được phép (`allowedRoles`), so sánh với thuộc tính `req.user.role`. Nếu vai trò của user nằm trong danh sách cho phép thì gọi `next()`, ngược lại trả về `403 Forbidden`.",
        "deep_dive": """1. Phân biệt AuthN vs AuthZ:
   - Authentication (AuthN - Xác thực): Bạn là ai? (Kiểm tra token/mật khẩu).
   - Authorization (AuthZ - Phân quyền): Bạn được phép làm gì? (Kiểm tra vai trò/quyền hạn).
2. Quyền chi tiết (Permissions/Claims): Trong hệ thống lớn, thay vì chỉ kiểm tra Role ('admin'), người ta kiểm tra cụ thể quyền Permissions (ví dụ: `'orders:delete'`, `'users:export'`).""",
        "code_example": """// Middleware kiểm tra quyền hạn (Role Guard)
const authorizeRoles = (...allowedRoles) => {
  return (req, res, next) => {
    if (!req.user || !allowedRoles.includes(req.user.role)) {
      return res.status(403).json({
        error: 'Quyền truy cập bị từ chối: Bạn không có đủ đặc quyền'
      });
    }
    next();
  };
};

// Route chỉ dành riêng cho Admin và Quản lý
app.delete('/api/orders/:id', authenticateToken, authorizeRoles('admin', 'manager'), (req, res) => {
  res.send('Đã xóa đơn hàng thành công');
});""",
        "tips": "Luôn đặt middleware `authenticateToken` chạy TRƯỚC `authorizeRoles` để đảm bảo đối tượng `req.user` đã được khởi tạo."
    },

    43: {
        "title_vi": "Cách bảo vệ mật khẩu và dữ liệu nhạy cảm trong ứng dụng Express?",
        "level": "Junior",
        "short_answer": "Bảo vệ mật khẩu đòi hỏi: (1) TUYỆT ĐỐI KHÔNG BAO GIỜ lưu mật khẩu dạng văn bản thuần (plain text), (2) Sử dụng thuật toán băm chậm có Salt như `bcrypt` hoặc `argon2` với salt rounds thích hợp (từ 10 đến 12), (3) Không bao giờ trả về trường `password` trong các response JSON, và (4) Mã hóa các trường dữ liệu nhạy cảm bằng AES-256.",
        "deep_dive": """1. Tại sao dùng bcrypt thay vì MD5/SHA256: MD5 và SHA256 được thiết kế để chạy siêu nhanh, hacker có thể dùng GPU thử hàng tỷ mật khẩu mỗi giây (Brute-force). Bcrypt là thuật toán băm cố tình làm chậm CPU, kháng lại các cuộc tấn công Rainbow Table nhờ tự động thêm Salt ngẫu nhiên.
2. Tách biệt trường password: Trong ORM (Mongoose/Prisma), luôn cấu hình `select: false` cho trường mật khẩu.""",
        "code_example": """const bcrypt = require('bcrypt');

const SALT_ROUNDS = 12; // Chi phí băm chuẩn mực

// 1. Băm mật khẩu khi đăng ký
async function hashPassword(plainPassword) {
  return await bcrypt.hash(plainPassword, SALT_ROUNDS);
}

// 2. So khớp khi đăng nhập
async function verifyPassword(plainPassword, hashedPassword) {
  return await bcrypt.compare(plainPassword, hashedPassword);
}""",
        "tips": "Đừng đặt salt rounds quá cao (> 14) vì nó sẽ chiếm dụng CPU quá lâu làm nghẽn Event Loop của Node.js. 10 - 12 rounds là mức cân bằng hoàn hảo."
    },

    44: {
        "title_vi": "Cách tích hợp Third-Party API an toàn trong Express?",
        "level": "Mid",
        "short_answer": "Sử dụng HTTP Client như `axios` hoặc native `fetch`. Đặt Timeout chặt chẽ cho mọi request, lưu trữ API keys trong biến môi trường, sử dụng khối `try/catch` để bắt lỗi mạng và trả về mã lỗi thích hợp cho client của bạn (như `502 Bad Gateway` thay vì làm crash app).",
        "deep_dive": """1. Timeout: Nếu không set timeout, khi server bên thứ ba bị treo, socket kết nối của bạn sẽ bị giữ mở vĩnh viễn, dẫn đến việc ứng dụng của bạn cạn kiệt tài nguyên.
2. Retry Pattern: Triển khai retry có độ trễ tăng dần (Exponential Backoff) cho các lỗi mạng tạm thời (mã 503 hoặc timeout).""",
        "code_example": """const axios = require('axios');

app.get('/api/weather', async (req, res, next) => {
  try {
    const response = await axios.get('https://api.weatherapi.com/v1/current.json', {
      params: { key: process.env.WEATHER_API_KEY, q: 'Hanoi' },
      timeout: 3000 // Hủy request nếu quá 3 giây
    });

    res.json({ weather: response.data });
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      return res.status(504).json({ error: 'Cổng dịch vụ thời tiết phản hồi quá hạn' });
    }
    res.status(502).json({ error: 'Không thể kết nối đến đối tác thời tiết bên ngoài' });
  }
});""",
        "tips": "Phân biệt rõ: Nếu API bên thứ ba lỗi, bạn nên trả về mã `502 Bad Gateway` hoặc `504 Gateway Timeout` cho client của bạn."
    },

    45: {
        "title_vi": "Các bước triển khai (Deploy) ứng dụng Express lên Cloud (AWS, Heroku, Render)?",
        "level": "Junior",
        "short_answer": "Các bước chuẩn: (1) Cấu hình script `\"start\": \"node server.js\"` trong `package.json`, (2) Sử dụng cổng động `process.env.PORT`, (3) Thiết lập biến môi trường trên bảng điều khiển của nhà cung cấp Cloud, (4) Đảm bảo file `.gitignore` đã loại trừ `node_modules` và `.env`, và (5) Kết nối Git repository để tự động kích hoạt quá trình build và deploy.",
        "deep_dive": """1. Docker Container: Cách hiện đại nhất là đóng gói ứng dụng Express thành Docker Image rồi triển khai lên AWS ECS, Google Cloud Run hoặc Render Web Service để độc lập hoàn toàn môi trường.""",
        "code_example": """// Đảm bảo cấu hình cổng động chuẩn Cloud
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server khởi động thành công trên cổng: ${PORT}`);
});""",
        "tips": "Nhớ bind vào địa chỉ `'0.0.0.0'` khi chạy bên trong Docker container để container có thể nhận traffic từ bên ngoài."
    },

    46: {
        "title_vi": "Cách đảm bảo ứng dụng Express có khả năng mở rộng (Scalable)?",
        "level": "Senior",
        "short_answer": "Khả năng mở rộng của Express dựa trên nguyên tắc: BIẾN NÓ THÀNH MỘT ỨNG DỤNG HOÀN TOÀN STATELESS (Phi trạng thái). Đẩy toàn bộ session và cache ra Redis, đẩy các file upload sang AWS S3, đẩy các tác vụ nặng vào Message Queue. Khi ứng dụng là stateless, ta có thể dễ dàng tăng số lượng bản sao (Horizontal Scaling) lên hàng chục containers phía sau Load Balancer mà không gặp bất kỳ xung đột nào.",
        "deep_dive": """1. Tận dụng Cluster: Chạy chế độ PM2 cluster mode hoặc nhân bản Pods trong Kubernetes.
2. Tách biệt Read/Write: Sử dụng Database Read-Replicas cho các câu truy vấn đọc chiếm 90% tải.
3. Asynchronous Offloading: Chuyển các việc nặng (gửi mail, xuất PDF) cho Worker tiến trình riêng.""",
        "code_example": """// Kiến trúc Stateless: Không lưu trữ biến trạng thái nào trong bộ nhớ server!
// Mọi thông tin người dùng được giải mã từ JWT hoặc đọc từ Redis tập trung.""",
        "tips": "Từ khóa cốt lõi: 'Stateless Application Architecture'."
    },

    47: {
        "title_vi": "Phương pháp luận Twelve-Factor App áp dụng vào Express như thế nào?",
        "level": "Senior",
        "short_answer": "Áp dụng 12-Factor App vào Express: (1) Khai báo rõ ràng dependencies trong `package.json`, (2) Cấu hình thông qua biến môi trường (`process.env`), (3) Coi Database và Redis là Backing Services có thể thay thế qua connection string, (4) Coi ứng dụng là các Stateless Processes độc lập, (5) Tự export cổng mạng thông qua `app.listen()`, và (6) Hỗ trợ Fast Startup & Graceful Shutdown qua việc lắng nghe tín hiệu `SIGTERM`.",
        "deep_dive": """1. Graceful Shutdown trong Express: Khi máy chủ nhận tín hiệu tắt từ Kubernetes/Docker, không dừng đột ngột mà gọi `server.close()` để phục vụ nốt các requests dở dang và đóng connection pools an toàn trước khi exit.""",
        "code_example": """const server = app.listen(process.env.PORT || 3000);

process.on('SIGTERM', () => {
  console.log('Nhận tín hiệu SIGTERM. Đang thực hiện Graceful Shutdown...');
  server.close(async () => {
    console.log('HTTP Server đã đóng.');
    await db.disconnect();
    process.exit(0);
  });
});""",
        "tips": "Giải thích Graceful Shutdown là tiêu chí bắt buộc để đạt điểm tuyệt đối cho câu hỏi về 12-Factor App."
    },

    48: {
        "title_vi": "Thử thách code: Viết Middleware giới hạn 100 requests / 1 giờ cho mỗi IP?",
        "level": "Mid",
        "short_answer": "Có thể sử dụng một bảng băm trong bộ nhớ hoặc dùng thư viện `express-rate-limit`. Để giải thích nguyên lý, ta theo dõi số lượng request và mốc thời gian reset của từng IP.",
        "deep_dive": """1. Giải pháp Production: Trong môi trường nhiều server, phải lưu bộ đếm Rate Limit trong Redis (`rate-limit-redis`) để các server cùng chia sẻ chung giới hạn của một địa chỉ IP.""",
        "code_example": """const rateLimit = require('express-rate-limit');

// Triển khai bằng thư viện chuẩn công nghiệp express-rate-limit
const hourlyLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 giờ (60 phút)
  max: 100, // Tối đa 100 requests mỗi IP
  standardHeaders: true, // Trả về headers chuẩn 'RateLimit-*'
  legacyHeaders: false,
  message: {
    status: 429,
    error: 'Bạn đã vượt quá giới hạn 100 requests mỗi giờ. Vui lòng thử lại sau.'
  }
});

// Áp dụng middleware cho toàn bộ các route /api/
app.use('/api/', hourlyLimiter);""",
        "tips": "Nhớ nhắc đến mã lỗi chuẩn HTTP `429 Too Many Requests` và header `Retry-After`."
    },

    49: {
        "title_vi": "Thử thách code: Viết Route nhận JSON payload và trả về payload đảo ngược thứ tự?",
        "level": "Junior",
        "short_answer": "Định nghĩa một route POST, đọc `req.body`. Nếu payload là mảng thì dùng `.reverse()`. Nếu là Object thì đảo ngược các cặp key-value bằng cách dùng `Object.entries(req.body).reverse()` rồi gom lại bằng `Object.fromEntries()`.",
        "deep_dive": """1. Kiểm tra định dạng đầu vào: Luôn xác minh xem client có gửi đúng JSON payload hay không trước khi xử lý.""",
        "code_example": """const express = require('express');
const app = express();
app.use(express.json());

app.post('/api/reverse-payload', (req, res) => {
  const body = req.body;

  if (!body || typeof body !== 'object') {
    return res.status(400).json({ error: 'Payload phải là một đối tượng JSON hoặc mảng hợp lệ' });
  }

  // Trường hợp là Array:
  if (Array.isArray(body)) {
    return res.json([...body].reverse());
  }

  // Trường hợp là Object: Đảo ngược thứ tự các thuộc tính
  const reversedEntries = Object.entries(body).reverse();
  const reversedObject = Object.fromEntries(reversedEntries);

  res.json({
    original: body,
    reversed: reversedObject
  });
});""",
        "tips": "Dùng `Object.fromEntries(Object.entries(obj).reverse())` là cú pháp hiện đại và tinh tế nhất của JavaScript ES2019."
    },

    50: {
        "title_vi": "Thử thách code: Xây dựng REST API hoàn chỉnh với các thao tác CRUD cho đối tượng Books?",
        "level": "Junior",
        "short_answer": "Xây dựng 5 endpoints chuẩn REST: (1) `GET /api/books` (Danh sách), (2) `GET /api/books/:id` (Chi tiết), (3) `POST /api/books` (Tạo mới), (4) `PUT /api/books/:id` (Cập nhật), và (5) `DELETE /api/books/:id` (Xóa). Sử dụng mảng trong bộ nhớ làm placeholder data store.",
        "deep_dive": """1. Status codes chuẩn mực:
   - GET/PUT thành công: 200 OK.
   - POST tạo mới thành công: 201 Created.
   - DELETE thành công: 204 No Content hoặc 200 OK kèm thông báo.
   - Không tìm thấy ID: 404 Not Found.""",
        "code_example": """const express = require('express');
const app = express();
app.use(express.json());

let books = [
  { id: 1, title: 'Clean Code', author: 'Robert C. Martin' },
  { id: 2, title: 'Refactoring', author: 'Martin Fowler' }
];

// 1. GET ALL
app.get('/api/books', (req, res) => res.json(books));

// 2. GET BY ID
app.get('/api/books/:id', (req, res) => {
  const book = books.find(b => b.id === parseInt(req.params.id));
  if (!book) return res.status(404).json({ error: 'Không tìm thấy sách' });
  res.json(book);
});

// 3. CREATE (POST)
app.post('/api/books', (req, res) => {
  const { title, author } = req.body;
  if (!title || !author) return res.status(400).json({ error: 'Tiêu đề và tác giả là bắt buộc' });
  const newBook = { id: Date.now(), title, author };
  books.push(newBook);
  res.status(201).json(newBook);
});

// 4. UPDATE (PUT)
app.put('/api/books/:id', (req, res) => {
  const book = books.find(b => b.id === parseInt(req.params.id));
  if (!book) return res.status(404).json({ error: 'Không tìm thấy sách' });
  book.title = req.body.title || book.title;
  book.author = req.body.author || book.author;
  res.json(book);
});

// 5. DELETE
app.delete('/api/books/:id', (req, res) => {
  const index = books.findIndex(b => b.id === parseInt(req.params.id));
  if (index === -1) return res.status(404).json({ error: 'Không tìm thấy sách' });
  books.splice(index, 1);
  res.status(204).send(); // 204 No Content
});""",
        "tips": "Viết mã rõ ràng, kiểm tra validation đầu vào và trả về đúng status codes 201, 204, 404 sẽ ghi điểm 10/10 trong bài test live-coding."
    },

    51: {
        "title_vi": "Chiến lược xây dựng ứng dụng thời gian thực (Real-Time) với Express.js?",
        "level": "Mid",
        "short_answer": "Express là framework HTTP hướng request-response. Để bổ sung tính năng thời gian thực, ta kết hợp Express với: (1) `Socket.IO` hoặc WebSocket thuần cho giao tiếp 2 chiều (chat, game, collab doc), hoặc (2) Server-Sent Events (SSE) cho dữ liệu 1 chiều từ server xuống client (thông báo, feed giá chứng khoán, stream AI LLM), kết hợp với Redis Pub/Sub khi chạy nhiều máy chủ.",
        "deep_dive": """1. Server-Sent Events (SSE): Rất nhẹ, chạy trực tiếp trên HTTP thuần của Express mà không cần cài thêm thư viện phức tạp. Chỉ cần set header `Content-Type: text/event-stream`.
2. Socket.IO với Express: Gắn chung vào cùng một instance `http.Server` để chia sẻ chung cổng mạng.""",
        "code_example": """const http = require('node:http');
const express = require('express');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app); // Gắn Express vào HTTP Server
const io = new Server(server, { cors: { origin: '*' } });

// Lắng nghe sự kiện Realtime
io.on('connection', (socket) => {
  console.log('Client kết nối Realtime:', socket.id);
  socket.on('chatMessage', (msg) => io.emit('broadcastMessage', msg));
});

server.listen(3000);""",
        "tips": "Nếu chỉ cần server đẩy thông báo 1 chiều xuống client, hãy đề xuất Server-Sent Events (SSE) vì nó dùng HTTP chuẩn, không bị tường lửa chặn và tốn ít tài nguyên hơn WebSocket."
    },

    52: {
        "title_vi": "Các kỹ thuật tối ưu hóa mã nguồn nâng cao cho Express.js?",
        "level": "Senior",
        "short_answer": "Tối ưu hóa nâng cao bao gồm: (1) Tránh hoàn toàn việc chặn Event Loop (không chạy các regex phức tạp hoặc thuật toán đệ quy sâu trên main thread), (2) Sử dụng Router Radix Tree hoặc chuyển sang Fastify nếu cần tốc độ routing tối đa, (3) Tối ưu hóa JSON serialization (dùng `fast-json-stringify`), (4) Hạn chế middleware dư thừa, và (5) Tận dụng HTTP/2 để truyền tải đa luồng.",
        "deep_dive": """1. JSON Serialization Overhead: `JSON.stringify` mặc định của V8 tốn khá nhiều CPU với các object lớn. Các thư viện tối ưu hóa schema có thể sinh mã C++ serialize nhanh hơn 2-3 lần.
2. Tắt các tính năng không dùng: `app.disable('etag')` nếu đã có CDN xử lý caching.""",
        "code_example": """// Tắt các thiết lập mặc định không cần thiết để tăng tốc độ phản hồi microsecond
app.disable('x-powered-by');
app.disable('etag'); // Nếu đã có Cloudflare CDN quản lý cache""",
        "tips": "Nhớ: Tối ưu hóa lớn nhất của Express luôn nằm ở tầng I/O (Database queries, Caching, Network) chứ ít khi nằm ở bản thân code JavaScript."
    },

    53: {
        "title_vi": "Khái niệm và lợi ích của Server-Side Rendering (SSR) trong Express?",
        "level": "Senior",
        "short_answer": "Server-Side Rendering trong Express là việc biên dịch toàn bộ giao diện HTML hoàn chỉnh trực tiếp trên máy chủ trước khi trả về cho trình duyệt. Lợi ích: Tối ưu SEO cho máy tìm kiếm Googlebot cào dữ liệu, hiển thị trang ngay tức thì trên các thiết bị di động cấu hình yếu, và cải thiện điểm Core Web Vitals (FCP, LCP).",
        "deep_dive": """1. SSR truyền thống: Dùng EJS/Pug render dữ liệu từ database vào template HTML.
2. SSR hiện đại: Node/Express kết hợp React (`renderToString`) hoặc Vue (`renderToString`) để render component.
3. Đánh đổi: SSR làm tiêu tốn CPU của server Express hơn rất nhiều so với việc chỉ phục vụ API JSON thuần túy.""",
        "code_example": """// Render giao diện SSR có sẵn dữ liệu giúp Google cào nội dung hoàn hảo
app.get('/products/:slug', async (req, res) => {
  const product = await db.getProduct(req.params.slug);
  res.render('product-detail', { product }); // HTML trả về đã có sẵn giá tiền và mô tả!
});""",
        "tips": "Senior Tip: Với các trang có nội dung ít thay đổi, kết hợp SSR với HTML Caching (lưu trữ file HTML đã render vào Redis) để giảm tải 95% CPU cho Express."
    },

    54: {
        "title_vi": "Cách đảm bảo mã nguồn Express dễ bảo trì (Maintainable) và tuân thủ Best Practices?",
        "level": "Senior",
        "short_answer": "Để code Express dễ bảo trì dài hạn: (1) Tuân thủ triệt để nguyên tắc Clean Architecture và SOLID, (2) Module hóa theo Domain/Feature thay vì gom tất cả controllers vào 1 folder khổng lồ, (3) Sử dụng TypeScript để có Type Safety và tự động gợi ý code, (4) Kiểm thử tự động với độ phủ test > 80%, và (5) Tự động sinh tài liệu Swagger/OpenAPI từ code.",
        "deep_dive": """1. Tránh Fat Controllers: Controller không được chứa quá 20-30 dòng code. Nhiệm vụ duy nhất của nó là nhận data, gọi Service và trả về status.
2. Xử lý lỗi bất đồng bộ tập trung: Không viết lặp lại các khối `try/catch` giống nhau ở khắp mọi nơi.""",
        "code_example": """// Sử dụng Async Wrapper để loại bỏ hoàn toàn các khối try/catch lặp đi lặp lại
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Route controller sạch sẽ 100%, không cần viết try/catch thủ công!
app.get('/api/users', asyncHandler(async (req, res) => {
  const users = await userService.getAllUsers();
  res.json(users);
}));""",
        "tips": "Mẫu `asyncHandler` là một trong những best practices được yêu thích nhất trong cộng đồng Express để giữ cho code luôn phẳng và sạch."
    },

    55: {
        "title_vi": "Nghiên cứu tình huống: Cấu trúc ứng dụng Express cho sàn thương mại điện tử quy mô lớn?",
        "level": "Senior",
        "short_answer": "Một sàn TMĐT lớn yêu cầu kiến trúc Microservices hoặc Modular Monolith phân chia theo các Domain nghiệp vụ rõ rệt: User/Auth Module, Product Catalog Module, Cart Module, Order Module, Payment Module. Hệ thống cần tích hợp: Redis Cache đa tầng cho danh mục sản phẩm, Message Queue (RabbitMQ) xử lý trừ kho và gửi email bất đồng bộ, Circuit Breaker bảo vệ cổng thanh toán, và Distributed Tracing để theo dõi luồng mua hàng.",
        "deep_dive": """1. Tránh nghẽn lúc Flash Sale: Các request đặt hàng được đẩy ngay vào hàng đợi (Queue), server trả về mã `202 Accepted`. Các worker phía sau sẽ tuần tự trừ kho theo cơ chế lạc quan (Optimistic Locking) trong Database để không bị quá tải.
2. Read/Write Split: Tách Database đọc (phục vụ khách xem hàng) và Database ghi (đặt hàng).""",
        "code_example": """// Luồng đặt hàng chịu tải cao trong E-Commerce
app.post('/api/orders/checkout', authenticateToken, async (req, res, next) => {
  try {
    // 1. Validate giỏ hàng
    // 2. Đẩy job xử lý thanh toán và giữ hàng vào Queue (chỉ mất 2ms)
    const job = await orderQueue.add('processOrder', {
      userId: req.user.id,
      cart: req.body.cart
    });

    // 3. Phản hồi ngay lập tức cho mobile app / web
    res.status(202).json({
      message: 'Đơn hàng đang được xếp hàng xử lý',
      trackingJobId: job.id
    });
  } catch (err) {
    next(err);
  }
});""",
        "tips": "Hãy nhắc đến từ khóa 'Eventual Consistency' (Tính nhất quán cuối cùng) và 'Optimistic Locking' khi giải quyết bài toán trừ kho đồng thời."
    },

    56: {
        "title_vi": "Các cân nhắc trọng yếu để xây dựng một API bảo mật tuyệt đối với Express?",
        "level": "Senior",
        "short_answer": "Bảo mật API toàn diện yêu cầu: (1) Bắt buộc HTTPS (HSTS), (2) Sử dụng `helmet` bảo vệ HTTP headers, (3) Rate Limiting chống Brute-force/DDoS, (4) Xác thực JWT với thời gian hết hạn ngắn, (5) Validate và sanitize 100% input đầu vào, (6) CORS whitelist nghiêm ngặt, (7) Không bao giờ để lộ stacktrace lỗi ra ngoài production, và (8) Ghi log bảo mật có cảnh báo tự động.",
        "deep_dive": """1. Giới hạn kích thước Body: `express.json({ limit: '10kb' })` để ngăn chặn kẻ tấn công gửi chuỗi JSON nặng 100MB làm cạn kiệt RAM server.
2. Chống Parameter Pollution: Dùng thư viện `hpp` để ngăn chặn việc gửi trùng nhiều params lừa bộ lọc bảo mật.""",
        "code_example": """const helmet = require('helmet');
const hpp = require('hpp');
const rateLimit = require('express-rate-limit');

// Bộ middleware phòng thủ tiêu chuẩn
app.use(helmet());
app.use(hpp()); // Chống HTTP Parameter Pollution
app.use(express.json({ limit: '10kb' })); // Chống tràn dung lượng
app.disable('x-powered-by'); // Ẩn danh tính máy chủ""",
        "tips": "Nắm vững OWASP API Security Top 10 (như BOLA - Broken Object Level Authorization) để chứng minh tư duy bảo mật cấp cao."
    },

    57: {
        "title_vi": "Cách quản lý Session trong hệ thống Express phân tán (Distributed Express App)?",
        "level": "Senior",
        "short_answer": "Trong hệ thống phân tán chạy nhiều instances Express phía sau Load Balancer, BẮT BUỘC phải sử dụng Centralized In-Memory Store (Redis Cluster) làm nơi lưu trữ session duy nhất thông qua `connect-redis`. Mọi instance Express đều kết nối vào cụm Redis này để đọc và ghi session chung với độ trễ < 1ms.",
        "deep_dive": """1. Tại sao không dùng Sticky Sessions: Sticky Sessions phụ thuộc vào Load Balancer map IP user vào 1 server cố định. Nếu server đó chết, user bị đăng xuất. Dùng Redis Cluster giúp người dùng kết nối vào bất kỳ server nào cũng giữ nguyên trạng thái đăng nhập.
2. Redis Replication: Thiết lập Redis Master-Replica để đảm bảo không bị mất session khi một node Redis bảo trì.""",
        "code_example": """const session = require('express-session');
const { RedisStore } = require('connect-redis');
const { createClient } = require('redis');

const redisClient = createClient({ url: process.env.REDIS_URL });
redisClient.connect().catch(console.error);

app.use(session({
  store: new RedisStore({ client: redisClient, prefix: 'sess:' }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true, httpOnly: true, maxAge: 86400000 }
}));""",
        "tips": "Redis là tiêu chuẩn vàng của ngành công nghiệp cho bài toán Distributed Session Management."
    },

    58: {
        "title_vi": "Kiến trúc Microservices tác động và định hình ứng dụng Express.js như thế nào?",
        "level": "Senior",
        "short_answer": "Trong kiến trúc Microservices, ứng dụng Express thường được tinh gọn thành các dịch vụ chuyên biệt siêu nhỏ (Single-purpose services) hoặc đóng vai trò làm API Gateway (BFF - Backend for Frontend). Tác động lớn nhất là Express phải chuyển dịch từ giao tiếp nội bộ trong RAM sang giao tiếp mạng phân tán (gRPC, REST, RabbitMQ), đòi hỏi phải triển khai cơ chế phát hiện dịch vụ (Service Discovery), Distributed Tracing, Circuit Breaker và quản lý lỗi phân tán.",
        "deep_dive": """1. Express làm API Gateway: Tiếp nhận toàn bộ requests từ client, thực hiện xác thực JWT tập trung, rate-limiting, sau đó định tuyến hoặc tổng hợp dữ liệu từ các microservices con phía trong mạng nội bộ.
2. Khả năng phục hồi (Resilience): Dùng thư viện `opossum` triển khai Circuit Breaker để khi một microservice con bị sập, toàn bộ hệ thống API Gateway không bị treo dây chuyền.""",
        "code_example": """// Express đóng vai trò API Gateway / Aggregator
app.get('/api/dashboard', authenticateToken, async (req, res, next) => {
  try {
    // Gọi song song sang các internal microservices độc lập
    const [userProfile, notifications, recentOrders] = await Promise.all([
      userService.getProfile(req.user.id),
      notificationService.getUnread(req.user.id),
      orderService.getRecents(req.user.id)
    ]);

    res.json({ userProfile, notifications, recentOrders });
  } catch (error) {
    next(error);
  }
});""",
        "tips": "Kết thúc xuất sắc: 'Express trong Microservices tỏa sáng rực rỡ nhất ở vai trò API Gateway và I/O-intensive Services nhờ tính gọn nhẹ, khởi động nhanh và khả năng xử lý stream phản hồi tuyệt vời.'"
    }
}
