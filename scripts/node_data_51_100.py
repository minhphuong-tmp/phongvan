"""Node.js Interview Questions & Answers Database (Part 2: Q51 - Q100)"""

NODE_ANSWERS_PART2 = {
    51: {
        "title_vi": "Các thực hành bảo mật tốt nhất (Security Best Practices) cho ứng dụng Node.js?",
        "level": "Senior",
        "short_answer": "Bảo mật Node.js yêu cầu tiếp cận đa tầng (Defense in Depth): (1) Sử dụng `helmet` để bảo vệ HTTP headers, (2) Validate và sanitize toàn bộ input người dùng bằng Zod/Joi, (3) Triển khai Rate Limiting chống Brute-force/DDoS, (4) Ngăn ngừa SQL/NoSQL Injection bằng Prepared Statements, (5) Chạy container với tài khoản phi root (non-root user), và (6) Quét lỗ hổng dependencies định kỳ bằng `npm audit` / Snyk.",
        "deep_dive": """1. Quản lý Dependencies: Hơn 85% mã nguồn trong ứng dụng Node.js đến từ `node_modules`. Luôn quét các lỗ hổng đã biết (CVEs) trong CI pipeline.
2. Không để rò rỉ thông tin nhạy cảm: Tắt `x-powered-by`, không bao giờ commit file `.env` hoặc API keys vào Git repository.
3. Chống Prototype Pollution: Đóng băng các prototype hoặc dùng `Object.create(null)` khi parse JSON từ người dùng lạ.""",
        "code_example": """const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();

// 1. Bảo vệ HTTP Headers
app.use(helmet());

// 2. Chống Brute-force & DDoS bằng Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 phút
  max: 100, // Tối đa 100 requests trên mỗi IP
  message: { error: 'Quá nhiều yêu cầu, vui lòng thử lại sau.' }
});
app.use('/api/', limiter);

// 3. Giới hạn kích thước payload chống tràn RAM (Denial of Service)
app.use(express.json({ limit: '10kb' }));""",
        "tips": "Nhắc đến OWASP Top 10 for Node.js và khuyến nghị chạy Node.js dưới một user Linux không có quyền sudo (`USER node` trong Dockerfile)."
    },

    52: {
        "title_vi": "Cách bảo vệ ứng dụng Node.js khỏi các cuộc tấn công Cross-Site Scripting (XSS)?",
        "level": "Mid",
        "short_answer": "Để chống XSS, Node.js backend cần: (1) Cấu hình chính sách bảo mật nội dung chặt chẽ (Content Security Policy - CSP) qua Helmet, (2) Làm sạch và mã hóa (sanitize/escape) mọi dữ liệu HTML đầu vào từ người dùng (dùng `xss` hoặc `DOMPurify`), (3) Thiết lập cờ `httpOnly` và `sameSite: 'strict'` cho Cookies để script độc hại không thể đọc được session token.",
        "deep_dive": """1. Các loại XSS:
   - Stored XSS: Mã độc được lưu vào database và thực thi mỗi khi trang web tải lại.
   - Reflected XSS: Mã độc nằm trong URL query parameter và phản chiếu ngay lập tức trên view.
   - DOM-based XSS: Xảy ra trực tiếp trên client JavaScript.
2. Vai trò của Backend: Backend không bao giờ được tin tưởng dữ liệu từ client. Bất kỳ đoạn văn bản nào trước khi lưu vào DB hoặc render ra template engine (EJS, Pug) đều phải được escape các ký tự đặc biệt (`<`, `>`, `&`, `\"`, `'`).""",
        "code_example": """const xss = require('xss');
const express = require('express');
const app = express();
app.use(express.json());

app.post('/api/comments', (req, res) => {
  const rawComment = req.body.comment;
  
  // ✅ Làm sạch mã độc: '<script>stealCookie()</script> Tuyệt vời!'
  // Sẽ được lọc bỏ hoàn toàn các tag script nguy hiểm
  const cleanComment = xss(rawComment);
  
  // Lưu cleanComment vào cơ sở dữ liệu...
  res.status(201).json({ success: true, comment: cleanComment });
});

// Thiết lập Cookie an toàn chống XSS đánh cắp Token
app.get('/api/login', (req, res) => {
  res.cookie('token', 'JWT_SECRET_VALUE', {
    httpOnly: true, // JavaScript phía client không thể đọc bằng document.cookie!
    secure: true,   // Bắt buộc kết nối HTTPS
    sameSite: 'strict'
  });
  res.json({ message: 'Đăng nhập an toàn' });
});""",
        "tips": "Điểm quan trọng nhất chống mất cắp session qua XSS: Luôn đặt thuộc tính `httpOnly: true` cho cookies chứa Auth Token."
    },

    53: {
        "title_vi": "Biến môi trường (Environment Variables) là gì và cách sử dụng chuẩn mực trong Node.js?",
        "level": "Junior",
        "short_answer": "Biến môi trường là các cặp khóa-giá trị được thiết lập ở cấp độ hệ điều hành bên ngoài mã nguồn, dùng để lưu trữ các thông tin cấu hình thay đổi theo môi trường (Development, Staging, Production) như số cổng PORT, Database URLs, và API Secrets. Trong Node.js, chúng được truy cập thông qua đối tượng toàn cục `process.env`.",
        "deep_dive": """1. Tải biến môi trường: Sử dụng thư viện `dotenv` trong file gốc (`require('dotenv').config()`) hoặc từ Node v20.6+ có thể dùng cờ native `node --env-file=.env app.js`.
2. Validation: Sử dụng thư viện như `zod` hoặc `envalid` để kiểm tra các biến môi trường bắt buộc lúc khởi động server. Nếu thiếu biến quan trọng (như `DATABASE_URL`), server lập tức dừng khởi động để tránh chạy sai logic.
3. Bảo mật: Tuyệt đối thêm `.env` vào file `.gitignore`! Chỉ commit `.env.example` với các giá trị mẫu rỗng.""",
        "code_example": """// Từ Node v20.6+: Không cần cài thêm thư viện 'dotenv'!
// Chạy lệnh: node --env-file=.env server.js

// Kiểm tra và validate biến môi trường chuẩn mực:
const requiredEnv = ['PORT', 'DATABASE_URL', 'JWT_SECRET'];
for (const envVar of requiredEnv) {
  if (!process.env[envVar]) {
    console.error(`FATAL: Thiếu biến môi trường bắt buộc: ${envVar}`);
    process.exit(1); // Dừng app ngay lập tức
  }
}

const PORT = parseInt(process.env.PORT, 10) || 3000;
console.log(`Khởi động server trên cổng: ${PORT}`);""",
        "tips": "Senior Tip: Nhắc đến cờ native mới của Node.js: `node --env-file=.env index.js`. Không cần cài thêm package `dotenv` nữa!"
    },

    54: {
        "title_vi": "WebSockets là gì và chúng hoạt động với Node.js như thế nào?",
        "level": "Mid",
        "short_answer": "WebSockets là giao thức mạng cung cấp kênh giao tiếp song công toàn phần (Full-Duplex), hai chiều, liên tục trên một kết nối TCP duy nhất giữa client và server. Không giống như HTTP (phải gửi request mới có response), WebSocket cho phép server chủ động đẩy dữ liệu (push) xuống client ngay lập tức khi có sự kiện với độ trễ cực thấp.",
        "deep_dive": """1. Handshake: Kết nối bắt đầu bằng một HTTP GET Request bình thường với header `Upgrade: websocket` và `Connection: Upgrade`. Server phản hồi `101 Switching Protocols` để chuyển sang giao thức WebSocket nhị phân.
2. Trọng lượng nhẹ: Sau khi kết nối được nâng cấp, các frame dữ liệu chỉ tốn 2 đến 10 bytes overhead (so với hàng trăm bytes headers của mỗi HTTP request).
3. Thư viện phổ biến: `ws` (siêu nhanh, nhẹ, chuẩn RFC 6455) và `Socket.IO` (có fallback polling, tự động reconnect, rooms).""",
        "code_example": """const http = require('node:http');
const { WebSocketServer } = require('ws');

const server = http.createServer();
const wss = new WebSocketServer({ server });

wss.on('connection', (ws, req) => {
  const clientIp = req.socket.remoteAddress;
  console.log(`Client mới kết nối từ: ${clientIp}`);

  // Gửi tin nhắn chào mừng
  ws.send(JSON.stringify({ type: 'WELCOME', message: 'Kết nối WebSocket thành công!' }));

  // Lắng nghe tin nhắn từ client
  ws.on('message', (data) => {
    console.log('Nhận dữ liệu:', data.toString());
    
    // Broadcast cho TẤT CẢ các client khác đang kết nối
    wss.clients.forEach(client => {
      if (client !== ws && client.readyState === ws.OPEN) {
        client.send(data);
      }
    });
  });
});

server.listen(8080, () => console.log('WebSocket Server running on ws://localhost:8080'));""",
        "tips": "Luôn triển khai cơ chế Heartbeat (Ping/Pong) định kỳ để phát hiện các kết nối 'chết' (zombie connections) do client mất sóng hoặc tắt máy mà không kịp gửi cờ TCP FIN."
    },

    55: {
        "title_vi": "Cách thiết lập một WebSocket Server hiệu năng cao trong Node.js sử dụng thư viện `ws`?",
        "level": "Mid",
        "short_answer": "Thư viện `ws` là giải pháp chuẩn công nghiệp nhanh và nhẹ nhất cho Node.js WebSocket. Ta thiết lập bằng cách gắn `WebSocketServer` vào HTTP server hiện có hoặc mở một cổng độc lập, cài đặt Ping/Pong định kỳ để dọn dẹp các kết nối ngắt đột ngột và xử lý xác thực token trong quá trình handshake.",
        "deep_dive": """1. Xác thực an toàn: Kiểm tra JWT token ngay trong sự kiện `'upgrade'` của HTTP server trước khi chấp nhận nâng cấp kết nối. Nếu token sai, từ chối ngay lập tức với mã `401 Unauthorized`.
2. Heartbeat (Giữ kết nối): Sử dụng cờ `isAlive = true` khi nhận sự kiện `'pong'`. Định kỳ mỗi 30s gọi `ws.ping()`. Nếu socket nào không trả lời pong, gọi `ws.terminate()` để giải phóng socket descriptor.""",
        "code_example": """const { WebSocketServer } = require('ws');

const wss = new WebSocketServer({ port: 8081 });

// Cài đặt cơ chế Ping/Pong phát hiện zombie socket
function heartbeat() {
  this.isAlive = true;
}

wss.on('connection', (ws) => {
  ws.isAlive = true;
  ws.on('pong', heartbeat);
});

const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (ws.isAlive === false) return ws.terminate(); // Hủy kết nối chết
    ws.isAlive = false;
    ws.ping(); // Gửi ping đến client
  });
}, 30000);

wss.on('close', () => clearInterval(interval));""",
        "tips": "Nếu hệ thống mở rộng nhiều instances sau Load Balancer, bạn phải sử dụng Redis Pub/Sub adapter để đồng bộ tin nhắn giữa các servers."
    },

    56: {
        "title_vi": "Cách triển khai (Deploy) ứng dụng Node.js lên môi trường Production chuẩn mực?",
        "level": "Senior",
        "short_answer": "Triển khai Production chuẩn mực đòi hỏi: (1) Đặt `NODE_ENV=production` để kích hoạt các tối ưu hóa của V8 và frameworks, (2) Sử dụng Process Manager (PM2) hoặc Docker + Kubernetes để tự động khởi động lại khi crash, (3) Đặt sau một Reverse Proxy (Nginx / Cloudflare) để xử lý SSL termination và static assets, (4) Áp dụng CI/CD tự động hóa kiểm thử và build, và (5) Giám sát logs và health checks.",
        "deep_dive": """1. Tác động của `NODE_ENV=production`: V8 tối ưu caching, Express tự động cache view templates, tắt chi tiết stacktrace trong error page, và hiệu năng tăng gấp 3-5 lần!
2. Graceful Shutdown: Lắng nghe tín hiệu `SIGTERM` và `SIGINT` từ OS/Kubernetes để hoàn thành nốt các requests đang chạy dở trước khi đóng server, tránh ngắt đột ngột người dùng.""",
        "code_example": """// Graceful Shutdown Pattern chuẩn mực cho Production
const server = app.listen(3000);

function handleShutdown(signal) {
  console.log(`Nhận được tín hiệu ${signal}. Đang đóng server an toàn...`);
  
  // Ngừng nhận request mới, chờ các request đang chạy hoàn tất (tối đa 10s)
  server.close(async () => {
    console.log('HTTP Server đã đóng.');
    try {
      // Đóng kết nối Database an toàn
      await databasePool.end();
      console.log('Database connection pool đã đóng.');
      process.exit(0);
    } catch (err) {
      console.error('Lỗi khi đóng database:', err);
      process.exit(1);
    }
  });

  // Ép buộc thoát nếu quá thời gian chờ (10s)
  setTimeout(() => {
    console.error('Ép buộc thoát do shutdown quá hạn!');
    process.exit(1);
  }, 10000);
}

process.on('SIGTERM', () => handleShutdown('SIGTERM'));
process.on('SIGINT', () => handleShutdown('SIGINT'));""",
        "tips": "Câu hỏi phỏng vấn thực tế: 'Điều gì xảy ra khi bạn gõ Ctrl+C hoặc khi Kubernetes giết Pod?' Hãy trả lời về cơ chế bắt tín hiệu `SIGTERM` và Graceful Shutdown."
    },

    57: {
        "title_vi": "PM2 là gì và được sử dụng như thế nào trong quản trị Node.js?",
        "level": "Mid",
        "short_answer": "PM2 là công cụ quản lý tiến trình (Production Process Manager) phổ biến nhất cho Node.js. Nó giúp giữ cho ứng dụng luôn luôn chạy (tự động hồi sinh khi bị crash), cung cấp chế độ Clustering không cần sửa code, quản lý nhật ký logs, theo dõi CPU/RAM realtime và hỗ trợ Zero-Downtime Reload.",
        "deep_dive": """1. Cluster Mode: `pm2 start app.js -i max` tự động sinh ra số lượng worker bằng số lõi CPU của máy chủ và cân bằng tải các request đến.
2. Zero-Downtime Reload: Lệnh `pm2 reload all` khởi động từng tiến trình mới trước khi tắt tiến trình cũ, giúp người dùng không bao giờ gặp lỗi gián đoạn dịch vụ khi deploy phiên bản code mới.
3. Startup Script: `pm2 startup` cấu hình hệ điều hành (systemd) tự động bật lại toàn bộ các ứng dụng Node.js khi server bị restart máy chủ vật lý.""",
        "code_example": """# File cấu hình chuẩn ecosystem.config.js
module.exports = {
  apps: [{
    name: 'ecommerce-backend',
    script: 'src/server.js',
    instances: 'max',         // Tận dụng toàn bộ CPU cores
    exec_mode: 'cluster',     // Chạy chế độ Cluster cân bằng tải
    autorestart: true,
    watch: false,
    max_memory_restart: '1G', // Tự restart nếu RAM vượt quá 1GB (chống leak)
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
};

# Các lệnh quản lý PM2 thường dùng:
# pm2 start ecosystem.config.js --env production
# pm2 reload all
# pm2 monit""",
        "tips": "Tham số `max_memory_restart: '1G'` là 'bảo hiểm' tuyệt vời cho production: nếu server có rò rỉ bộ nhớ, PM2 sẽ âm thầm restart worker đó mà không làm sập toàn bộ hệ thống."
    },

    58: {
        "title_vi": "Cách đóng gói và tối ưu hóa ứng dụng Node.js với Docker (Multi-stage Build)?",
        "level": "Senior",
        "short_answer": "Để tối ưu hóa Docker cho Node.js: (1) Sử dụng Docker Multi-stage build để tách biệt giai đoạn build (chứa devDependencies) và giai đoạn chạy production, (2) Sử dụng base image nhẹ (như `node:20-alpine`), (3) Chạy ứng dụng dưới user không có đặc quyền (`USER node`), (4) Tận dụng Docker layer caching bằng cách copy `package*.json` trước khi copy mã nguồn.",
        "deep_dive": """1. Giảm kích thước image: Multi-stage build giúp giảm dung lượng image từ ~1.2GB xuống dưới 120MB!
2. Dumb-init: Node.js không được thiết kế để chạy làm PID 1 bên trong container, dẫn đến việc không xử lý đúng các tín hiệu `SIGTERM` và zombie processes. Cần cài đặt `tini` hoặc `dumb-init` làm init process.
3. Lệnh cài đặt: Dùng `npm ci --only=production` để cài đặt nhanh chóng và chuẩn xác theo file lock.""",
        "code_example": """# Dockerfile đa tầng (Multi-stage build) tối ưu chuẩn Senior
# STAGE 1: Build & Dependencies
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build # Nếu có bước biên dịch TypeScript

# STAGE 2: Production Runtime siêu nhẹ
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Cài đặt dumb-init để xử lý signals chính xác
RUN apk add --no-cache dumb-init

COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy code đã biên dịch từ stage builder
COPY --from=builder /app/dist ./dist

# Chạy bằng user an toàn (đã có sẵn trong alpine image)
USER node
EXPOSE 3000

CMD [\"dumb-init\", \"node\", \"dist/server.js\"]""",
        "tips": "Điểm mấu chốt khi viết Dockerfile: Luôn `COPY package*.json ./` và `RUN npm ci` TRƯỚC KHI `COPY . .`. Làm như vậy Docker sẽ cache lại layer dependencies, giúp các lần build code sau chỉ mất 2 giây thay vì phải tải lại toàn bộ npm packages."
    },

    59: {
        "title_vi": "Cách quản lý phiên bản (Versioning) của một RESTful API trong Node.js?",
        "level": "Mid",
        "short_answer": "Quản lý phiên bản API nhằm đảm bảo khi cập nhật các tính năng mới hoặc thay đổi cấu trúc dữ liệu trả về, các ứng dụng mobile/frontend cũ vẫn tiếp tục hoạt động bình thường mà không bị gãy (breaking changes). Có 3 chiến lược phổ biến: (1) URI Versioning (`/api/v1/...`), (2) Header Versioning (`Accept-Version: 1.0.0`), và (3) Query Parameter (`?v=1`). Trong đó URI Versioning là phổ biến và dễ bảo trì nhất.",
        "deep_dive": """1. URI Versioning: Thân thiện với cache của CDN, dễ theo dõi trong log server.
2. Tổ chức thư mục code:
   - `src/controllers/v1/user.controller.js`
   - `src/controllers/v2/user.controller.js`
3. Chu kỳ Deprecation: Khi ra mắt v2, đánh dấu v1 là deprecated bằng cách trả về header `Deprecation: true` hoặc `Sunset: <date>`, duy trì v1 tối thiểu 6-12 tháng trước khi tắt hoàn toàn.""",
        "code_example": """const express = require('express');
const app = express();

const v1Router = express.Router();
const v2Router = express.Router();

// V1: Trả về họ tên gộp
v1Router.get('/profile', (req, res) => {
  res.json({ fullName: 'Nguyễn Văn An' });
});

// V2: Trả về họ và tên tách biệt (Breaking change với v1)
v2Router.get('/profile', (req, res) => {
  res.json({ firstName: 'An', lastName: 'Nguyễn' });
});

// Đăng ký route theo version
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

app.listen(3000);""",
        "tips": "Senior Tip: Nhắc đến RFC 8594 (Sunset HTTP Header) dùng để thông báo cho đối tác ngày giờ chính xác một API phiên bản cũ sẽ chính thức ngừng hoạt động."
    },

    60: {
        "title_vi": "Semantic Versioning (SemVer) là gì và tầm quan trọng của nó trong Node.js?",
        "level": "Junior",
        "short_answer": "Semantic Versioning (SemVer) là quy ước đặt tên phiên bản phần mềm theo chuẩn format `MAJOR.MINOR.PATCH` (Ví dụ: `2.4.1`). SemVer giúp các nhà phát triển và công cụ quản lý gói npm hiểu được mức độ thay đổi của mã nguồn và tự động nâng cấp an toàn.",
        "deep_dive": """Ý nghĩa của từng số:
1. `MAJOR` (ví dụ 1.0.0 -> 2.0.0): Tăng khi có các thay đổi làm gãy tính tương thích ngược (Breaking Changes / Incompatible API changes).
2. `MINOR` (ví dụ 2.4.0 -> 2.5.0): Tăng khi thêm tính năng mới nhưng vẫn hoàn toàn tương thích ngược (Backwards-compatible functionality).
3. `PATCH` (ví dụ 2.5.1 -> 2.5.2): Tăng khi sửa lỗi bugs và hoàn toàn tương thích ngược (Backwards-compatible bug fixes).
* Ký hiệu trong package.json:
- `^1.2.3` (Caret): Cho phép cập nhật minor và patch (< 2.0.0).
- `~1.2.3` (Tilde): Chỉ cho phép cập nhật patch (< 1.3.0).""",
        "code_example": """# Kiểm tra phiên bản package và SemVer
npm view express version        # Xem bản mới nhất trên registry
npm view express versions       # Xem lịch sử toàn bộ các versions

# Giả sử package.json có: \"lodash\": \"^4.17.20\"
# Khi chạy npm update, npm có thể nâng lên 4.17.21 (patch) hoặc 4.18.0 (minor)
# Nhưng nó TUYỆT ĐỐI KHÔNG BAO GIỜ tự nâng lên 5.0.0 (major)!""",
        "tips": "Cẩn thận với các package có phiên bản `0.y.z` (Major = 0): Theo quy ước SemVer, bất kỳ bản minor nào của 0.y.z cũng có thể chứa breaking changes!"
    },

    61: {
        "title_vi": "Sự khác biệt giữa `exports` và `module.exports` trong CommonJS?",
        "level": "Mid",
        "short_answer": "Trong CommonJS, `module.exports` là đối tượng THỰC TẾ được hàm `require()` trả về. Biến `exports` ban đầu chỉ đơn thuần là một biến tham chiếu (shortcut / alias) trỏ đến cùng vùng nhớ của `module.exports`. Nếu bạn gán lại `exports = myFunction`, bạn đã bẻ gãy mối liên kết tham chiếu đó và hàm sẽ không được xuất ra ngoài!",
        "deep_dive": """1. Cơ chế nội bộ của Node.js:
Trước khi chạy file, Node.js bọc code trong Module Wrapper:
`(function (exports, require, module, __filename, __dirname) { ... })`
Trong đó `exports = module.exports = {};`
2. Đúng: `exports.foo = 'bar'` (thêm thuộc tính vào đối tượng chung).
3. Đúng: `module.exports = class User {}` (xuất ra class hoặc function duy nhất).
4. Sai: `exports = class User {}` (không có tác dụng, require vẫn nhận về `{}`).""",
        "code_example": """// === math.js ===
// ✅ CÁCH 1: Thêm thuộc tính thông qua exports
exports.add = (a, b) => a + b;
exports.subtract = (a, b) => a - b;

// === logger.js ===
// ✅ CÁCH 2: Xuất trực tiếp 1 hàm hoặc class bằng module.exports
module.exports = function log(msg) {
  console.log(`[LOG]: ${msg}`);
};

// ❌ SAI LẦM PHỔ BIẾN:
// exports = function bad() {} // Sẽ bị require() trả về {} rỗng!""",
        "tips": "Quy tắc nằm lòng: Nếu muốn export một Function, một Class, hoặc một Giá trị đơn lẻ, LUÔN LUÔN dùng `module.exports`. Chỉ dùng `exports` khi muốn xuất một object chứa nhiều tiện ích con."
    },

    62: {
        "title_vi": "Cách tạo một máy chủ TCP socket cơ bản trong Node.js với module `net`?",
        "level": "Mid",
        "short_answer": "Module `net` là core module của Node.js dùng để xây dựng các máy chủ và máy khách chạy trên giao thức truyền dẫn TCP ở tầng Transport (Layer 4). Sử dụng `net.createServer()` để tạo TCP server, lắng nghe sự kiện `'connection'`, và thao tác trực tiếp với đối tượng `net.Socket` (một Duplex Stream).",
        "deep_dive": """1. Khác biệt với HTTP: HTTP chạy trên nền TCP (Layer 7). Module `net` cho phép giao tiếp dữ liệu nhị phân hoặc chuỗi văn bản thô theo giao thức tùy biến riêng của doanh nghiệp với độ trễ tối thiểu (như giao thức nhúng IoT, chat nhị phân, gaming socket).
2. Xử lý Socket: `socket.write()` để gửi data, `socket.on('data', chunk)` để nhận data, và `socket.end()` để đóng kết nối.""",
        "code_example": """const net = require('node:net');

const server = net.createServer((socket) => {
  console.log(`Client TCP đã kết nối: ${socket.remoteAddress}:${socket.remotePort}`);

  socket.write('Chào mừng bạn đến với TCP Raw Server của Node.js!\\r\\n');

  // Lắng nghe dữ liệu nhị phân thô
  socket.on('data', (data) => {
    console.log('Nhận từ client:', data.toString().trim());
    // Phản hồi Echo lại cho client
    socket.write(`Echo: ${data}`);
  });

  socket.on('end', () => console.log('Client đã ngắt kết nối TCP.'));
  socket.on('error', (err) => console.error('Lỗi socket:', err.message));
});

server.listen(9000, () => console.log('TCP Server listening on port 9000'));""",
        "tips": "Bạn có thể kiểm tra TCP server vừa tạo dễ dàng từ Terminal bằng lệnh `nc localhost 9000` (Netcat) hoặc `telnet localhost 9000`."
    },

    63: {
        "title_vi": "REPL trong Node.js là gì và các ứng dụng thực tế của nó?",
        "level": "Junior",
        "short_answer": "REPL là viết tắt của Read-Eval-Print Loop. Đây là môi trường dòng lệnh tương tác trực tiếp đi kèm sẵn với Node.js. Nó thực hiện chu trình: Đọc (Read) code người dùng nhập vào, Đánh giá/Thực thi (Eval) qua V8 Engine, In (Print) kết quả ra màn hình và Lặp lại (Loop) chờ lệnh kế tiếp. Có thể kích hoạt bằng cách gõ `node` trong terminal.",
        "deep_dive": """1. Các phím tắt và biến đặc biệt trong REPL:
   - `_` (dấu gạch dưới): Lưu giá trị kết quả của biểu thức gần nhất vừa được tính toán!
   - `.help`: Xem các lệnh điều khiển.
   - `.break` / `.clear`: Thoát khỏi khối lệnh đa dòng.
   - `.exit`: Thoát khỏi môi trường REPL.
2. Ứng dụng thực tế: Thử nghiệm nhanh các hàm regex, kiểm tra kết quả tính toán ngày tháng, debug module, hoặc tích hợp REPL vào server đang chạy qua TCP socket để quản trị viên thao tác trực tiếp với dữ liệu trong RAM.""",
        "code_example": """# Thao tác minh họa trong Terminal:
$ node
Welcome to Node.js v20.12.0.
> 100 * 1.5
150
> _ + 50     // Biến '_' chứa giá trị 150 ở trên
200
> const crypto = require('node:crypto');
undefined
> crypto.randomBytes(4).toString('hex');
'4a8f9c1b'
> .exit""",
        "tips": "Biến `_` trong REPL cực kỳ tiện dụng khi bạn tính toán chuỗi phép tính dài từng bước một."
    },

    64: {
        "title_vi": "Vai trò của Reverse Proxy (như Nginx) khi đứng trước ứng dụng Node.js?",
        "level": "Senior",
        "short_answer": "Mặc dù Node.js có khả năng chạy HTTP server độc lập, nhưng trong production LUÔN LUÔN nên đặt nó sau một Reverse Proxy như Nginx hoặc AWS ALB. Reverse Proxy đảm nhận các nhiệm vụ: (1) SSL/TLS Termination giải phóng gánh nặng mã hóa cho CPU Node.js, (2) Phục vụ Static Files (CSS, JS, hình ảnh) với hiệu năng C gốc siêu nhanh, (3) Cân bằng tải (Load Balancing) giữa nhiều instances Node.js, (4) Giảm tải tấn công DDoS và nén Gzip/Brotli.",
        "deep_dive": """1. Single Point of Security: Nginx chặn các request dị dạng, áp dụng rate limit ở tầng OS C trước khi request kịp chạm tới Node.js Event Loop.
2. Cấu hình Reverse Proxy trong Express: Cần bật `app.set('trust proxy', 1)` để Express lấy đúng địa chỉ IP thực tế của người dùng thông qua header `X-Forwarded-For`.""",
        "code_example": """# Cấu hình Nginx mẫu chuyển tiếp request vào Node.js (Port 3000)
server {
    listen 80;
    server_name api.myshop.com;
    return 301 https://$host$request_uri; # Bắt buộc HTTPS
}

server {
    listen 443 ssl http2;
    server_name api.myshop.com;

    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    # Phục vụ file tĩnh trực tiếp từ ổ cứng, không qua Node.js
    location /static/ {
        alias /var/www/myshop/public/;
        expires 30d;
        access_log off;
    }

    # Chuyển tiếp request API vào Node.js Server
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade; # Hỗ trợ WebSocket
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}""",
        "tips": "Đừng bao giờ để Node.js phục vụ các file ảnh/video tĩnh nặng hàng GB trên production. Hãy để Nginx hoặc AWS S3/Cloudflare CDN làm điều đó để giữ cho Event Loop của Node.js hoàn toàn rảnh rỗi xử lý business logic."
    },

    65: {
        "title_vi": "Node.js Streams nâng cao hiệu năng ứng dụng như thế nào?",
        "level": "Senior",
        "short_answer": "Streams nâng cao hiệu năng thông qua 2 yếu tố cốt tử: (1) Hiệu quả Không gian (Spatial Efficiency): Dữ liệu được xử lý theo từng khối nhỏ (chunks mặc định 16KB-64KB), giúp bộ nhớ RAM không bao giờ bị phình to theo kích thước file, và (2) Hiệu quả Thời gian (Temporal Efficiency): Bắt đầu xử lý và truyền dữ liệu cho client ngay lập tức khi chunk đầu tiên sẵn sàng mà không cần đợi tải xong toàn bộ dữ liệu.",
        "deep_dive": """1. Tiết kiệm thời gian: Client có thể xem video hoặc giải nén dữ liệu ngay khi byte đầu tiên được stream tới.
2. Backpressure Control: Khi Stream Writable bị đầy bộ đệm (highWaterMark), nó gửi tín hiệu bảo Stream Readable tạm dừng đọc (`drain` event). Cơ chế này ngăn chặn hiện tượng tràn bộ nhớ khi máy khách mạng chậm tải từ máy chủ mạng siêu tốc.
3. Chống Crash OOM: Cho phép ứng dụng xử lý file dữ liệu 50GB trên một máy chủ RAM chỉ có 512MB.""",
        "code_example": """const http = require('node:http');
const fs = require('node:fs');

http.createServer((req, res) => {
  // ❌ TỒI: Đọc hết 2GB video vào RAM rồi mới gửi
  // fs.readFile('video.mp4', (err, data) => res.end(data)); // Crash RAM ngay nếu nhiều user!

  // ✅ XUẤT SẮC: Sử dụng Stream Pipe
  // Tiêu tốn ít hơn 20MB RAM bất kể dung lượng video lớn bao nhiêu!
  const videoStream = fs.createReadStream('video.mp4');
  res.writeHead(200, { 'Content-Type': 'video/mp4' });
  videoStream.pipe(res);
}).listen(3000);""",
        "tips": "Từ khóa đắt giá nhất khi phỏng vấn về Streams: 'Backpressure' và 'Constant Memory Footprint'."
    },

    66: {
        "title_vi": "Mô tả một số Frameworks và Thư viện phổ biến nhất trong hệ sinh thái Node.js?",
        "level": "Junior",
        "short_answer": "Hệ sinh thái Node.js có các giải pháp đa dạng: (1) Express.js (Tiêu chuẩn tối giản, phổ biến nhất), (2) NestJS (Framework cấp doanh nghiệp kiến trúc hướng đối tượng, chặt chẽ, dựa trên TypeScript và Angular patterns), (3) Fastify (Tập trung tối đa vào tốc độ và JSON Schema validation), (4) Koa (Được tạo bởi tác giả Express, sử dụng async middleware hiện đại), và (5) Hapi (Thiết kế tập trung vào cấu hình bảo mật).",
        "deep_dive": """1. NestJS: Rất được ưa chuộng trong các dự án công ty lớn nhờ áp dụng Dependency Injection (DI), Modules, Controllers, Services và tích hợp sẵn TypeScript chuẩn mực.
2. Fastify: Nhanh hơn Express gấp 2-3 lần nhờ bộ sinh schema JSON siêu tối ưu (`fast-json-stringify`) và routing dựa trên radix-tree.
3. Next.js / Nuxt: Full-stack meta-frameworks chạy trên Node.js để render SSR cho React và Vue.""",
        "code_example": """// So sánh nhanh triết lý định tuyến:
// Express: app.get('/users', (req, res) => res.json([]));
// Fastify: fastify.get('/users', async (request, reply) => []);
// NestJS: 
// @Controller('users')
// export class UsersController {
//   @Get()
//   findAll(): User[] { return this.usersService.findAll(); }
// }""",
        "tips": "Nếu dự án mới bắt đầu và cần hiệu năng JSON API cao nhất, hãy mạnh dạn đề xuất Fastify. Nếu dự án có nhiều lập trình viên cùng làm việc với kiến trúc doanh nghiệp lớn, đề xuất NestJS."
    },

    67: {
        "title_vi": "Koa.js khác biệt như thế nào so với Express.js?",
        "level": "Mid",
        "short_answer": "Koa.js được phát triển bởi chính đội ngũ tạo ra Express, nhằm mục đích trở thành phiên bản nhỏ hơn, biểu cảm hơn và hiện đại hơn. Điểm khác biệt lớn nhất là mô hình Middleware 'Hành tây' (Onion Model) dựa trên Promise và Async/Await, cùng với việc loại bỏ hoàn toàn routing và view engine ra khỏi core để đạt được sự tối giản tuyệt đối.",
        "deep_dive": """1. Onion Model: Trong Koa, khi gọi `await next()`, luồng thực thi đi sâu vào bên trong middleware tiếp theo, sau đó quay ngược trở lại các dòng code nằm sau `await next()` theo chiều ngược lại (y như bóc từng lớp vỏ hành tây).
2. Xử lý lỗi sạch sẽ: Nhờ cơ chế Promise xuyên suốt, toàn bộ lỗi bất đồng bộ ở các tầng sâu đều có thể được bắt gọn bằng một khối `try/catch` duy nhất ở middleware ngoài cùng.
3. Không kèm router: Bạn phải cài thêm `@koa/router` nếu muốn dùng routing.""",
        "code_example": """const Koa = require('koa');
const app = new Koa();

// Middleware 1: Đo thời gian phản hồi (Onion Model)
app.use(async (ctx, next) => {
  const start = Date.now();
  console.log('1. Bắt đầu Middleware 1 (Đi vào)');
  
  await next(); // Chuyển sang middleware tiếp theo và CHỜ NÓ XONG
  
  const ms = Date.now() - start;
  console.log(`4. Kết thúc Middleware 1 (Đi ra) - Xử lý hết: ${ms}ms`);
  ctx.set('X-Response-Time', `${ms}ms`);
});

// Middleware 2: Trả kết quả
app.use(async (ctx, next) => {
  console.log('2. Đang ở Middleware 2');
  ctx.body = { message: 'Xin chào từ Koa Onion Architecture!' };
  console.log('3. Xử lý xong Middleware 2');
});

app.listen(3000);""",
        "tips": "Vẽ hình 'Củ hành tây' (Onion Architecture) và giải thích cách `await next()` cho phép can thiệp cả trước (Downstream) và sau (Upstream) khi response được sinh ra."
    },

    68: {
        "title_vi": "NestJS là gì và khi nào nên lựa chọn NestJS cho dự án Node.js?",
        "level": "Senior",
        "short_answer": "NestJS là framework Node.js tiến bộ được xây dựng trên TypeScript, kết hợp nhuần nhuyễn giữa Lập trình hướng đối tượng (OOP), Lập trình hàm (FP) và Lập trình phản ứng chức năng (FRP). Dưới nền tảng, NestJS mặc định sử dụng Express (hoặc có thể chuyển sang Fastify). Nên chọn NestJS khi xây dựng các ứng dụng doanh nghiệp quy mô lớn, cần cấu trúc dự án nghiêm ngặt, dễ kiểm thử và có nhiều nhân sự cùng phát triển.",
        "deep_dive": """1. Tính năng nổi bật:
   - Dependency Injection (Inversion of Control - IoC) container mạnh mẽ.
   - Kiến trúc phân tầng rõ rệt: Modules, Controllers (định tuyến/HTTP), Providers/Services (Business logic).
   - Pipes (Validate dữ liệu với class-validator), Guards (Xác thực phân quyền JWT/RBAC), Interceptors (Biến đổi response).
2. Khi nào KHÔNG NÊN dùng: Dự án serverless micro-function siêu nhỏ hoặc script đơn giản, vì NestJS có độ phức tạp ban đầu cao và thời gian khởi động lâu hơn Express thuần.""",
        "code_example": """// user.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class UserService {
  getProfile(id: string) {
    return { id, name: 'Alice', role: 'Engineer' };
  }
}

// user.controller.ts
import { Controller, Get, Param } from '@nestjs/common';
import { UserService } from './user.service';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {} // Dependency Injection

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.userService.getProfile(id);
  }
}""",
        "tips": "Nếu bạn từng có kinh nghiệm làm Spring Boot (Java) hoặc Angular, NestJS sẽ cho cảm giác quen thuộc 100% nhờ việc áp dụng chung các mẫu thiết kế Decorators và Dependency Injection."
    },

    69: {
        "title_vi": "Lợi ích của việc sử dụng TypeScript kết hợp với Node.js trong môi trường doanh nghiệp?",
        "level": "Mid",
        "short_answer": "TypeScript mang lại hệ thống Static Typing (Kiểm tra kiểu dữ liệu tĩnh) ngay trong thời gian viết code (compile-time), giúp loại bỏ hơn 40% các lỗi thường gặp trong JavaScript (như `Cannot read properties of undefined`). Nó cung cấp khả năng tự động gợi ý code (IntelliSense) tuyệt vời, tái cấu trúc (refactoring) mã nguồn an toàn và đóng vai trò như một bản tài liệu sống (living documentation) cho hệ thống backend lớn.",
        "deep_dive": """1. Type Safety giữa Backend & Frontend: Cho phép chia sẻ chung các Interfaces/DTOs giữa React/Vue frontend và Node.js backend.
2. Công cụ thực thi hiện đại:
   - `tsx` hoặc `ts-node` cho môi trường dev.
   - `esbuild`, `swc`, `tsc` cho quá trình build production siêu tốc.
   - Node.js v22.6+ đã bắt đầu hỗ trợ cờ thực thi trực tiếp TypeScript không cần biên dịch trước (`node --experimental-strip-types`).""",
        "code_example": """// DTO (Data Transfer Object) với TypeScript Interface
interface CreateUserDto {
  email: string;
  age: number;
  role: 'admin' | 'user';
}

function registerUser(dto: CreateUserDto): { success: boolean; id: string } {
  // Trình biên dịch sẽ báo lỗi đỏ NGAY LẬP TỨC nếu truyền thiếu age hoặc role sai
  console.log(`Tạo người dùng: ${dto.email} với quyền ${dto.role}`);
  return { success: true, id: 'u_101' };
}

registerUser({ email: 'john@work.com', age: 28, role: 'admin' });""",
        "tips": "Nhớ nhấn mạnh: 'TypeScript chỉ kiểm tra kiểu dữ liệu ở COMPILE-TIME. Khi chạy trên Production nó đã bị biên dịch thành JavaScript thuần. Vì vậy để xác thực an toàn dữ liệu từ người dùng gửi lên ở RUNTIME, ta vẫn bắt buộc phải dùng các thư viện như Zod hoặc Joi.'"
    },

    70: {
        "title_vi": "Cách tích hợp ứng dụng Node.js với Third-Party API an toàn và có khả năng chịu lỗi?",
        "level": "Senior",
        "short_answer": "Tích hợp API bên thứ ba an toàn đòi hỏi: (1) Đặt Timeout cho mọi request (tránh treo socket vĩnh viễn), (2) Triển khai cơ chế Retry với Exponential Backoff khi gặp lỗi mạng tạm thời, (3) Áp dụng Circuit Breaker Pattern để ngắt kết nối tự động khi dịch vụ đối tác sập, (4) Lưu trữ API Keys an toàn trong biến môi trường, và (5) Sử dụng HTTP client hiện đại như Native `fetch` hoặc `axios` có cấu hình connection pooling.",
        "deep_dive": """1. Timeout: Không bao giờ gửi request mà không có timeout! Mặc định nhiều thư viện không có timeout, nếu bên thứ ba bị lag, hàng ngàn requests của bạn sẽ bị nghẽn dẫn đến cạn kiệt tài nguyên server.
2. Circuit Breaker: Thư viện `opossum` giúp theo dõi tỉ lệ lỗi. Nếu bên thứ ba fail quá 50%, circuit mở (Open), các request sau sẽ trả lỗi ngay lập tức hoặc dùng fallback cache mà không cần tốn thời gian gọi sang bên thứ ba nữa.""",
        "code_example": """// Sử dụng Native Fetch với AbortController để đặt Timeout chặt chẽ
async function callPartnerApiWithTimeout(endpoint, timeoutMs = 3000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(endpoint, {
      signal: controller.signal,
      headers: {
        'Authorization': `Bearer ${process.env.PARTNER_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Partner API HTTP Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error(`Request bị hủy do quá thời gian chờ ${timeoutMs}ms`);
    }
    throw error;
  } finally {
    clearTimeout(timeoutId); // Dọn dẹp timer
  }
}""",
        "tips": "Từ khóa bắt buộc phải có khi phỏng vấn Senior: 'Idempotency Key' (khóa lũy thoái) khi gọi các API thanh toán bên thứ ba để đảm bảo dù có retry nhiều lần thì khách hàng cũng chỉ bị trừ tiền đúng 1 lần."
    },

    71: {
        "title_vi": "Socket.IO là gì và nó khác biệt gì so với chuẩn WebSocket thuần túy?",
        "level": "Mid",
        "short_answer": "Socket.IO KHÔNG PHẢI là một triển khai WebSocket đơn thuần. Nó là một thư viện thời gian thực (Real-time) xây dựng trên nền tảng WebSocket, cung cấp thêm các tính năng dự phòng thông minh (Fallback mechanism như HTTP Long-Polling nếu mạng chặn WebSocket), tự động kết nối lại khi mất mạng (Auto-reconnection), hỗ trợ Rooms & Namespaces, và gửi tin nhắn dạng sự kiện tùy biến.",
        "deep_dive": """1. Khả năng tương thích: Socket.IO client không thể kết nối trực tiếp vào một server WebSocket thuần (`ws`), và ngược lại. Cả 2 đầu bắt buộc phải dùng thư viện Socket.IO.
2. Rooms & Namespaces: Cho phép chia nhỏ luồng dữ liệu (ví dụ: `io.to('room_vietnam').emit('goal')`) rất dễ dàng mà không cần phải tự lập trình quản lý danh sách mảng sockets thủ công.
3. Scaling: Khi chạy nhiều server, Socket.IO sử dụng `@socket.io/redis-adapter` để đồng bộ phát sóng tin nhắn giữa các cụm server.""",
        "code_example": """const { Server } = require('socket.io');
const io = new Server(3000, {
  cors: { origin: '*' }
});

io.on('connection', (socket) => {
  console.log('Client kết nối:', socket.id);

  // Tham gia vào một phòng cụ thể
  socket.on('join_room', (roomId) => {
    socket.join(roomId);
    console.log(`Socket ${socket.id} đã vào phòng ${roomId}`);
  });

  // Gửi tin nhắn đến một phòng riêng biệt
  socket.on('send_message', ({ roomId, message }) => {
    io.to(roomId).emit('new_message', { sender: socket.id, message });
  });
});""",
        "tips": "Nếu ứng dụng của bạn cần tính năng chat, thông báo realtime trên nhiều thiết bị mạng chập chờn, Socket.IO là lựa chọn tuyệt vời. Nhưng nếu cần streaming dữ liệu microsecond tần suất cực cao (như sàn giao dịch tiền điện tử), WebSocket thuần (`ws` hoặc `uWebSockets.js`) sẽ nhanh và ít overhead hơn."
    },

    72: {
        "title_vi": "Cách sử dụng GraphQL trong Node.js và so sánh ưu thế với REST?",
        "level": "Mid",
        "short_answer": "GraphQL là một ngôn ngữ truy vấn cho API do Facebook phát triển. Trong Node.js, GraphQL được triển khai phổ biến qua Apollo Server, Yoga hoặc GraphQL.js. Ưu thế lớn nhất của GraphQL là client có thể yêu cầu chính xác những trường dữ liệu mình cần (Declarative Data Fetching), giải quyết triệt để 2 vấn nạn kinh điển của REST: Over-fetching (nhận thừa dữ liệu) và Under-fetching (phải gọi nhiều endpoint liên tiếp để gom đủ thông tin).",
        "deep_dive": """1. Schema Definition Language (SDL): Định nghĩa rõ ràng Types, Queries (đọc) và Mutations (ghi).
2. Resolvers: Các hàm phụ trách tìm nạp dữ liệu cho từng trường cụ thể.
3. Vấn đề N+1 Query: Điểm yếu chí tử của GraphQL nếu không cẩn thận. Giải quyết bắt buộc bằng cách dùng thư viện `DataLoader` của Facebook để gom nhóm (batching) và ghi nhớ (caching) các câu truy vấn cơ sở dữ liệu.""",
        "code_example": """const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');

// 1. Định nghĩa TypeDefs
const typeDefs = `#graphql
  type Book {
    id: ID!
    title: String!
    author: String!
  }

  type Query {
    books: [Book]
  }
`;

// 2. Định nghĩa Resolvers
const resolvers = {
  Query: {
    books: () => [
      { id: '1', title: 'Clean Architecture', author: 'Robert C. Martin' }
    ]
  }
};

const server = new ApolloServer({ typeDefs, resolvers });
startStandaloneServer(server, { listen: { port: 4000 } })
  .then(({ url }) => console.log(`GraphQL Server sẵn sàng tại: ${url}`));""",
        "tips": "Câu hỏi bẫy Senior: 'Làm thế nào để xử lý N+1 Problem trong GraphQL?' Trả lời ngay: Dùng `DataLoader` để batch các IDs và query DB 1 lần duy nhất bằng `WHERE id IN (...)`."
    },

    73: {
        "title_vi": "Node.js tương tác và phục vụ các Frontend Frameworks (React, Vue, Angular) như thế nào?",
        "level": "Junior",
        "short_answer": "Node.js tương tác với frontend frameworks theo 2 vai trò chính: (1) Môi trường phát triển & Build Tool (chạy Vite, Webpack để bundle mã nguồn JS/CSS), và (2) Runtime Server đóng vai trò REST/GraphQL Backend API cung cấp dữ liệu JSON, hoặc làm Server-Side Rendering (SSR) / BFF (Backend-for-Frontend) server.",
        "deep_dive": """1. Tách biệt hoàn toàn (Decoupled SPA): Frontend build thành các file tĩnh HTML/JS/CSS và deploy lên CDN/S3. Node.js chạy độc lập trên server chỉ phục vụ API endpoints. Giao tiếp qua HTTP/HTTPS với CORS được cấu hình chuẩn.
2. Tích hợp monorepo: Sử dụng công cụ Turborepo hoặc Nx để quản lý cả frontend và backend Node.js trong cùng một kho lưu trữ Git, chia sẻ chung các TypeScript types.""",
        "code_example": """// Cấu hình CORS để cho phép ứng dụng React/Vue (chạy localhost:5173) gọi API
const express = require('express');
const cors = require('cors');
const app = express();

const corsOptions = {
  origin: ['http://localhost:5173', 'https://my-production-app.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true // Cho phép gửi cookies qua domain khác
};

app.use(cors(corsOptions));

app.get('/api/data', (req, res) => {
  res.json({ message: 'Dữ liệu an toàn cho Frontend' });
});""",
        "tips": "Luôn tránh dùng `cors({ origin: '*' })` khi ứng dụng có sử dụng cookie hoặc token xác thực phiên làm việc."
    },

    74: {
        "title_vi": "Server-Side Rendering (SSR) là gì và làm thế nào để thực hiện với Node.js?",
        "level": "Senior",
        "short_answer": "Server-Side Rendering (SSR) là quá trình render mã nguồn của các components UI (React, Vue) thành chuỗi HTML hoàn chỉnh trực tiếp trên server Node.js trước khi gửi về cho trình duyệt. Lợi ích vượt trội là tối ưu hóa điểm SEO (Search Engine Optimization), cho phép máy tìm kiếm Google cào nội dung dễ dàng, và giảm đáng kể thời gian hiển thị nội dung đầu tiên (First Contentful Paint - FCP).",
        "deep_dive": """1. Hydration: Khi chuỗi HTML được tải về trình duyệt, JavaScript client sẽ tải sau và 'hồi sinh' (hydrate) các event listeners để trang web tương tác được bình thường.
2. Đánh đổi (Trade-offs): SSR làm tăng tải CPU của server Node.js rất nhiều vì phải render cây DOM ảo liên tục. Cần kết hợp các kỹ thuật Caching (HTML Caching trên CDN hoặc Redis).
3. Frameworks hiện đại: Thay vì tự viết `ReactDOMServer.renderToString()`, ngày nay người ta luôn dùng Next.js (cho React) hoặc Nuxt.js (cho Vue).""",
        "code_example": """// Nguyên lý cốt lõi SSR trong Node.js với React
const express = require('express');
const React = require('react');
const ReactDOMServer = require('react-dom/server');

const app = express();

function MyComponent({ title }) {
  return React.createElement('h1', null, `Xin chào SSR: ${title}`);
}

app.get('/', (req, res) => {
  // Render component thành chuỗi HTML trực tiếp trên Node server
  const htmlContent = ReactDOMServer.renderToString(
    React.createElement(MyComponent, { title: 'Node.js Senior' })
  );

  res.send(`
    <!DOCTYPE html>
    <html>
      <head><title>Trang SSR</title></head>
      <body>
        <div id=\"root\">${htmlContent}</div>
      </body>
    </html>
  `);
});""",
        "tips": "Phân biệt rõ: SSR (render tại thời điểm request trên Node.js), SSG (Static Site Generation - render trước toàn bộ trang lúc build), và CSR (Client-Side Rendering - chỉ tải file JS rỗng rồi browser tự render)."
    },

    75: {
        "title_vi": "Các quy ước viết mã (Coding Conventions) và Best Practices hàng đầu trong Node.js?",
        "level": "Junior",
        "short_answer": "Các quy ước chuẩn mực bao gồm: (1) Tuân thủ quy chuẩn đặt tên (camelCase cho hàm/biến, PascalCase cho Class/Types, UPPER_SNAKE_CASE cho hằng số), (2) Sử dụng `const` làm mặc định, chỉ dùng `let` khi cần gán lại, tuyệt đối cấm `var`, (3) Luôn dùng hàm bất đồng bộ (`async/await`) thay vì các hàm `*Sync`, (4) Cấu trúc thư mục theo tính năng hoặc mô hình 3 lớp (Controllers, Services, Repositories), và (5) Tự động định dạng bằng Prettier và ESLint.",
        "deep_dive": """1. Tránh Magic Numbers / Strings: Luôn định nghĩa các hằng số rõ ràng.
2. Clean Error Handling: Kế thừa class `Error` chuẩn, không bao giờ `throw \"chuỗi ký tự\"`.
3. Không làm nghẽn Event Loop: Hạn chế các hàm JSON.parse khổng lồ hoặc biểu thức Regular Expression phức tạp (ReDoS attacks).""",
        "code_example": """// Cấu trúc dự án 3 lớp chuẩn mực (Layered Architecture):
// src/
// ├── controllers/    # Tiếp nhận request, gọi service, trả response HTTP
// ├── services/       # Chứa 100% Business Logic nghiệp vụ
// ├── repositories/   # Thao tác trực tiếp với Database (ORM/SQL)
// ├── middlewares/    # Auth, Validation, Rate Limit, Error
// ├── config/         # Cấu hình biến môi trường
// └── app.js          # Khởi tạo Express app""",
        "tips": "Nhắc đến nguyên tắc SOLID và Clean Code khi tổ chức các file service trong Node.js."
    },

    76: {
        "title_vi": "Cách đảm bảo ứng dụng Node.js tuân thủ các nguyên tắc The Twelve-Factor App?",
        "level": "Senior",
        "short_answer": "Twelve-Factor App là bộ quy chuẩn kinh điển để xây dựng các ứng dụng Cloud-Native hiện đại có khả năng mở rộng cao: (1) Quản lý mã nguồn trên 1 codebase Git duy nhất, (2) Khai báo phụ thuộc tường minh qua package.json, (3) Cấu hình tách biệt hoàn toàn qua Biến môi trường (`process.env`), (4) Coi Database và Cache là Backing Services có thể đính kèm linh hoạt, (5) Tách biệt nghiêm ngặt Build, Release và Run, (6) Thực thi ứng dụng dưới dạng Stateless Processes (không lưu trạng thái trong RAM), và (7) Graceful Shutdown qua tín hiệu SIGTERM.",
        "deep_dive": """Yếu tố then chốt số 6 (Stateless): Không bao giờ lưu file upload của người dùng vào ổ cứng cục bộ của server Node.js, vì khi ứng dụng scale lên 10 instances trên các máy khác nhau, user kết nối vào máy 2 sẽ không thấy ảnh lưu trên máy 1. Phải đẩy file sang AWS S3 / Cloud Storage và lưu session trong Redis!""",
        "code_example": """// Tuân thủ Factor III (Config): Đọc cấu hình từ môi trường, không hardcode
const dbConfig = {
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT, 10),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
};

// Tuân thủ Factor VI (Stateless): Đẩy trạng thái ra ngoài Redis
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');

const redisClient = createClient({ url: process.env.REDIS_URL });
// Toàn bộ session được chia sẻ qua Redis, server Node hoàn toàn Stateless!""",
        "tips": "Khi được hỏi 'Làm thế nào để ứng dụng Node.js sẵn sàng scale trên Kubernetes?', hãy trả lời ngay: 'Bằng cách tuân thủ triệt để 12-Factor App, đặc biệt là tính Stateless và Graceful Shutdown.'"
    },

    77: {
        "title_vi": "Code Linting là gì và cách áp dụng ESLint & Prettier trong dự án Node.js?",
        "level": "Junior",
        "short_answer": "Linting là quá trình phân tích tĩnh mã nguồn để phát hiện sớm các lỗi lập trình tiềm ẩn, biến không sử dụng, vi phạm chuẩn bảo mật và bắt buộc phong cách code nhất quán trong toàn team. Trong Node.js, `ESLint` đảm nhận việc kiểm tra logic mã và bắt lỗi, trong khi `Prettier` phụ trách việc tự động định dạng thẩm mỹ (dấu chấm phẩy, khoảng trắng, xuống dòng).",
        "deep_dive": """1. Thiết lập Git Hooks với Husky & lint-staged: Tự động chạy ESLint kiểm tra code trước khi cho phép lập trình viên gõ lệnh `git commit`. Nếu code có lỗi, commit bị chặn ngay lập tức.
2. Plugin bảo mật: Cài thêm `eslint-plugin-security` để tự động phát hiện các lỗ hổng như Regex DoS, unsafe regex, hoặc child_process command injection.""",
        "code_example": """# Cài đặt bộ công cụ chuẩn
npm install -D eslint prettier eslint-config-prettier

# Cấu hình mẫu trong package.json
{
  \"scripts\": {
    \"lint\": \"eslint src/**/*.js\",
    \"lint:fix\": \"eslint src/**/*.js --fix\",
    \"format\": \"prettier --write 'src/**/*.{js,json,md}'\"
  }
}""",
        "tips": "Phân biệt rõ: ESLint giải quyết bài toán CHẤT LƯỢNG CODE (Code Quality - ví dụ cấm dùng biến chưa khai báo), còn Prettier giải quyết bài toán ĐỊNH DẠNG (Formatting - ví dụ tab 2 space hay 4 space)."
    },

    78: {
        "title_vi": "Các chiến lược mở rộng (Scaling) ứng dụng Node.js từ góc nhìn Senior Architect?",
        "level": "Senior",
        "short_answer": "Mở rộng Node.js áp dụng 3 trục theo Scale Cube: (1) Mở rộng theo chiều dọc (Vertical Scaling - Tăng RAM/CPU máy chủ và dùng Cluster/Worker Threads), (2) Mở rộng theo chiều ngang (Horizontal Scaling - Tăng số lượng instances/containers phía sau Load Balancer), và (3) Mở rộng theo phân rã chức năng (Functional Decomposition - Chuyển đổi từ Monolith sang Microservices hoặc chia nhỏ theo dữ liệu sharding).",
        "deep_dive": """1. Vượt qua giới hạn đơn luồng:
   - Tầng Server: Dùng Node.js Cluster hoặc chạy nhiều container Docker trên Kubernetes.
   - Tầng Network: Dùng Nginx hoặc AWS ALB để cân bằng tải (Round-robin, Least connections).
   - Tầng Data: Tách Read/Write Replicas cho Database, đặt Redis Cache ở phía trước để gánh 80% truy vấn đọc.
   - Tầng Background: Đẩy các tác vụ nặng vào Message Queue (RabbitMQ / BullMQ) để xử lý bất đồng bộ.""",
        "code_example": """// Kiến trúc xử lý tác vụ nặng không làm nghẽn luồng chính:
// Thay vì xử lý xuất file Excel 500k dòng trực tiếp trong HTTP request...
app.post('/api/export-reports', async (req, res) => {
  // 1. Đẩy tác vụ vào Queue (BullMQ / Redis)
  await reportQueue.add('generateReport', { userId: req.user.id });
  
  // 2. Trả về ngay lập tức cho người dùng mã 202 Accepted!
  res.status(202).json({
    status: 'Đã tiếp nhận yêu cầu. Hệ thống đang tạo file báo cáo trong background!'
  });
});""",
        "tips": "Nguyên lý sống còn: 'Không bao giờ để công việc tính toán nặng chiếm dụng Event Loop của Web API server. Luôn đẩy sang Worker Queue riêng biệt.'"
    },

    79: {
        "title_vi": "Cách quản lý Session trong một hệ thống Node.js được mở rộng nhiều máy chủ (Distributed Scaling)?",
        "level": "Senior",
        "short_answer": "Trong hệ thống chạy nhiều cụm server Node.js đằng sau Load Balancer, bộ nhớ RAM là cục bộ cho từng máy. Không bao giờ được dùng cơ chế lưu session mặc định trong memory (`MemoryStore`). Hai giải pháp chuẩn mực là: (1) Chuyển hoàn toàn sang kiến trúc Stateless sử dụng JSON Web Tokens (JWT), hoặc (2) Lưu trữ phiên làm việc tập trung (Centralized Session Store) trên cụm cơ sở dữ liệu in-memory tốc độ cao như Redis.",
        "deep_dive": """1. Nhược điểm của Sticky Sessions (Session Affinity): Buộc người dùng luôn kết nối vào đúng 1 server nhất định. Khi server đó chết hoặc restart, toàn bộ phiên của người dùng trên server đó bị mất, và khả năng cân bằng tải bị lệch lạc.
2. Lợi thế của Redis Store: Bất kỳ server Node nào tiếp nhận request cũng có thể đọc và ghi session từ Redis trong thời gian < 1ms. Khi người dùng đăng xuất, server chỉ cần xóa key trong Redis là lập tức thu hồi phiên trên toàn thế giới.""",
        "code_example": """const session = require('express-session');
const { RedisStore } = require('connect-redis');
const { createClient } = require('redis');

// 1. Kết nối Redis tập trung
const redisClient = createClient({ url: process.env.REDIS_URL });
redisClient.connect().catch(console.error);

// 2. Cấu hình express-session sử dụng RedisStore
app.use(
  session({
    store: new RedisStore({ client: redisClient, prefix: 'sess:' }),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,      // Bắt buộc HTTPS
      httpOnly: true,    // Chống XSS
      maxAge: 1000 * 60 * 60 * 24 // 1 ngày
    }
  })
);""",
        "tips": "Nếu chọn giải pháp JWT, hãy luôn lưu ý vấn đề thu hồi token (Token Revocation). Để có thể logout JWT ngay lập tức, bạn vẫn cần dùng một Redis Blacklist lưu trữ các token bị hủy trước khi hết hạn."
    },

    80: {
        "title_vi": "Kiến trúc Microservices ảnh hưởng như thế nào đến khả năng mở rộng của ứng dụng Node.js?",
        "level": "Senior",
        "short_answer": "Microservices cho phép ứng dụng Node.js mở rộng độc lập từng phần chức năng cụ thể (Granular Scalability) thay vì phải scale toàn bộ cục Monolith cồng kềnh. Ví dụ: Dịch vụ tìm kiếm hoặc thanh toán có lượng truy cập cao có thể được scale lên 20 pods, trong khi dịch vụ quản lý thông tin tài khoản chỉ cần 2 pods. Node.js với kích thước container nhẹ và khởi động nhanh là nền tảng lý tưởng cho mô hình này.",
        "deep_dive": """1. Lợi ích:
   - Isolation (Cô lập lỗi): Lỗi ở dịch vụ gửi mail không thể làm sập dịch vụ thanh toán.
   - Đa dạng công nghệ: Có thể dùng Node.js cho các I/O services tốc độ cao, và dùng Python cho dịch vụ AI/ML.
2. Thách thức lớn:
   - Network Latency giữa các dịch vụ.
   - Data Consistency: Không còn tính toàn vẹn ACID của một database duy nhất -> Phải dùng Eventual Consistency (Tính nhất quán cuối cùng) và Event-Driven Architecture (Kafka/RabbitMQ).""",
        "code_example": """// Minh họa giao tiếp bất đồng bộ giữa các Microservices qua Sự kiện
// Order Service phát ra sự kiện 'order_created'
// Không cần gọi HTTP trực tiếp sang Payment và Inventory (loại bỏ ghép nối chặt chẽ)
messageBroker.publish('order_events', {
  event: 'ORDER_CREATED',
  data: { orderId: 789, total: 1000 }
});""",
        "tips": "Senior Tip: Hãy nhắc đến Fallacies of Distributed Computing (Những lầm tưởng về điện toán phân tán): 'Mạng không bao giờ đáng tin cậy 100%, độ trễ không bao giờ bằng 0'. Do đó luôn cần Circuit Breaker và Idempotency."
    },

    81: {
        "title_vi": "Hàng đợi thông điệp (Message Queues) là gì và tại sao chúng thiết yếu trong Node.js?",
        "level": "Senior",
        "short_answer": "Message Queue là hạ tầng trung gian lưu trữ các thông điệp bất đồng bộ giữa các thành phần sản xuất (Producers) và các thành phần tiêu thụ (Consumers). Message Queues thiết yếu trong Node.js để: (1) San phẳng các đợt tăng đột biến lưu lượng (Traffic Spikes / Load Leveling), (2) Tách rời các hệ thống (Decoupling), và (3) Xử lý các tác vụ tốn CPU hoặc I/O nặng ngầm ở background mà không làm block Event Loop chính.",
        "deep_dive": """1. Các công nghệ Message Queue thông dụng:
   - Redis-based (BullMQ, Bee-Queue): Siêu nhanh, dễ cài đặt, hoàn hảo cho hầu hết dự án Node.js.
   - RabbitMQ: Hỗ trợ định tuyến phức tạp (Direct, Topic, Fanout exchanges), cam kết tin cậy cao.
   - Apache Kafka: Thông lượng hàng triệu events/giây, lưu trữ event log bền vững.
2. Các tính năng then chốt: Tự động retry khi thất bại, Delayed jobs (hẹn giờ chạy), Dead Letter Queue (DLQ - gom các tin nhắn lỗi nhiều lần để lập trình viên điều tra).""",
        "code_example": """const { Queue, Worker } = require('bullmq');

// 1. Tạo hàng đợi email với kết nối Redis
const emailQueue = new Queue('email_queue', { connection: { host: 'localhost', port: 6379 } });

// 2. Producer: Thêm task vào hàng đợi (mất 2ms, không làm lag web server)
async function queueWelcomeEmail(userEmail) {
  await emailQueue.add('sendWelcome', { to: userEmail }, { attempts: 3, backoff: { type: 'exponential', delay: 1000 } });
}

// 3. Consumer / Worker: Chạy trên tiến trình riêng độc lập
const worker = new Worker('email_queue', async (job) => {
  console.log(`Đang gửi mail cho: ${job.data.to}...`);
  // Gọi SMTP gửi mail thật...
}, { connection: { host: 'localhost', port: 6379 } });""",
        "tips": "Luôn luôn cấu hình Dead Letter Queue (DLQ). Nếu một job thất bại quá 5 lần, nó phải được chuyển vào DLQ để không làm tắc nghẽn các jobs khác và gửi thông báo khẩn qua Slack/Telegram cho đội ngũ dev."
    },

    82: {
        "title_vi": "Cách triển khai RabbitMQ trong Node.js sử dụng thư viện `amqplib`?",
        "level": "Mid",
        "short_answer": "Sử dụng thư viện `amqplib` (hỗ trợ Promise/async-await). Quy trình triển khai bao gồm: (1) Kết nối đến RabbitMQ server (`amqp.connect`), (2) Tạo kênh giao tiếp (`createChannel`), (3) Khai báo hàng đợi (`assertQueue` với cờ `durable: true`), (4) Gửi tin nhắn bằng `sendToQueue`, và (5) Phía consumer sử dụng `channel.consume()` và BẮT BUỘC gọi `channel.ack()` để xác nhận hoàn thành.",
        "deep_dive": """1. Cơ chế Acknowledgment (`ack` vs `nack`): Nếu worker bị crash giữa chừng trước khi gửi `ack`, RabbitMQ sẽ giữ lại tin nhắn và tự động gửi lại cho worker khác (đảm bảo không mất dữ liệu).
2. Prefetch Count (`channel.prefetch(1)`): Cực kỳ quan trọng! Giới hạn mỗi worker chỉ nhận đúng 1 tin nhắn tại một thời điểm, làm xong mới nhận tiếp, giúp cân bằng tải đều giữa các workers (Fair Dispatch) thay vì chia đều mù quáng (Round-robin).""",
        "code_example": """const amqp = require('amqplib');

async function startRabbitMQWorker() {
  const conn = await amqp.connect('amqp://localhost');
  const channel = await conn.createChannel();
  const queue = 'order_processing';

  await channel.assertQueue(queue, { durable: true });
  
  // Chỉ nhận 1 job tại 1 thời điểm
  channel.prefetch(1);

  console.log('Worker đang chờ nhận đơn hàng từ RabbitMQ...');

  channel.consume(queue, async (msg) => {
    if (msg !== null) {
      const order = JSON.parse(msg.content.toString());
      console.log('Đang xử lý đơn hàng:', order.id);

      try {
        // Thực hiện logic xử lý...
        channel.ack(msg); // ✅ Báo cáo RabbitMQ: Đã hoàn tất, có thể xóa job!
      } catch (err) {
        // Gặp lỗi: requeue lại hoặc gửi vào Dead Letter Exchange
        channel.nack(msg, false, false);
      }
    }
  });
}

startRabbitMQWorker();""",
        "tips": "Nếu quên gọi `channel.ack(msg)`, RabbitMQ sẽ giữ toàn bộ tin nhắn trong trạng thái 'Unacknowledged', làm cạn kiệt RAM của RabbitMQ server."
    },

    83: {
        "title_vi": "Ý nghĩa và trường hợp sử dụng của ZeroMQ (ØMQ) trong Node.js?",
        "level": "Senior",
        "short_answer": "ZeroMQ là một thư viện mạng tin nhắn hiệu năng cực cao chạy trực tiếp dưới dạng Socket mở rộng mà KHÔNG CẦN một Message Broker trung gian chuyên dụng (Brokerless Messaging Library). Nó cho phép các tiến trình kết nối trực tiếp với nhau theo các mẫu truyền tin như In-proc, IPC, TCP, PUB/SUB, PUSH/PULL với độ trễ tính bằng microsecond và thông lượng khổng lồ.",
        "deep_dive": """1. Brokerless Architecture: Khác với RabbitMQ cần một server trung gian điều phối, ZeroMQ cho phép các tiến trình Node.js bắn message trực tiếp thẳng vào nhau qua socket.
2. Trường hợp sử dụng: Giao dịch tài chính cao tần (High-Frequency Trading), viễn thông, mạng nội bộ phân tán giữa các cụm node cần độ trễ thấp nhất có thể.
3. Thư viện: Dùng package `zeromq` (viết bằng C++ bindings).""",
        "code_example": """// Ví dụ Producer (Push Socket) với zeromq v6+
const zmq = require('zeromq');

async function runProducer() {
  const sock = new zmq.Push();
  await sock.bind('tcp://127.0.0.1:5555');
  console.log('Producer đã bind vào port 5555');

  for (let i = 0; i < 5; i++) {
    await sock.send(JSON.stringify({ index: i, timestamp: Date.now() }));
    console.log(`Đã gửi message ${i}`);
  }
}
// runProducer();""",
        "tips": "ZeroMQ phù hợp nhất khi bạn kiểm soát hoàn toàn hệ thống mạng nội bộ và cần tối ưu từng microsecond độ trễ."
    },

    84: {
        "title_vi": "Các nền tảng Cloud (AWS, Azure, GCP) hỗ trợ triển khai ứng dụng Node.js như thế nào?",
        "level": "Mid",
        "short_answer": "Các nền tảng điện toán đám mây cung cấp 3 mô hình triển khai Node.js chính: (1) Serverless (AWS Lambda, Google Cloud Functions, Azure Functions) - tự động co giãn theo từng request, (2) Container as a Service (AWS ECS / Fargate, Google Cloud Run) - đóng gói Docker container chạy linh hoạt, và (3) Platform as a Service (AWS Elastic Beanstalk, Azure App Service) - chỉ cần đẩy mã nguồn, hạ tầng tự cấu hình.",
        "deep_dive": """1. AWS Lambda: Cực kỳ tiết kiệm chi phí cho các API lưu lượng thấp đến trung bình, tính tiền theo từng mili-giây thực thi. Nhược điểm: Cold start latency.
2. Google Cloud Run: Lựa chọn hiện đại hàng đầu hiện nay cho Node.js: đóng gói Docker container chuẩn, hỗ trợ tự scale về 0 khi không có truy vấn và scale lên hàng nghìn containers trong tích tắc khi tải cao.
3. Managed Kubernetes (AWS EKS, GKE): Dành cho các hệ thống vi dịch vụ khổng lồ của doanh nghiệp lớn.""",
        "code_example": """// Ví dụ Handler chuẩn cho AWS Lambda trên Node.js v20 (ESM)
export const handler = async (event, context) => {
  const method = event.requestContext?.http?.method || 'GET';
  
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: 'Hello from AWS Lambda running Node.js 20!',
      requestId: context.awsRequestId
    })
  };
};""",
        "tips": "Điểm cộng phỏng vấn: Hãy đề cập đến công cụ SST (Serverless Stack) hoặc AWS SAM / Serverless Framework khi xây dựng hệ thống cloud serverless."
    },

    85: {
        "title_vi": "Kiến trúc Serverless là gì và liên hệ như thế nào với Node.js?",
        "level": "Mid",
        "short_answer": "Serverless (FaaS - Function as a Service) là mô hình điện toán đám mây trong đó nhà cung cấp hạ tầng (AWS, GCP) hoàn toàn chịu trách nhiệm quản lý server, phân bổ tài nguyên và mở rộng quy mô. Lập trình viên chỉ cần viết các hàm xử lý độc lập (functions). Node.js là ngôn ngữ phổ biến nhất trong thế giới Serverless nhờ tốc độ khởi động tức thì (Fast Cold Starts) và cú pháp bất đồng bộ gọn gàng.",
        "deep_dive": """1. Cold Start vs Warm Start:
   - Cold Start: Lần đầu tiên function được gọi sau thời gian nhàn rỗi, nhà cung cấp phải tải container mới và khởi động Node.js runtime (~100ms-300ms).
   - Warm Start: Function tái sử dụng container cũ đã có sẵn (~5ms-10ms).
2. Tối ưu hóa Cold Start: Sử dụng `esbuild` để bundle mã nguồn thành 1 file duy nhất, chỉ import đúng những gì cần thiết (ví dụ dùng `@aws-sdk/client-s3` thay vì import toàn bộ thư viện `aws-sdk` khổng lồ).""",
        "code_example": """// Tối ưu hóa Database Connection trong AWS Lambda:
// Khởi tạo connection bên ngoài hàm handler để tái sử dụng qua các Warm Starts!
const { MongoClient } = require('mongodb');
let cachedDb = null;

async function connectToDatabase() {
  if (cachedDb) return cachedDb; // Tái sử dụng kết nối cũ
  const client = await MongoClient.connect(process.env.MONGODB_URI);
  cachedDb = client.db('production');
  return cachedDb;
}

exports.handler = async (event) => {
  const db = await connectToDatabase();
  const items = await db.collection('products').find().toArray();
  return { statusCode: 200, body: JSON.stringify(items) };
};""",
        "tips": "Quy tắc vàng Serverless: Luôn đặt việc khởi tạo kết nối Database (Database Connection Pool) ở bên ngoài scope của hàm `handler` để tái sử dụng giữa các lần thực thi."
    },

    86: {
        "title_vi": "Cách quản lý nhiều phiên bản Node.js trên cùng một máy tính?",
        "level": "Junior",
        "short_answer": "Sử dụng các công cụ quản lý phiên bản Node (Node Version Managers). Ba công cụ hàng đầu là: (1) `nvm` (Node Version Manager - công cụ truyền thống phổ biến nhất), (2) `fnm` (Fast Node Manager - viết bằng Rust, tốc độ siêu nhanh gấp 40 lần nvm), và (3) `volta` (công cụ quản lý phiên bản thông minh tự động chuyển đổi phiên bản dựa trên cấu hình dự án).",
        "deep_dive": """1. Tự động chuyển version: Tạo file `.nvmrc` hoặc `.node-version` chứa chuỗi phiên bản (ví dụ `20.12.0`) ở thư mục gốc của project. Khi ai đó clone dự án về, họ chỉ cần gõ `nvm use` là môi trường khớp 100%.
2. Volta: Cực kỳ mạnh vì nó lưu cấu hình trong trường `\"volta\": { \"node\": \"20.12.0\" }` của `package.json`, bất kỳ ai dùng terminal cd vào thư mục là Volta tự động chuyển đổi âm thầm không cần gõ lệnh.""",
        "code_example": """# Thao tác với nvm:
echo '20.12.0' > .nvmrc    # Tạo file khóa phiên bản cho cả team
nvm use                    # Tự động đọc file .nvmrc và chuyển phiên bản

# Cài đặt fnm (khuyên dùng hiện đại):
# brew install fnm (trên Mac)
fnm install 20
fnm use 20""",
        "tips": "Luôn tạo file `.nvmrc` trong mọi dự án của công ty để các lập trình viên không bao giờ bị lệch phiên bản Node.js khi phối hợp làm việc."
    },

    87: {
        "title_vi": "File `.env` là gì và cơ chế hoạt động của thư viện `dotenv`?",
        "level": "Junior",
        "short_answer": "File `.env` là file văn bản thuần túy chứa các cặp khóa-giá trị (`KEY=VALUE`) đại diện cho các thông tin cấu hình nhạy cảm của dự án. Thư viện `dotenv` khi được gọi lúc khởi động sẽ đọc file `.env`, phân tích cú pháp (parse) nội dung và gán các cặp khóa này vào đối tượng toàn cục `process.env` của Node.js.",
        "deep_dive": """1. Nguyên tắc không ghi đè: `dotenv` mặc định KHÔNG ghi đè lên các biến môi trường đã tồn tại sẵn trong hệ điều hành máy chủ (OS level env vars). Điều này rất hữu ích khi deploy production, bạn có thể truyền thẳng biến từ Docker/Kubernetes mà không sợ file `.env` đè lên.
2. Từ Node.js v20.6+: Không cần cài thêm thư viện `dotenv`, bạn có thể chạy cờ có sẵn của Node: `node --env-file=.env index.js`.""",
        "code_example": """# File: .env (TUYỆT ĐỐI KHÔNG COMMIT LÊN GIT)
PORT=5000
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
JWT_SECRET=super_secret_key_999

# File: src/app.js
require('dotenv').config(); // Đọc và nạp biến ngay dòng đầu tiên

console.log('Cổng Server:', process.env.PORT);
console.log('Database URL:', process.env.DATABASE_URL);""",
        "tips": "Quy tắc an ninh bắt buộc: Luôn luôn kiểm tra file `.gitignore` đã có dòng `.env` chưa trước khi gõ `git push`."
    },

    88: {
        "title_vi": "Mô tả cách tổ chức cấu hình ứng dụng với module `config` (node-config)?",
        "level": "Mid",
        "short_answer": "`node-config` là thư viện phổ biến giúp tổ chức các tệp cấu hình phân tầng theo môi trường một cách bài bản. Nó tự động nạp và gộp (merge) các file cấu hình nằm trong thư mục `config/` (như `default.json`, `development.json`, `production.json`) dựa trên giá trị của biến môi trường `NODE_ENV`.",
        "deep_dive": """1. Cơ chế kế thừa phân tầng:
   - File `default.json`: Chứa các cấu hình mặc định dùng chung cho mọi môi trường.
   - File `production.json`: Ghi đè chỉ những thuộc tính cần thay đổi khi chạy production.
2. Bất biến (Immutability): Các đối tượng trả về từ `config.get('myProp')` được đóng băng (`Object.freeze`), ngăn chặn bất kỳ dòng code nào vô tình thay đổi giá trị cấu hình trong quá trình runtime.""",
        "code_example": """// config/default.json
{
  \"server\": { \"port\": 3000 },
  \"db\": { \"name\": \"app_dev\" }
}

// config/production.json
{
  \"db\": { \"name\": \"app_prod\" }
}

// src/server.js
const config = require('config');

const port = config.get('server.port'); // 3000
const dbName = config.get('db.name');   // Tự động chuyển thành 'app_prod' khi NODE_ENV=production
console.log(`Chạy kết nối tới DB: ${dbName} trên port ${port}`);""",
        "tips": "Kết hợp `node-config` với biến môi trường thông qua file `custom-environment-variables.json` để vừa có cấu trúc phân tầng vừa không lưu lộ mật khẩu trong git."
    },

    89: {
        "title_vi": "Khái niệm CI/CD và cách triển khai cho ứng dụng Node.js?",
        "level": "Mid",
        "short_answer": "CI (Continuous Integration - Tích hợp liên tục) là quy trình tự động hóa việc kiểm tra, linting và chạy toàn bộ unit/integration test mỗi khi lập trình viên tạo Pull Request hoặc push code mới. CD (Continuous Deployment / Delivery - Triển khai liên tục) là quy trình tự động build Docker image, chạy migrations và deploy code đã được kiểm thử an toàn lên server Production mà không cần can thiệp thủ công.",
        "deep_dive": """1. Các giai đoạn trong CI/CD pipeline cho Node.js:
   - Checkout code & Setup Node environment.
   - Cache `node_modules` (dựa trên hash của `package-lock.json`).
   - Cài đặt sạch sẽ bằng `npm ci`.
   - Chạy linter (`npm run lint`).
   - Chạy kiểm thử tự động (`npm test`).
   - Build TypeScript / Bundling (`npm run build`).
   - Build & Push Docker image sang Docker Hub / AWS ECR.
   - Cập nhật phiên bản trên cụm Kubernetes hoặc máy chủ production.""",
        "code_example": """# Quy trình ngắn gọn trong Terminal khi CI chạy:
npm ci                  # Cài đặt chính xác 100% theo lockfile
npm run lint            # Kiểm tra lỗi cú pháp và chuẩn code
npm run test:coverage   # Chạy test, kiểm tra độ phủ code > 80%
npm run build           # Biên dịch ra thư mục dist""",
        "tips": "Điểm quan trọng trong CI: Luôn dùng lệnh `npm ci` thay vì `npm install`. Lệnh `npm ci` đảm bảo môi trường build hoàn toàn tương thích và không tự ý sửa đổi file lock."
    },

    90: {
        "title_vi": "Cách thiết lập một CI/CD Pipeline hoàn chỉnh cho dự án Node.js bằng GitHub Actions?",
        "level": "Senior",
        "short_answer": "Sử dụng GitHub Actions bằng cách tạo file workflow YAML tại `.github/workflows/ci-cd.yml`. Pipeline sẽ tự động kích hoạt khi có sự kiện `push` hoặc `pull_request` vào nhánh `main`, thực thi các bước kiểm thử trên ma trận các phiên bản Node khác nhau (Node 18, 20), và kích hoạt bước deploy nếu toàn bộ bài test đều xanh.",
        "deep_dive": """1. Matrix Strategy: Cho phép chạy song song các bài test trên nhiều phiên bản Node.js cùng lúc để đảm bảo tính tương thích.
2. Cache Dependency: Dùng action `actions/setup-node@v4` với thuộc tính `cache: 'npm'` giúp rút ngắn thời gian chạy CI từ 3 phút xuống còn 30 giây!
3. Secrets: Lưu trữ an toàn các khóa SSH hoặc Docker token trong mục GitHub Repository Secrets.""",
        "code_example": """# .github/workflows/ci.yml
name: Node.js CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    - name: Checkout mã nguồn
      uses: actions/checkout@v4

    - name: Thiết lập Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm' # Tự động cache node_modules siêu nhanh

    - name: Cài đặt dependencies
      run: npm ci

    - name: Kiểm tra Linter
      run: npm run lint

    - name: Chạy Unit Tests
      run: npm test""",
        "tips": "Hãy thiết lập Branch Protection Rules trên GitHub: Bắt buộc workflow 'test' phải PASS 100% thì nút Merge Pull Request mới được phép bấm."
    },

    91: {
        "title_vi": "Cách điều tra và giải quyết sự cố một ứng dụng Node.js chạy chậm trong thực tế?",
        "level": "Senior",
        "short_answer": "Quy trình điều tra bài bản theo các bước: (1) Đo lường và phân loại điểm nghẽn (CPU-bound vs I/O-bound), (2) Kiểm tra Event Loop Delay - nếu delay cao, chứng tỏ có code đồng bộ block hoặc thuật toán nặng, (3) Kiểm tra thời gian truy vấn Database (Slow Queries) và độ trễ gọi Third-party API qua APM (Datadog/New Relic), (4) Tạo CPU Profile bằng cờ `--cpu-prof` và mở trên Chrome DevTools để xem Flamegraph các hàm tốn nhiều mili-giây nhất.",
        "deep_dive": """1. Sử dụng V8 Profiler tích hợp sẵn:
   Chạy `node --cpu-prof app.js`. Sau khi test tải, Node.js sinh ra file `CPU.xxx.cpuprofile`. Nạp file này vào tab Performance của Chrome DevTools để nhìn trực tiếp hàm nào chiếm đỉnh biểu đồ lửa (Flamegraph).
2. Các thủ phạm kinh điển:
   - ReDoS (Regular Expression Denial of Service): Biểu thức chính quy lồng nhau gây quay vòng đệ quy (catastrophic backtracking).
   - Truy vấn N+1 SQL hoặc thiếu Index database.
   - Thao tác `JSON.parse` một payload khổng lồ hàng trăm MB trên luồng chính.""",
        "code_example": """# 1. Khởi động app với bộ ghi CPU profile
node --cpu-prof --cpu-prof-interval=1000 app.js

# 2. Dùng autocannon bắn tải để tái hiện hiện tượng chậm
npx autocannon -c 50 -d 15 http://localhost:3000/api/slow-endpoint

# 3. Mở file *.cpuprofile vừa sinh ra trong Google Chrome:
# Mở tab Performance -> Bấm nút Load Profile (mũi tên hướng lên) để xem biểu đồ Flame Graph!""",
        "tips": "Senior Tip: Nhắc đến câu lệnh `clinic flame` của bộ công cụ chẩn đoán Clinic.js - một công cụ mã nguồn mở cực kỳ nổi tiếng để vẽ Flamegraph phát hiện nghẽn Node.js."
    },

    92: {
        "title_vi": "Cách xử lý File Upload dung lượng lớn trong Node.js an toàn và hiệu quả?",
        "level": "Mid",
        "short_answer": "Không bao giờ được nạp toàn bộ file upload vào bộ nhớ RAM! Thay vào đó, sử dụng các thư viện stream-based parser như `busboy` hoặc `multer` (cấu hình diskStorage hoặc memoryStorage có giới hạn chặt chẽ). Trong các hệ thống hiện đại, giải pháp tối ưu nhất là cấp phát Presigned URL (S3 / GCS) để client upload TRỰC TIẾP lên Cloud Storage mà không cần đi qua server Node.js.",
        "deep_dive": """1. Các nguy cơ bảo mật khi Upload File:
   - Kẻ tấn công upload file shell độc hại (ví dụ `.php`, `.sh`).
   - Zip Bomb: File nén nhỏ nhưng khi giải nén bung ra 100GB làm cạn kiệt ổ cứng.
   - Giả mạo phần mở rộng: File đuôi `.jpg` nhưng nội dung bên trong thực chất là mã thực thi nhị phân -> Bắt buộc kiểm tra Magic Bytes (File Signature) bằng thư viện `file-type`.
2. Kiểm soát: Giới hạn kích thước file (`limits: { fileSize: 5 * 1024 * 1024 }`), lọc whitelist MIME types.""",
        "code_example": """const express = require('express');
const multer = require('multer');
const path = require('node:path');

const app = express();

// Cấu hình lưu file ra ổ đĩa kèm giới hạn an toàn
const upload = multer({
  dest: 'uploads/',
  limits: {
    fileSize: 5 * 1024 * 1024, // Tối đa 5MB
    files: 1 // Chỉ cho phép 1 file mỗi lần
  },
  fileFilter: (req, file, cb) => {
    // Chỉ chấp nhận file ảnh JPEG và PNG
    const allowed = ['image/jpeg', 'image/png'];
    if (allowed.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Chỉ chấp nhận định dạng ảnh JPEG hoặc PNG!'), false);
    }
  }
});

app.post('/api/upload-avatar', upload.single('avatar'), (req, res) => {
  res.json({ message: 'Upload thành công!', fileInfo: req.file });
});""",
        "tips": "Cách trả lời tầm vóc Senior: 'Với các file nặng như Video hoặc tài liệu hàng trăm MB, kiến trúc chuẩn của chúng tôi là client yêu cầu backend cấp một S3 Pre-signed URL, sau đó client upload trực tiếp từ trình duyệt lên S3 bucket. Server Node.js hoàn toàn không phải tốn 1 byte băng thông nào để trung chuyển file.'"
    },

    93: {
        "title_vi": "Cách xử lý các tác vụ tính toán nặng (Heavy Computation / CPU-Intensive) trong Node.js?",
        "level": "Senior",
        "short_answer": "Vì Node.js có main thread đơn luồng, các tác vụ tính toán nặng (như mã hóa video, xử lý ảnh lớn, huấn luyện ML, tính toán ma trận) nếu chạy trên main thread sẽ làm đóng băng toàn bộ ứng dụng. Các giải pháp chuẩn mực gồm: (1) Sử dụng `worker_threads` để chạy trên CPU core khác trong cùng process, (2) Đẩy sang background job queue (BullMQ/RabbitMQ) cho một Dedicated Worker Service xử lý, hoặc (3) Viết C++ Addons / Rust (thông qua N-API) để tối ưu hóa tốc độ tính toán.",
        "deep_dive": """1. Worker Threads Pool: Duy trì một nhóm threads sẵn sàng qua thư viện `piscina`, tránh chi phí tạo mới worker liên tục.
2. Tách riêng máy chủ: Trong kiến trúc microservices, luôn tách Web API Service (I/O heavy) và Background Worker Service (CPU heavy) ra thành 2 container/máy chủ vật lý riêng biệt. Nếu background worker tiêu tốn 100% CPU, web API vẫn phản hồi cho khách hàng mượt mà.""",
        "code_example": """// Sử dụng thư viện Piscina (Worker Thread Pool chuẩn công nghiệp)
const Piscina = require('piscina');

const piscina = new Piscina({
  filename: path.resolve(__dirname, 'heavy-math-worker.js'),
  maxThreads: 4 // Giới hạn 4 worker threads
});

app.post('/api/process-data', async (req, res) => {
  // Giao việc cho Thread Pool, main thread không bị block dù chỉ 1ms!
  const result = await piscina.run(req.body.largeDataset);
  res.json({ success: true, result });
});""",
        "tips": "Nắm vững nguyên lý: 'Giữ cho Event Loop luôn rảnh rỗi'. Bất kỳ thứ gì tốn hơn 10-20ms CPU đều phải được cân nhắc đẩy ra Worker Thread hoặc Queue."
    },

    94: {
        "title_vi": "Vai trò của Node.js trong hệ sinh thái DevOps và tự động hóa?",
        "level": "Junior",
        "short_answer": "Node.js đóng vai trò quan trọng trong DevOps nhờ khả năng viết các công cụ dòng lệnh (CLI tools) mạnh mẽ, kịch bản tự động hóa (automation scripts) đa nền tảng, tích hợp sâu rộng với các công cụ Infrastructure as Code (AWS CDK sử dụng TypeScript/Node.js để định nghĩa hạ tầng), và các công cụ quản lý build, kiểm thử trong CI/CD pipelines.",
        "deep_dive": """1. Node.js CLI Ecosystem: Hầu hết các công cụ DevOps CLI phổ biến hàng đầu như Serverless Framework, AWS CDK, Prisma CLI, Docker compose tooling đều được phát triển bằng Node.js / TypeScript.
2. Thư viện tiện ích: `commander`, `yargs`, `chalk`, `execa` giúp viết các script tự động hóa hệ thống đẹp mắt, dễ bảo trì hơn rất nhiều so với các file Bash shell phức tạp.""",
        "code_example": """#!/usr/bin/env node
// Tạo một công cụ CLI DevOps tự động hóa kiểm tra sức khỏe hệ thống
const { program } = require('commander');

program
  .version('1.0.0')
  .description('DevOps Health Checker Tool')
  .option('-p, --port <number>', 'Cổng cần kiểm tra', '3000')
  .action((options) => {
    console.log(`Đang kiểm tra kết nối tới port: ${options.port}...`);
    // Logic ping socket...
  });

program.parse(process.argv);""",
        "tips": "AWS CDK (Cloud Development Kit) sử dụng TypeScript/Node.js làm ngôn ngữ hàng đầu để tạo VPC, EC2, RDS bằng code thay vì phải viết file YAML CloudFormation nhàm chán."
    },

    95: {
        "title_vi": "Khái niệm đóng gói Container (Containerization) và lợi ích đối với Node.js?",
        "level": "Mid",
        "short_answer": "Containerization (thông qua Docker) là việc đóng gói mã nguồn ứng dụng Node.js cùng toàn bộ môi trường phụ thuộc, phiên bản runtime Node cụ thể, thư viện hệ thống và cấu hình thành một đơn vị chuẩn hóa gọi là Container Image. Lợi ích: Đảm bảo tính nhất quán tuyệt đối giữa máy tính lập trình viên và máy chủ production ('chạy được trên máy tôi thì cũng chạy được trên production'), dễ dàng mở rộng tự động (Autoscaling), và cô lập bảo mật.",
        "deep_dive": """1. Tránh phụ thuộc hệ điều hành: Tránh lỗi kinh điển khi cài các native module C++ (như `bcrypt`, `sharp`) trên macOS chạy được nhưng khi deploy lên Ubuntu server bị lỗi biên dịch.
2. Tốc độ triển khai: Khởi động một container Node.js chỉ mất 1-2 giây, cho phép hệ thống hồi phục ngay lập tức khi gặp sự cố.""",
        "code_example": """# File .dockerignore (BẮT BUỘC ĐỂ KHÔNG COPY THƯ MỤC NẶNG LÊN CONTAINER)
node_modules
npm-debug.log
dist
.env
.git""",
        "tips": "Luôn tạo file `.dockerignore` trước khi gõ `docker build`! Nếu không có `.dockerignore`, Docker sẽ copy toàn bộ thư mục `node_modules` cục bộ trên máy dev vào container, gây xung đột kiến trúc CPU và làm phình to image."
    },

    96: {
        "title_vi": "Node.js được ứng dụng trong lĩnh vực Internet of Things (IoT) như thế nào?",
        "level": "Mid",
        "short_answer": "Node.js được sử dụng rộng rãi trong IoT nhờ mô hình hướng sự kiện (Event-Driven) cực kỳ phù hợp với bản chất phát tín hiệu định kỳ của các cảm biến (sensors). Node.js chạy mượt mà trên các máy tính đơn bo mạch (Single Board Computers như Raspberry Pi), xử lý các giao thức mạng IoT nhẹ như MQTT và CoAP, và đóng vai trò làm IoT Hub thu thập và phân tích dữ liệu thiết bị theo thời gian thực.",
        "deep_dive": """1. Giao thức MQTT: Giao thức truyền tin nhị phân siêu nhẹ Publish/Subscribe thiết kế riêng cho các thiết bị mạng băng thông thấp, pin yếu. Thư viện `mqtt.js` là client MQTT mạnh nhất cho Node.js.
2. Thư viện phần cứng: `johnny-five` (điều khiển Arduino, Tessel, Raspberry Pi bằng JavaScript), `onoff` (thao tác trực tiếp với các chân GPIO của mạch).""",
        "code_example": """const mqtt = require('mqtt');
// Kết nối tới MQTT Broker của hệ thống Smart Home
const client = mqtt.connect('mqtt://broker.hivemq.com');

client.on('connect', () => {
  console.log('Đã kết nối vào IoT Broker thành công');
  // Lắng nghe dữ liệu nhiệt độ từ cảm biến phòng khách
  client.subscribe('home/living-room/temperature');
});

client.on('message', (topic, message) => {
  const temp = parseFloat(message.toString());
  console.log(`[IoT Update] Nhiệt độ hiện tại: ${temp}°C`);
  if (temp > 35) {
    console.warn('CẢNH BÁO: Nhiệt độ quá cao, tự động bật điều hòa!');
  }
});""",
        "tips": "Điểm chú ý: Node.js thích hợp chạy trên các thiết bị Gateway (như Raspberry Pi chạy Linux), chứ không thể chạy trực tiếp trên các vi điều khiển siêu nhỏ RAM 32KB như ESP8266/Arduino (với các chip này người ta dùng C/C++ hoặc Espruino)."
    },

    97: {
        "title_vi": "Những yếu tố then chốt cần cân nhắc khi phát triển ứng dụng Node.js cho thiết bị IoT?",
        "level": "Senior",
        "short_answer": "Khi phát triển Node.js cho IoT, cần đặc biệt lưu ý: (1) Hạn chế tối đa dung lượng bộ nhớ RAM và tiêu thụ điện năng (pin), (2) Khả năng chịu đựng khi mất kết nối mạng chập chờn (Offline Data Buffering & Reconnect), (3) Bảo mật thiết bị (Mã hóa đường truyền TLS/mTLS, xác thực chứng chỉ X.509, bảo vệ cập nhật firmware OTA - Over The Air), và (4) Giới hạn số lần ghi thẻ nhớ microSD để tránh làm hỏng phần cứng.",
        "deep_dive": """1. Giảm thiểu rò rỉ RAM: Trên server có 32GB RAM thì leak 50MB không sao, nhưng trên thiết bị IoT chỉ có 256MB RAM, một rò rỉ nhỏ sẽ gây crash toàn bộ phần cứng sau 2 ngày.
2. SQLite / Local Storage Buffer: Khi mất sóng WiFi, ứng dụng phải lưu tạm dữ liệu đo đạc vào SQLite cục bộ. Khi có mạng trở lại mới đồng bộ lên Cloud.""",
        "code_example": """// Cấu hình MQTT Client có cơ chế tự động giữ hàng đợi tin nhắn khi mất mạng
const client = mqtt.connect('mqtt://my-iot-cloud.com', {
  reconnectPeriod: 5000,    // Thử kết nối lại mỗi 5s
  queueQoSZero: true,       // Giữ hàng đợi tin nhắn ngay cả khi đang offline
  clean: false,             // Duy trì phiên Persistent Session
  clientId: 'device_sensor_livingroom_01'
});""",
        "tips": "Từ khóa bảo mật IoT đắt giá: 'Mutual TLS (mTLS)' - cả thiết bị lẫn server đều phải kiểm tra chứng chỉ số của nhau trước khi truyền tin."
    },

    98: {
        "title_vi": "Có thể sử dụng Node.js cho Trí tuệ nhân tạo (AI) và Học máy (Machine Learning) không? Bằng cách nào?",
        "level": "Mid",
        "short_answer": "Hoàn toàn CÓ THỂ, đặc biệt là trong giai đoạn Dự đoán (Inference) và triển khai mô hình. Mặc dù Python thống trị về huấn luyện mô hình sâu (Deep Learning Training), nhưng Node.js cực kỳ mạnh mẽ trong việc nhúng và chạy các mô hình AI đã huấn luyện sẵn thông qua TensorFlow.js, ONNX Runtime Node, hoặc tích hợp với các mô hình ngôn ngữ lớn (LLMs như OpenAI, Anthropic, Gemini) qua REST và LangChain.js.",
        "deep_dive": """1. TensorFlow.js for Node: Cho phép chạy trực tiếp các mô hình TensorFlow có tăng tốc phần cứng qua backend C++ và GPU (CUDA).
2. ONNX Runtime Node: Định dạng mô hình mở phổ quát. Bạn có thể train model bằng PyTorch trên Python, xuất ra file `.onnx` và nạp vào Node.js chạy với tốc độ C++ cực nhanh.
3. AI Agent & LLMs: Node.js là ngôn ngữ hàng đầu để xây dựng các AI Agents nhờ khả năng xử lý stream phản hồi (Server-Sent Events) từ OpenAI/Claude API mượt mà.""",
        "code_example": """// Sử dụng AI SDK hoặc Fetch để Stream câu trả lời từ LLM trong Node.js
const { OpenAI } = require('openai');
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function streamAiResponse(prompt, res) {
  const stream = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
    stream: true // Kích hoạt Server-Sent Events Stream
  });

  res.setHeader('Content-Type', 'text/event-stream');
  for await (const chunk of stream) {
    const text = chunk.choices[0]?.delta?.content || '';
    res.write(`data: ${text}\\n\\n`); // Stream từng từ về cho client
  }
  res.end();
}""",
        "tips": "Hãy phân biệt rõ: Đừng dùng Node.js để huấn luyện các mạng neural khổng lồ từ đầu (hãy dùng Python/PyTorch). Hãy dùng Node.js để phục vụ mô hình (Serving), Inference và xây dựng ứng dụng tích hợp GenAI."
    },

    99: {
        "title_vi": "Các thư viện và công cụ Machine Learning tiêu biểu cho Node.js?",
        "level": "Junior",
        "short_answer": "Các thư viện nổi bật bao gồm: (1) `@tensorflow/tfjs-node` (Cung cấp bindings native C++ cho TensorFlow), (2) `onnxruntime-node` (Chạy các mô hình ONNX đa nền tảng tối ưu), (3) `brain.js` (Thư viện mạng nơ-ron đơn giản, dễ học cho người mới bắt đầu), (4) `natural` (Xử lý ngôn ngữ tự nhiên cơ bản: tokenization, stemming, tf-idf), và (5) `langchain` / `@ai-sdk/openai` (Xây dựng ứng dụng LLM và RAG hiện đại).",
        "deep_dive": """1. `tfjs-node`: Tận dụng thư viện C++ native libtensorflow giúp tốc độ tính toán ma trận nhanh gấp nhiều lần so với chạy TensorFlow.js thuần bằng JavaScript trong trình duyệt.
2. `natural`: Phù hợp cho các bài toán phân loại sắc thái văn bản (Sentiment Analysis) đơn giản hoặc phân tích từ khóa mà không cần đến mô hình AI cồng kềnh.""",
        "code_example": """// Phân tích cảm xúc văn bản nhanh với thư viện 'natural'
const natural = require('natural');
const Analyzer = natural.SentimentAnalyzer;
const stemmer = natural.PorterStemmer;

const analyzer = new Analyzer('English', stemmer, 'afinn');

// Đánh giá cảm xúc câu văn (trả về điểm số âm/dương)
const score1 = analyzer.getSentiment(['This', 'Node.js', 'server', 'is', 'amazing', 'and', 'fast']);
console.log('Điểm cảm xúc tích cực:', score1); // > 0 (Positive)

const score2 = analyzer.getSentiment(['The', 'application', 'is', 'slow', 'and', 'terrible']);
console.log('Điểm cảm xúc tiêu cực:', score2); // < 0 (Negative)""",
        "tips": "Nếu dự án cần tính năng AI hiện đại năm 2026, hãy giới thiệu Vercel AI SDK (`ai`) kết hợp Node.js để làm việc với GenAI và RAG."
    },

    100: {
        "title_vi": "Tổng hợp các Best Practices toàn diện nhất khi thiết kế RESTful API trong Node.js?",
        "level": "Senior",
        "short_answer": "Một RESTful API đẳng cấp doanh nghiệp trong Node.js cần hội tụ đầy đủ: (1) Tuân thủ chuẩn đặt tên URI dạng danh từ số nhiều phân cấp rõ ràng, (2) Quản lý phiên bản chặt chẽ (`/api/v1/`), (3) Áp dụng phân trang (Cursor-based Pagination cho dữ liệu lớn), (4) Sử dụng HTTP Status Codes và cấu trúc phản hồi lỗi đồng nhất, (5) Bảo mật nhiều lớp (Helmet, Rate-limit, CORS, Input validation), (6) Nén dữ liệu gzip và hỗ trợ ETag caching, và (7) Tài liệu hóa tự động bằng OpenAPI / Swagger.",
        "deep_dive": """1. Cấu trúc phản hồi lỗi đồng nhất (Uniform Error Response):
Mọi lỗi trả về cho client nên tuân theo định dạng chuẩn (ví dụ RFC 7807 Problem Details):
`{ success: false, error: { code: 'INVALID_INPUT', message: '...', details: [...] } }`
2. Phân trang: Thay vì dùng `OFFSET` chậm chạp trên hàng triệu dòng, hãy dùng Keyset / Cursor Pagination (`?limit=20&after_cursor=...`).
3. Idempotency: Hỗ trợ header `Idempotency-Key` cho các endpoint thanh toán và tạo đơn hàng.""",
        "code_example": """// Cấu trúc Response chuẩn mực và middleware bắt lỗi tập trung
const express = require('express');
const app = express();
app.use(express.json());

// Chuẩn hóa phản hồi thành công
function sendSuccess(res, data, statusCode = 200, meta = null) {
  return res.status(statusCode).json({
    success: true,
    data,
    meta,
    timestamp: new Date().toISOString()
  });
}

// Route mẫu có phân trang chuẩn
app.get('/api/v1/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  
  const users = [{ id: 1, name: 'Alex' }];
  const total = 100;

  sendSuccess(res, users, 200, {
    page,
    limit,
    totalPages: Math.ceil(total / limit),
    totalCount: total
  });
});""",
        "tips": "Câu trả lời hoàn hảo cho câu 100: 'Một API tốt không chỉ chạy đúng logic, mà còn phải thân thiện với các lập trình viên khác (Developer Experience - DX) thông qua tài liệu Swagger đầy đủ và các thông báo lỗi trực quan, chính xác.'"
    }
}
