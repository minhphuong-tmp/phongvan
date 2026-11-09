"""Vue.js Interview Questions & Answers Database (Part 1: Q1 - Q50)"""

VUE_ANSWERS_PART1 = {
    1: {
        "title_vi": "Vue.js là gì và tại sao bạn lại lựa chọn Vue.js cho dự án?",
        "level": "Junior",
        "short_answer": "Vue.js là một framework JavaScript tiến bộ (Progressive Framework) dùng để xây dựng giao diện người dùng (UI) và các ứng dụng đơn trang (SPA). Điểm mạnh vượt trội của Vue là tính linh hoạt: có thể dùng như một thư viện nhúng đơn giản bằng thẻ `<script>` (tương tự jQuery) hoặc mở rộng thành một framework toàn diện với SFC, Vue Router, Pinia và Vite. Vue có đường cong học tập cực kỳ êm ái, cú pháp trực quan và hệ thống phản ứng (Reactivity) mạnh mẽ.",
        "deep_dive": """1. Triết lý Tiến bộ (Progressive): Bạn có thể áp dụng Vue vào một phần nhỏ của trang web hiện có mà không cần cấu hình build phức tạp, sau đó dần dần mở rộng ra toàn bộ dự án khi cần.
2. Hệ sinh thái chính chủ (First-party ecosystem): Router, State Management (Pinia), Build Tool (Vite), DevTools đều do chính đội ngũ nòng cốt của Vue phát triển và duy trì, đảm bảo tính đồng bộ và ổn định cao.
3. So sánh nhanh:
   - So với React: Vue có template syntax trực quan hơn JSX với nhiều người mới, ít boilerplate hơn, reactivity tự động theo dõi dependencies mà không cần lo lắng về dependency array như trong `useEffect`.
   - So với Angular: Vue nhẹ hơn rất nhiều, linh hoạt hơn và không ép buộc cấu trúc OOP/TypeScript ngặt nghèo ngay từ đầu.""",
        "code_example": """<!-- Khởi tạo nhanh Vue 3 với CDN không cần cài đặt build tool -->
<div id=\"app\">
  <h1>{{ message }}</h1>
  <button @click=\"count++\">Đã bấm: {{ count }} lần</button>
</div>

<script type=\"module\">
  import { createApp, ref } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';

  createApp({
    setup() {
      const message = ref('Xin chào từ Vue.js 3!');
      const count = ref(0);
      return { message, count };
    }
  }).mount('#app');
</script>""",
        "tips": "Điểm cộng phỏng vấn: Hãy nhắc đến khái niệm 'Approachable, Performant and Versatile' - 3 từ khóa định vị cốt lõi của Vue 3."
    },

    2: {
        "title_vi": "Cách thiết lập một dự án Vue.js chuẩn mực hiện nay?",
        "level": "Junior",
        "short_answer": "Cách chuẩn mực, hiện đại và nhanh nhất hiện nay là sử dụng lệnh chính thức `npm create vue@latest`. Công cụ này sử dụng Vite làm Build Tool mặc định (thay thế hoàn toàn Vue CLI cũ dựa trên Webpack), cung cấp trình hướng dẫn tương tác để lựa chọn TypeScript, Vue Router, Pinia, ESLint, Prettier và Vitest.",
        "deep_dive": """1. Tại sao Vite thay thế Vue CLI: Vue CLI dùng Webpack phải bundle toàn bộ mã nguồn trước khi khởi động dev server (mất vài chục giây trong dự án lớn). Vite tận dụng Native ES Modules của trình duyệt và esbuild viết bằng Go, giúp server khởi động tức thì (< 300ms) và Hot Module Replacement (HMR) cực nhanh.
2. Cấu trúc dự án:
   - `src/main.js`: Điểm vào (Entry point) gắn kết app vào thẻ `#app`.
   - `src/App.vue`: Root Single File Component.
   - `src/components/`: Chứa các component tái sử dụng.
   - `vite.config.js`: Cấu hình plugin và alias đường dẫn `@`.""",
        "code_example": """# Lệnh khởi tạo dự án Vue 3 chính thức:
npm create vue@latest my-vue-app

# Các tùy chọn khuyến nghị:
# ✔ Add TypeScript? ... Yes
# ✔ Add JSX Support? ... No
# ✔ Add Vue Router for Single Page Application development? ... Yes
# ✔ Add Pinia for state management? ... Yes
# ✔ Add Vitest for Unit Testing? ... Yes
# ✔ Add ESLint for code quality? ... Yes
# ✔ Add Prettier for code formatting? ... Yes

cd my-vue-app
npm install
npm run dev # Khởi động dev server Vite siêu tốc""",
        "tips": "Nếu nhà tuyển dụng hỏi về Vue CLI (`@vue/cli`), hãy tự tin trả lời: 'Vue CLI hiện đã ở chế độ bảo trì (Maintenance Mode). Dự án chính thức của Vue khuyến nghị 100% chuyển sang Vite'."
    },

    3: {
        "title_vi": "Giải thích toàn diện về Vòng đời Component (Lifecycle Hooks) trong Vue 3?",
        "level": "Mid",
        "short_answer": "Vòng đời Component là chuỗi các giai đoạn từ khi component được khởi tạo, gắn vào DOM, cập nhật dữ liệu, cho đến khi bị hủy bỏ. Vue cung cấp các hàm hooks để lập trình viên can thiệp vào các thời điểm này. Trong Vue 3 Composition API, các hook phổ biến nhất là `onMounted()`, `onUpdated()`, `onUnmounted()`, và `onBeforeUnmount()`.",
        "deep_dive": """Các giai đoạn chính:
1. Creation (Khởi tạo): Trong `<script setup>`, code chạy trực tiếp tương đương với `beforeCreate` và `created` trong Options API.
2. Mounting (Gắn DOM):
   - `onBeforeMount()`: DOM ảo đã biên dịch xong, chuẩn bị gắn vào DOM thật.
   - `onMounted()`: DOM thật đã được render xong. Nơi DUY NHẤT an toàn để gọi API, thao tác trực tiếp với DOM element qua template ref, hoặc khởi tạo thư viện bên thứ 3 (Chart.js, Swiper).
3. Updating (Cập nhật):
   - `onBeforeUpdate()` & `onUpdated()`: Chạy khi dữ liệu phản ứng thay đổi và DOM được tái render.
4. Destruction / Unmounting (Hủy bỏ):
   - `onBeforeUnmount()` & `onUnmounted()`: Chạy khi component bị tháo khỏi màn hình (`v-if=false` hoặc chuyển trang). Nơi BẮT BUỘC để dọn dẹp `clearInterval()`, hủy socket listener, hoặc remove event listener window để chống memory leak!""",
        "code_example": """<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const timer = ref(0);
let intervalId = null;

// Chạy ngay khi DOM đã sẵn sàng
onMounted(() => {
  console.log('Component đã được Mount vào DOM!');
  intervalId = setInterval(() => {
    timer.value++;
  }, 1000);
});

// BẮT BUỘC dọn dẹp tài nguyên khi component bị hủy
onUnmounted(() => {
  console.log('Dọn dẹp timer chống rò rỉ bộ nhớ...');
  clearInterval(intervalId);
});
</script>

<template>
  <div>Thời gian đã trôi qua: {{ timer }} giây</div>
</template>""",
        "tips": "Senior Tip: Không bao giờ quên giải thích việc dọn dẹp timer / listeners trong `onUnmounted()` để tránh rò rỉ bộ nhớ (Memory Leaks)."
    },

    4: {
        "title_vi": "Components trong Vue.js là gì và cách sử dụng chúng?",
        "level": "Junior",
        "short_answer": "Components là các khối giao diện độc lập, khép kín và có thể tái sử dụng (chứa đầy đủ logic HTML, CSS và JavaScript). Components giúp chia nhỏ giao diện người dùng phức tạp thành các phần nhỏ dễ quản lý, dễ kiểm thử và bảo trì.",
        "deep_dive": """1. Cây Component (Component Tree): Một ứng dụng Vue điển hình có cấu trúc dạng cây, bắt đầu từ `App.vue` (Root) chia nhánh thành Header, Sidebar, Content, và các lá là Button, Card.
2. Giao tiếp giữa các component:
   - Cha truyền dữ liệu xuống Con: Dùng `props`.
   - Con phát sự kiện báo hiệu lên Cha: Dùng `$emit` (`defineEmits`).
   - Cung cấp dữ liệu sâu qua nhiều tầng không cần prop drilling: Dùng `provide / inject`.
3. Trong Vue 3 `<script setup>`: Khi import component con, component tự động được đăng ký cục bộ mà không cần khai báo thuộc tính `components: { ... }` như Options API cũ.""",
        "code_example": """<!-- ChildButton.vue -->
<script setup>
defineProps({
  label: { type: String, default: 'Bấm vào đây' },
  variant: { type: String, default: 'primary' }
});

const emit = defineEmits(['customClick']);
</script>

<template>
  <button :class=\"['btn', variant]\" @click=\"emit('customClick')\">
    {{ label }}
  </button>
</template>

<!-- ParentView.vue -->
<script setup>
import ChildButton from './ChildButton.vue'; // Tự động đăng ký!

function handleAction() {
  alert('Đã nhận sự kiện từ nút con!');
}
</script>

<template>
  <ChildButton label=\"Lưu thay đổi\" variant=\"success\" @customClick=\"handleAction\" />
</template>""",
        "tips": "Quy tắc đặt tên Component: Nên dùng PascalCase khi import trong script (`ChildButton`) và có thể dùng PascalCase hoặc kebab-case trong template (`<ChildButton />` hoặc `<child-button />`)."
    },

    5: {
        "title_vi": "Cách ràng buộc dữ liệu (Data Binding) hiển thị lên giao diện trong Vue?",
        "level": "Junior",
        "short_answer": "Vue cung cấp các cách ràng buộc dữ liệu trực quan: (1) Interpolation cú pháp ria mép (Mustache syntax) `{{ expression }}` để hiển thị văn bản, (2) `v-bind:` (hoặc viết tắt `:`) để ràng buộc thuộc tính HTML (attributes như `:href`, `:src`, `:class`), và (3) `v-html` để render chuỗi HTML thô (cần thận trọng với XSS).",
        "deep_dive": """1. Biểu thức JavaScript trong `{{ }}`: Cho phép tính toán biểu thức đơn dòng (như `{{ ok ? 'YES' : 'NO' }}`, `{{ message.split('').reverse().join('') }}`). Không hỗ trợ các câu lệnh điều khiển đa dòng như `if/else` hay `for` (khi đó phải dùng computed).
2. Tự động Unwrap: Trong template, bạn có thể gọi trực tiếp `{{ count }}` mà không cần phải gõ `{{ count.value }}` vì Vue template compiler tự động unwrap ref.""",
        "code_example": """<script setup>
import { ref } from 'vue';

const websiteName = ref('Học Vue 3 Pro');
const logoUrl = ref('https://vuejs.org/images/logo.png');
const isSubscribed = ref(true);
</script>

<template>
  <div>
    <!-- Ràng buộc nội dung văn bản -->
    <h2>Khóa học: {{ websiteName.toUpperCase() }}</h2>

    <!-- Ràng buộc thuộc tính động với dấu hai chấm ':' -->
    <img :src=\"logoUrl\" alt=\"Logo\" width=\"50\">

    <!-- Ràng buộc điều kiện hiển thị class -->
    <p :class=\"{ active: isSubscribed, disabled: !isSubscribed }\">
      Trạng thái: {{ isSubscribed ? 'Đã kích hoạt' : 'Hết hạn' }}
    </p>
  </div>
</template>""",
        "tips": "Cẩn trọng tuyệt đối với `v-html`: Không bao giờ render nội dung do người dùng tự nhập vào qua `v-html` vì nó mở toang lỗ hổng tấn công XSS (Cross-Site Scripting)."
    },

    6: {
        "title_vi": "Vue Instance là gì và vai trò của hàm `createApp` trong Vue 3?",
        "level": "Junior",
        "short_answer": "Vue Instance là đối tượng ứng dụng trung tâm điều khiển một phần hoặc toàn bộ trang web. Trong Vue 2, instance được tạo bằng `new Vue()`. Trong Vue 3, kiến trúc được nâng cấp bằng hàm `createApp(RootComponent)` tạo ra một Application Instance độc lập, cho phép gắn plugins (Router, Pinia), đăng ký global components mà không làm ô nhiễm các instances Vue khác trên cùng một trang.",
        "deep_dive": """1. Khắc phục hạn chế của Vue 2: Trong Vue 2, các lệnh cấu hình toàn cục như `Vue.use()` hay `Vue.component()` ảnh hưởng đến tất cả các instance, gây khó khăn khi viết unit test hoặc khi nhúng nhiều widget Vue trên cùng một website micro-frontend.
2. Chuỗi cấu hình mượt mà (Chaining):
   `createApp(App).use(router).use(pinia).mount('#app');`
3. Phương thức `.mount(container)`: Gắn ứng dụng đã cấu hình hoàn chỉnh vào một phần tử DOM cụ thể trên trang HTML.""",
        "code_example": """// main.js - Chuẩn mực khởi tạo Vue 3
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

const app = createApp(App);

// Đăng ký plugins cho instance riêng biệt này
app.use(createPinia());
app.use(router);

// Cấu hình bắt lỗi toàn cục
app.config.errorHandler = (err, instance, info) => {
  console.error('Lỗi Vue toàn cục:', err, info);
};

// Mount vào phần tử HTML có id=\"app\"
app.mount('#app');""",
        "tips": "Nhớ: Phương thức `mount()` luôn luôn phải được gọi ở CUỐI CÙNG sau khi đã đăng ký tất cả các plugins và directives."
    },

    7: {
        "title_vi": "Giải thích về Virtual DOM (DOM ảo) trong Vue.js và cơ chế tối ưu hóa Diffing của Vue 3?",
        "level": "Senior",
        "short_answer": "Virtual DOM (VDOM) là một cấu trúc cây các đối tượng JavaScript thuần túy đại diện cho cây DOM thật của trình duyệt. Thay vì thao tác trực tiếp lên DOM thật (vốn rất chậm và tốn kém hiệu năng layout/repaint), Vue thực hiện các phép so sánh (Diffing) trên Virtual DOM để tính toán sự khác biệt tối thiểu, sau đó gộp lại thành một lần cập nhật duy nhất lên DOM thật (Patching).",
        "deep_dive": """Tối ưu hóa đột phá của Vue 3 Compiler:
1. Patch Flags: Vue 3 phân tích tĩnh template ngay lúc biên dịch (Compile-time analysis). Những nút nào có nội dung động sẽ được đánh dấu bằng bitwise Patch Flags (ví dụ `TEXT`, `CLASS`, `PROPS`). Khi render lại, thuật toán diffing BỎ QUA HOÀN TOÀN các nút tĩnh và chỉ kiểm tra đúng các nút có cờ!
2. Hoisting (Nâng biến tĩnh): Các phần tử HTML tĩnh (Static elements) được nhấc ra khỏi hàm render và tái sử dụng qua mọi lần render, không tốn RAM cấp phát lại.
3. Cache Event Handlers: Các hàm xử lý sự kiện như `@click=\"handleClick\"` được cache lại để tránh kích hoạt re-render không cần thiết cho component con.""",
        "code_example": """// Minh họa cấu trúc một VNode (Virtual Node) đơn giản:
const vnode = {
  type: 'button',
  props: {
    class: 'btn-primary',
    onClick: () => console.log('clicked')
  },
  children: 'Bấm vào tôi',
  patchFlag: 1 // PatchFlags.TEXT - Vue 3 chỉ theo dõi sự thay đổi của text này!
};""",
        "tips": "So sánh Senior: Virtual DOM của Vue 3 nhanh hơn đáng kể so với React nhờ chiến lược 'Compiler-Informed Virtual DOM' - tận dụng trình biên dịch template thông minh để bỏ qua việc duyệt cây toàn bộ."
    },

    8: {
        "title_vi": "Directives trong Vue.js là gì? Liệt kê các Directives thông dụng nhất?",
        "level": "Junior",
        "short_answer": "Directives là các thuộc tính đặc biệt có tiền tố `v-` được gắn vào các thẻ HTML trong template của Vue. Directives áp dụng các hành vi phản ứng đặc biệt lên phần tử DOM khi giá trị của biểu thức thay đổi. Các directive phổ biến nhất gồm: `v-if`, `v-else`, `v-show`, `v-for`, `v-bind` (`:`), `v-on` (`@`), `v-model`, `v-slot` (`#`), `v-text` và `v-html`.",
        "deep_dive": """1. Cấu trúc đầy đủ của Directive:
   `v-directive:argument.modifier=\"expression\"`
   Ví dụ: `v-on:submit.prevent=\"handleSubmit\"`
   - `v-on`: Tên directive.
   - `:submit`: Argument (đối số).
   - `.prevent`: Modifier (bổ từ, tương đương e.preventDefault()).
   - `\"handleSubmit\"`: Biểu thức giá trị.""",
        "code_example": """<script setup>
import { ref } from 'vue';
const isVisible = ref(true);
const fruits = ref(['Táo', 'Chuối', 'Cam']);
</script>

<template>
  <div>
    <!-- v-if / v-else điều kiện -->
    <p v-if=\"isVisible\">Nội dung đang hiển thị</p>
    <p v-else>Nội dung đã bị ẩn</p>

    <!-- v-for lặp danh sách (BẮT BUỘC có :key) -->
    <ul>
      <li v-for=\"(item, index) in fruits\" :key=\"index\">
        {{ index + 1 }}. {{ item }}
      </li>
    </ul>

    <!-- v-on bắt sự kiện -->
    <button @click=\"isVisible = !isVisible\">Chuyển đổi ẩn/hiện</button>
  </div>
</template>""",
        "tips": "Luôn luôn gắn thuộc tính `:key` độc nhất khi dùng `v-for` để thuật toán diffing của Virtual DOM hoạt động chính xác."
    },

    9: {
        "title_vi": "Cách xử lý dữ liệu nhập từ người dùng và Form Submissions trong Vue?",
        "level": "Junior",
        "short_answer": "Sử dụng directive `v-model` để ràng buộc dữ liệu 2 chiều (Two-Way Data Binding) giữa các thẻ input/textarea/select và biến trạng thái trong script. Để xử lý gửi form, sử dụng `@submit.prevent=\"handleSubmit\"` để tự động ngăn chặn hành vi tải lại trang mặc định của trình duyệt.",
        "deep_dive": """1. Các Form Modifiers cực kỳ hữu ích:
   - `v-model.lazy`: Chỉ cập nhật dữ liệu khi người dùng chuyển focus ra ngoài (sự kiện `change` thay vì `input`).
   - `v-model.number`: Tự động ép kiểu chuỗi nhập vào thành kiểu Số (`Number`).
   - `v-model.trim`: Tự động cắt bỏ các khoảng trắng thừa ở đầu và cuối chuỗi.
2. Thư viện Validate chuẩn: Với các form phức tạp trong doanh nghiệp, nên kết hợp với VeeValidate hoặc Vuelidate cùng Schema Zod.""",
        "code_example": """<script setup>
import { ref } from 'vue';

const formData = ref({
  username: '',
  age: null,
  role: 'developer',
  termsAccepted: false
});

function handleSubmit() {
  console.log('Dữ liệu gửi lên API:', formData.value);
  alert('Gửi form thành công!');
}
</script>

<template>
  <!-- .prevent ngăn reload trang mặc định -->
  <form @submit.prevent=\"handleSubmit\">
    <input v-model.trim=\"formData.username\" placeholder=\"Họ tên\" required />
    <input v-model.number=\"formData.age\" type=\"number\" placeholder=\"Tuổi\" />
    
    <select v-model=\"formData.role\">
      <option value=\"developer\">Lập trình viên</option>
      <option value=\"designer\">Thiết kế</option>
    </select>

    <label>
      <input type=\"checkbox\" v-model=\"formData.termsAccepted\" /> Đồng ý điều khoản
    </label>

    <button type=\"submit\" :disabled=\"!formData.termsAccepted\">Đăng Ký</button>
  </form>
</template>""",
        "tips": "Điểm cộng phỏng vấn: Nhắc đến việc `v-model` trên thẻ input thực chất chỉ là cú pháp viết tắt của `:value=\"data\"` kết hợp `@input=\"data = $event.target.value\"`."
    },

    10: {
        "title_vi": "Thuộc tính `methods` trong Options API và sự thay thế của nó trong Composition API?",
        "level": "Junior",
        "short_answer": "Trong Options API (Vue 2), `methods` là một object chứa các hàm xử lý sự kiện hoặc logic tính toán, được gọi thông qua từ khóa `this.myMethod()`. Trong Vue 3 Composition API (`<script setup>`), khái niệm `methods` không còn cần thiết; bạn chỉ cần khai báo các hàm JavaScript tiêu chuẩn (`function` hoặc arrow function) và chúng tự động sẵn sàng sử dụng trong template.",
        "deep_dive": """1. Vấn đề của Options API `methods`:
   - Phụ thuộc vào ngữ cảnh `this`, dễ gây lỗi mất ngữ cảnh khi dùng trong callback.
   - Không được cache kết quả (khác với `computed`). Mỗi khi component re-render, method gọi trong template sẽ bị thực thi lại từ đầu.
2. Ưu thế của Composition API: Các hàm có thể được tách rời ra các composable files riêng (`useUser.js`) và tái sử dụng xuyên suốt toàn bộ dự án.""",
        "code_example": """<!-- Vue 3 Composition API: Không cần khai báo 'methods'! -->
<script setup>
import { ref } from 'vue';

const counter = ref(0);

// Khai báo hàm trực tiếp đơn giản và rõ ràng
function increment() {
  counter.value++;
}

const reset = () => {
  counter.value = 0;
};
</script>

<template>
  <div>
    <p>Giá trị: {{ counter }}</p>
    <button @click=\"increment\">Tăng</button>
    <button @click=\"reset\">Đặt lại</button>
  </div>
</template>""",
        "tips": "Khi được hỏi 'Khi nào nên dùng method thay vì computed trong template?', hãy trả lời: 'Chỉ dùng method khi cần truyền tham số động cho hàm tính toán, hoặc cho các hàm xử lý sự kiện phản hồi lại hành động của người dùng (như click, submit)'."
    },

    11: {
        "title_vi": "Sự khác biệt cốt lõi giữa `v-bind` và `v-model` trong Vue?",
        "level": "Junior",
        "short_answer": "`v-bind` (viết tắt `:`) là ràng buộc dữ liệu MỘT CHIỀU (One-Way Data Binding): truyền dữ liệu từ component/script vào một thuộc tính HTML hoặc prop của component con. Trong khi đó, `v-model` là ràng buộc dữ liệu HAI CHIỀU (Two-Way Data Binding): dữ liệu vừa được đẩy từ script ra view, vừa tự động cập nhật ngược lại script ngay khi người dùng thay đổi trên giao diện.",
        "deep_dive": """1. Cơ chế dưới nền tảng của `v-model`:
   `v-model=\"text\"` thực chất là 'đường cú pháp' (syntactic sugar) tương đương với:
   `:value=\"text\" @input=\"text = $event.target.value\"`
2. `v-model` trên Custom Component (Vue 3):
   Tương đương với việc truyền prop `:modelValue=\"data\"` và lắng nghe sự kiện `@update:modelValue=\"data = $event\"`.
3. Nhiều v-model trên cùng 1 component: Vue 3 cho phép khai báo nhiều `v-model:firstName` và `v-model:lastName` trên cùng một component con rất tiện lợi.""",
        "code_example": """<script setup>
import { ref } from 'vue';
const username = ref('admin');
</script>

<template>
  <div>
    <!-- 1. v-bind (Một chiều): Đổi trên input KHÔNG làm đổi biến username trong script! -->
    <input :value=\"username\" />

    <!-- 2. v-model (Hai chiều): Gõ phím trên input lập tức cập nhật biến username! -->
    <input v-model=\"username\" />
  </div>
</template>""",
        "tips": "Cách trả lời chuẩn Senior: 'v-model thực chất chỉ là cú pháp rút gọn kết hợp giữa một v-bind truyền prop vào và một v-on lắng nghe sự kiện phát ra'."
    },

    12: {
        "title_vi": "Computed Properties (`computed`) là gì và tại sao chúng lại quan trọng?",
        "level": "Junior",
        "short_answer": "`computed` là thuộc tính tính toán phái sinh (derived state) dựa trên các trạng thái phản ứng khác. Điểm quan trọng nhất của `computed` là cơ chế TỰ ĐỘNG GHI NHỚ BỘ ĐỆM (Reactive Caching): nó chỉ thực sự tính toán lại khi một trong các dependencies phản ứng của nó thay đổi giá trị. Nếu dependencies giữ nguyên, các lần gọi lại sẽ trả về ngay lập tức giá trị đã cache mà không tốn CPU.",
        "deep_dive": """1. Tối ưu hiệu năng: Nếu bạn có một phép tính lọc mảng 10,000 phần tử, việc đưa vào `computed` giúp phép tính chỉ chạy 1 lần duy nhất khi mảng thay đổi, dù cho component có re-render hàng trăm lần vì các biến khác.
2. Mặc định là Read-only: Bạn không thể gán trực tiếp `fullName.value = 'New Name'` trừ khi định nghĩa cả Getter và Setter cho computed property.
3. Thuần khiết (Pure): Bên trong computed function KHÔNG ĐƯỢC có tác dụng phụ (side-effects) như gọi API hay thay đổi biến khác.""",
        "code_example": """<script setup>
import { ref, computed } from 'vue';

const cart = ref([
  { id: 1, name: 'Sách', price: 100, qty: 2 },
  { id: 2, name: 'Bút', price: 20, qty: 5 }
]);

// ✅ Tự động cache: Chỉ tính toán lại khi mảng cart thay đổi!
const totalCost = computed(() => {
  console.log('Đang tính tổng tiền đơn hàng...');
  return cart.value.reduce((sum, item) => sum + (item.price * item.qty), 0);
});
</script>

<template>
  <div>
    <p>Tổng tiền: {{ totalCost }} đ</p>
    <p>Tổng tiền hiển thị lần 2 (lấy từ cache): {{ totalCost }} đ</p>
  </div>
</template>""",
        "tips": "Từ khóa then chốt khi phỏng vấn về `computed`: 'Reactive Caching based on Dependencies'."
    },

    13: {
        "title_vi": "So sánh chi tiết sự khác biệt giữa `computed` và `methods` trong Vue?",
        "level": "Junior",
        "short_answer": "Sự khác biệt cốt tử là CƠ CHẾ CACHING: `computed` có bộ nhớ đệm (cached) dựa trên các reactive dependencies và chỉ chạy lại khi dependency thay đổi. Trong khi đó, `methods` KHÔNG HỀ CÓ CACHING; mỗi khi component được re-render, mọi method được gọi trong template đều bị thực thi lại từ đầu.",
        "deep_dive": """Bảng so sánh:
1. Caching: Computed = Có; Method = Không.
2. Tham số: Computed = Không nhận tham số từ template (là một thuộc tính); Method = Có thể nhận tham số linh hoạt (`formatPrice(item.price)`).
3. Mục đích sử dụng:
   - Dùng `computed`: Cho dữ liệu phái sinh, tính toán đắt đỏ, lọc danh sách.
   - Dùng `methods`: Cho các sự kiện người dùng (click, submit, change) hoặc khi bắt buộc phải truyền tham số cho từng item trong vòng lặp `v-for`.""",
        "code_example": """<script setup>
import { ref, computed } from 'vue';

const items = ref([10, 20, 30]);

// Computed: Chỉ chạy 1 lần
const totalComputed = computed(() => {
  return items.value.reduce((a, b) => a + b, 0);
});

// Method: Chạy mỗi khi có bất kỳ render nào
function totalMethod() {
  return items.value.reduce((a, b) => a + b, 0);
}
</script>""",
        "tips": "Nếu bạn thấy ai đó dùng `method` chỉ để format dữ liệu mà không nhận tham số, hãy khuyên họ đổi sang `computed` ngay để tăng hiệu năng ứng dụng."
    },

    14: {
        "title_vi": "Watchers (`watch` và `watchEffect`) trong Vue là gì và khi nào nên sử dụng?",
        "level": "Mid",
        "short_answer": "`watch` và `watchEffect` được sử dụng để thực thi các TÁC DỤNG PHỤ (Side Effects) bất đồng bộ hoặc đắt đỏ khi dữ liệu phản ứng thay đổi (ví dụ: gọi API tìm kiếm khi ô input thay đổi, lưu dữ liệu vào localStorage, log analytics).",
        "deep_dive": """1. Khác biệt giữa `watch` và `watchEffect`:
   - `watch(source, callback, options)`: Chỉ theo dõi nguồn được chỉ định rõ ràng (explicit source). Không chạy ngay lúc khởi tạo (lazy by default, trừ khi bật `immediate: true`). Cung cấp cả giá trị mới và giá trị cũ `(newVal, oldVal)`.
   - `watchEffect(callback)`: Tự động phát hiện và theo dõi mọi biến phản ứng được đọc bên trong hàm. Luôn chạy ngay lập tức 1 lần lúc component khởi tạo (eager).
2. Tùy chọn `deep: true`: Bắt buộc khi muốn theo dõi các thuộc tính lồng sâu bên trong một Object phức tạp.""",
        "code_example": """<script setup>
import { ref, watch, watchEffect } from 'vue';

const searchQuery = ref('');
const searchResults = ref([]);

// 1. Sử dụng watch để gọi API debounce khi người dùng gõ tìm kiếm
watch(searchQuery, async (newQuery, oldQuery) => {
  console.log(`Từ khóa đổi từ \"${oldQuery}\" sang \"${newQuery}\"`);
  if (newQuery.length >= 2) {
    const res = await fetch(`/api/search?q=${newQuery}`);
    searchResults.value = await res.json();
  }
});

// 2. watchEffect: Tự động theo dõi bất kỳ biến nào được dùng bên trong
watchEffect(() => {
  console.log('Current search length:', searchQuery.value.length);
});
</script>""",
        "tips": "Quy tắc vàng: 'Nếu bạn cần biến đổi dữ liệu để hiển thị lên UI, hãy dùng `computed`. Nếu bạn cần thực hiện tác vụ phụ (Side Effect: gọi API, ghi log, chỉnh sửa DOM ngoài), hãy dùng `watch`'."
    },

    15: {
        "title_vi": "Cách ràng buộc Inline Styles (`:style`) trong Vue template linh hoạt?",
        "level": "Junior",
        "short_answer": "Vue hỗ trợ ràng buộc inline styles thông qua directive `:style`. Bạn có thể truyền vào một Object JavaScript (tự động hỗ trợ camelCase hoặc kebab-case đóng trong nháy), một Computed Property trả về style object, hoặc một Mảng (Array) các style objects để gộp nhiều kiểu dáng lại với nhau.",
        "deep_dive": """1. Tự động thêm tiền tố trình duyệt (Vendor Prefixing): Khi sử dụng một thuộc tính CSS yêu cầu tiền tố trình duyệt (như `transform` hay `user-select`), Vue sẽ tự động kiểm tra và thêm các tiền tố thích hợp (`-webkit-`, `-moz-`)!
2. Đa giá trị (Multiple Values): Có thể truyền mảng giá trị để fallback: `:style=\"{ display: ['-webkit-box', '-ms-flexbox', 'flex'] }\"`.""",
        "code_example": """<script setup>
import { ref, computed } from 'vue';

const baseColor = ref('#10b981');
const fontSize = ref(18);

// Ràng buộc qua Computed Object sạch sẽ
const boxStyle = computed(() => ({
  backgroundColor: baseColor.value,
  fontSize: `${fontSize.value}px`,
  borderRadius: '8px',
  padding: '16px',
  boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
}));
</script>

<template>
  <div :style=\"boxStyle\">
    Khối giao diện với dynamic styling!
  </div>
</template>""",
        "tips": "Tránh viết inline style object quá dài trực tiếp trên thẻ HTML template. Hãy gom chúng vào một `computed` property để code template luôn trong sáng và dễ đọc."
    },

    16: {
        "title_vi": "Cách truyền dữ liệu từ Component cha xuống Component con bằng Props?",
        "level": "Junior",
        "short_answer": "Trong Vue, dữ liệu tuân theo Luồng dữ liệu một chiều (One-Way Data Flow). Component cha truyền dữ liệu xuống qua các thuộc tính tùy biến trên thẻ component con (sử dụng `:propName=\"data\"`), và component con khai báo nhận dữ liệu bằng macro `defineProps()` trong `<script setup>`.",
        "deep_dive": """1. Bất biến (Props are Read-only): Component con TUYỆT ĐỐI KHÔNG ĐƯỢC phép trực tiếp gán lại hoặc làm thay đổi giá trị của prop nhận được (`props.item = newItem` sẽ ném cảnh báo đỏ). Nếu muốn thay đổi, con phải phát sự kiện `$emit` yêu cầu cha cập nhật, hoặc copy prop vào một biến `ref` nội bộ.
2. Khai báo kiểu (Type Declaration): Trong TypeScript có thể dùng cú pháp generic thanh lịch: `defineProps<{ title: string; count?: number }>()`.""",
        "code_example": """<!-- ChildCard.vue -->
<script setup>
// Khai báo props với validation chuẩn
const props = defineProps({
  title: { type: String, required: true },
  views: { type: Number, default: 0 },
  tags: { type: Array, default: () => [] } // Kiểu Array/Object phải dùng Factory Function!
});
</script>

<template>
  <div class=\"card\">
    <h3>{{ title }}</h3>
    <p>Lượt xem: {{ views }}</p>
  </div>
</template>

<!-- Parent.vue -->
<script setup>
import ChildCard from './ChildCard.vue';
</script>

<template>
  <ChildCard title=\"Học Vue 3 Nâng Cao\" :views=\"1250\" />
</template>""",
        "tips": "Bẫy phỏng vấn: Với kiểu dữ liệu `Array` hoặc `Object`, thuộc tính `default` trong props BẮT BUỘC phải là một Factory Function trả về giá trị mới (`default: () => []`), tránh việc tất cả các component con dùng chung 1 vùng nhớ tham chiếu!"
    },

    17: {
        "title_vi": "Thực hành Validation và thiết lập Default values cho Props trong Vue?",
        "level": "Junior",
        "short_answer": "Props validation đảm bảo dữ liệu truyền vào component đáp ứng đúng yêu cầu nghiệp vụ. Bạn có thể định nghĩa kiểu dữ liệu (`type`), tính bắt buộc (`required: true`), giá trị mặc định (`default`), và hàm kiểm tra tính hợp lệ tùy biến (`validator(value)`).",
        "deep_dive": """1. Các kiểu dữ liệu hỗ trợ: `String`, `Number`, `Boolean`, `Array`, `Object`, `Date`, `Function`, `Symbol` hoặc bất kỳ Class tùy biến nào.
2. Hàm `validator`: Nhận giá trị prop và trả về `true` nếu hợp lệ, `false` nếu sai (kèm theo cảnh báo rõ ràng trên console lúc dev).""",
        "code_example": """<script setup>
defineProps({
  status: {
    type: String,
    required: true,
    // Hàm kiểm tra giá trị chỉ được nằm trong danh sách cho phép
    validator: (value) => ['pending', 'success', 'failed'].includes(value)
  },
  timeout: {
    type: Number,
    default: 5000
  }
});
</script>""",
        "tips": "Props validation chạy trong môi trường phát triển (Development) để cảnh báo cho lập trình viên. Trên Production build, các validation này tự động được lược bỏ để tối ưu hiệu năng."
    },

    18: {
        "title_vi": "Prop Drilling là gì và các giải pháp khắc phục trong Vue.js?",
        "level": "Mid",
        "short_answer": "Prop Drilling là hiện tượng dữ liệu phải được truyền qua quá nhiều tầng components trung gian (từ Ông -> Cha -> Con -> Cháu) chỉ để phục vụ cho component Cháu ở đáy cùng, dù các component trung gian hoàn toàn không cần sử dụng dữ liệu đó. Khắc phục bằng cách sử dụng `provide / inject` hoặc Quản lý trạng thái tập trung (Pinia).",
        "deep_dive": """1. Tác hại của Prop Drilling: Làm các component trung gian bị phụ thuộc không cần thiết, cực kỳ khó tái cấu trúc và dễ gây lỗi khi đổi tên prop.
2. Giải pháp 1: `provide / inject` (Cặp đôi hoàn hảo cho cấu trúc component phân cấp sâu).
3. Giải pháp 2: Pinia Store (Dành cho trạng thái toàn cục dùng chung ở khắp nơi).
4. Giải pháp 3: Component Composition / Slots (Truyền trực tiếp component con vào slot của component cha).""",
        "code_example": """<!-- GrandParent.vue (Cung cấp dữ liệu) -->
<script setup>
import { provide, ref } from 'vue';
const theme = ref('dark');

// Cung cấp biến theme cho BẤT KỲ component con cháu nào bên dưới
provide('appTheme', theme);
</script>

<!-- DeepChild.vue (Hứng dữ liệu ở bất kỳ độ sâu nào mà không qua trung gian) -->
<script setup>
import { inject } from 'vue';
const theme = inject('appTheme', 'light'); // 'light' là giá trị fallback
</script>

<template>
  <div :class=\"theme\">Giao diện kế thừa Theme từ Ông tổ!</div>
</template>""",
        "tips": "Nếu dữ liệu chỉ dùng trong một cụm tính năng phân cấp (ví dụ cụm Form và FormItem), hãy dùng `provide/inject`. Nếu dữ liệu dùng toàn app (như User info, Cart), hãy dùng Pinia."
    },

    19: {
        "title_vi": "Slots trong Vue.js components là gì và có những loại Slot nào?",
        "level": "Mid",
        "short_answer": "Slots là cơ chế phân phối nội dung (Content Distribution API) lấy cảm hứng từ chuẩn Web Components. Nó cho phép component cha truyền một đoạn mã template (HTML, components khác) vào bên trong component con. Có 3 loại Slots: Default Slot, Named Slots (Slot có tên), và Scoped Slots (Slot có phạm vi truyền dữ liệu từ con ngược lên cha).",
        "deep_dive": """1. Default Slot: Thẻ `<slot></slot>` đơn giản nhất.
2. Named Slots: Cho phép đặt tên `<slot name=\"header\">`, `<slot name=\"footer\">`. Cha sử dụng cú pháp `#header` hoặc `v-slot:header`.
3. Scoped Slots: Cực kỳ mạnh mẽ! Cho phép component con truyền dữ liệu (slot props) ngược ra cho cha để cha tự quyết định cách hiển thị dữ liệu đó (rất phổ biến khi viết Table, List components).""",
        "code_example": """<!-- BaseModal.vue (Component Con có Named Slots) -->
<template>
  <div class=\"modal-backdrop\">
    <div class=\"modal-box\">
      <header><slot name=\"header\">Tiêu đề mặc định</slot></header>
      <main><slot></slot></main> <!-- Default slot -->
      <footer><slot name=\"footer\"></slot></footer>
    </div>
  </div>
</template>

<!-- App.vue (Component Cha sử dụng) -->
<template>
  <BaseModal>
    <template #header>
      <h2>Xác nhận xóa tài khoản</h2>
    </template>

    <p>Bạn có chắc chắn muốn xóa không? Hành động này không thể hoàn tác.</p>

    <template #footer>
      <button class=\"btn-danger\">Xác nhận</button>
    </template>
  </BaseModal>
</template>""",
        "tips": "Cú pháp viết tắt: Dùng ký tự thăng `#` thay cho `v-slot:`. Ví dụ `#header` thay vì `v-slot:header`."
    },

    20: {
        "title_vi": "Cách thiết kế một Component có khả năng tái sử dụng cao (Reusable Component) trong Vue?",
        "level": "Senior",
        "short_answer": "Để component có thể tái sử dụng tối đa trong toàn doanh nghiệp: (1) Áp dụng nguyên tắc Single Responsibility (mỗi component làm tốt một việc duy nhất), (2) Sử dụng Props có validation và default rõ ràng cho cấu hình hiển thị, (3) Sử dụng Emits có type kiểm soát các tương tác, (4) Cung cấp Slots để cha có thể tùy biến giao diện linh hoạt (Inversion of Control), và (5) Giữ component ở trạng thái 'ngu ngốc' (Dumb/Presentational Component) không tự ý gọi API bên trong.",
        "deep_dive": """1. Smart vs Dumb Components:
   - Dumb Component: Chỉ nhận props, render UI và emit events. Hoàn toàn độc lập với API, dễ viết Storybook và Unit test.
   - Smart Component (Container): Quản lý state, gọi API từ Pinia, sau đó truyền dữ liệu xuống cho các Dumb components hiển thị.
2. Khả năng truy cập (Accessibility - a11y): Thiết kế đầy đủ aria attributes và hỗ trợ phím bấm.""",
        "code_example": """<!-- Reusable BaseInput.vue chuẩn Design System -->
<script setup>
defineProps({
  modelValue: [String, Number],
  label: String,
  error: String,
  type: { type: String, default: 'text' }
});

defineEmits(['update:modelValue']);
</script>

<template>
  <div class=\"form-group\" :class=\"{ 'has-error': !!error }\">
    <label v-if=\"label\">{{ label }}</label>
    <input
      :type=\"type\"
      :value=\"modelValue\"
      @input=\"$emit('update:modelValue', $event.target.value)\"
      class=\"input-control\"
    />
    <span v-if=\"error\" class=\"error-msg\">{{ error }}</span>
  </div>
</template>""",
        "tips": "Luôn phân tách rõ ràng ranh giới giữa UI Components (tái sử dụng được) và Feature/Page Components (chứa business logic đặc thù)."
    },

    21: {
        "title_vi": "Cách xử lý các sự kiện gốc (Native DOM Events) trong Vue?",
        "level": "Junior",
        "short_answer": "Sử dụng directive `v-on:` (hoặc viết tắt là `@`) gắn vào phần tử DOM. Bạn có thể truyền tên hàm xử lý (`@click=\"handleClick\"`) hoặc viết biểu thức inline (`@click=\"count++\"`). Vue tự động truyền đối tượng sự kiện gốc `event` (`MouseEvent`, `KeyboardEvent`) vào hàm.",
        "deep_dive": """1. Truy cập đối tượng `$event` trong inline expression:
   `@click=\"warn('Form chưa lưu', $event)\"`
2. Tự động unbind: Vue tự động gỡ bỏ các event listeners khi component bị unmounted, giúp bạn không bao giờ lo lắng về việc rò rỉ bộ nhớ từ các sự kiện template.""",
        "code_example": """<script setup>
function handleMouseMove(event) {
  console.log(`Tọa độ chuột: X=${event.clientX}, Y=${event.clientY}`);
}
</script>

<template>
  <div class=\"box\" @mousemove=\"handleMouseMove\">
    Rê chuột qua vùng này để xem tọa độ
  </div>
</template>""",
        "tips": "Nhớ: Trong inline statement, biến đại diện cho native event luôn có tên là `$event`."
    },

    22: {
        "title_vi": "Event Propagation (Lan truyền sự kiện) là gì và cách kiểm soát trong Vue?",
        "level": "Mid",
        "short_answer": "Event Propagation là cơ chế trong trình duyệt khi một sự kiện xảy ra trên phần tử con, nó sẽ nổi bọt (Bubbling) dần lên tất cả các phần tử cha bao bọc nó. Trong Vue, bạn có thể kiểm soát hoàn toàn hành vi này mà không cần gọi `e.stopPropagation()` thủ công bằng cách sử dụng Event Modifiers: `.stop` (chặn nổi bọt) và `.capture` (kích hoạt ở pha lắng nghe trước).",
        "deep_dive": """1. Event Bubbling (Nổi bọt): Click vào nút con bên trong thẻ cha sẽ vô tình kích hoạt cả sự kiện click của thẻ cha.
2. Giải pháp Modifier: `@click.stop` gọi ngầm `event.stopPropagation()`, ngăn sự kiện lan lên cha.
3. `.self`: Chỉ kích hoạt nếu sự kiện xuất phát từ chính phần tử đó chứ không phải từ phần tử con.""",
        "code_example": """<template>
  <!-- Thẻ cha có sự kiện click mở modal -->
  <div class=\"card-parent\" @click=\"openParentModal\">
    <h3>Thẻ sản phẩm</h3>

    <!-- Nút con có .stop: Bấm vào đây KHÔNG kích hoạt openParentModal! -->
    <button @click.stop=\"addToCart\">Thêm vào giỏ</button>
  </div>
</template>""",
        "tips": "Sử dụng `.stop` giúp code gọn gàng hơn rất nhiều so với việc phải truyền `(event)` vào hàm và viết dòng `event.stopPropagation()`."
    },

    23: {
        "title_vi": "Mô tả chi tiết tác dụng của hai bộ bổ từ `.prevent` và `.stop`?",
        "level": "Junior",
        "short_answer": "`.prevent` tương đương với việc gọi `event.preventDefault()`: ngăn chặn hành vi mặc định của trình duyệt (ví dụ: không cho thẻ form reload lại trang khi submit, không cho thẻ `<a>` nhảy link). `.stop` tương đương với `event.stopPropagation()`: ngăn chặn sự kiện nổi bọt lên các phần tử cha.",
        "deep_dive": """1. Nối chuỗi Modifiers (Chaining): Vue cho phép ghép nhiều modifiers liên tiếp trên cùng một sự kiện!
   Ví dụ: `@click.stop.prevent=\"doSomething\"` (Vừa ngăn nổi bọt vừa chặn hành vi mặc định).
2. Thứ tự quan trọng: Thứ tự ghép modifiers quyết định thứ tự thực thi.""",
        "code_example": """<template>
  <!-- Ngăn reload trang khi submit form -->
  <form @submit.prevent=\"submitData\">
    <input type=\"text\" required />
    <button type=\"submit\">Lưu</button>
  </form>

  <!-- Ngăn thẻ <a> nhảy trang và chặn luôn nổi bọt -->
  <a href=\"https://google.com\" @click.stop.prevent=\"customNavigate\">
    Liên kết điều hướng nội bộ
  </a>
</template>""",
        "tips": "Modifier `.prevent` trên form submit là cú pháp phổ biến nhất trong mọi ứng dụng Single Page App của Vue."
    },

    24: {
        "title_vi": "Khi nào nên sử dụng bộ bổ từ sự kiện `.once` trong Vue?",
        "level": "Junior",
        "short_answer": "Modifier `.once` đảm bảo hàm xử lý sự kiện chỉ được kích hoạt DUY NHẤT MỘT LẦN. Sau lần kích hoạt đầu tiên, event listener sẽ tự động bị hủy bỏ hoàn toàn. Rất hữu ích cho các hành động không được phép lặp lại như: mở thông báo chào mừng lần đầu, bấm nút kích hoạt ưu đãi một lần, hoặc tải dữ liệu khởi tạo.",
        "deep_dive": """1. Khác biệt với các modifier khác: Không giống như `.prevent` hay `.stop` chỉ dùng cho DOM events, `.once` có thể áp dụng được cho CẢ sự kiện gốc của DOM lẫn sự kiện tùy biến của component con (`@customEvent.once`).""",
        "code_example": """<template>
  <!-- Nút nhận quà chỉ bấm được duy nhất 1 lần trong phiên -->
  <button @click.once=\"claimReward\">
    Nhận thưởng chào mừng (Chỉ 1 lần duy nhất)
  </button>
</template>""",
        "tips": "Thay vì phải tạo biến cờ `let hasTriggered = false` trong script, chỉ cần thêm `.once` ngay trên template là xong."
    },

    25: {
        "title_vi": "Cách tạo và phát ra sự kiện tùy biến (Custom Events) trong Vue 3?",
        "level": "Junior",
        "short_answer": "Component con sử dụng macro `defineEmits()` trong `<script setup>` để khai báo danh sách các sự kiện mà nó có thể phát ra. Khi cần thông báo cho cha, con gọi hàm `emit('eventName', payload)`. Component cha lắng nghe sự kiện này bằng cú pháp `@eventName=\"handleEvent\"`.",
        "deep_dive": """1. Luồng dữ liệu ngược: Props đi xuống, Events đi lên (Props Down, Events Up).
2. Validation cho Emits: Bạn có thể viết hàm validate dữ liệu payload của sự kiện ngay trong `defineEmits` để đảm bảo dữ liệu gửi lên cha là chính xác.
3. Quy ước đặt tên: Khuyên dùng camelCase trong script (`emit('itemDeleted')`) và kebab-case khi lắng nghe trên template (`@item-deleted=\"...\"`) hoặc thống nhất camelCase trong Vue 3.""",
        "code_example": """<!-- ChildItem.vue -->
<script setup>
// Khai báo emits rõ ràng
const emit = defineEmits({
  // Có thể validate payload
  deleteItem: (id) => typeof id === 'number'
});

function handleDelete(id) {
  emit('deleteItem', id); // Bắn sự kiện lên cha kèm payload
}
</script>

<template>
  <button @click=\"handleDelete(101)\">Xóa phần tử</button>
</template>

<!-- ParentList.vue -->
<script setup>
import ChildItem from './ChildItem.vue';

function onUserDeleted(id) {
  console.log('Cha đã nhận được yêu cầu xóa item:', id);
}
</script>

<template>
  <ChildItem @deleteItem=\"onUserDeleted\" />
</template>""",
        "tips": "Luôn khai báo toàn bộ sự kiện bằng `defineEmits()`. Điều này giúp component tự làm tài liệu và cảnh báo nếu có sự kiện trùng với DOM native event."
    },

    26: {
        "title_vi": "Mục đích và cách dùng của `v-if` và `v-for`? Tại sao không nên dùng chung trên một phần tử?",
        "level": "Mid",
        "short_answer": "`v-if` dùng để hiển thị phần tử có điều kiện (thực sự gắn hoặc tháo DOM node). `v-for` dùng để lặp mảng hoặc object để render danh sách. TUYỆT ĐỐI KHÔNG NÊN DÙNG CHUNG `v-if` và `v-for` TRÊN CÙNG MỘT PHẦN TỬ vì lý do độ ưu tiên và hiệu năng; trong Vue 3 `v-if` có độ ưu tiên cao hơn `v-for`, dẫn đến việc `v-if` không thể truy cập vào biến lặp của `v-for`.",
        "deep_dive": """1. Khác biệt độ ưu tiên giữa Vue 2 và Vue 3:
   - Trong Vue 2: `v-for` ưu tiên cao hơn `v-if` (gây lãng phí hiệu năng vì lặp qua toàn bộ mảng rồi mới lọc từng phần tử).
   - Trong Vue 3: `v-if` ưu tiên cao hơn `v-for`. Khi viết `<li v-for=\"user in users\" v-if=\"user.isActive\">`, Vue 3 sẽ báo lỗi vì `user` chưa hề tồn tại khi `v-if` chạy!
2. Giải pháp chuẩn:
   - Cách 1: Sử dụng `computed` để lọc danh sách trước khi đưa vào `v-for`.
   - Cách 2: Bọc `v-for` bên trong hoặc dùng thẻ ảo `<template v-for=\"...\">` kết hợp `v-if`.""",
        "code_example": """<script setup>
import { ref, computed } from 'vue';

const users = ref([
  { id: 1, name: 'Alex', active: true },
  { id: 2, name: 'Bob', active: false },
  { id: 3, name: 'Charlie', active: true }
]);

// ✅ CÁCH TỐT NHẤT: Lọc trước bằng computed
const activeUsers = computed(() => users.value.filter(u => u.active));
</script>

<template>
  <ul>
    <!-- Dùng mảng đã lọc sạch sẽ, hiệu năng tối ưu -->
    <li v-for=\"user in activeUsers\" :key=\"user.id\">
      {{ user.name }}
    </li>
  </ul>
</template>""",
        "tips": "Đây là câu hỏi kinh điển trong mọi cuộc phỏng vấn Vue. Hãy giải thích rõ sự thay đổi độ ưu tiên giữa Vue 2 và Vue 3 để chứng minh sự am hiểu sâu sắc."
    },

    27: {
        "title_vi": "So sánh chi tiết sự khác biệt giữa `v-show` và `v-if`?",
        "level": "Junior",
        "short_answer": "`v-if` là hiển thị có điều kiện 'thực sự' (Lazy/True Conditional): nó phá hủy và tạo lại phần tử cùng toàn bộ các component con bên trong DOM. Trong khi đó, `v-show` LUÔN LUÔN render phần tử vào DOM ngay từ đầu, và chỉ đơn thuần bật/tắt thuộc tính CSS `display: none` để ẩn/hiện.",
        "deep_dive": """So sánh chi phí:
1. Chi phí khởi tạo ban đầu (Initial Render Cost):
   - `v-if`: Thấp hơn nếu điều kiện ban đầu là `false` (nó không làm gì cả).
   - `v-show`: Cao hơn vì luôn phải render phần tử bất kể điều kiện là gì.
2. Chi phí chuyển đổi (Toggle Cost):
   - `v-if`: Rất cao vì phải tháo gỡ, khởi tạo lại DOM và kích hoạt lại lifecycle hooks.
   - `v-show`: Siêu nhẹ vì chỉ thay đổi 1 thuộc tính CSS.
3. Khi nào dùng gì:
   - Dùng `v-show`: Cho các thành phần bật/tắt liên tục (Dropdowns, Tabs, Tooltips, Accordion).
   - Dùng `v-if`: Cho các thành phần ít khi thay đổi trong suốt phiên làm việc (quyền Admin, trang Đăng nhập/Đăng ký).""",
        "code_example": """<template>
  <!-- v-show: Phần tử vẫn nằm trong HTML, chỉ thêm style=\"display: none;\" -->
  <div v-show=\"isDropdownOpen\" class=\"menu\">
    Danh sách menu
  </div>

  <!-- v-if: Nếu isAdmin=false, phần tử bị xóa sổ hoàn toàn khỏi DOM -->
  <admin-panel v-if=\"isAdmin\" />
</template>""",
        "tips": "Nếu component con có các tác vụ nặng trong `onMounted()`, dùng `v-if` sẽ khiến `onMounted` chạy lại mỗi lần mở, còn `v-show` chỉ chạy `onMounted` đúng 1 lần duy nhất lúc đầu."
    },

    28: {
        "title_vi": "Liệt kê và tóm tắt công dụng của toàn bộ Built-in Directives trong Vue?",
        "level": "Junior",
        "short_answer": "Vue cung cấp các built-in directives: `v-text` (cập nhật textContent), `v-html` (cập nhật innerHTML), `v-show` (toggle CSS display), `v-if` / `v-else-if` / `v-else` (rẽ nhánh DOM), `v-for` (lặp danh sách), `v-on` (bắt sự kiện), `v-bind` (ràng buộc thuộc tính), `v-model` (ràng buộc 2 chiều), `v-slot` (phân phối nội dung), `v-pre` (bỏ qua biên dịch), `v-once` (chỉ render 1 lần duy nhất), `v-memo` (ghi nhớ memoize cây sub-DOM), và `v-cloak` (ẩn template thô lúc chưa tải xong).",
        "deep_dive": """1. `v-memo` (Mới trong Vue 3.2): Directive hiệu năng cao! Nhận mảng dependencies, chỉ re-render phần tử nếu một trong các dependencies thay đổi. Cực kỳ hữu dụng để tăng tốc các bảng dữ liệu `v-for` hơn 1000 dòng.
2. `v-once`: Render phần tử và mọi con của nó đúng 1 lần duy nhất, sau đó coi như nội dung tĩnh để bỏ qua trong các lần diffing tiếp theo.""",
        "code_example": """<template>
  <!-- v-pre: Giữ nguyên văn bản, không biên dịch thẻ {{ }} -->
  <span v-pre>{{ Đoạn này sẽ không bị Vue dịch }}</span>

  <!-- v-once: Chỉ render 1 lần, biến count tăng không làm thay đổi số này -->
  <h1 v-once>Tiêu đề cố định: {{ initialTitle }}</h1>
</template>""",
        "tips": "Nhắc đến directive `v-memo` của Vue 3.2+ sẽ gây ấn tượng mạnh với người phỏng vấn về khả năng tối ưu hóa bảng dữ liệu lớn."
    },

    29: {
        "title_vi": "Sự khác biệt cốt lõi giữa `v-bind` và `v-on` trong Vue?",
        "level": "Junior",
        "short_answer": "`v-bind` (viết tắt `:`) dùng để ĐẨY DỮ LIỆU TỪ TRẠNG THÁI VÀO GIAO DIỆN (State -> View) bằng cách gán giá trị cho các thuộc tính HTML hoặc props của component. Trong khi đó, `v-on` (viết tắt `@`) dùng để LẮNG NGHE CÁC SỰ KIỆN TỪ GIAO DIỆN ĐẨY VÀO TRẠNG THÁI (View -> State) bằng cách kích hoạt các hàm xử lý khi người dùng tương tác.",
        "deep_dive": """1. Chiều dữ liệu: `v-bind` là chiều đi xuống (Outbound / Downwards). `v-on` là chiều đi lên (Inbound / Upwards).
2. Khi kết hợp cả hai: Ta tạo ra Two-Way Data Binding (`v-model = v-bind + v-on`).""",
        "code_example": """<template>
  <!-- v-bind (:) gán giá trị biến vào thuộc tính disabled -->
  <!-- v-on (@) lắng nghe sự kiện click từ người dùng -->
  <button :disabled=\"isLoading\" @click=\"fetchData\">
    {{ isLoading ? 'Đang tải...' : 'Tải lại dữ liệu' }}
  </button>
</template>""",
        "tips": "Hãy ghi nhớ mẹo nhanh: Dấu `:` là đưa dữ liệu vào, dấu `@` là bắt hành động ra."
    },

    30: {
        "title_vi": "Render Functions trong Vue là gì và khi nào nên sử dụng thay cho Templates?",
        "level": "Senior",
        "short_answer": "Render Function là hàm JavaScript sử dụng trực tiếp hàm tạo Virtual DOM `h()` (Hyperscript) để mô tả cây giao diện người dùng thay vì viết bằng HTML template. Mặc dù templates đáp ứng được 95% trường hợp, nhưng Render Functions cần thiết khi bạn cần TOÀN BỘ SỨC MẠNH CỦA JAVASCRIPT để tạo các components có tính linh hoạt và động lực học cực cao (Dynamic Heading, Dynamic Component Wrappers).",
        "deep_dive": """1. Hàm `h(type, props, children)`:
   - `type`: Tên thẻ HTML (như `'div'`, `'h1'`) hoặc một Component Object.
   - `props`: Object chứa attributes, props, event listeners.
   - `children`: Nội dung chuỗi, mảng các vnodes khác hoặc slots.
2. JSX: Cho phép viết cú pháp tương tự HTML nhưng biên dịch trực tiếp sang các hàm `h()` của render function.""",
        "code_example": """<!-- DynamicHeading component dùng Render Function -->
<script>
import { h } from 'vue';

export default {
  props: {
    level: { type: Number, required: true } // level từ 1 đến 6
  },
  setup(props, { slots }) {
    // Trả về một Render Function linh hoạt theo prop level:
    // Sinh ra <h1>, <h2>, ... <h6> tương ứng một cách tự nhiên!
    return () => h(`h${props.level}`, {}, slots.default ? slots.default() : []);
  }
};
</script>

<!-- Sử dụng: <DynamicHeading :level=\"2\">Tiêu đề H2</DynamicHeading> -->""",
        "tips": "Ví dụ kinh điển nhất để chứng minh khi nào nên dùng Render Function là component `DynamicHeading` (tạo thẻ h1-h6 động dựa trên prop `level`), điều mà nếu viết bằng template sẽ phải dùng 6 khối `v-if/v-else-if` rất cồng kềnh."
    },

    31: {
        "title_vi": "Vuex là gì và vị trí lịch sử của nó trong hệ sinh thái Vue?",
        "level": "Junior",
        "short_answer": "Vuex là thư viện quản lý trạng thái tập trung (State Management Pattern + Library) chính thức của Vue trong các phiên bản trước đây (đặc biệt là Vue 2). Lấy cảm hứng từ kiến trúc Flux của Facebook, Vuex duy trì một kho lưu trữ duy nhất (Single Source of Truth) đảm bảo trạng thái chỉ có thể bị đột biến theo cách có thể dự đoán được.",
        "deep_dive": """1. Luồng dữ liệu một chiều nghiêm ngặt trong Vuex:
   `State -> View -> Actions (bất đồng bộ) -> Mutations (đồng bộ) -> State`
2. Vị trí hiện tại: Trong Vue 3, Pinia đã chính thức trở thành thư viện quản lý trạng thái khuyến nghị thay thế hoàn toàn Vuex. Vuex hiện đã ở chế độ bảo trì (Maintenance Mode).""",
        "code_example": """// Cấu trúc cơ bản của Vuex 4 trong Vue 3
import { createStore } from 'vuex';

export const store = createStore({
  state: () => ({ count: 0 }),
  mutations: {
    increment(state) { state.count++; } // BẮT BUỘC ĐỒNG BỘ
  },
  actions: {
    asyncIncrement({ commit }) {
      setTimeout(() => commit('increment'), 1000); // Cho phép bất đồng bộ
    }
  }
});""",
        "tips": "Nếu được hỏi về state management trong dự án mới hôm nay, hãy trả lời: 'Với dự án mới, chúng tôi luôn chọn Pinia thay vì Vuex'."
    },

    32: {
        "title_vi": "Khái niệm 'Store' trong quản lý trạng thái tập trung?",
        "level": "Junior",
        "short_answer": "Store là một đối tượng chứa toàn bộ trạng thái (State) của ứng dụng. Khác với một biến toàn cục thông thường (plain global object), Store có 2 đặc tính sống còn: (1) Tính phản ứng (Reactive): khi trạng thái trong store thay đổi, mọi component đang sử dụng dữ liệu đó sẽ tự động cập nhật ngay lập tức, và (2) Tính dự đoán (Predictable): không thể tùy tiện sửa đổi trạng thái từ bên ngoài mà phải thông qua các actions/mutations được kiểm soát.",
        "deep_dive": """1. Single Source of Truth: Toàn bộ thông tin đăng nhập của User, giỏ hàng, cài đặt ứng dụng đều nằm tại Store, giúp các component ở các nhánh cây xa nhau không phải truyền props lòng vòng.
2. Time-Travel Debugging: Cho phép Vue DevTools ghi lại lịch sử từng thay đổi trạng thái và tua ngược thời gian để tìm bug.""",
        "code_example": """// Minh họa tính năng của một Store hiện đại với Pinia
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null);
  const isAuthenticated = computed(() => !!currentUser.value);

  function login(userData) {
    currentUser.value = userData;
  }

  return { currentUser, isAuthenticated, login };
});""",
        "tips": "Nhớ 2 từ khóa: 'Reactive' và 'Predictable'."
    },

    33: {
        "title_vi": "Cách quản lý trạng thái toàn cục trong Vue 3 mà KHÔNG CẦN dùng Vuex hay Pinia?",
        "level": "Mid",
        "short_answer": "Nhờ hệ thống Reactivity độc lập của Vue 3, bạn hoàn toàn có thể tạo một Global Store nhẹ nhàng mà không cần cài thêm bất kỳ thư viện nào bằng cách sử dụng hàm `reactive()` hoặc `ref()` bên trong một file JavaScript/TypeScript thông thường (thường gọi là mô hình Reactive State Composable).",
        "deep_dive": """1. Ưu điểm: Không cần tốn thêm dung lượng bundle cài đặt Pinia/Vuex, cực kỳ phù hợp cho các ứng dụng vừa và nhỏ.
2. Bảo vệ tính bất biến (Read-only State): Sử dụng hàm `readonly()` bọc bên ngoài state để ngăn các component con tự ý sửa biến mà bắt buộc phải gọi qua các hàm mutator được định nghĩa sẵn.""",
        "code_example": """// store/simpleStore.js (Tự tạo Store toàn cục không cần thư viện)
import { reactive, readonly } from 'vue';

const state = reactive({
  theme: 'dark',
  notifications: []
});

// Chỉ xuất ra bản readonly để component không tự ý sửa trực tiếp
export const useThemeStore = () => {
  const setTheme = (newTheme) => {
    state.theme = newTheme;
  };

  const addNotification = (msg) => {
    state.notifications.push(msg);
  };

  return {
    state: readonly(state), // Bảo vệ state
    setTheme,
    addNotification
  };
};""",
        "tips": "Đây là câu hỏi thể hiện độ hiểu sâu về Vue 3: Hệ thống phản ứng của Vue 3 hoạt động độc lập ngoài component, do đó bạn có thể tạo store tùy biến chỉ bằng 5 dòng code `reactive()`!"
    },

    34: {
        "title_vi": "Bốn khái niệm cốt lõi của Vuex và so sánh tương đương trong Pinia?",
        "level": "Mid",
        "short_answer": "Bốn khái niệm cốt lõi của Vuex là: State (dữ liệu), Getters (dữ liệu phái sinh/computed), Mutations (hàm biến đổi state đồng bộ duy nhất), và Actions (hàm xử lý logic bất đồng bộ). Trong Pinia hiện đại, khái niệm `Mutations` ĐÃ BỊ LOẠI BỎ HOÀN TOÀN; Pinia chỉ còn 3 phần: State, Getters và Actions.",
        "deep_dive": """Bảng ánh xạ tương đương:
- `state`: Lưu trữ dữ liệu -> Tương đương `ref()` trong Pinia.
- `getters`: Tính toán bộ đệm -> Tương đương `computed()` trong Pinia.
- `mutations`: Đã bị khai tử trong Pinia vì gây rườm rà không cần thiết.
- `actions`: Xử lý cả logic đồng bộ lẫn bất đồng bộ (gọi API) trong Pinia.""",
        "code_example": """// So sánh cú pháp Pinia Setup Store cực kỳ gọn gàng:
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0);                        // State
  const doubleCount = computed(() => count.value * 2); // Getter
  
  function increment() { count.value++; }      // Action (thay thế cả mutation!)
  async function fetchNewCount() {             // Async Action
    const res = await fetch('/api/count');
    count.value = await res.json();
  }

  return { count, doubleCount, increment, fetchNewCount };
});""",
        "tips": "Điểm mấu chốt: Trong Pinia, bạn có thể thay đổi trực tiếp `store.count++` mà không cần phải commit mutation."
    },

    35: {
        "title_vi": "Mục đích phân tách giữa Mutations và Actions trong Vuex?",
        "level": "Mid",
        "short_answer": "Trong kiến trúc Vuex cũ, việc phân tách nhằm đảm bảo tính toàn vẹn của lịch sử trạng thái: (1) `Mutations` BẮT BUỘC PHẢI LÀ ĐỒNG BỘ (Synchronous) để Vue DevTools có thể chụp chính xác ảnh snapshot trạng thái trước và sau mỗi lần thay đổi, (2) `Actions` là nơi chứa toàn bộ các tác vụ BẤT ĐỒNG BỘ (Asynchronous như gọi API, setTimeout) và sau khi có dữ liệu thì `commit` sang Mutation.",
        "deep_dive": """1. Hậu quả nếu viết code bất đồng bộ trong Mutation: Vue DevTools sẽ không thể biết khi nào mutation thực sự kết thúc, dẫn đến việc Time-Travel Debugging bị loạn nhịp hoàn toàn.
2. Pinia giải quyết ra sao: Nhờ kiến trúc mới, Pinia theo dõi trực tiếp các thay đổi mà không cần chia tách rườm rà giữa mutations và actions nữa.""",
        "code_example": """// Vuex quy định nghiêm ngặt:
// Action xử lý Async -> Commit vào Mutation xử lý Sync
actions: {
  async fetchUserData({ commit }, userId) {
    const data = await api.getUser(userId); // Bất đồng bộ
    commit('SET_USER', data);               // Chuyển giao sang Mutation
  }
},
mutations: {
  SET_USER(state, payload) {
    state.user = payload; // ĐỒNG BỘ 100%
  }
}""",
        "tips": "Quy tắc nằm lòng Vuex: 'Actions xử lý Async, Mutations chỉ chạy Sync'."
    },

    36: {
        "title_vi": "Vue Router là gì và tại sao nó là công cụ thiết yếu cho Single Page Applications (SPA)?",
        "level": "Junior",
        "short_answer": "Vue Router là thư viện định tuyến chính thức của Vue.js. Trong một ứng dụng SPA, trình duyệt không tải lại toàn bộ trang từ máy chủ mỗi khi chuyển đường dẫn; thay vào đó, Vue Router chặn sự kiện thay đổi URL trên thanh địa chỉ, tự động tải và tráo đổi component tương ứng trên màn hình mà không cần reload trang.",
        "deep_dive": """1. Thành phần cốt lõi:
   - `<router-view>`: Vị trí hiển thị component khớp với URL hiện tại.
   - `<router-link to=\"/path\">`: Thẻ tạo liên kết điều hướng an toàn (thay thế thẻ `<a>`).
2. Tích hợp sâu: Quản lý lịch sử trình duyệt (Back/Forward), hỗ trợ Navigation Guards bảo vệ các trang yêu cầu đăng nhập, và tự động cuộn trang (Scroll Behavior).""",
        "code_example": """import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';

const routes = [
  { path: '/', component: HomeView },
  { 
    path: '/about', 
    // Lazy-loading: Chỉ tải file code khi người dùng thực sự bấm vào trang About!
    component: () => import('./views/AboutView.vue') 
  }
];

export const router = createRouter({
  history: createWebHistory(),
  routes
});""",
        "tips": "Luôn dùng kỹ thuật Lazy Loading `() => import('./View.vue')` cho tất cả các routes phụ để giảm kích thước bundle ban đầu."
    },

    37: {
        "title_vi": "Cách thiết lập Vue Router trong một dự án Vue 3?",
        "level": "Junior",
        "short_answer": "Thiết lập gồm 3 bước: (1) Cài đặt `vue-router@4`, (2) Tạo file cấu hình `router/index.js` gọi `createRouter()` với lịch sử `createWebHistory()` và mảng các routes, (3) Trong `main.js` gọi `app.use(router)`, và đặt thẻ `<router-view />` trong `App.vue`.",
        "deep_dive": """1. Các chế độ History:
   - `createWebHistory()`: Sử dụng HTML5 History API (`/users/profile`), URL đẹp, chuẩn SEO nhưng yêu cầu cấu hình máy chủ Nginx rewrite về `index.html`.
   - `createWebHashHistory()`: Sử dụng dấu thăng (`/#/users/profile`), hoạt động được trên mọi máy chủ mà không cần cấu hình rewrite nhưng xấu và không tốt cho SEO.""",
        "code_example": """<!-- App.vue -->
<template>
  <nav>
    <router-link to=\"/\">Trang chủ</router-link> |
    <router-link to=\"/products\">Sản phẩm</router-link>
  </nav>

  <!-- Nơi component tương ứng với URL sẽ được render -->
  <router-view />
</template>""",
        "tips": "Cảnh báo triển khai Production: Khi dùng HTML5 History Mode (`createWebHistory`), nếu người dùng F5 tại trang `/about`, server Nginx sẽ báo lỗi 404 nếu không cấu hình lệnh `try_files $uri $uri/ /index.html;`."
    },

    38: {
        "title_vi": "Cách điều hướng giữa các trang (Programmatic Navigation) trong Vue 3?",
        "level": "Junior",
        "short_answer": "Sử dụng composable `useRouter()` trong Composition API để lấy đối tượng router. Bạn có thể sử dụng các hàm: `router.push('/path')` (chuyển trang và lưu vào lịch sử), `router.replace('/path')` (thay thế trang hiện tại không thể bấm Back lại), hoặc `router.go(n)` (tiến/lùi n bước lịch sử).",
        "deep_dive": """1. Điều hướng theo tên (Named Routes): Khuyên dùng `router.push({ name: 'UserDetail', params: { id: 123 } })` thay vì ghép chuỗi URL cứng. Nếu sau này đổi path URL, toàn bộ ứng dụng không bị hỏng.""",
        "code_example": """<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function handleLoginSuccess() {
  // 1. Chuyển hướng tới trang Dashboard
  router.push('/dashboard');

  // 2. Hoặc chuyển trang có kèm query parameters
  // router.push({ path: '/search', query: { q: 'vue3' } });

  // 3. Thay thế (replace) không cho phép người dùng bấm nút Back quay lại trang login
  // router.replace('/home');
}
</script>

<template>
  <button @click=\"handleLoginSuccess\">Đăng Nhập Thành Công</button>
</template>""",
        "tips": "Nhớ: Dùng `router.replace()` cho trang Login để sau khi đăng nhập xong, người dùng bấm nút Back trình duyệt sẽ không bị quay lại form đăng nhập nữa."
    },

    39: {
        "title_vi": "Dynamic Route (Định tuyến động) là gì và cách trích xuất tham số trong Vue Router?",
        "level": "Junior",
        "short_answer": "Dynamic Route cho phép khớp nhiều URL khác nhau vào cùng một Component bằng cách sử dụng các tham số động có tiền tố dấu hai chấm `:` (ví dụ: `/users/:id`). Để đọc tham số này trong component, sử dụng composable `useRoute()` và truy cập qua `route.params.id`.",
        "deep_dive": """1. Bẫy tái sử dụng component: Khi chuyển từ `/users/1` sang `/users/2`, Vue sẽ TÁI SỬ DỤNG component hiện tại chứ không hủy đi tạo lại! Do đó các hook `onMounted()` sẽ KHÔNG CHẠY LẠI.
2. Giải pháp: Lắng nghe sự thay đổi của tham số bằng `watch(() => route.params.id, (newId) => fetchUser(newId))` hoặc thêm `:key=\"route.fullPath\"` vào `<router-view>`.""",
        "code_example": """<script setup>
import { useRoute } from 'vue-router';
import { ref, watch, onMounted } from 'vue';

const route = useRoute();
const userId = ref(route.params.id);

function loadUser(id) {
  console.log('Tải dữ liệu cho người dùng ID:', id);
}

onMounted(() => loadUser(route.params.id));

// Theo dõi khi người dùng chuyển từ user này sang user khác trên cùng component
watch(() => route.params.id, (newId) => {
  userId.value = newId;
  loadUser(newId);
});
</script>

<template>
  <div>Thông tin chi tiết người dùng: {{ userId }}</div>
</template>""",
        "tips": "Câu hỏi bẫy kinh điển: 'Tại sao chuyển giữa các dynamic route thì dữ liệu trên trang không tự cập nhật?' Hãy trả lời ngay về cơ chế component reuse và giải pháp dùng `watch` trên `route.params`."
    },

    40: {
        "title_vi": "Cách cấu hình Nested Routes (Định tuyến lồng nhau) trong Vue Router?",
        "level": "Mid",
        "short_answer": "Nested Routes được cấu hình bằng thuộc tính `children: [...]` bên trong định nghĩa của route cha. Component của route cha phải chứa một thẻ `<router-view>` nội bộ để làm nơi hiển thị cho các component con tương ứng.",
        "deep_dive": """1. Đường dẫn con: Nếu path của route con bắt đầu bằng dấu gạch chéo `/` (ví dụ `/profile`), nó sẽ được coi là đường dẫn tuyệt đối từ root. Để nối tiếp cha, hãy dùng đường dẫn tương đối (ví dụ `path: 'profile'`).
2. Ứng dụng: Cực kỳ phổ biến trong các trang Dashboard có Sidebar cố định và vùng nội dung thay đổi theo từng tab.""",
        "code_example": """// router/index.js
const routes = [
  {
    path: '/user/:id',
    component: UserLayout, // Chứa <router-view> bên trong
    children: [
      {
        path: '', // Khi vào đúng /user/:id
        component: UserHome
      },
      {
        path: 'profile', // Khớp /user/:id/profile
        component: UserProfile
      },
      {
        path: 'settings', // Khớp /user/:id/settings
        component: UserSettings
      }
    ]
  }
];""",
        "tips": "Luôn nhớ: Phải có `<router-view>` bên trong template của component cha thì route con mới có chỗ hiển thị."
    },

    41: {
        "title_vi": "Mixins trong Vue là gì và tại sao chúng bị coi là Anti-Pattern trong Vue 3?",
        "level": "Mid",
        "short_answer": "Mixins là cơ chế chia sẻ logic giữa các components trong Vue 2 bằng cách gộp các options (data, methods, computed) vào component. Trong Vue 3, Mixins bị coi là Anti-Pattern và được THAY THẾ HOÀN TOÀN bằng Composition API (Composables) do Mixins có các nhược điểm nghiêm trọng: Xung đột tên thuộc tính (Name collisions), Nguồn gốc dữ liệu ngầm không rõ ràng (Implicit dependencies), và khó tái cấu trúc.",
        "deep_dive": """1. Vấn đề của Mixin: Khi một component nạp 3 mixins khác nhau, bạn không thể biết một biến `this.isLoading` xuất phát từ mixin nào. Nếu 2 mixin cùng đặt tên 1 biến là `data`, chúng sẽ âm thầm ghi đè lên nhau gây lỗi hiểm hóc.
2. Composable giải quyết triệt để: Composable là các hàm thuần túy trả về đối tượng rõ ràng, cho phép đổi tên biến (destructuring rename) và tường minh 100% nguồn gốc dữ liệu.""",
        "code_example": """// ❌ Mixin cũ thời Vue 2 (Gây rối rắm):
// mixins: [userMixin, authMixin, analyticsMixin]

// ✅ Composable chuẩn mực trong Vue 3:
import { useUser } from '@/composables/useUser';
import { useAuth } from '@/composables/useAuth';

const { user, fetchUser } = useUser();
const { isAuthenticated, login } = useAuth(); // Tường minh 100%!""",
        "tips": "Khi được hỏi về Mixins, hãy khẳng định: 'Mixins hiện đã lỗi thời trong Vue 3. Toàn bộ logic dùng chung hiện nay được viết bằng Custom Composables'."
    },

    42: {
        "title_vi": "Quy tắc hợp nhất (Merge Strategies) khi Component sử dụng Mixins?",
        "level": "Senior",
        "short_answer": "Khi một mixin và một component chứa các tùy chọn trùng tên, Vue áp dụng các chiến lược hợp nhất mặc định: (1) Với `data`: Thuộc tính của Component luôn được ưu tiên ghi đè lên mixin, (2) Với `methods`, `components`, `directives`: Thuộc tính của Component ghi đè lên mixin, và (3) Với `Lifecycle Hooks`: TẤT CẢ các hooks cùng tên được gộp thành một mảng; Hook của Mixin chạy TRƯỚC, Hook của Component chạy SAU.",
        "deep_dive": """1. Nguy cơ lỗi ngầm: Nếu 2 mixins khác nhau cùng có hook `mounted()`, cả 2 hook đều chạy theo thứ tự nạp mixin, dễ gây các thao tác gọi API trùng lặp nếu lập trình viên không để ý.""",
        "code_example": """// Minh họa thứ tự thực thi của Lifecycle Hooks với Mixin:
// 1. mixinA mounted() chạy đầu tiên
// 2. mixinB mounted() chạy thứ hai
// 3. component mounted() chạy cuối cùng""",
        "tips": "Hiểu rõ quy tắc merge của Options API giúp bạn dễ dàng bảo trì hoặc di chuyển các dự án Vue 2 cũ sang Vue 3."
    },

    43: {
        "title_vi": "Custom Directives trong Vue là gì và cách tạo một directive tự động focus vào ô input?",
        "level": "Mid",
        "short_answer": "Custom Directives cho phép lập trình viên đóng gói các thao tác can thiệp trực tiếp vào phần tử DOM tầng thấp để tái sử dụng trên nhiều thẻ khác nhau. Trong `<script setup>`, bất kỳ biến nào bắt đầu bằng tiền tố `v` viết theo chuẩn camelCase (ví dụ `vFocus`) sẽ tự động được nhận diện làm directive `v-focus`.",
        "deep_dive": """1. Các hooks trong một Custom Directive:
   - `created(el, binding, vnode)`
   - `beforeMount(el, binding, vnode)`
   - `mounted(el, binding, vnode)`: Thường dùng nhất để thao tác với DOM sau khi phần tử đã được gắn vào trang.
   - `updated(el, binding, vnode)`
   - `unmounted(el, binding, vnode)`: Dọn dẹp sự kiện.""",
        "code_example": """<script setup>
// Khai báo Custom Directive cục bộ trong <script setup>
// Tên biến bắt đầu bằng 'v' + TênDirective (vFocus -> v-focus)
const vFocus = {
  mounted: (el) => {
    el.focus(); // Tự động focus con trỏ vào ô nhập ngay khi render!
  }
};
</script>

<template>
  <!-- Sử dụng directive v-focus -->
  <input v-focus placeholder=\"Ô này tự động được focus khi mở trang\" />
</template>""",
        "tips": "Chỉ dùng Custom Directives khi bạn thực sự cần thao tác trực tiếp với DOM (như autofocus, click-outside, v-mask định dạng số tiền, lazy-loading ảnh)."
    },

    44: {
        "title_vi": "Cách đăng ký một Custom Directive toàn cục (Global Directive)?",
        "level": "Junior",
        "short_answer": "Trong file `main.js`, sử dụng phương thức `app.directive('directive-name', directiveDefinition)` trên đối tượng ứng dụng tạo bởi `createApp()`. Sau khi đăng ký toàn cục, directive có thể sử dụng ở bất kỳ component nào trong toàn dự án mà không cần khai báo lại.",
        "deep_dive": """1. Ví dụ Directive kiểm tra quyền (v-permission): Ẩn hoặc xóa một nút bấm khỏi DOM nếu người dùng hiện tại không có quyền tương ứng trong hệ thống.""",
        "code_example": """// main.js
import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

// Đăng ký Global Directive v-highlight
app.directive('highlight', {
  mounted(el, binding) {
    el.style.backgroundColor = binding.value || 'yellow';
  }
});

app.mount('#app');

// Trong bất kỳ file template nào:
// <p v-highlight=\"'#a7f3d0'\">Đoạn văn được tô màu nền toàn cục!</p>""",
        "tips": "Đặt tên directive toàn cục không cần có chữ `v-` trong lệnh đăng ký `app.directive('highlight', ...)`."
    },

    45: {
        "title_vi": "Thảo luận trường hợp thực tế hữu dụng nhất cho Custom Directive: Click Outside để đóng Dropdown?",
        "level": "Mid",
        "short_answer": "Một trong những trường hợp thực tế xuất sắc nhất của Custom Directive là `v-click-outside`. Khi người dùng mở một Menu Dropdown hoặc Modal, nếu họ bấm chuột ra bất kỳ vị trí nào bên ngoài vùng của Menu, directive này sẽ phát hiện và tự động kích hoạt hàm đóng Menu lại.",
        "deep_dive": """1. Cơ chế hoạt động:
   - Trong `mounted()`: Gắn sự kiện `document.addEventListener('click', handler)`.
   - Trong `handler`: Kiểm tra xem phần tử bị click (`event.target`) có nằm BÊN TRONG phần tử directive gắn vào (`el.contains(event.target)`) hay không. Nếu KHÔNG nằm bên trong, gọi hàm callback do người dùng truyền vào.
   - Trong `unmounted()`: BẮT BUỘC gỡ bỏ `document.removeEventListener` để không bị rò rỉ bộ nhớ!""",
        "code_example": """<script setup>
import { ref } from 'vue';
const isOpen = ref(false);

const vClickOutside = {
  mounted(el, binding) {
    el._clickOutsideHandler = (event) => {
      // Nếu click ra ngoài el thì kích hoạt hàm callback
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el._clickOutsideHandler);
  },
  unmounted(el) {
    document.removeEventListener('click', el._clickOutsideHandler);
  }
};

function closeMenu() {
  isOpen.value = false;
}
</script>

<template>
  <div v-click-outside=\"closeMenu\" class=\"dropdown-container\">
    <button @click=\"isOpen = !isOpen\">Mở Menu</button>
    <div v-show=\"isOpen\" class=\"dropdown-menu\">
      <p>Mục 1</p><p>Mục 2</p>
    </div>
  </div>
</template>""",
        "tips": "Nếu trong dự án thực tế, bạn có thể dùng sẵn hàm `onClickOutside()` cực kỳ mạnh mẽ từ thư viện mã nguồn mở hàng đầu `@vueuse/core`."
    },

    46: {
        "title_vi": "Vite là gì và tại sao nó thay thế Vue CLI làm công cụ build mặc định cho Vue?",
        "level": "Junior",
        "short_answer": "Vite là công cụ build frontend thế hệ mới do chính Evan You (tác giả của Vue) tạo ra. Vite thay thế hoàn toàn Vue CLI vì giải quyết triệt để vấn đề tốc độ phát triển: Khởi động dev server tức thì (< 300ms) bất kể kích thước dự án, cập nhật thay đổi mã nguồn ngay lập tức (Hot Module Replacement siêu tốc), và tối ưu hóa bundle sản xuất bằng Rollup và esbuild.",
        "deep_dive": """1. Tại sao Webpack / Vue CLI bị chậm: Webpack tiếp cận theo kiểu 'Bundler-based': nó phải phân tích, nạp và đóng gói toàn bộ cây module trước khi server có thể chạy. Dự án càng to, thời gian chờ khởi động càng kéo dài từ vài chục giây đến vài phút.
2. Tại sao Vite siêu nhanh: Vite tiếp cận theo kiểu 'Native ESM-based': trình duyệt trực tiếp yêu cầu từng module qua HTTP request theo chuẩn ES Modules hiện đại, Vite chỉ biên dịch đúng file bạn đang mở trên màn hình!""",
        "code_example": """// vite.config.js - Cấu hình tối giản và mạnh mẽ
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'node:path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Rút gọn đường dẫn @ trỏ tới src
    },
  },
  server: {
    port: 3000,
    open: true
  }
});""",
        "tips": "Vite hiện nay không chỉ là tiêu chuẩn của Vue mà còn trở thành công cụ build hàng đầu cho React, Svelte và toàn bộ hệ sinh thái frontend."
    },

    47: {
        "title_vi": "Cách tích hợp bộ tiền xử lý CSS (SASS / SCSS) vào dự án Vue 3 với Vite?",
        "level": "Junior",
        "short_answer": "Trong các dự án sử dụng Vite, bạn KHÔNG CẦN phải cài đặt `sass-loader` hay cấu hình Webpack phức tạp. Bạn chỉ cần chạy duy nhất một lệnh cài đặt compiler: `npm install -D sass`. Sau đó trong component Vue, chỉ cần thêm thuộc tính `lang=\"scss\"` vào thẻ `<style>` là có thể sử dụng đầy đủ các tính năng của SASS/SCSS.",
        "deep_dive": """1. Cấu hình biến dùng chung toàn cục: Bạn có thể cấu hình `additionalData` trong `vite.config.js` để tự động nạp file biến `variables.scss` vào mọi component mà không cần phải gõ lệnh `@import` thủ công ở từng file.""",
        "code_example": """# Bước 1: Cài đặt SASS
npm install -D sass

<!-- Bước 2: Dùng ngay trong component -->
<template>
  <div class=\"box\">
    <span class=\"text\">SCSS trong Vue 3</span>
  </div>
</template>

<style lang=\"scss\" scoped>
$primary-color: #42b883;

.box {
  padding: 20px;
  .text {
    color: $primary-color;
    font-weight: bold;
    &:hover { text-decoration: underline; }
  }
}
</style>""",
        "tips": "Nhớ: Trong Vite, chỉ cần cài package `sass`, không cần cài `sass-loader`."
    },

    48: {
        "title_vi": "Mục đích và các tính năng mạnh mẽ của Vue DevTools?",
        "level": "Junior",
        "short_answer": "Vue DevTools là tiện ích mở rộng trình duyệt (Browser Extension) chính thức phục vụ việc gỡ lỗi ứng dụng Vue. Các tính năng cốt lõi bao gồm: (1) Kiểm tra cây Component và sửa đổi trực tiếp giá trị của Props / State theo thời gian thực, (2) Theo dõi dòng thời gian phát sự kiện (Events Timeline), (3) Time-Travel Debugging cho Pinia/Vuex, (4) Quản lý định tuyến và params của Vue Router, và (5) Phân tích hiệu năng render (Performance Profiler).",
        "deep_dive": """1. Vite Vue DevTools (In-App DevTools): Từ phiên bản mới, Vue hỗ trợ `vite-plugin-vue-devtools` tích hợp trực tiếp bảng điều khiển DevTools ngay bên trong giao diện web của ứng dụng mà không bắt buộc người dùng phải cài extension trình duyệt!""",
        "code_example": """// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import VueDevTools from 'vite-plugin-vue-devtools';

export default defineConfig({
  plugins: [
    vue(),
    VueDevTools() // Kích hoạt DevTools nhúng trực tiếp cực kỳ tiện lợi
  ],
});""",
        "tips": "Nếu component không cập nhật giao diện, mở Vue DevTools kiểm tra xem biến reactive có thực sự đổi giá trị không là cách bắt bệnh nhanh nhất."
    },

    49: {
        "title_vi": "Cách cấu hình các môi trường khác nhau (Development, Staging, Production) trong Vue với Vite?",
        "level": "Mid",
        "short_answer": "Vite sử dụng các file `.env` theo chuẩn quy ước. Để biến môi trường có thể phơi bày và đọc được trong mã nguồn frontend của Vue, BẮT BUỘC tên biến phải có tiền tố `VITE_` (ví dụ `VITE_API_URL`). Trong code, bạn truy cập biến thông qua đối tượng `import.meta.env.VITE_API_URL` thay vì `process.env` cũ.",
        "deep_dive": """1. Phân cấp file môi trường:
   - `.env`: Dùng chung cho mọi môi trường.
   - `.env.development`: Chạy khi gõ `npm run dev` (`import.meta.env.MODE === 'development'`).
   - `.env.production`: Chạy khi gõ `npm run build`.
   - `.env.local`: File cục bộ trên máy dev (phải cho vào `.gitignore`).
2. Các biến có sẵn của Vite:
   - `import.meta.env.MODE`: Chuỗi môi trường hiện tại.
   - `import.meta.env.PROD`: Boolean (`true` nếu là production build).
   - `import.meta.env.DEV`: Boolean (`true` nếu là local dev).""",
        "code_example": """# File: .env.development
VITE_API_BASE_URL=http://localhost:3000/api
VITE_APP_TITLE=Shop Dev

# File: .env.production
VITE_API_BASE_URL=https://api.myproductionshop.com
VITE_APP_TITLE=My Production Shop

// src/services/api.js (Truy cập an toàn trong code)
const apiUrl = import.meta.env.VITE_API_BASE_URL;
console.log('Đang kết nối tới:', apiUrl);""",
        "tips": "Bẫy phỏng vấn: 'Tại sao tôi khai báo API_KEY trong file .env mà import.meta.env.API_KEY lại bị undefined?' Trả lời ngay: Thiếu tiền tố `VITE_`! Vite cố tình làm vậy để bảo vệ các biến môi trường nhạy cảm của máy tính không bị vô tình lộ ra ngoài trình duyệt."
    },

    50: {
        "title_vi": "Các chiến lược tối ưu hóa hiệu năng (Performance Optimization) hàng đầu cho ứng dụng Vue.js?",
        "level": "Senior",
        "short_answer": "Tối ưu hóa hiệu năng Vue toàn diện bao gồm: (1) Lazy Loading routes và components bằng `defineAsyncComponent()`, (2) Sử dụng Virtual Scrolling (`vue-virtual-scroller`) cho danh sách hàng vạn phần tử, (3) Tận dụng directive `v-memo` và `v-once` để bỏ qua diffing các phần tử tĩnh, (4) Đóng băng dữ liệu tĩnh lớn bằng `shallowRef()` hoặc `markRaw()`, (5) Dọn dẹp triệt để timers và event listeners trong `onUnmounted`, và (6) Tối ưu hóa kích thước build bằng Tree-shaking và nén ảnh WebP/AVIF.",
        "deep_dive": """1. Sức mạnh của `shallowRef()`: Với một danh sách dữ liệu 100,000 dòng tải từ API về chỉ để hiển thị, việc dùng `ref()` sẽ khiến Vue duyệt đệ quy qua từng thuộc tính của 100,000 objects để tạo Proxy (tốn hàng trăm MB RAM). Dùng `shallowRef()` chỉ theo dõi biến ở tầng ngoài cùng, giảm 90% thời gian khởi tạo và tiết kiệm bộ nhớ RAM khổng lồ!
2. Async Components: Tách nhỏ các modals, dialogs hiếm khi mở thành các chunk riêng chỉ tải về khi bấm nút.""",
        "code_example": """<script setup>
import { shallowRef, defineAsyncComponent } from 'vue';

// 1. Tối ưu dữ liệu lớn chỉ đọc bằng shallowRef
const largeDataset = shallowRef([]);

// 2. Tải component Modal bất đồng bộ khi cần dùng
const HeavyChartModal = defineAsyncComponent(() =>
  import('@/components/HeavyChartModal.vue')
);
</script>""",
        "tips": "Khi được hỏi về tối ưu Vue cho dữ liệu lớn, hãy đưa ra vũ khí `shallowRef()` và `v-memo`. Đây là hai kỹ thuật chuẩn Senior giúp phân biệt lập trình viên thông thường với chuyên gia tối ưu."
    }
}
