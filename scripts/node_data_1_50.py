"""Node.js Interview Questions & Answers Database (Part 1: Q1 - Q50)"""

NODE_ANSWERS_PART1 = {
    1: {
        "title_vi": "Node.js là gì và tại sao lại được sử dụng rộng rãi?",
        "level": "Junior",
        "short_answer": "Node.js là một runtime environment mã nguồn mở, đa nền tảng, chạy JavaScript phía server dựa trên V8 JavaScript Engine của Google Chrome. Node.js sử dụng mô hình I/O phi chặn (non-blocking), hướng sự kiện (event-driven), giúp xây dựng các ứng dụng mạng có khả năng mở rộng cao và xử lý đồng thời hàng nghìn kết nối với tài nguyên bộ nhớ tối thiểu.",
        "deep_dive": """1. Kiến trúc cốt lõi: Kết hợp giữa V8 Engine (biên dịch JS sang mã máy C++) và thư viện libuv (xử lý Event Loop, Thread Pool cho các tác vụ I/O bất đồng bộ).
2. Single-Threaded Event Loop: Xử lý request trên 1 luồng chính duy nhất, đẩy các tác vụ nặng (file I/O, network DNS, crypto) sang libuv worker pool (mặc định 4 threads).
3. Trường hợp sử dụng tối ưu: Các ứng dụng I/O-heavy như Chat realtime, RESTful API, Streaming data, Single Page App backends, Microservices. Không tối ưu cho tác vụ CPU-intensive (xử lý video, tính toán ma trận) nếu không dùng Worker Threads.""",
        "code_example": """const http = require('http');

// Tạo HTTP Server bất đồng bộ xử lý non-blocking I/O
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({
    status: 'success',
    message: 'Hello from Node.js Event-Driven Architecture!',
    timestamp: new Date().toISOString()
  }));
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});""",
        "tips": "Điểm cộng lớn khi phỏng vấn: Đừng chỉ nói 'Node.js là single-threaded'. Hãy giải thích rõ ràng rằng JavaScript code chạy single-threaded trên main event loop, nhưng bản thân Node.js bên dưới là multi-threaded nhờ libuv C++ thread pool."
    },

    2: {
        "title_vi": "Node.js xử lý Child Threads và đa luồng như thế nào?",
        "level": "Mid",
        "short_answer": "Node.js xử lý đa luồng thông qua nhiều cơ chế: (1) libuv Thread Pool ngầm bên dưới cho I/O, (2) module `child_process` để fork/spawn tiến trình độc lập, và (3) module `worker_threads` (từ Node v10.5+) cho phép tạo các luồng thực sự chia sẻ chung bộ nhớ qua SharedArrayBuffer.",
        "deep_dive": """1. libuv Worker Pool: Mặc định có 4 threads (có thể cấu hình qua biến môi trường UV_THREADPOOL_SIZE=n), phục vụ fs, crypto, zlib, dns.lookup.
2. child_process: (spawn, exec, fork) tạo ra OS process mới riêng biệt với memory space riêng, giao tiếp qua IPC channel.
3. worker_threads: Chạy song song nhiều V8 isolate trên cùng một tiến trình, tiết kiệm RAM hơn fork, thích hợp tuyệt đối cho tính toán CPU-heavy (mã hóa, nén ảnh, xử lý dữ liệu lớn).""",
        "code_example": """// main.js - Sử dụng worker_threads cho tác vụ tính toán nặng
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

if (isMainThread) {
  // Main thread: không bị block, vẫn tiếp tục lắng nghe request
  const worker = new Worker(__filename, { workerData: { countTo: 1e8 } });
  
  worker.on('message', result => console.log('Worker hoàn thành:', result));
  worker.on('error', err => console.error('Worker lỗi:', err));
  console.log('Main thread vẫn chạy mượt mà, không bị lag!');
} else {
  // Worker thread: chạy trên CPU core riêng
  let sum = 0;
  for (let i = 0; i < workerData.countTo; i++) sum += i;
  parentPort.postMessage({ total: sum });
}""",
        "tips": "Senior Tip: Phân biệt rõ khi nào dùng `cluster/child_process` (mỗi tiến trình 1 V8 riêng, cô lập hoàn toàn, dùng để scale app) và khi nào dùng `worker_threads` (chia sẻ bộ nhớ, dùng giải quyết bottleneck CPU)."
    },

    3: {
        "title_vi": "Mô hình lập trình hướng sự kiện (Event-Driven) trong Node.js hoạt động ra sao?",
        "level": "Junior",
        "short_answer": "Lập trình hướng sự kiện là mô hình trong đó luồng điều khiển của ứng dụng được kích hoạt bởi các sự kiện (events) như click, I/O hoàn thành, kết nối socket mới, hay dữ liệu gửi đến qua stream. Đối tượng phát ra sự kiện (Event Emitter) và các hàm lắng nghe (Listeners/Handlers) sẽ phản hồi lại sự kiện đó.",
        "deep_dive": """1. Observer Pattern: Module `events` với class `EventEmitter` là xương sống của mọi module trong Node.js (http.Server, fs.ReadStream, socket, process đều kế thừa EventEmitter).
2. Quy trình: Khi một thao tác I/O hoàn thành, libuv gửi callback vào Event Loop queue, Event Loop kích hoạt listener tương ứng.
3. Đồng bộ vs Bất đồng bộ: Mặc định EventEmitter gọi các listener theo thứ tự ĐỒNG BỘ khi `emit()` được gọi, trừ khi bên trong listener dùng `setImmediate` hoặc `process.nextTick`.""",
        "code_example": """const EventEmitter = require('events');

class OrderService extends EventEmitter {}
const orderService = new OrderService();

// Đăng ký listener lắng nghe sự kiện 'orderPlaced'
orderService.on('orderPlaced', (order) => {
  console.log(`[Email] Đang gửi email xác nhận cho đơn hàng #${order.id}`);
});

orderService.on('orderPlaced', (order) => {
  console.log(`[Inventory] Trừ kho cho sản phẩm ${order.productId}`);
});

// Phát sự kiện (trigger)
console.log('Khách hàng bấm thanh toán...');
orderService.emit('orderPlaced', { id: 101, productId: 'MACBOOK-M3', price: 2000 });""",
        "tips": "Lưu ý cảnh báo rò rỉ bộ nhớ: EventEmitter có giới hạn mặc định `defaultMaxListeners = 10`. Nếu bạn gắn quá 10 listeners mà không remove, Node.js sẽ in warning `MaxListenersExceededWarning` cảnh báo memory leak."
    },

    4: {
        "title_vi": "Event Loop trong Node.js là gì và các giai đoạn (phases) của nó hoạt động như thế nào?",
        "level": "Senior",
        "short_answer": "Event Loop là cơ chế liên tục kiểm tra và điều phối việc thực thi mã code, thu thập và xử lý các sự kiện, cũng như thực thi các tác vụ con trong hàng đợi callback. Event Loop giúp Node.js thực hiện các thao tác non-blocking I/O dù chỉ chạy trên 1 luồng JavaScript duy nhất.",
        "deep_dive": """Event Loop của libuv gồm 6 pha (phases) lặp tuần tự:
1. Timers: Thực thi callback của `setTimeout()` và `setInterval()`.
2. Pending Callbacks: Xử lý I/O callbacks bị hoãn từ vòng lặp trước (ví dụ lỗi mạng TCP ECONNREFUSED).
3. Idle, Prepare: Dùng nội bộ bởi libuv.
4. Poll: Pha quan trọng nhất - tính toán thời gian block chờ I/O mới và xử lý các sự kiện I/O (ngoại trừ timers, close, setImmediate).
5. Check: Thực thi callback của `setImmediate()`.
6. Close Callbacks: Xử lý các sự kiện đóng, ví dụ `socket.on('close', ...)`.
* Chú ý Microtasks: `process.nextTick()` queue và Promise microtask queue được ưu tiên thực thi ngay lập tức sau mỗi tác vụ và giữa các giai đoạn!""",
        "code_example": """console.log('1. Đồng bộ (Start)');

setTimeout(() => console.log('5. Timers phase: setTimeout'), 0);
setImmediate(() => console.log('6. Check phase: setImmediate'));

Promise.resolve().then(() => console.log('3. Microtask: Promise.then'));
process.nextTick(() => console.log('2. Microtask ưu tiên cao nhất: process.nextTick'));

console.log('4. Đồng bộ (End)');

// Output chính xác:
// 1. Đồng bộ (Start)
// 4. Đồng bộ (End)
// 2. Microtask ưu tiên cao nhất: process.nextTick
// 3. Microtask: Promise.then
// 5. Timers phase: setTimeout (hoặc Check phase tùy context I/O)
// 6. Check phase: setImmediate""",
        "tips": "Câu hỏi sát thủ Senior: 'Trong một I/O cycle (ví dụ trong fs.readFile), giữa setImmediate và setTimeout(..., 0), cái nào luôn chạy trước?' Đáp án: `setImmediate` luôn chạy trước vì sau khi I/O callback xong ở Poll phase, Event Loop chuyển ngay sang Check phase!"
    },

    5: {
        "title_vi": "Sự khác biệt giữa Node.js và các công nghệ máy chủ truyền thống (Apache, PHP, Java Servlets)?",
        "level": "Mid",
        "short_answer": "Máy chủ truyền thống (như Apache/PHP đa luồng) áp dụng mô hình Thread-per-request: mỗi kết nối khách chiếm 1 thread riêng và bị block khi chờ I/O (Database, Disk). Trong khi đó, Node.js áp dụng kiến trúc Single-Threaded Event Loop kết hợp Non-blocking I/O: 1 thread duy nhất phục vụ hàng vạn kết nối đồng thời mà không bị block.",
        "deep_dive": """1. Tiêu tốn bộ nhớ: 1 thread trong Apache/Java tốn 1MB - 2MB stack RAM. 10,000 kết nối tốn 10GB-20GB RAM (gây crash hoặc swap disk - C10K problem). Node.js chỉ tốn vài chục bytes cho 1 socket descriptor.
2. Context Switching: Đa luồng truyền thống tốn chi phí CPU khổng lồ để chuyển đổi ngữ cảnh giữa hàng nghìn threads. Node.js không bị tốn chi phí context switch trên main loop.
3. Điểm yếu của Node.js: Nếu có 1 request thực hiện thuật toán nặng chiếm dụng CPU (như vòng lặp vô tận), toàn bộ người dùng khác sẽ bị đứng hình. Mô hình đa luồng truyền thống chỉ bị treo luồng của người đó.""",
        "code_example": """// Minh họa non-blocking trong Node.js:
// Hàng ngàn requests vào cùng lúc không ai phải chờ ai hoàn thành database query
const fs = require('fs');

console.time('Non-blocking');
fs.readFile(__filename, (err, data) => {
  console.log(`Đã đọc xong file (${data.length} bytes)`);
});
console.log('Server vẫn thoải mái phục vụ các requests khác ngay lập tức!');
console.timeEnd('Non-blocking');""",
        "tips": "Khi so sánh, hãy dùng thuật ngữ C10K Problem và Context Switching Overhead. Đó là hai điểm mạnh cốt tử giúp Node.js chiến thắng các hệ thống cũ trong các bài toán web hiện đại."
    },

    6: {
        "title_vi": "Khái niệm 'Non-blocking' (Phi chặn) trong Node.js nghĩa là gì?",
        "level": "Junior",
        "short_answer": "'Non-blocking' có nghĩa là các thao tác I/O (đọc ghi đĩa, truy vấn cơ sở dữ liệu, gọi API bên ngoài) không bắt CPU JavaScript phải dừng lại chờ đợi kết quả trả về. Thay vào đó, hàm sẽ ủy thác cho hệ điều hành/libuv thực thi ngầm và tiếp tục chạy ngay các dòng code tiếp theo.",
        "deep_dive": """1. Blocking I/O: `const data = fs.readFileSync('data.txt')` khiến toàn bộ tiến trình dừng lại cho đến khi đọc xong từng byte trên ổ cứng. Không request nào khác được phục vụ trong lúc này.
2. Non-blocking I/O: `fs.readFile('data.txt', callback)` trả về quyền điều khiển ngay lập tức. Libuv thực thi ngầm ở background, khi có dữ liệu thì đưa callback vào Event Loop queue.
3. Lợi ích: Tối ưu hóa tối đa thời gian nhàn rỗi (idle time) của CPU để đạt throughput cực lớn.""",
        "code_example": """const fs = require('fs');

console.log('--- 1. Bắt đầu tác vụ ---');

// Thao tác Non-blocking (Asynchronous)
fs.readFile(__filename, 'utf8', (err, content) => {
  if (err) throw err;
  console.log('--- 3. Đã đọc xong file bất đồng bộ ---');
});

console.log('--- 2. Dòng này chạy ngay lập tức mà không bị nghẽn! ---');""",
        "tips": "Luôn tránh sử dụng các hàm có hậu tố `Sync` (như `readFileSync`, `writeFileSync`) trong route handlers của production server, vì chúng biến Node.js thành blocking single-thread gây treo toàn bộ ứng dụng."
    },

    7: {
        "title_vi": "Cách cập nhật Node.js lên phiên bản mới nhất?",
        "level": "Junior",
        "short_answer": "Cách chuẩn và chuyên nghiệp nhất trong môi trường phát triển là sử dụng công cụ quản lý phiên bản Node như `nvm` (Node Version Manager) hoặc `fnm` (Fast Node Manager). Trên production hoặc container, thường cập nhật phiên bản base image trong Dockerfile.",
        "deep_dive": """1. Với nvm (khuyên dùng):
- Cài bản mới nhất: `nvm install node`
- Cài bản LTS mới nhất (khuyến nghị cho production): `nvm install --lts`
- Chuyển phiên bản: `nvm use --lts`
- Đặt mặc định: `nvm alias default 'lts/*'`
2. Với Volta hoặc fnm: Quản lý tự động theo từng project thông qua cấu hình `engines` trong `package.json`.
3. Kiểm tra bảo mật: Trước khi nâng cấp, luôn kiểm tra Node.js Release Schedule và Changelog xem có breaking changes không.""",
        "code_example": """# Các lệnh thực thi trong Terminal:
nvm ls-remote --lts          # Xem danh sách các phiên bản LTS có sẵn
nvm install 20               # Cài đặt Node.js LTS v20
nvm use 20                   # Chuyển sang dùng v20
node -v                      # Kiểm tra phiên bản hiện tại (ví dụ: v20.12.0)
npm -v                       # Kiểm tra phiên bản npm đi kèm""",
        "tips": "Luôn khuyên dùng phiên bản LTS (Long-Term Support) cho dự án doanh nghiệp để đảm bảo tính ổn định và bảo mật trong vòng 30 tháng."
    },

    8: {
        "title_vi": "'npm' là gì và được sử dụng để làm gì?",
        "level": "Junior",
        "short_answer": "npm (Node Package Manager) vừa là kho lưu trữ mã nguồn mở (registry) lớn nhất thế giới cho các thư viện JavaScript, vừa là công cụ dòng lệnh (CLI) đi kèm với Node.js dùng để cài đặt, cập nhật, chia sẻ và quản lý các gói phụ thuộc (dependencies) trong dự án.",
        "deep_dive": """1. npm Registry: Cơ sở dữ liệu trực tuyến chứa hàng triệu package JS.
2. npm CLI: Quản lý vòng đời dự án (init, install, test, build, publish).
3. Phân biệt các loại dependencies:
   - `dependencies`: Cần thiết cho ứng dụng chạy ở môi trường production.
   - `devDependencies`: Chỉ dùng trong quá trình code, test, build (như typescript, jest, nodemon).
   - `peerDependencies`: Yêu cầu ứng dụng chủ phải cài phiên bản package tương thích (phổ biến khi viết plugin).""",
        "code_example": """# Khởi tạo dự án mới với cài đặt mặc định
npm init -y

# Cài đặt dependency chạy production (lưu vào dependencies)
npm install express dotenv

# Cài đặt dependency phát triển (lưu vào devDependencies)
npm install -D nodemon jest eslint

# Chạy script được định nghĩa trong package.json
npm run dev""",
        "tips": "Senior Tip: Nhắc đến lệnh `npm ci` (Clean Install). Khác với `npm install`, `npm ci` xóa `node_modules` và cài đặt chính xác 100% theo file `package-lock.json`, cực kỳ quan trọng trong CI/CD pipeline."
    },

    9: {
        "title_vi": "Cách quản lý các package trong một dự án Node.js?",
        "level": "Mid",
        "short_answer": "Quản lý package bao gồm việc định nghĩa phụ thuộc trong `package.json`, khóa phiên bản bằng lockfile (`package-lock.json`), tuân thủ Semantic Versioning, quét lỗ hổng bảo mật bằng `npm audit`, và dọn dẹp các thư viện không sử dụng.",
        "deep_dive": """1. Lockfile (`package-lock.json`): Đảm bảo tính nhất quán (deterministic build) giữa tất cả các máy dev và server staging/production.
2. Quét bảo mật: Chạy định kỳ `npm audit` hoặc tích hợp Snyk/Dependabot để phát hiện CVEs trong cây phụ thuộc.
3. Cập nhật an toàn: Sử dụng công cụ như `npm-check-updates` (ncu) để kiểm tra các phiên bản mới và kiểm thử kỹ lưỡng trước khi nâng cấp major version.""",
        "code_example": """# Kiểm tra các package đã lỗi thời
npm outdated

# Quét và tự động sửa các lỗi bảo mật có thể
npm audit
npm audit fix

# Gỡ bỏ package không còn dùng
npm uninstall lodash

# Cài đặt chính xác không tự cập nhật caret (^)
npm install express --save-exact""",
        "tips": "Tuyệt đối commit `package-lock.json` vào Git repository! Không bao giờ thêm nó vào `.gitignore`."
    },

    10: {
        "title_vi": "File `package.json` là gì và chứa những thông tin cốt lõi nào?",
        "level": "Junior",
        "short_answer": "File `package.json` là bản mô tả trung tâm (manifest) của bất kỳ dự án Node.js nào. Nó chứa thông tin metadata về dự án (tên, phiên bản, tác giả), danh sách các thư viện phụ thuộc (`dependencies`, `devDependencies`), cấu hình script thực thi, và các thiết lập module.",
        "deep_dive": """Các trường quan trọng nhất:
- `name` & `version`: Định danh duy nhất của package.
- `scripts`: Các alias lệnh CLI rút gọn (`npm start`, `npm test`).
- `dependencies` & `devDependencies`: Phân tách ranh giới build và runtime.
- `type`: `\"module\"` (kích hoạt ES Modules với import/export) hoặc `\"commonjs\"` (dùng require).
- `engines`: Chỉ định phiên bản Node.js/npm tối thiểu yêu cầu để chạy ứng dụng.""",
        "code_example": """{
  \"name\": \"my-ecommerce-api\",
  \"version\": \"1.0.0\",
  \"description\": \"High performance Node.js backend\",
  \"main\": \"src/server.js\",
  \"type\": \"module\",
  \"scripts\": {
    \"start\": \"node src/server.js\",
    \"dev\": \"nodemon src/server.js\",
    \"test\": \"jest --coverage\"
  },
  \"dependencies\": {
    \"express\": \"^4.19.2\",
    \"zod\": \"^3.22.4\"
  },
  \"devDependencies\": {
    \"nodemon\": \"^3.1.0\",
    \"jest\": \"^29.7.0\"
  },
  \"engines\": {
    \"node\": \">=20.0.0\"
  }
}""",
        "tips": "Cẩn thận với dấu `^` (caret: cho phép update minor/patch) và `~` (tilde: chỉ cho phép update patch). Để an toàn tuyệt đối trong dự án lớn, hãy ghim phiên bản cụ thể hoặc dựa vào lockfile."
    },

    11: {
        "title_vi": "Liệt kê và mô tả các Core Modules quan trọng nhất của Node.js?",
        "level": "Junior",
        "short_answer": "Node.js cung cấp sẵn các module tích hợp sẵn (core modules) không cần cài đặt thêm qua npm, bao gồm: `fs` (File System), `http` & `https` (Web server), `path` (Xử lý đường dẫn), `events` (EventEmitter), `crypto` (Mã hóa, hashing), `os` (Thông tin hệ điều hành), `stream` (Xử lý luồng dữ liệu) và `cluster` (Tận dụng đa nhân CPU).",
        "deep_dive": """1. `fs`: Đọc, ghi, xóa file đồng bộ và bất đồng bộ (khuyên dùng `fs/promises`).
2. `path`: Chuẩn hóa đường dẫn tương thích giữa Windows (\\) và POSIX (/).
3. `crypto`: Cung cấp các thuật toán mã hóa AES, hashing SHA-256, HMAC, tạo random UUID.
4. `stream`: Xử lý dữ liệu lớn không làm tràn RAM.
5. `os` & `process`: Đọc CPU info, free memory, biến môi trường, thoát tiến trình an toàn.""",
        "code_example": """// Sử dụng tiền tố 'node:' chuẩn hiện đại từ Node v16+
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');

console.log('OS Platform:', os.platform(), os.arch());
console.log('Total CPUs:', os.cpus().length);
console.log('Free RAM:', (os.freemem() / 1024 / 1024 / 1024).toFixed(2), 'GB');

const uuid = crypto.randomUUID();
console.log('Generated UUID v4:', uuid);

const fullPath = path.resolve(__dirname, 'uploads', 'avatar.png');
console.log('Normalized Path:', fullPath);""",
        "tips": "Senior Tip: Luôn dùng cú pháp `node:fs`, `node:path`, `node:crypto`. Tiền tố `node:` ngăn ngừa xung đột nếu vô tình có thư viện bên ngoài cùng tên, đồng thời tối ưu tốc độ phân giải module của V8."
    },

    12: {
        "title_vi": "Cách tạo một HTTP Server cơ bản trong Node.js sử dụng core module `http`?",
        "level": "Junior",
        "short_answer": "Sử dụng hàm `http.createServer()` truyền vào một callback nhận 2 tham số `req` (IncomingMessage - một Readable Stream) và `res` (ServerResponse - một Writable Stream), sau đó gọi `server.listen(port)` để bắt đầu lắng nghe kết nối.",
        "deep_dive": """1. Request Handling: `req` chứa thông tin method, url, headers. Để đọc body POST, ta phải lắng nghe sự kiện `'data'` và `'end'` vì dữ liệu được truyền dạng chunks.
2. Response Writing: Dùng `res.writeHead()` để set status code và headers, `res.write()` để gửi chunk dữ liệu và `res.end()` để hoàn tất kết nối HTTP.
3. Kế thừa: `http.Server` kế thừa từ `net.Server` và `EventEmitter`, kích hoạt các sự kiện `'request'`, `'connection'`, `'close'`.""",
        "code_example": """const http = require('node:http');

const server = http.createServer((req, res) => {
  const { method, url } = req;
  
  if (method === 'GET' && url === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'OK', uptime: process.uptime() }));
  }
  
  if (method === 'POST' && url === '/api/echo') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ received: body }));
    });
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Route Not Found');
});

server.listen(4000, () => console.log('HTTP Server listening on port 4000'));""",
        "tips": "Điểm chú ý: Luôn gọi `res.end()` để đóng kết nối client. Nếu quên gọi `res.end()`, request từ trình duyệt/client sẽ bị treo vĩnh viễn (timeout)."
    },

    13: {
        "title_vi": "Mục đích của File System (`fs`) module và sự khác biệt giữa các API của nó?",
        "level": "Mid",
        "short_answer": "Module `fs` cho phép tương tác trực tiếp với hệ thống tập tin của hệ điều hành (đọc, ghi, sửa, xóa, theo dõi file và thư mục). `fs` cung cấp 3 cách tiếp cận: Synchronous (gây block), Callback-based bất đồng bộ truyền thống, và Promise-based (`fs/promises`) hiện đại hỗ trợ `async/await`.",
        "deep_dive": """1. `fs/promises`: Khuyến nghị sử dụng trong 95% trường hợp code hiện đại vì cú pháp sạch sẽ, dễ bắt lỗi bằng `try/catch`.
2. `fs.createReadStream` / `createWriteStream`: Bắt buộc sử dụng khi kích thước file lớn hơn vài chục MB để không làm cạn kiệt V8 Heap Memory.
3. `fs.watch` vs `fs.watchFile`: `fs.watch` dựa trên sự kiện native của OS (inotify/kqueue), nhanh và nhẹ hơn `fs.watchFile` (chạy polling định kỳ gây tốn CPU).""",
        "code_example": """const fs = require('node:fs/promises');
const path = require('node:path');

async function manageFiles() {
  const filePath = path.join(__dirname, 'demo.txt');
  try {
    // 1. Ghi file bất đồng bộ không block
    await fs.writeFile(filePath, 'Dữ liệu nhật ký hệ thống\\n', 'utf8');
    
    // 2. Nối thêm dữ liệu
    await fs.appendFile(filePath, 'Thời gian: ' + new Date().toISOString());
    
    // 3. Đọc nội dung file
    const content = await fs.readFile(filePath, 'utf8');
    console.log('Nội dung file:\\n', content);
    
    // 4. Xóa file sau khi dùng xong
    await fs.unlink(filePath);
    console.log('Đã dọn dẹp file an toàn.');
  } catch (error) {
    console.error('Lỗi thao tác File System:', error.message);
  }
}

manageFiles();""",
        "tips": "Không bao giờ dùng `fs.readFileSync` bên trong route handler của Express hay Web Server phục vụ nhiều users cùng lúc."
    },

    14: {
        "title_vi": "Lớp `Buffer` trong Node.js là gì và tại sao lại cần thiết?",
        "level": "Mid",
        "short_answer": "Lớp `Buffer` là cấu trúc dữ liệu đại diện cho vùng nhớ có kích thước cố định được cấp phát bên ngoài V8 JavaScript Heap (trong bộ nhớ C++). Buffer được dùng để lưu trữ và xử lý trực tiếp dữ liệu nhị phân thô (raw binary data) khi làm việc với file streams, mạng TCP, hình ảnh hoặc mã hóa crypto.",
        "deep_dive": """1. Tại sao cần Buffer: Trước ES6, JavaScript thuần chỉ có kiểu String và không có khả năng thao tác với các luồng byte nhị phân. Buffer giải quyết việc giao tiếp nhị phân tốc độ cao với tầng OS C++.
2. Cấp phát an toàn:
   - `Buffer.alloc(size)`: Cấp phát bộ nhớ và điền giá trị 0 vào tất cả các byte (an toàn tuyệt đối, tránh lộ dữ liệu cũ).
   - `Buffer.allocUnsafe(size)`: Cấp phát siêu tốc nhưng không xóa bộ nhớ cũ (có thể chứa dữ liệu nhạy cảm nếu không ghi đè cẩn thận).
3. Chuyển đổi: Hỗ trợ encode/decode qua nhiều bảng mã: `'utf8'`, `'base64'`, `'hex'`, `'binary'`.""",
        "code_example": """// 1. Tạo buffer từ chuỗi UTF-8
const buf1 = Buffer.from('Học Node.js Senior');
console.log('Buffer nhị phân (Hex):', buf1);
console.log('Độ dài tính bằng Bytes:', buf1.length); // 21 bytes (do dấu tiếng Việt chiếm nhiều byte)

// 2. Chuyển đổi qua Base64
const base64Str = buf1.toString('base64');
console.log('Base64:', base64Str);

// 3. Giải mã ngược lại
const buf2 = Buffer.from(base64Str, 'base64');
console.log('Giải mã lại:', buf2.toString('utf8'));

// 4. Cấp phát buffer an toàn
const safeBuffer = Buffer.alloc(10);
safeBuffer.write('Hello');
console.log('Safe Buffer:', safeBuffer);""",
        "tips": "Bẫy phỏng vấn: `Buffer.byteLength(str)` khác với `str.length`. Chuỗi 'Xin chào' có `str.length = 8`, nhưng `Buffer.byteLength('Xin chào')` là 10 bytes vì ký tự 'à' tốn 2 bytes UTF-8."
    },

    15: {
        "title_vi": "Streams trong Node.js là gì và có những loại Stream nào?",
        "level": "Senior",
        "short_answer": "Stream là đối tượng cho phép đọc dữ liệu từ một nguồn hoặc ghi dữ liệu đến một đích theo từng mảnh nhỏ (chunks) một cách liên tục mà không cần phải tải toàn bộ file vào bộ nhớ RAM. Có 4 loại Stream cơ bản: Readable (đọc), Writable (ghi), Duplex (cả đọc và ghi), và Transform (biến đổi dữ liệu trên đường truyền).",
        "deep_dive": """1. Bốn loại Stream:
   - `Readable`: Ví dụ `fs.createReadStream`, `http.IncomingMessage` (req).
   - `Writable`: Ví dụ `fs.createWriteStream`, `http.ServerResponse` (res).
   - `Duplex`: Cả 2 chiều độc lập, ví dụ `net.Socket`.
   - `Transform`: Duplex stream vừa nhận dữ liệu vừa biến đổi, ví dụ `zlib.createGzip()`.
2. Vấn đề Backpressure: Xảy ra khi nguồn đọc gửi dữ liệu nhanh hơn tốc độ mà đích ghi có thể xử lý. Nếu không kiểm soát, RAM sẽ phình to dẫn đến Crash OOM.
3. Giải pháp: Sử dụng `stream.pipeline()` thay cho `.pipe()` thủ công để tự động quản lý backpressure và xử lý lỗi/dọn dẹp tài nguyên triệt để.""",
        "code_example": """const fs = require('node:fs');
const zlib = require('node:zlib');
const { pipeline } = require('node:stream/promises');

async function compressLargeFile() {
  try {
    // Đọc file lớn -> Nén Gzip -> Ghi ra file mới
    // Bộ nhớ RAM duy trì ổn định dưới 30MB dù file gốc nặng 5GB!
    await pipeline(
      fs.createReadStream('huge_database_dump.sql'),
      zlib.createGzip(),
      fs.createWriteStream('huge_database_dump.sql.gz')
    );
    console.log('Nén file dung lượng lớn thành công bằng Stream Pipeline!');
  } catch (err) {
    console.error('Lỗi trong chuỗi Stream:', err);
  }
}

compressLargeFile();""",
        "tips": "Điểm cộng lớn khi phỏng vấn: Giải thích vì sao `pipeline()` tốt hơn `.pipe()`. Cú pháp `.pipe()` cũ không tự động hủy (destroy) các stream thượng nguồn khi có lỗi xảy ra ở downstream, dễ gây rò rỉ file descriptor."
    },

    16: {
        "title_vi": "Cách đọc và ghi file trong Node.js hiệu quả nhất?",
        "level": "Junior",
        "short_answer": "Tùy thuộc vào dung lượng file: Với file nhỏ (dưới 10MB), sử dụng `fs/promises` (`readFile`, `writeFile`) cho code đơn giản và tiện lợi. Với file lớn (từ vài chục MB đến hàng GB), bắt buộc dùng `fs.createReadStream` và `fs.createWriteStream` kết hợp `stream.pipeline` để stream dữ liệu.",
        "deep_dive": """1. Giới hạn V8 Buffer: V8 heap memory mặc định ~1.4GB trên 64-bit OS. Nếu dùng `fs.readFile` đọc file 2GB, Node.js sẽ ném lỗi `RangeError: File size is greater than possible Buffer: 0x7fffffff bytes`.
2. Line-by-line reading: Đọc từng dòng của file log hàng triệu dòng bằng module `readline` kết hợp ReadStream để memory tiêu tốn gần như bằng 0.""",
        "code_example": """const fs = require('node:fs');
const readline = require('node:readline');

async function readLogLineByLine(filePath) {
  const fileStream = fs.createReadStream(filePath);
  
  // Đọc từng dòng một, không tải hết file vào RAM
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let errorCount = 0;
  for await (const line of rl) {
    if (line.includes('[ERROR]')) errorCount++;
  }

  console.log(`Tìm thấy tổng cộng ${errorCount} dòng lỗi.`);
}""",
        "tips": "Khi được hỏi 'Làm thế nào để xử lý file log 10GB trong Node.js?', câu trả lời chuẩn luôn là: Sử dụng `readline` kết hợp `fs.createReadStream`."
    },

    17: {
        "title_vi": "Cách sử dụng `EventEmitter` trong Node.js?",
        "level": "Mid",
        "short_answer": "`EventEmitter` nằm trong module `events`. Ta có thể kế thừa hoặc khởi tạo một instance của `EventEmitter`, đăng ký xử lý sự kiện bằng các phương thức `.on()`, `.once()`, và phát sự kiện bằng `.emit(eventName, ...args)`.",
        "deep_dive": """1. Các phương thức cốt lõi:
   - `on(event, listener)`: Lắng nghe nhiều lần.
   - `once(event, listener)`: Chỉ kích hoạt duy nhất một lần rồi tự hủy listener.
   - `removeListener(event, listener)` / `off()`: Hủy đăng ký listener cụ thể.
   - `removeAllListeners([event])`: Xóa toàn bộ listeners.
2. Xử lý lỗi đặc biệt: Sự kiện `'error'` trong EventEmitter là bắt buộc phải được bắt! Nếu emit `'error'` mà không có listener nào đăng ký cho nó, Node.js sẽ ném uncaught exception và crash toàn bộ tiến trình!""",
        "code_example": """const EventEmitter = require('node:events');

class PaymentGateway extends EventEmitter {
  processPayment(userId, amount) {
    console.log(`Đang xử lý trừ tiền ${amount}đ cho user ${userId}...`);
    
    // Giả lập logic kiểm tra
    if (amount <= 0) {
      // BẮT BUỘC có listener 'error', nếu không app sẽ crash!
      return this.emit('error', new Error('Số tiền thanh toán không hợp lệ'));
    }
    
    setTimeout(() => {
      this.emit('success', { transactionId: 'TX12345', amount });
    }, 500);
  }
}

const gateway = new PaymentGateway();

// Bắt buộc đăng ký bắt lỗi
gateway.on('error', (err) => console.error('Bắt được lỗi Payment:', err.message));

gateway.once('success', (data) => {
  console.log('Thanh toán thành công lần đầu:', data);
});

gateway.processPayment('user_01', 500000);
gateway.processPayment('user_01', -100); // Kích hoạt sự kiện error""",
        "tips": "Luôn luôn lắng nghe sự kiện `'error'` trên bất kỳ EventEmitter instance nào bạn tạo ra hoặc nhận được từ third-party."
    },

    18: {
        "title_vi": "Module `querystring` là gì và so sánh với Web API `URLSearchParams`?",
        "level": "Junior",
        "short_answer": "`querystring` là module cũ của Node.js dùng để parse và định dạng chuỗi URL query (ví dụ: `?page=1&limit=10`). Tuy nhiên, hiện nay module này đã bị đánh dấu DEPRECATED (lỗi thời) và được khuyến nghị thay thế hoàn toàn bằng chuẩn WHATWG `URLSearchParams`.",
        "deep_dive": """1. Nhược điểm của `querystring`: Không tuân thủ hoàn toàn các chuẩn mã hóa URI của WHATWG, không hỗ trợ tốt nested query parameters.
2. Chuẩn mới `URLSearchParams`: Là một global object có sẵn trong cả Browser và Node.js hiện đại, hỗ trợ các hàm `.get()`, `.set()`, `.append()`, `.has()`, `.entries()` rất tiện lợi.""",
        "code_example": """// Chuẩn hiện đại: Sử dụng URLSearchParams (Global, không cần require)
const searchParams = new URLSearchParams('category=laptops&brand=apple&price_max=2500');

console.log('Brand:', searchParams.get('brand')); // 'apple'
searchParams.append('tag', 'sale');
searchParams.set('price_max', '2000');

console.log('Query String mới:', searchParams.toString());
// category=laptops&brand=apple&price_max=2000&tag=sale""",
        "tips": "Trả lời câu này như một Senior: 'Module querystring hiện đã legacy/deprecated, trong production hiện nay chúng tôi luôn sử dụng WHATWG URL và URLSearchParams theo chuẩn ECMAScript quốc tế.'"
    },

    19: {
        "title_vi": "Cách quản lý và chuẩn hóa đường dẫn file với module `path` trong Node.js?",
        "level": "Junior",
        "short_answer": "Module `path` cung cấp các tiện ích để xử lý và biến đổi đường dẫn tệp. Các hàm phổ biến nhất bao gồm: `path.join()` (nối các chuỗi đường dẫn), `path.resolve()` (tạo đường dẫn tuyệt đối), `path.basename()`, `path.dirname()`, và `path.extname()`.",
        "deep_dive": """1. Khác biệt giữa `path.join()` và `path.resolve()`:
   - `path.join('/a', 'b', 'c')` đơn giản là nối các chuỗi lại với dấu gạch chéo chuẩn theo OS: `/a/b/c`.
   - `path.resolve('a', 'b')` hoạt động giống như lệnh `cd` trong terminal: nó phân giải đường dẫn tương đối thành một đường dẫn TUYỆT ĐỐI bắt đầu từ thư mục làm việc hiện tại (`process.cwd()`).
2. Đa nền tảng: Windows dùng dấu gạch chéo ngược `\\`, POSIX/Linux/macOS dùng `/`. Sử dụng `path` giúp code chạy mượt mà trên mọi hệ điều hành mà không bị lỗi gõ cứng (hardcoded slashes).""",
        "code_example": """const path = require('node:path');

const samplePath = '/projects/shop/public/images/logo.png';

console.log('Thư mục cha (dirname):', path.dirname(samplePath)); // /projects/shop/public/images
console.log('Tên file (basename):', path.basename(samplePath));   // logo.png
console.log('Đuôi mở rộng (extname):', path.extname(samplePath)); // .png

// path.resolve biến đổi thành đường dẫn tuyệt đối đầy đủ từ ổ đĩa
const absPath = path.resolve('data', 'users.json');
console.log('Đường dẫn tuyệt đối:', absPath);""",
        "tips": "Trong ES Modules (`type: \"module\"`), `__dirname` và `__filename` không tồn tại sẵn. Để tái tạo lại chúng: `import { fileURLToPath } from 'node:url'; const __dirname = path.dirname(fileURLToPath(import.meta.url));`."
    },

    20: {
        "title_vi": "Callbacks trong Node.js là gì?",
        "level": "Junior",
        "short_answer": "Callback là một hàm được truyền dưới dạng đối số (argument) vào một hàm khác, và được dự định gọi lại (call back) tại một thời điểm trong tương lai sau khi một tác vụ bất đồng bộ (như đọc file, query database) đã hoàn thành.",
        "deep_dive": """1. Cơ chế hoạt động: Hàm bất đồng bộ nhận callback, khởi chạy tác vụ ngầm ở tầng OS/libuv và kết thúc ngay. Khi tác vụ xong, libuv đẩy callback vào hàng đợi của Event Loop để V8 thực thi.
2. Error-First Callback Convention: Quy ước chuẩn mực của Node.js: tham số đầu tiên của callback luôn là đối tượng `Error` (hoặc `null` nếu không có lỗi), các tham số tiếp theo là dữ liệu kết quả.""",
        "code_example": """function getUserData(userId, callback) {
  setTimeout(() => {
    if (!userId) {
      return callback(new Error('UserId không được để trống'), null);
    }
    // Thành công: error = null, data = user object
    callback(null, { id: userId, name: 'Alex Johnson', role: 'Developer' });
  }, 100);
}

// Gọi hàm với error-first callback pattern
getUserData(101, (err, user) => {
  if (err) {
    return console.error('Lỗi xảy ra:', err.message);
  }
  console.log('Lấy thông tin thành công:', user.name);
});""",
        "tips": "Luôn kiểm tra `if (err) return callback(err);` đầu tiên trong callback để tránh lỗi unhandled exception hoặc tiếp tục thực thi code khi đã xảy ra lỗi."
    },

    21: {
        "title_vi": "Callback Hell là gì và có những cách nào để khắc phục?",
        "level": "Junior",
        "short_answer": "Callback Hell (hay Pyramid of Doom) là hiện tượng các hàm callback bị lồng nhau qua nhiều tầng liên tiếp khi thực hiện chuỗi các tác vụ bất đồng bộ phụ thuộc nhau, khiến code bị thụt lề sâu về bên phải, cực kỳ khó đọc, khó bảo trì và dễ bỏ sót việc bắt lỗi. Khắc phục bằng cách sử dụng Promises, Async/Await hoặc module hóa tách hàm.",
        "deep_dive": """1. Tác hại: Biến scope bị rối, luồng dữ liệu khó kiểm soát, logic bắt lỗi lặp đi lặp lại ở mỗi tầng callback.
2. Giải pháp 1: Tách các hàm con độc lập có tên riêng (Modularization).
3. Giải pháp 2: Chuyển đổi sang Promises và dùng cú pháp chuỗi `.then().catch()`.
4. Giải pháp 3 (Tối ưu nhất): Dùng `async/await` kết hợp `try/catch` giúp code bất đồng bộ trông phẳng và trực quan như code đồng bộ.""",
        "code_example": """// ❌ Callback Hell (Pyramid of Doom):
// getUser(id, (err, user) => {
//   getOrders(user.id, (err, orders) => {
//     getOrderDetails(orders[0].id, (err, details) => { ... })
//   })
// })

// ✅ Khắc phục bằng Async/Await phẳng và sạch đẹp:
async function displayOrderDetails(userId) {
  try {
    const user = await getUser(userId);
    const orders = await getOrders(user.id);
    const details = await getOrderDetails(orders[0].id);
    console.log('Chi tiết đơn hàng:', details);
  } catch (error) {
    console.error('Bắt lỗi tập trung tại 1 nơi:', error.message);
  }
}""",
        "tips": "Nếu gặp thư viện cũ chỉ hỗ trợ callback, bạn có thể biến đổi nhanh chóng thành Promise bằng hàm tiện ích có sẵn `const { promisify } = require('node:util');`."
    },

    22: {
        "title_vi": "Giải thích về Promises trong Node.js?",
        "level": "Junior",
        "short_answer": "Promise là một đối tượng đại diện cho kết quả cuối cùng (thành công hoặc thất bại) của một tác vụ bất đồng bộ. Một Promise có 3 trạng thái: Pending (đang chờ), Fulfilled (hoàn thành thành công với giá trị), và Rejected (thất bại với lý do/lỗi).",
        "deep_dive": """1. Bất biến (Immutability): Khi một Promise đã chuyển sang Fulfilled hoặc Rejected, trạng thái của nó được đóng băng vĩnh viễn và không thể thay đổi.
2. Chaining: Cho phép nối chuỗi các tác vụ tuần tự qua `.then()`, mỗi `.then()` trả về một Promise mới.
3. Utility Methods hữu ích:
   - `Promise.all([p1, p2])`: Chạy song song, thất bại ngay nếu 1 promise lỗi (Fail-fast).
   - `Promise.allSettled()`: Chờ TẤT CẢ promises hoàn thành dù thành công hay lỗi.
   - `Promise.race()`: Lấy kết quả của promise hoàn thành nhanh nhất.""",
        "code_example": """// Tạo một Promise
function checkServerStatus(url) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const isOnline = true;
      if (isOnline) resolve({ url, status: 'Online', code: 200 });
      else reject(new Error('Server Offline'));
    }, 200);
  });
}

// Chạy song song nhiều promises
Promise.allSettled([
  checkServerStatus('https://api.domain1.com'),
  checkServerStatus('https://api.domain2.com')
]).then(results => {
  results.forEach(res => {
    if (res.status === 'fulfilled') console.log('Thành công:', res.value);
    else console.log('Thất bại:', res.reason.message);
  });
});""",
        "tips": "Bắt buộc luôn có `.catch()` ở cuối chuỗi Promise, hoặc Node.js sẽ cảnh báo `UnhandledPromiseRejectionWarning` (và trong các phiên bản Node mới sẽ dừng tiến trình)."
    },

    23: {
        "title_vi": "Cách thức hoạt động của `async/await` trong Node.js?",
        "level": "Mid",
        "short_answer": "`async/await` là cú pháp 'đường cú pháp' (syntactic sugar) được xây dựng trên nền tảng của Promises và Generators. Từ khóa `async` biến một hàm thành một hàm luôn trả về một Promise, và từ khóa `await` tạm dừng việc thực thi bên trong hàm async cho đến khi Promise được giải quyết (resolve), mà không hề block luồng chính của Event Loop.",
        "deep_dive": """1. Dưới tầng V8: Khi gặp `await`, V8 lưu lại execution context của hàm async vào microtask queue và nhường quyền điều khiển CPU lại cho Event Loop để tiếp tục xử lý các sự kiện khác.
2. Xử lý lỗi: Dùng cấu trúc `try/catch` chuẩn của JavaScript, giúp bắt cả lỗi đồng bộ lẫn lỗi bất đồng bộ tại cùng một block code.
3. Chạy song song vs Tuần tự: Tránh việc lạm dụng `await` tuần tự các tác vụ độc lập. Hãy dùng `Promise.all([task1(), task2()])` để tối đa hóa hiệu năng I/O.""",
        "code_example": """async function fetchDashboardData(userId) {
  try {
    console.time('Fetch');
    
    // ✅ Chạy song song (Parallel) 2 tác vụ độc lập
    const [profile, notifications] = await Promise.all([
      fetchUserProfile(userId),
      fetchUserNotifications(userId)
    ]);
    
    console.timeEnd('Fetch');
    return { profile, notifications };
  } catch (error) {
    console.error('Lỗi tải dữ liệu dashboard:', error);
    throw error;
  }
}

async function fetchUserProfile(id) { return { id, name: 'Sarah' }; }
async function fetchUserNotifications(id) { return ['Thông báo 1', 'Thông báo 2']; }

fetchDashboardData('U123').then(data => console.log('Kết quả:', data));""",
        "tips": "Sai lầm phổ biến khi phỏng vấn: Viết `const a = await getA(); const b = await getB();` khi `getA` và `getB` hoàn toàn không phụ thuộc nhau. Điều này làm tăng gấp đôi thời gian phản hồi!"
    },

    24: {
        "title_vi": "Sự khác biệt giữa phương thức Đồng bộ (Sync) và Bất đồng bộ (Async) trong module `fs`?",
        "level": "Junior",
        "short_answer": "Phương thức Synchronous (ví dụ `fs.readFileSync`) thực thi trực tiếp trên luồng chính của Node.js, bắt toàn bộ Event Loop phải dừng lại chờ đợi ổ cứng đọc xong file. Phương thức Asynchronous (ví dụ `fs.readFile` hoặc `fs.promises.readFile`) giao tác vụ cho libuv thread pool chạy ngầm và gọi lại kết quả qua callback/promise, không làm gián đoạn các requests khác.",
        "deep_dive": """1. Khi nào được dùng Sync: Chỉ nên dùng các phương thức `Sync` trong giai đoạn khởi động server (Bootstrapping), ví dụ: nạp file cấu hình `config.json`, đọc chứng chỉ SSL trước khi mở port.
2. Khi nào cấm dùng Sync: Tuyệt đối cấm trong mọi route handler của HTTP server, WebSocket handler, hoặc bất kỳ nơi nào phục vụ người dùng concurrent. 1 hàm sync 100ms có thể làm nghẽn hàng nghìn requests đang đợi.""",
        "code_example": """const fs = require('node:fs');
const fsPromises = require('node:fs/promises');

// 1. Chỉ dùng khi khởi động ứng dụng
function loadConfigSync() {
  console.log('Nạp cấu hình ứng dụng (Sync)...');
  const raw = fs.readFileSync('package.json', 'utf8');
  return JSON.parse(raw);
}

// 2. Dùng trong runtime phục vụ người dùng
async function logUserAction(action) {
  // Hoàn toàn bất đồng bộ, không làm lag web server
  await fsPromises.appendFile('audit.log', `[${new Date().toISOString()}] ${action}\\n`);
}""",
        "tips": "Quy tắc vàng: 'Sync lúc Boot, Async lúc Run'."
    },

    25: {
        "title_vi": "Node.js xử lý các HTTP Requests và Responses như thế nào?",
        "level": "Mid",
        "short_answer": "Khi một client gửi HTTP Request, OS tạo một TCP socket kết nối với server. Parser HTTP nội bộ của Node.js (llhttp viết bằng C) sẽ phân tích gói tin stream. Đối tượng `IncomingMessage` (Readable Stream) và `ServerResponse` (Writable Stream) được khởi tạo và truyền vào callback của sự kiện `'request'`.",
        "deep_dive": """1. Phân luồng dữ liệu dạng Chunk: Dữ liệu body được chia thành các Buffer chunks phát ra qua sự kiện `'data'`. Khi kết thúc body, sự kiện `'end'` được kích hoạt.
2. Keep-Alive: Mặc định HTTP 1.1 tái sử dụng kết nối TCP cho nhiều requests tiếp theo của cùng một client để giảm độ trễ handshake TCP.
3. Xử lý Headers: Headers được gửi đi ngay khi dòng đầu tiên của body được ghi hoặc khi gọi `res.writeHead()`. Sau khi headers đã gửi, nếu cố gắng gọi `res.setHeader()` sẽ gây ra lỗi kinh điển `ERR_HTTP_HEADERS_SENT`.""",
        "code_example": """const http = require('node:http');

http.createServer((req, res) => {
  console.log(`Nhận request: ${req.method} ${req.url}`);
  
  // Kiểm tra header
  const userAgent = req.headers['user-agent'];
  
  // Set headers trả về
  res.setHeader('X-Powered-By', 'Node.js Core');
  res.writeHead(200, { 'Content-Type': 'application/json' });

  // Ghi body và hoàn tất
  res.end(JSON.stringify({
    message: 'Request đã được xử lý thành công',
    clientAgent: userAgent
  }));
}).listen(8080);""",
        "tips": "Lỗi `Error [ERR_HTTP_HEADERS_SENT]: Cannot set headers after they are sent to the client` là lỗi số 1 mà các lập trình viên Node.js hay gặp khi quên từ khóa `return` trước `res.send()` hoặc `res.end()`."
    },

    26: {
        "title_vi": "Express.js là gì và tại sao nó lại là framework quan trọng hàng đầu cho Node.js?",
        "level": "Junior",
        "short_answer": "Express.js là framework web tối giản (minimalist), linh hoạt và phổ biến nhất cho Node.js. Nó cung cấp một lớp trừu tượng thanh lịch trên module `http` thuần, bao gồm hệ thống định tuyến (Routing) mạnh mẽ, kiến trúc Middleware tiện dụng, xử lý request/response trực quan và hệ sinh thái plugin đồ sộ.",
        "deep_dive": """1. Giảm thiểu boilerplate: Nếu dùng `http` thuần, bạn phải tự phân tích URL, parse query, parse JSON body, xử lý CORS, map route thủ công. Express đóng gói tất cả những việc này chỉ với vài dòng lệnh.
2. Triết lý Unopinionated: Express không bắt buộc người dùng tuân theo cấu trúc thư mục cứng nhắc hay ORM cụ thể nào, trao quyền tự do cấu trúc cho kiến trúc sư phần mềm.
3. Cơ sở nền tảng: Hầu hết các framework lớn khác như NestJS, Sails.js, Feathers ban đầu đều xây dựng trên nền tảng của Express.""",
        "code_example": """const express = require('express');
const app = express();

// Middleware tích hợp parse JSON tự động
app.use(express.json());

// Định nghĩa route gọn gàng
app.get('/api/users/:id', (req, res) => {
  res.json({ id: req.params.id, name: 'Alice' });
});

app.listen(3000, () => console.log('Express app running on port 3000'));""",
        "tips": "Điểm cộng phỏng vấn: Nhấn mạnh Express hoạt động xoay quanh 2 khái niệm cốt lõi: 'Routing' và 'Middleware Chain'."
    },

    27: {
        "title_vi": "Cách xây dựng một RESTful API chuẩn mực với Node.js?",
        "level": "Mid",
        "short_answer": "Xây dựng RESTful API chuẩn mực yêu cầu: Sử dụng đúng các HTTP methods (GET, POST, PUT, PATCH, DELETE), đặt tên endpoint danh từ số nhiều (e.g., `/api/v1/products`), trả về HTTP status code chính xác (200, 201, 400, 401, 403, 404, 500), validate dữ liệu đầu vào (Zod/Joi), phân trang (pagination) và xử lý lỗi tập trung.",
        "deep_dive": """1. Statelessness: Mỗi request từ client phải chứa đầy đủ thông tin xác thực (ví dụ Bearer JWT), server không lưu session state.
2. Chuẩn hóa Status Code:
   - 200 OK (Thành công), 201 Created (Tạo mới thành công), 204 No Content (Xóa thành công).
   - 400 Bad Request (Sai định dạng payload), 401 Unauthorized (Chưa đăng nhập), 403 Forbidden (Không có quyền).
   - 404 Not Found, 429 Too Many Requests (Rate limit), 500 Internal Server Error.
3. Clean Architecture: Tách thành các lớp Controllers -> Services -> Repositories/Models.""",
        "code_example": """const express = require('express');
const app = express();
app.use(express.json());

let products = [{ id: 1, name: 'Bàn phím cơ', price: 150 }];

// GET: Lấy danh sách sản phẩm (có phân trang)
app.get('/api/v1/products', (req, res) => {
  res.status(200).json({ success: true, count: products.length, data: products });
});

// POST: Tạo mới sản phẩm
app.post('/api/v1/products', (req, res) => {
  const { name, price } = req.body;
  if (!name || !price) {
    return res.status(400).json({ success: false, message: 'Tên và giá là bắt buộc' });
  }
  const newProduct = { id: Date.now(), name, price };
  products.push(newProduct);
  res.status(201).json({ success: true, data: newProduct });
});""",
        "tips": "Nhớ áp dụng API Versioning ngay từ đầu (ví dụ `/api/v1/...`) để không làm gián đoạn các ứng dụng mobile/frontend cũ khi nâng cấp hệ thống."
    },

    28: {
        "title_vi": "Middleware trong ngữ cảnh Node.js / Express là gì?",
        "level": "Junior",
        "short_answer": "Middleware là các hàm trung gian có quyền truy cập vào đối tượng Request (`req`), Response (`res`), và hàm `next()` trong chu trình request-response của ứng dụng. Middleware có thể thực thi mã, thay đổi req/res, kết thúc chu trình trả response, hoặc gọi `next()` để chuyển quyền cho middleware kế tiếp.",
        "deep_dive": """1. Pipeline Pattern: Các middleware xếp thành một chuỗi (chain). Nếu một middleware không gọi `next()` và cũng không gửi response (ví dụ `res.send()`), request sẽ bị treo mãi mãi.
2. Các loại Middleware:
   - Application-level middleware: `app.use(fn)`
   - Router-level middleware: `router.use(fn)`
   - Error-handling middleware: Nhận đủ 4 tham số `(err, req, res, next)`
   - Built-in middleware: `express.json()`, `express.static()`
   - Third-party middleware: `cors`, `helmet`, `morgan`.""",
        "code_example": """const express = require('express');
const app = express();

// Middleware xác thực Token
const authMiddleware = (req, res, next) => {
  const token = req.headers['authorization'];
  if (token === 'Secret-Token-123') {
    req.user = { id: 1, role: 'admin' };
    return next(); // Cho phép đi tiếp vào route handler
  }
  return res.status(401).json({ error: 'Truy cập bị từ chối: Token không hợp lệ' });
};

app.get('/api/protected-dashboard', authMiddleware, (req, res) => {
  res.json({ message: `Chào mừng ${req.user.role}! Dữ liệu bảo mật đây.` });
});""",
        "tips": "Câu hỏi bẫy: 'Làm thế nào Express nhận biết một middleware là error-handler?' Trọng tâm: Express kiểm tra thuộc tính `fn.length === 4` (tức có đủ 4 tham số khai báo `(err, req, res, next)`)."
    },

    29: {
        "title_vi": "Cách bảo vệ an toàn HTTP Headers trong ứng dụng Node.js?",
        "level": "Mid",
        "short_answer": "Cách chuẩn mực và nhanh nhất là sử dụng thư viện `helmet`. Helmet tự động thiết lập hoặc loại bỏ các HTTP response headers quan trọng nhằm ngăn chặn các cuộc tấn công web phổ biến như XSS, Clickjacking, MIME sniffing, và ẩn thông tin công nghệ máy chủ.",
        "deep_dive": """Các headers an ninh quan trọng mà Helmet cấu hình:
1. `Content-Security-Policy` (CSP): Giới hạn nguồn gốc các script, style, hình ảnh được phép tải.
2. `X-Frame-Options: SAMEORIGIN` / `DENY`: Chống tấn công Clickjacking (không cho iframe trang web trên domain lạ).
3. `X-Content-Type-Options: nosniff`: Ngăn chặn trình duyệt tự ý đoán sai MIME type.
4. `Strict-Transport-Security` (HSTS): Bắt buộc trình duyệt chỉ kết nối qua HTTPS.
5. Ẩn `X-Powered-By`: Xóa header tiết lộ bạn đang dùng Node.js/Express để hacker không thể khai thác lỗ hổng đã biết.""",
        "code_example": """const express = require('express');
const helmet = require('helmet');

const app = express();

// Tích hợp 15 middleware bảo mật HTTP headers chỉ với 1 dòng
app.use(helmet());

// Tùy chỉnh cụ thể Content Security Policy nếu cần
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: [\"'self'\"],
      scriptSrc: [\"'self'\", \"https://trustedscripts.com\"],
    },
  })
);

app.get('/', (req, res) => res.send('Secure Node Server!'));""",
        "tips": "Nếu không dùng Helmet, tối thiểu bạn phải chạy `app.disable('x-powered-by')` để hacker không biết server chạy Express."
    },

    30: {
        "title_vi": "Cách xử lý lỗi (Error Handling) toàn diện trong ứng dụng Node.js?",
        "level": "Mid",
        "short_answer": "Xử lý lỗi toàn diện cần kết hợp nhiều tầng: (1) Dùng `try/catch` với async/await, (2) Tạo các class Error tùy biến kế thừa từ `Error`, (3) Cấu hình middleware xử lý lỗi tập trung trong framework, (4) Lắng nghe hai sự kiện toàn cục quan trọng của tiến trình: `process.on('uncaughtException')` và `process.on('unhandledRejection')`.",
        "deep_dive": """1. Phân loại lỗi:
   - Operational Errors (Lỗi vận hành): Dự đoán được (user nhập sai pass, file not found, db timeout). Cần xử lý êm đẹp và thông báo lỗi rõ ràng.
   - Programmer Errors (Lỗi lập trình): Bugs (truy cập property của undefined, syntax error). Cần log đầy đủ stacktrace và khởi động lại process an toàn.
2. Tại sao nên thoát process khi gặp `uncaughtException`: Vì khi xảy ra lỗi unhandled, trạng thái bộ nhớ của tiến trình có thể đã bị hỏng. Tiếp tục chạy có thể gây sai lệch dữ liệu người dùng.""",
        "code_example": """// 1. Lớp lỗi chuẩn cho ứng dụng
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

// 2. Bắt lỗi unhandled toàn cục
process.on('unhandledRejection', (reason, promise) => {
  console.error('CRITICAL: Phát hiện Unhandled Rejection:', reason);
  // Đóng kết nối an toàn và thoát, process manager (PM2) sẽ restart lại
  process.exit(1);
});

process.on('uncaughtException', (err) => {
  console.error('CRITICAL: Phát hiện Uncaught Exception:', err);
  process.exit(1);
});""",
        "tips": "Senior Tip: Trong production, không bao giờ để lộ full stacktrace của lỗi ra cho client vì hacker có thể nhìn thấy đường dẫn thư mục và cấu trúc database của bạn."
    },

    31: {
        "title_vi": "Mô hình Error-First Callback trong Node.js là gì?",
        "level": "Junior",
        "short_answer": "Error-First Callback (còn gọi là Node-style callback) là quy ước thiết kế chuẩn trong toàn bộ hệ sinh thái Node.js. Quy ước này quy định: Tham số ĐẦU TIÊN của hàm callback luôn dành cho đối tượng lỗi (`err`). Nếu thao tác thành công, `err` sẽ là `null` hoặc `undefined`, và kết quả trả về sẽ nằm ở các tham số tiếp theo.",
        "deep_dive": """1. Lý do ra đời: Trong môi trường bất đồng bộ, lập trình viên không thể dùng `try/catch` bọc bên ngoài lời gọi hàm để bắt lỗi xảy ra ở tương lai. Error-first callback đảm bảo lập trình viên luôn bắt buộc phải kiểm tra lỗi trước khi chạm vào dữ liệu.
2. Tiêu chuẩn chuyển đổi: Thư viện `util.promisify` hoạt động dựa trên giả định 100% các hàm tuân thủ đúng quy ước error-first callback.""",
        "code_example": """const fs = require('node:fs');

// Đọc file tuân thủ Error-First Callback
fs.readFile('database.json', 'utf8', (err, data) => {
  // BƯỚC 1: Luôn kiểm tra lỗi đầu tiên
  if (err) {
    console.error('Đã xảy ra lỗi đọc file:', err.code, err.message);
    return; // Dừng thực thi ngay lập tức
  }

  // BƯỚC 2: Khi chắc chắn không có lỗi mới xử lý data
  try {
    const parsed = JSON.parse(data);
    console.log('Dữ liệu đã nạp:', parsed);
  } catch (parseErr) {
    console.error('Lỗi cú pháp JSON:', parseErr.message);
  }
});""",
        "tips": "Hãy chú ý lỗi `err.code`: Các mã lỗi chuẩn OS như `ENOENT` (không tìm thấy file), `EACCES` (không có quyền truy cập) giúp xử lý logic chính xác thay vì so sánh chuỗi message."
    },

    32: {
        "title_vi": "Các kỹ thuật Debugging phổ biến nhất cho ứng dụng Node.js?",
        "level": "Mid",
        "short_answer": "Các kỹ thuật gỡ lỗi bao gồm: (1) Sử dụng cờ `--inspect` hoặc `--inspect-brk` để debug trực quan qua Chrome DevTools hoặc VS Code Debugger, (2) Dùng module `debug` với biến môi trường `DEBUG=*`, (3) Ghi log có cấu trúc bằng Pino/Winston, và (4) Phân tích Core Dump hoặc Heap Snapshot khi bị rò rỉ bộ nhớ.",
        "deep_dive": """1. Chrome DevTools qua V8 Inspector: Chạy `node --inspect server.js`, mở trình duyệt gõ `chrome://inspect`. Bạn có đầy đủ Breakpoints, Call Stack, Scope Variables, Watch Expressions y như debug trên frontend.
2. VS Code launch.json: Tạo cấu hình `pwa-node` với F5 để debug từng dòng mã trực tiếp trong IDE.
3. ND_DEBUG / console: Tránh lạm dụng `console.log` trong production vì `console.log` là blocking I/O khi ghi ra terminal/stdout!""",
        "code_example": """// .vscode/launch.json để debug 1-click trong VS Code
{
  \"version\": \"0.2.0\",
  \"configurations\": [
    {
      \"type\": \"pwa-node\",
      \"request\": \"launch\",
      \"name\": \"Debug Node.js App\",
      \"skipFiles\": [\"<node_internals>/**\"],
      \"program\": \"${workspaceFolder}/src/server.js\",
      \"restart\": true,
      \"console\": \"integratedTerminal\"
    }
  ]
}""",
        "tips": "Khi app bị treo (hang) trên production, hãy dùng lệnh `kill -USR1 <pid>` để kích hoạt inspector port trên một tiến trình Node.js đang chạy mà không cần khởi động lại nó!"
    },

    33: {
        "title_vi": "Giải thích chi tiết về `process.nextTick()`?",
        "level": "Senior",
        "short_answer": "`process.nextTick()` không phải là một phần kỹ thuật của Event Loop libuv. Thay vào đó, nó đưa callback vào một hàng đợi đặc biệt gọi là `nextTickQueue`. Hàng đợi này được Node.js vét sạch (xử lý ngay lập tức) ngay sau khi thao tác JavaScript hiện tại kết thúc, TRƯỚC KHI Event Loop tiếp tục bước sang pha kế tiếp.",
        "deep_dive": """1. Mức độ ưu tiên: `nextTickQueue` có độ ưu tiên cao hơn cả `Promise.then` (microtask queue) và cao hơn rất nhiều so với `setImmediate` hay `setTimeout`.
2. Nguy cơ làm đói I/O (I/O Starvation): Nếu bạn gọi đệ quy `process.nextTick()`, Event Loop sẽ bị 'bỏ đói' hoàn toàn vì không bao giờ đến được pha Poll để nhận I/O mới hay xử lý network!
3. Trường hợp sử dụng thực tế: Cho phép một hàm phát ra sự kiện hoặc chạy callback bất đồng bộ NGAY SAU KHI hàm gọi nó đã hoàn thành việc gán biến, nhưng trước khi bất kỳ I/O nào khác diễn ra.""",
        "code_example": """function createAsyncEmitter() {
  const EventEmitter = require('node:events');
  const emitter = new EventEmitter();
  
  // Dùng nextTick để listener kịp đăng ký trước khi sự kiện được bắn ra
  process.nextTick(() => {
    emitter.emit('ready', { status: 'Database connected' });
  });
  
  return emitter;
}

const myResource = createAsyncEmitter();
// Người dùng đăng ký listener đồng bộ ngay dòng tiếp theo
myResource.on('ready', (data) => {
  console.log('Nhận được sự kiện:', data.status); // Vẫn bắt được thành công!
});""",
        "tips": "Khuyên dùng: Hầu hết tài liệu chính thức của Node.js khuyên bạn nên ưu tiên dùng `setImmediate()` thay vì `process.nextTick()` để tránh nguy cơ nghẽn Event Loop."
    },

    34: {
        "title_vi": "Đối tượng toàn cục (`global`) trong Node.js là gì?",
        "level": "Junior",
        "short_answer": "`global` là đối tượng phạm vi cao nhất (global namespace) trong Node.js, tương đương với `window` trong trình duyệt. Mọi biến hoặc hàm được gắn vào `global` đều có thể truy cập ở bất kỳ file nào mà không cần `require` hay `import`. Từ ECMAScript 2020, `globalThis` được chuẩn hóa để dùng chung cho cả Node.js và Browser.",
        "deep_dive": """1. Các thuộc tính có sẵn trên global: `console`, `process`, `Buffer`, `setTimeout`, `setInterval`, `clearTimeout`, `setImmediate`.
2. Khác biệt với Browser: Trong trình duyệt, khai báo `var x = 10` sẽ tự động gắn `x` vào `window`. Nhưng trong Node.js, mỗi file là một Module khép kín được bọc trong Module Wrapper Function, nên `var x = 10` ở cấp root của file chỉ là biến cục bộ của module đó, KHÔNG bị lọt vào `global`.""",
        "code_example": """// Chuẩn quốc tế hiện đại: dùng globalThis
console.log(globalThis === global); // true trong Node.js

// Gắn một biến toàn cục (chỉ nên dùng khi cực kỳ cần thiết)
global.__APP_START_TIME__ = Date.now();

// Ở bất kỳ file nào khác:
console.log('App đã chạy được:', Date.now() - global.__APP_START_TIME__, 'ms');""",
        "tips": "Best practice: Tránh làm ô nhiễm global scope (`global pollution`). Luôn sử dụng cơ chế Module `import/export` rõ ràng để mã nguồn dễ kiểm thử và không bị xung đột tên biến ngầm."
    },

    35: {
        "title_vi": "Các framework phổ biến để kiểm thử (Testing) trong Node.js?",
        "level": "Mid",
        "short_answer": "Các framework phổ biến nhất bao gồm: Jest (all-in-one phổ biến nhất), Vitest (siêu nhanh dựa trên Vite), Mocha + Chai (linh hoạt, truyền thống), Supertest (kiểm thử HTTP endpoints), và Node.js Native Test Runner (`node:test` tích hợp sẵn từ Node v18+).",
        "deep_dive": """1. `node:test` (Native): Từ Node.js v18/v20+, bạn có thể viết test không cần cài thêm bất kỳ package bên ngoài nào (`npm i` không tốn MB nào cho testing framework).
2. Phân loại kiểm thử:
   - Unit Test: Kiểm tra hàm/service độc lập (Jest/Vitest).
   - Integration Test: Kiểm tra API kết nối DB thật hoặc testcontainers (Supertest).
   - E2E Test: Kiểm tra toàn bộ luồng nghiệp vụ.""",
        "code_example": """// Viết test bằng Node.js Native Test Runner (node:test) có sẵn
const test = require('node:test');
const assert = require('node:assert/strict');

function sum(a, b) {
  return a + b;
}

test('Hàm sum hoạt động chính xác', () => {
  assert.equal(sum(2, 3), 5);
  assert.notEqual(sum(1, 1), 3);
});

test('Kiểm tra hàm bất đồng bộ', async () => {
  const result = await Promise.resolve('Success');
  assert.strictEqual(result, 'Success');
});
// Chạy terminal: node --test""",
        "tips": "Điểm cộng phỏng vấn: Hãy giới thiệu rằng Node.js từ v18+ đã có sẵn `node:test` và `node:assert`, giúp giảm bớt kích thước phụ thuộc của project đáng kể khi không cần cài thêm Jest khổng lồ."
    },

    36: {
        "title_vi": "Khái niệm Mocking trong kiểm thử Node.js là gì?",
        "level": "Mid",
        "short_answer": "Mocking là kỹ thuật thay thế một thành phần phụ thuộc thực tế (như Database, Third-party Payment API, Email Service, File I/O) bằng một đối tượng giả lập (Mock/Stub/Spy) có hành vi được kiểm soát. Mục đích là để cô lập thành phần cần kiểm thử, đảm bảo bài test chạy nhanh, độc lập và ổn định.",
        "deep_dive": """1. Spy: Theo dõi xem một hàm có được gọi không, gọi bao nhiêu lần và với tham số nào.
2. Stub: Thay thế hàm thật và trả về dữ liệu mẫu định sẵn mà không thực thi logic thật bên dưới.
3. Mock: Đối tượng hoàn chỉnh có kỳ vọng cụ thể về các lời gọi hàm.
4. Thư viện phổ biến: Sinon.js, Jest (`jest.fn()`, `jest.spyOn()`, `jest.mock()`), hoặc `test.mock` trong native test runner.""",
        "code_example": """// Ví dụ Mocking với Jest
const paymentService = {
  chargeCreditCard: async (card, amount) => {
    // Trong thực tế, gọi sang Stripe API thật tốn tiền và mạng
    throw new Error('Không thể gọi API thật trong unit test!');
  }
};

// Kiểm thử logic xử lý thanh toán
async function checkout(cart, paymentFn) {
  const success = await paymentFn('CARD_123', cart.total);
  return success ? 'ORDER_CONFIRMED' : 'PAYMENT_FAILED';
}

// Trong file test:
const mockCharge = jest.fn().mockResolvedValue(true);

const result = await checkout({ total: 500 }, mockCharge);
expect(result).toBe('ORDER_CONFIRMED');
expect(mockCharge).toHaveBeenCalledTimes(1);
expect(mockCharge).toHaveBeenCalledWith('CARD_123', 500);""",
        "tips": "Quy tắc vàng: 'Unit test không bao giờ được phép gửi request mạng thật ra ngoài Internet hay ghi dữ liệu vào production database.'"
    },

    37: {
        "title_vi": "Tại sao Benchmarking (Đo lường hiệu năng) lại quan trọng trong Node.js?",
        "level": "Senior",
        "short_answer": "Benchmarking giúp định lượng chính xác hiệu năng của hệ thống (RPS - Requests Per Second, Latency p95/p99, Memory/CPU usage), phát hiện các điểm nghẽn (bottlenecks), kiểm chứng việc tối ưu hóa code có thực sự mang lại kết quả, và đảm bảo hệ thống đáp ứng được cam kết SLA khi lưu lượng người dùng tăng đột biến.",
        "deep_dive": """1. Công cụ benchmark HTTP: `autocannon` (viết bằng Node.js, siêu mạnh), `wrk`, `k6`, `Apache Bench (ab)`.
2. Micro-benchmarking: Dùng `benchmark.js` để so sánh tốc độ giữa các thuật toán/hàm nội bộ.
3. Chú ý V8 JIT Warmup: V8 cần thời gian thực thi nhiều lần (warmup) để tối ưu hóa mã qua TurboFan. Khi benchmark cần chạy warm-up phase trước khi lấy số liệu thống kê chính thức.""",
        "code_example": """# Sử dụng autocannon để load test HTTP API 
# 100 kết nối đồng thời trong vòng 20 giây:
npx autocannon -c 100 -d 20 -p 10 http://localhost:3000/api/products

# Kết quả quan trọng cần đọc:
# - Latency (Average, p99): Độ trễ phản hồi của 99% users
# - Req/Sec: Số request server gánh được trong 1 giây
# - 2xx/Non-2xx: Tỉ lệ thành công và lỗi""",
        "tips": "Senior Tip: Đừng chỉ nhìn vào tốc độ trung bình (Average Latency). Trong thế giới thực, p99 Latency (1% người dùng gặp độ trễ cao nhất) mới là thước đo phản ánh độ mượt mà của hệ thống khi có nghẽn I/O."
    },

    38: {
        "title_vi": "Cách kiểm thử một HTTP Server trong Node.js với `supertest`?",
        "level": "Mid",
        "short_answer": "`supertest` là thư viện trừu tượng hóa việc kiểm thử các endpoint HTTP trong Node.js. Nó cho phép gửi các HTTP requests giả lập trực tiếp đến đối tượng `app` của Express/HTTP mà không cần phải thực sự bind vào một cổng mạng thực tế (`listen`), giúp các bài test chạy cực kỳ nhanh và không lo xung đột cổng mạng (port collision).",
        "deep_dive": """1. Cơ chế: Supertest tận dụng hàm `server.listen(0)` ngầm để cấp phát một ephemeral port ngẫu nhiên, hoặc truyền trực tiếp đối tượng request vào handler.
2. Assertions: Supertest tích hợp sẵn các assertion cho status code, header, content-type và body JSON, hoặc có thể kết hợp với Jest `expect()`.""",
        "code_example": """const request = require('supertest');
const express = require('express');

// Khởi tạo app (không gọi app.listen)
const app = express();
app.get('/api/users', (req, res) => {
  res.status(200).json([{ id: 1, name: 'John Doe' }]);
});

// Viết bài test
describe('GET /api/users', () => {
  it('phải trả về danh sách users với status 200 và content-type JSON', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect('Content-Type', /json/)
      .expect(200);

    expect(Array.isArray(response.body)).toBe(true);
    expect(response.body[0].name).toBe('John Doe');
  });
});""",
        "tips": "Luôn tách file khởi tạo `app.js` (chỉ chứa route và middleware) riêng biệt với file `server.js` (chứa `app.listen(PORT)`). Điều này giúp việc import `app` vào bài test bằng supertest hoàn toàn trong sạch."
    },

    39: {
        "title_vi": "Cách kết nối cơ sở dữ liệu MySQL với Node.js và quản lý Connection Pool?",
        "level": "Mid",
        "short_answer": "Sử dụng thư viện `mysql2` (khuyên dùng `mysql2/promise` thay vì `mysql` cũ). Trong môi trường sản xuất, BẮT BUỘC phải sử dụng Connection Pool (`createPool`) thay vì tạo kết nối đơn lẻ (`createConnection`) để tái sử dụng các kết nối TCP đã mở sẵn, giảm độ trễ và tránh làm sập database server khi có nhiều truy vấn đồng thời.",
        "deep_dive": """1. Connection Pool: Quản lý sẵn một nhóm kết nối mở (ví dụ 10-20 connections). Khi có query, lấy 1 connection từ pool, thực thi xong trả lại pool cho request khác mượn.
2. Chống SQL Injection: Luôn sử dụng Parameterized Queries (truyền mảng `[values]` vào dấu hỏi chấm `?`), không bao giờ ghép chuỗi (string concatenation) câu lệnh SQL.""",
        "code_example": """const mysql = require('mysql2/promise');

// Khởi tạo Connection Pool
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'secret',
  database: 'ecommerce_db',
  waitForConnections: true,
  connectionLimit: 15, // Tối đa 15 kết nối đồng thời
  queueLimit: 0
});

async function getUserById(userId) {
  // ✅ An toàn chống SQL Injection với Prepared Statements
  const query = 'SELECT id, email, created_at FROM users WHERE id = ?';
  const [rows] = await pool.execute(query, [userId]);
  return rows[0];
}""",
        "tips": "Ưu tiên dùng `pool.execute()` thay vì `pool.query()` trong `mysql2` vì `execute` tận dụng cơ chế binary prepared statements ở tầng database server, vừa bảo mật hơn vừa nhanh hơn."
    },

    40: {
        "title_vi": "Cách sử dụng NoSQL Database như MongoDB trong Node.js với Mongoose?",
        "level": "Mid",
        "short_answer": "MongoDB kết nối hoàn hảo với Node.js thông qua MongoDB Native Driver hoặc ODM (Object Data Modeling) như Mongoose. Mongoose cung cấp giải pháp lập mô hình dữ liệu có cấu trúc Schema rõ ràng, xác thực dữ liệu tự động (validation), quản lý middleware hooks (pre/post save) và tự động quản lý Connection Pooling.",
        "deep_dive": """1. BSON & JSON: MongoDB lưu trữ dưới dạng BSON (Binary JSON), tương thích tự nhiên 100% với các đối tượng JavaScript trong Node.js.
2. Connection Management: `mongoose.connect()` duy trì một connection pool ngầm (mặc định maxPoolSize = 100), tự động kết nối lại khi mất mạng (auto-reconnect).
3. Lean Queries: Dùng `.lean()` khi chỉ đọc dữ liệu để tăng tốc độ truy vấn gấp 3-5 lần bằng cách trả về plain JS object thay vì Mongoose Hydrated Documents.""",
        "code_example": """const mongoose = require('mongoose');

// Định nghĩa Schema
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true, lowercase: true },
  age: { type: Number, min: 18 },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

async function bootstrap() {
  await mongoose.connect('mongodb://localhost:27017/my_app', {
    maxPoolSize: 20
  });

  // Tối ưu hóa đọc dữ liệu với .lean()
  const users = await User.find({ age: { $gte: 20 } }).lean();
  console.log('Users:', users);
}""",
        "tips": "Senior Tip: Luôn thêm `.lean()` cho các query chỉ dùng để đọc (GET requests). Mongoose document bình thường chứa rất nhiều getters, setters và internal state, tiêu tốn rất nhiều RAM nếu trả về hàng nghìn records."
    },

    41: {
        "title_vi": "Vai trò của ORM/ODM trong Node.js và so sánh các giải pháp hiện đại?",
        "level": "Mid",
        "short_answer": "ORM (Object-Relational Mapping - cho SQL) và ODM (Object-Document Mapping - cho NoSQL) đóng vai trò làm cầu nối giữa code hướng đối tượng trong Node.js và hệ quản trị cơ sở dữ liệu. Nó giúp quản lý Database Migrations, cung cấp Type Safety, tự động sinh SQL queries, chống SQL injection và tăng tốc độ phát triển phần mềm.",
        "deep_dive": """1. Các ORM nổi bật hiện nay:
   - Prisma: ORM thế hệ mới phổ biến nhất, Type-safe tự động từ schema, syntax hiện đại, DX (Developer Experience) xuất sắc.
   - Drizzle ORM: Siêu nhẹ, gần sát với SQL thuần, hiệu năng cao nhất, không có overhead.
   - TypeORM / Sequelize: Các ORM truyền thống theo phong cách ActiveRecord / Data Mapper (thường dùng trong NestJS).
2. Đánh đổi (Trade-offs): ORM sinh ra câu query trừu tượng, đôi khi có thể tạo ra các câu SQL suboptimal nếu không kiểm soát (vấn đề N+1 queries). Với các báo cáo phức tạp, viết raw SQL vẫn tối ưu hơn.""",
        "code_example": """// Ví dụ cú pháp truy vấn Type-Safe với Prisma ORM
// const user = await prisma.user.findUnique({
//   where: { email: 'alice@prisma.io' },
//   include: { posts: true } // Tự động JOIN an toàn
// });""",
        "tips": "Khi phỏng vấn Senior, hãy nêu rõ quan điểm: 'ORM rất tốt cho 80% tác vụ CRUD hàng ngày và migrations. Nhưng với 20% các tác vụ báo cáo tài chính, aggregate phức tạp, tôi luôn chủ động viết Raw SQL có đánh index cẩn thận để đảm bảo hiệu năng.'"
    },

    42: {
        "title_vi": "Cách giám sát và theo dõi hiệu năng (Performance Monitoring) của ứng dụng Node.js trong Production?",
        "level": "Senior",
        "short_answer": "Giám sát hiệu năng Node.js cần bao quát 3 khía cạnh: (1) Số liệu hạ tầng & runtime (Event Loop lag, CPU usage, V8 Memory Heap), (2) APM (Application Performance Monitoring - Datadog, New Relic, Prometheus + Grafana), và (3) Logging tập trung (ELK Stack, OpenTelemetry) kết hợp cảnh báo tự động.",
        "deep_dive": """1. Event Loop Lag: Chỉ số sinh tử của Node.js! Nếu event loop delay > 100ms, nghĩa là ứng dụng đang bị nghẽn CPU hoặc có synchronous blocking code.
2. V8 Garbage Collection Metrics: Theo dõi tần suất và thời gian dừng của GC (Major vs Minor GC pauses).
3. OpenTelemetry: Chuẩn công nghiệp mã nguồn mở để theo dõi Distributed Tracing xuyên suốt các microservices.""",
        "code_example": """// Đo lường Event Loop Delay bằng core module `perf_hooks` (tích hợp sẵn)
const { monitorEventLoopDelay } = require('node:perf_hooks');

const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();

// Định kỳ mỗi 10 giây xuất số liệu sang hệ thống giám sát (Prometheus)
setInterval(() => {
  const p99DelayMs = (h.percentile(99) / 1e6).toFixed(2);
  const maxDelayMs = (h.max / 1e6).toFixed(2);
  
  console.log(`[Metrics] Event Loop Lag - p99: ${p99DelayMs}ms | Max: ${maxDelayMs}ms`);
  
  if (p99DelayMs > 100) {
    console.warn('CẢNH BÁO: Event loop đang bị delay nghiêm trọng!');
  }
  h.reset();
}, 10000);""",
        "tips": "Nếu nhà tuyển dụng hỏi 'Bạn dùng metrics gì để xác định Node server sắp quá tải?', câu trả lời hay nhất là: 'Event Loop Delay và Resident Set Size (RSS) memory, chứ không đơn thuần chỉ nhìn vào CPU usage.'"
    },

    43: {
        "title_vi": "Clustering trong Node.js là gì và nó hoạt động như thế nào?",
        "level": "Senior",
        "short_answer": "Clustering là cơ chế cho phép tận dụng tối đa tất cả các nhân (cores) của CPU trên máy chủ bằng cách khởi tạo một nhóm các tiến trình Node.js con (workers) cùng chia sẻ một cổng mạng duy nhất. Module `cluster` sử dụng tiến trình cha (Primary/Master) để phân phối các kết nối đến các tiến trình con bằng thuật toán Round-Robin.",
        "deep_dive": """1. Cơ chế chia sẻ Port: Master process lắng nghe trên cổng (ví dụ 3000), khi có kết nối TCP mới, Master chuyển giao trực tiếp socket file descriptor qua kênh IPC (Inter-Process Communication) cho một worker rảnh rỗi.
2. Độc lập bộ nhớ: Mỗi worker là một process độc lập với V8 instance và memory heap riêng biệt (~30MB-50MB RAM mỗi worker). Nếu một worker bị crash do lỗi, Master có thể fork ngay worker mới thay thế (Zero Downtime).
3. Hạn chế: Vì không chia sẻ bộ nhớ, trạng thái phiên (sessions) hoặc cache trong RAM biến cục bộ không thể dùng chung giữa các workers -> Cần Redis làm external store.""",
        "code_example": """const cluster = require('node:cluster');
const http = require('node:http');
const os = require('node:os');

if (cluster.isPrimary) {
  const numCPUs = os.cpus().length;
  console.log(`Primary Master ${process.pid} đang khởi chạy trên ${numCPUs} CPU cores...`);

  // Fork các workers bằng số nhân CPU
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Tự động hồi sinh worker nếu bị chết (Auto-recovery)
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} bị dừng (${signal || code}). Đang tạo worker mới...`);
    cluster.fork();
  });
} else {
  // Các Workers cùng chia sẻ port 8000
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Phản hồi từ Worker PID: ${process.pid}\\n`);
  }).listen(8000);
  
  console.log(`Worker ${process.pid} đã sẵn sàng.`);
}""",
        "tips": "Trong thực tế production với Docker và Kubernetes, người ta thường ít tự viết code `cluster` thủ công mà để Kubernetes quản lý các Pods, hoặc dùng PM2 Cluster Mode (`pm2 start app.js -i max`)."
    },

    44: {
        "title_vi": "Cách phát hiện và ngăn ngừa rò rỉ bộ nhớ (Memory Leaks) trong ứng dụng Node.js?",
        "level": "Senior",
        "short_answer": "Rò rỉ bộ nhớ trong Node.js xảy ra khi các đối tượng không còn sử dụng nhưng vẫn bị tham chiếu bởi một chuỗi tham chiếu gốc (GC Root), khiến V8 Garbage Collector không thể thu hồi. Các nguyên nhân phổ biến nhất: Biến toàn cục vô tình tạo ra, Closures giữ lại scope lớn, EventListeners không được gỡ bỏ, và lưu trữ Cache trong bộ nhớ trong (in-memory) không có giới hạn.",
        "deep_dive": """1. Các nguyên nhân hàng đầu:
   - `EventEmitter` leaks: Gắn listener vào singleton event mà quên `.removeListener()`.
   - In-memory Object Cache: Dùng một object `const cache = {}` lưu trữ mọi thứ mãi mãi mà không dùng thuật toán LRU (Least Recently Used) hay giới hạn TTL.
   - Timers (`setInterval`): Quên gọi `clearInterval`.
2. Cách phát hiện:
   - Chụp Heap Snapshots bằng `--inspect` qua Chrome DevTools hoặc `v8.getHeapSnapshot()`.
   - So sánh 2 file snapshot (Comparison View) để tìm đối tượng nào tăng đột biến.""",
        "code_example": """// ❌ NGUY CƠ RÒ RỈ BỘ NHỚ:
const leakCache = [];
function handleRequest(req) {
  leakCache.push(req); // Giữ tham chiếu toàn bộ request mãi mãi trong RAM!
}

// ✅ GIẢI PHÁP AN TOÀN: Dùng LRU Cache có giới hạn dung lượng
const { LRUCache } = require('lru-cache');

const safeCache = new LRUCache({
  max: 1000, // Tối đa 1000 phần tử, tự động loại bỏ phần tử cũ nhất
  ttl: 1000 * 60 * 5 // Hết hạn sau 5 phút
});

safeCache.set('user:101', { name: 'Dan' });""",
        "tips": "Cách Senior trả lời khi ứng dụng leak RAM: 'Tôi sẽ cấu hình cảnh báo RSS memory, dùng cờ `--max-old-space-size` để khống chế heap, sau đó kích hoạt dump Heap Snapshot tự động khi heap vượt ngưỡng 85% để phân tích GC retained size.'"
    },

    45: {
        "title_vi": "Mục đích và cách sử dụng cờ `--inspect` trong Node.js?",
        "level": "Junior",
        "short_answer": "Cờ `--inspect` kích hoạt V8 Inspector bên trong tiến trình Node.js, mở một cổng WebSocket lắng nghe (mặc định là `127.0.0.1:9229`) để các công cụ bên ngoài như Chrome DevTools, VS Code, hoặc WebStorm kết nối vào và điều khiển việc gỡ lỗi (debugging), theo dõi biến, đặt breakpoint và chụp memory snapshot.",
        "deep_dive": """1. `--inspect` vs `--inspect-brk`:
   - `--inspect`: Chạy server bình thường và mở port debug.
   - `--inspect-brk`: Mở port debug và TẠM DỪNG TIẾN TRÌNH ngay tại dòng code đầu tiên, giúp bạn kịp đặt breakpoint trước khi bất kỳ logic nào chạy.
2. Bảo mật: Mặc định lắng nghe trên `localhost`. Tuyệt đối không bao giờ mở `--inspect=0.0.0.0:9229` ra Internet công cộng vì bất kỳ ai cũng có thể thực thi mã tùy ý trên máy chủ qua debugger protocol!""",
        "code_example": """# Khởi động app với cờ inspect
node --inspect app.js

# Hoặc dừng ngay dòng đầu tiên để chờ debugger gắn vào
node --inspect-brk app.js

# Mở Google Chrome và truy cập:
# chrome://inspect
# Bấm vào "Open dedicated DevTools for Node" để bắt đầu debug.""",
        "tips": "Nếu muốn đổi port mặc định: `node --inspect=9230 app.js`."
    },

    46: {
        "title_vi": "Node.js xử lý bài toán đồng thời (Concurrency) như thế nào dù là đơn luồng?",
        "level": "Senior",
        "short_answer": "Node.js xử lý đồng thời dựa trên kiến trúc Non-blocking I/O và Reactor Pattern. Bản thân code JavaScript chạy trên một luồng duy nhất (Single Thread), nhưng các thao tác I/O tốn thời gian (Network, Disk, Database) được ủy thác cho hạt nhân hệ điều hành (thông qua epoll trên Linux, kqueue trên macOS, IOCP trên Windows) hoặc libuv thread pool. Khi có kết quả, Event Loop đưa callback vào thực thi tuần tự mà không có hiện tượng race condition ở mức luồng.",
        "deep_dive": """1. Phân biệt Concurrency vs Parallelism:
   - Concurrency (Đồng thời): Xử lý nhiều việc trong cùng một khoảng thời gian bằng cách chuyển đổi giữa chúng (giao việc cho OS và tiếp tục nhận request mới). Đây là cách Node.js hoạt động.
   - Parallelism (Song song): Thực sự chạy nhiều tác vụ cùng một thời điểm trên nhiều CPU cores vật lý (Node.js dùng Worker Threads hoặc Cluster để đạt được điều này).
2. Lợi thế: Không cần khóa đồng bộ (mutexes, locks, semaphores) nên hoàn toàn tránh được lỗi Deadlock phức tạp của các ngôn ngữ đa luồng truyền thống.""",
        "code_example": """// Minh họa Concurrency: 3 requests được gửi đi gần như cùng 1 thời điểm
// Không cái nào phải chờ cái nào hoàn thành mới được kích hoạt!
console.time('Concurrency');

Promise.all([
  fetch('https://httpbin.org/delay/1'),
  fetch('https://httpbin.org/delay/1'),
  fetch('https://httpbin.org/delay/1')
]).then(() => {
  // Tổng thời gian chỉ mất ~1 giây thay vì 3 giây tuần tự!
  console.timeEnd('Concurrency');
});""",
        "tips": "Khái niệm mấu chốt để ghi điểm tuyệt đối: 'Reactor Pattern' và 'Asynchronous Non-blocking Event Demultiplexer'."
    },

    47: {
        "title_vi": "Sự khác biệt giữa module `process` và module `child_process` trong Node.js?",
        "level": "Mid",
        "short_answer": "`process` là một đối tượng toàn cục cung cấp thông tin và quyền kiểm soát đối với chính tiến trình Node.js ĐANG CHẠY HIỆN TẠI (như PID, môi trường, bộ nhớ, thoát ứng dụng). Trong khi đó, `child_process` là một module dùng để sinh ra (spawn) CÁC TIẾN TRÌNH CON MỚI riêng biệt từ tiến trình cha nhằm chạy các lệnh hệ điều hành hoặc file script khác.",
        "deep_dive": """1. `process`: Cho phép truy cập `process.env`, `process.argv`, `process.memoryUsage()`, `process.exit()`.
2. `child_process`: Cung cấp 4 phương thức chính:
   - `spawn()`: Tối ưu cho dữ liệu luồng lớn (Stream data).
   - `exec()`: Chạy lệnh shell và gom toàn bộ output vào buffer (có giới hạn buffer size).
   - `execFile()`: Chạy trực tiếp file thực thi nhị phân mà không qua shell (an toàn hơn exec).
   - `fork()`: Biến thể đặc biệt của spawn để tạo tiến trình Node.js con mới, tự động thiết lập kênh giao tiếp 2 chiều IPC (Inter-Process Communication).""",
        "code_example": """const { exec, fork } = require('node:child_process');

// 1. Chạy lệnh shell với exec
exec('node -v', (err, stdout) => {
  console.log('Phiên bản Node con:', stdout.trim());
});

// 2. Fork một tiến trình Node.js con và giao tiếp qua IPC
// const child = fork('./heavy-computation.js');
// child.send({ task: 'calculate' });
// child.on('message', (result) => console.log('Kết quả từ con:', result));""",
        "tips": "Cẩn trọng lỗ hổng Command Injection khi dùng `exec()`. Nếu nhận tham số từ người dùng truyền vào chuỗi lệnh shell, kẻ tấn công có thể chèn dấu chấm phẩy `; rm -rf /` để phá hoại server. Luôn ưu tiên dùng `spawn` hoặc `execFile` với mảng tham số riêng biệt."
    },

    48: {
        "title_vi": "Worker Threads hoạt động như thế nào trong Node.js?",
        "level": "Senior",
        "short_answer": "`worker_threads` (từ Node.js v12+) cho phép thực thi mã JavaScript đa luồng thực sự trên các nhân CPU khác nhau bên trong CÙNG MỘT TIẾN TRÌNH. Khác với `child_process` tạo process mới tốn kém bộ nhớ, các Worker Threads chia sẻ chung bộ nhớ thông qua `SharedArrayBuffer` và giao tiếp bất đồng bộ qua `MessagePort`.",
        "deep_dive": """1. Kiến trúc bên trong: Mỗi Worker Thread có một V8 Isolate riêng biệt, một Context riêng và một Event Loop riêng của nó.
2. Dữ liệu truyền nhận:
   - Mặc định sử dụng HTML structured clone algorithm (sao chép đối tượng).
   - Dùng `SharedArrayBuffer` hoặc `ArrayBuffer` dạng Transferable Objects để chuyển giao quyền sở hữu bộ nhớ ngay lập tức (zero-copy overhead).
3. Thread Pool Pattern: Không nên tạo và hủy worker liên tục (do chi phí khởi động V8 Isolate). Hãy sử dụng thư viện như `piscina` để duy trì một Worker Thread Pool tái sử dụng.""",
        "code_example": """// heavy-task.js (Worker code)
const { parentPort, workerData } = require('node:worker_threads');

function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(workerData.number);
parentPort.postMessage(result);

// main.js
// const { Worker } = require('node:worker_threads');
// const worker = new Worker('./heavy-task.js', { workerData: { number: 42 } });
// worker.on('message', (ans) => console.log('Fibonacci(42) =', ans));""",
        "tips": "Nhớ: Worker Threads chỉ dùng cho CPU-intensive tasks (mã hóa, thuật toán phức tạp, nén dữ liệu). Đừng dùng Worker Threads cho các tác vụ I/O (Database, Network) vì Event Loop mặc định của Node.js đã làm việc đó hiệu quả hơn rất nhiều."
    },

    49: {
        "title_vi": "Node.js được áp dụng trong kiến trúc Microservices như thế nào?",
        "level": "Mid",
        "short_answer": "Node.js là một trong những lựa chọn hàng đầu cho kiến trúc Microservices nhờ tốc độ khởi động cực nhanh (fast cold start), dung lượng container siêu nhẹ, khả năng xử lý I/O cao cho các API Gateway và tích hợp tự nhiên với các giao thức giao tiếp microservice hiện đại như gRPC, HTTP/REST, WebSockets và Message Brokers (RabbitMQ, Kafka).",
        "deep_dive": """1. Tối ưu tài nguyên: Một container Node.js chạy Alpine Linux chỉ tốn ~50MB RAM, cho phép chạy hàng chục dịch vụ nhỏ trên cùng một cụm máy chủ mà không tốn kém tài nguyên như Java Spring Boot.
2. API Gateway: Node.js thường được dùng làm API Gateway để tổng hợp dữ liệu (BFF - Backend For Frontend), định tuyến, xác thực JWT và rate-limiting.
3. Resilience (Khả năng chịu lỗi): Áp dụng các mẫu thiết kế Circuit Breaker (dùng thư viện `opossum`) để ngăn chặn việc sập dây chuyền (cascading failures).""",
        "code_example": """// Ví dụ mô hình BFF / API Gateway đơn giản với Node.js
const express = require('express');
const axios = require('axios');
const app = express();

app.get('/api/user-dashboard/:id', async (req, res) => {
  const userId = req.params.id;
  try {
    // Gọi đồng thời đến 2 microservices độc lập
    const [userRes, ordersRes] = await Promise.all([
      axios.get(`http://user-service:4001/users/${userId}`),
      axios.get(`http://order-service:4002/orders/user/${userId}`)
    ]);

    res.json({
      user: userRes.data,
      recentOrders: ordersRes.data
    });
  } catch (error) {
    res.status(502).json({ error: 'Một trong các microservices thượng nguồn bị lỗi' });
  }
});""",
        "tips": "Điểm cộng Senior: Thảo luận về 'Distributed Tracing' với OpenTelemetry và giải pháp xử lý 'Distributed Transactions' bằng Saga Pattern thay vì 2-Phase Commit."
    },

    50: {
        "title_vi": "Giải thích các cơ chế giao tiếp liên tiến trình (IPC) trong kiến trúc Node.js?",
        "level": "Senior",
        "short_answer": "IPC (Inter-Process Communication) cho phép các tiến trình Node.js trao đổi thông tin với nhau. Các cơ chế chính bao gồm: (1) Built-in IPC Channel qua `child_process.fork()` bằng hàm `send()` và sự kiện `'message'`, (2) Unix Domain Sockets / Windows Named Pipes qua core module `net`, (3) Shared Memory qua `SharedArrayBuffer` trong worker threads, và (4) Network-based IPC qua Redis Pub/Sub, gRPC hoặc RabbitMQ cho các tiến trình trên các server khác nhau.",
        "deep_dive": """1. Node.js Built-in IPC: Dưới nền tảng sử dụng Unix domain sockets (trên Linux/macOS) hoặc Named Pipes (trên Windows). Dữ liệu được tuần tự hóa dạng JSON qua stream nhị phân.
2. Truyền File Descriptor: Một tính năng cực kỳ mạnh của Node.js IPC là khả năng gửi đối tượng Socket hoặc Server thực sự từ tiến trình cha sang tiến trình con (`child.send('server', serverHandle)`). Đây chính là cách module `cluster` phân phối kết nối TCP!""",
        "code_example": """// master.js
const { fork } = require('node:child_process');
const worker = fork('./worker.js');

// Gửi tin nhắn qua kênh IPC tích hợp
worker.send({ command: 'START_TASK', payload: { taskId: 999 } });

// Lắng nghe kết quả trả về từ worker
worker.on('message', (msg) => {
  console.log('Nhận tin nhắn từ Worker:', msg);
});

// worker.js
process.on('message', (msg) => {
  if (msg.command === 'START_TASK') {
    // Xử lý logic...
    process.send({ status: 'COMPLETED', taskId: msg.payload.taskId });
  }
});""",
        "tips": "Khi trao đổi dữ liệu dung lượng lớn qua IPC giữa các tiến trình trên cùng 1 server vật lý, Unix Domain Sockets nhanh hơn kết nối TCP Loopback (`localhost`) từ 20-30% vì không phải đi qua toàn bộ network stack của OS."
    }
}
