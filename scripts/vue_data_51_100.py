"""Vue.js Interview Questions & Answers Database (Part 2: Q51 - Q100)"""

VUE_ANSWERS_PART2 = {
    51: {
        "title_vi": "Functional Components trong Vue là gì và vị thế của chúng trong Vue 3?",
        "level": "Mid",
        "short_answer": "Functional Components là các component phi trạng thái (Stateless), không có instance, không có lifecycle hooks, chỉ đơn giản là một hàm nhận props và context rồi trả về Virtual DOM (VNodes). Trong Vue 2, chúng được sử dụng rộng rãi để tăng tốc độ render. Tuy nhiên trong Vue 3, do Stateful Components thông thường đã được tối ưu hóa cực kỳ mạnh mẽ, sự chênh lệch hiệu năng không còn đáng kể và Functional Components hiện nay chủ yếu dùng cho các trường hợp đặc biệt viết bằng JSX/Render Functions.",
        "deep_dive": """1. Cú pháp trong Vue 3: Đơn giản là một hàm JavaScript tiêu chuẩn nhận `(props, context)`.
2. Không còn cần khai báo `functional: true`: Trong Vue 3 SFC, thẻ `<template functional>` đã bị loại bỏ hoàn toàn.""",
        "code_example": """// Functional Component dạng hàm thuần trong Vue 3
import { h } from 'vue';

const DynamicBadge = (props, context) => {
  return h('span', { class: `badge badge-${props.type}` }, context.slots.default());
};

DynamicBadge.props = ['type'];
export default DynamicBadge;""",
        "tips": "Nếu được hỏi 'Có nên chuyển toàn bộ component sang functional component trong Vue 3 để tăng tốc không?', câu trả lời là KHÔNG CẦN, vì Vue 3 đã tối ưu component thường nhanh tương đương functional component."
    },

    52: {
        "title_vi": "Cách sử dụng cặp tính năng `provide` và `inject` trong Vue 3?",
        "level": "Mid",
        "short_answer": "`provide` và `inject` là cặp tính năng giải quyết triệt để vấn nạn Prop Drilling. Component tổ tiên ở tầng trên sử dụng `provide('key', value)` để cung cấp dữ liệu, và BẤT KỲ component con cháu nào ở bất kỳ độ sâu nào bên dưới cây phân cấp đều có thể gọi `inject('key', defaultValue)` để lấy dữ liệu mà không cần thông qua các tầng trung gian.",
        "deep_dive": """1. Giữ tính phản ứng (Reactivity): Nếu bạn truyền một biến `ref` hoặc `reactive` vào `provide`, component con khi `inject` sẽ giữ nguyên tính phản ứng! Khi cha đổi giá trị, con tự động cập nhật theo.
2. Best practice cập nhật dữ liệu: Nếu component con cần thay đổi dữ liệu của `provide`, bạn nên `provide` kèm theo một HÀM CẬP NHẬT (Mutator function) từ cha, và bọc giá trị bằng `readonly()` để con không tự ý sửa đổi bừa bãi.""",
        "code_example": """<!-- Component Cha (Ancestor.vue) -->
<script setup>
import { provide, ref, readonly } from 'vue';

const location = ref('Hà Nội');
function updateLocation(newLoc) {
  location.value = newLoc;
}

// Cung cấp dữ liệu readonly kèm hàm cập nhật an toàn
provide('locationData', {
  location: readonly(location),
  updateLocation
});
</script>

<!-- Component Cháu (DeepDescendant.vue) -->
<script setup>
import { inject } from 'vue';

const { location, updateLocation } = inject('locationData');
</script>

<template>
  <div>
    <p>Địa điểm hiện tại: {{ location }}</p>
    <button @click=\"updateLocation('Đà Nẵng')\">Chuyển địa điểm</button>
  </div>
</template>""",
        "tips": "Để tránh xung đột tên key khi làm dự án lớn, hãy sử dụng `Symbol()` làm Injection Key: `const key = Symbol(); provide(key, ...);`."
    },

    53: {
        "title_vi": "Đăng ký Component Toàn cục (Global) vs Cục bộ (Local) trong Vue?",
        "level": "Junior",
        "short_answer": "Đăng ký Toàn cục bằng `app.component('MyComponent', MyComponent)` giúp component có thể sử dụng ở bất kỳ đâu trong dự án mà không cần import, nhưng có nhược điểm làm mất tính năng Tree-shaking (khiến dung lượng file build to hơn dù không dùng đến). Đăng ký Cục bộ bằng cách import trực tiếp trong component nào cần dùng, giúp code tường minh, hỗ trợ Tree-shaking và tối ưu hóa kích thước bundle.",
        "deep_dive": """1. Trong Vue 3 `<script setup>`: Khi bạn viết `import MyButton from './MyButton.vue'`, component đó tự động được đăng ký cục bộ trong template ngay lập tức mà không cần thêm bất kỳ boilerplate nào.
2. Khi nào nên đăng ký toàn cục: Chỉ nên áp dụng cho các Base UI components xuất hiện ở khắp mọi nơi (như BaseButton, BaseIcon, BaseSpinner).""",
        "code_example": """// main.js - Đăng ký toàn cục (Chỉ dùng cho component cốt lõi)
import BaseSpinner from '@/components/base/BaseSpinner.vue';
app.component('BaseSpinner', BaseSpinner);

<!-- Trong component bất kỳ: Dùng trực tiếp không cần import -->
<template>
  <BaseSpinner />
</template>""",
        "tips": "Khuyên dùng đăng ký Cục bộ trong 90% trường hợp để tận dụng tối đa khả năng Tree-shaking của Vite/Rollup."
    },

    54: {
        "title_vi": "Cách xử lý dữ liệu không phản ứng (Non-reactive Data) để tối ưu RAM trong Vue?",
        "level": "Senior",
        "short_answer": "Khi làm việc với các đối tượng dữ liệu khổng lồ (bản đồ 3D Three.js, bảng dữ liệu 100,000 dòng từ API chỉ để hiển thị, hoặc các instance của Class bên thứ 3 phức tạp), việc đưa chúng vào `ref()` hay `reactive()` sẽ khiến Vue tốn CPU và RAM để bọc Proxy đệ quy. Để ngăn chặn điều này, ta sử dụng hàm `shallowRef()`, `markRaw()`, hoặc lưu dữ liệu dưới dạng biến thông thường bên ngoài `setup`.",
        "deep_dive": """1. `shallowRef()`: Chỉ theo dõi sự thay đổi của thuộc tính `.value` ở tầng ngoài cùng, hoàn toàn không biến các thuộc tính con bên trong thành reactive.
2. `markRaw()`: Đánh dấu một đối tượng vĩnh viễn không bao giờ bị chuyển đổi thành Proxy reactive.""",
        "code_example": """<script setup>
import { shallowRef, markRaw } from 'vue';
import * as THREE from 'three';

// 1. Tối ưu: Three.js Scene chứa hàng nghìn ma trận, dùng markRaw để Vue không can thiệp
const scene = markRaw(new THREE.Scene());

// 2. Danh sách 50,000 records từ database chỉ để hiển thị bảng
const rawTableData = shallowRef([]);

async function loadData() {
  const res = await fetch('/api/large-dataset');
  // Gán lại .value để kích hoạt render 1 lần, không tốn RAM bọc proxy từng phần tử
  rawTableData.value = await res.json();
}
</script>""",
        "tips": "Nếu ứng dụng Vue của bạn bị lag giật khi hiển thị biểu đồ Chart.js hoặc Leaflet/Mapbox, thủ phạm 99% là bạn đã vô tình bọc instance của Chart vào `reactive()`. Hãy dùng `shallowRef` hoặc `markRaw` để giải quyết ngay lập tức!"
    },

    55: {
        "title_vi": "Khái niệm Higher-Order Components (HOC) trong Vue và sự thay thế của nó?",
        "level": "Senior",
        "short_answer": "Higher-Order Component (HOC) là một hàm nhận vào một Component và trả về một Component mới đã được tăng cường tính năng hoặc dữ liệu (mô hình Decorator phổ biến trong React). Trong Vue, HOC ít phổ biến hơn do Vue có hệ thống Template và Slots rất mạnh. Trong Vue 3, toàn bộ mục đích sử dụng của HOC đã được THAY THẾ HOÀN TOÀN bằng Custom Composables và Scoped Slots vì chúng sạch sẽ và dễ hiểu hơn nhiều.",
        "deep_dive": """1. Nhược điểm của HOC trong Vue: Khó truyền props xuống component bọc bên trong, làm mất các named slots, và khó khăn trong việc suy luận kiểu dữ liệu với TypeScript.
2. Giải pháp hiện đại: Sử dụng Composable để chia sẻ logic xử lý dữ liệu, và dùng Component con bình thường để hiển thị giao diện.""",
        "code_example": """// Thay vì viết HOC withLoading(Component)...
// Trong Vue 3, ta viết Composable useAsyncData():
export function useAsyncData(fetchFn) {
  const data = ref(null);
  const loading = ref(true);
  const error = ref(null);

  fetchFn()
    .then(res => data.value = res)
    .catch(err => error.value = err)
    .finally(() => loading.value = false);

  return { data, loading, error };
}""",
        "tips": "Khẳng định với nhà tuyển dụng: 'Composables trong Vue 3 giải quyết 100% các bài toán mà HOC giải quyết nhưng với cú pháp đơn giản, không bị lồng cây component và hỗ trợ TypeScript hoàn hảo'."
    },

    56: {
        "title_vi": "Hệ thống phản ứng (Reactivity System) của Vue hoạt động như thế nào?",
        "level": "Senior",
        "short_answer": "Hệ thống Reactivity của Vue hoạt động dựa trên mô hình Xuất bản - Đăng ký (Pub/Sub) kết hợp Dependency Tracking (Theo dõi phụ thuộc). Khi một biến phản ứng được đọc (Get) trong quá trình render, Vue sẽ 'thu thập' hiệu ứng đó làm phụ thuộc (Track). Khi biến phản ứng bị gán giá trị mới (Set), Vue sẽ 'kích hoạt' lại tất cả các hiệu ứng phụ thuộc đó để tự động cập nhật giao diện (Trigger).",
        "deep_dive": """1. Cơ chế trong Vue 2: Dùng `Object.defineProperty()` can thiệp getter/setter. Hạn chế: không phát hiện được việc thêm/xóa thuộc tính mới hoặc thay đổi phần tử mảng qua chỉ số `arr[0] = x`.
2. Cơ chế trong Vue 3: Nâng cấp hoàn toàn lên JavaScript `Proxy`. Proxy bọc toàn bộ đối tượng và chặn được mọi thao tác (get, set, deleteProperty, has, ownKeys), hỗ trợ đầy đủ `Map`, `Set` và mảng mà không gặp bất kỳ giới hạn nào của Vue 2!""",
        "code_example": """// Minh họa nguyên lý cốt lõi của Reactivity qua Proxy trong Vue 3:
function reactive(target) {
  return new Proxy(target, {
    get(obj, key, receiver) {
      track(obj, key); // 1. Thu thập hàm render đang chạy vào danh sách theo dõi
      return Reflect.get(obj, key, receiver);
    },
    set(obj, key, value, receiver) {
      const result = Reflect.set(obj, key, value, receiver);
      trigger(obj, key); // 2. Kích hoạt thông báo cho các hàm render cập nhật lại DOM!
      return result;
    }
  });
}""",
        "tips": "Hai từ khóa cốt lõi của Vue 3 Reactivity: `track()` (thu thập dependency lúc get) và `trigger()` (kích hoạt effect lúc set)."
    },

    57: {
        "title_vi": "Cách thêm thuộc tính mới vào đối tượng một cách phản ứng trong Vue 2 vs Vue 3?",
        "level": "Mid",
        "short_answer": "Trong Vue 2, do hạn chế của `Object.defineProperty`, việc gán trực tiếp `this.myObj.newProp = 123` sẽ KHÔNG phản ứng lên giao diện; bắt buộc phải dùng `Vue.set(this.myObj, 'newProp', 123)`. Trong Vue 3, nhờ sử dụng `Proxy`, bạn có thể thoải mái thêm hoặc xóa bất kỳ thuộc tính mới nào bằng cú pháp JavaScript bình thường (`myObj.newProp = 123`), Vue 3 tự động nhận biết và cập nhật DOM ngay lập tức!",
        "deep_dive": """1. Khai tử `Vue.set()`: Trong Vue 3, hàm `Vue.set()` và `Vue.delete()` đã bị loại bỏ hoàn toàn vì không còn cần thiết nữa.
2. Xóa thuộc tính: Trong Vue 3, chỉ cần dùng toán tử `delete myObj.prop` là DOM tự cập nhật.""",
        "code_example": """<script setup>
import { reactive } from 'vue';

const user = reactive({ name: 'Alex' });

function addAgeProperty() {
  // ✅ Trong Vue 3: Thêm thuộc tính mới tự nhiên 100%, giao diện tự cập nhật ngay!
  user.age = 28;
}
</script>

<template>
  <div>
    <p>Tên: {{ user.name }}</p>
    <p v-if=\"user.age\">Tuổi: {{ user.age }}</p>
    <button @click=\"addAgeProperty\">Thêm Tuổi</button>
  </div>
</template>""",
        "tips": "Nếu gặp câu hỏi về `Vue.set()` hoặc `$set`, hãy nhấn mạnh ngay rằng đó là vấn đề quá khứ của Vue 2. Trong Vue 3 Proxy, hạn chế này đã được giải quyết triệt để."
    },

    58: {
        "title_vi": "Mô hình Observer Pattern được áp dụng như thế nào trong Vue Reactivity?",
        "level": "Senior",
        "short_answer": "Vue Reactivity là một biến thể thanh lịch của Observer Pattern: (1) Subject (Chủ thể): Là các biến dữ liệu phản ứng được bọc bởi Proxy. Mỗi thuộc tính của dữ liệu duy trì một tập hợp các subscribers (Dep), (2) Observer (Người quan sát): Là các Reactive Effects (như hàm render component, `computed`, `watchEffect`), và (3) Khi Subject thay đổi giá trị, nó thông báo (notify) đến tất cả các Observers đăng ký để tự động tính toán lại.",
        "deep_dive": """1. Tự động hoàn toàn: Khác với Observer Pattern thủ công phải viết `subject.subscribe(observer)`, Vue thực hiện việc đăng ký hoàn toàn ngầm định (Implicit Dependency Tracking) khi thuộc tính được đọc trong quá trình effect đang chạy.""",
        "code_example": """// Minh họa dòng chảy:
// Effect (Observer) đang chạy -> Đọc state.count (Subject)
// -> state.count tự động thêm Effect này vào danh sách lắng nghe
// -> Khi state.count thay đổi -> Phát lệnh thông báo Effect chạy lại!""",
        "tips": "Nhắc đến việc Vue không yêu cầu khai báo mảng phụ thuộc thủ công như React `useEffect([a, b])` chính là nhờ cơ chế Observer tự động này."
    },

    59: {
        "title_vi": "Vai trò của lớp `Dep` (Dependency) trong hệ thống phản ứng của Vue?",
        "level": "Senior",
        "short_answer": "`Dep` (Dependency) đóng vai trò như một cầu nối lưu trữ danh sách các Effects (Subscribers) đang phụ thuộc vào một thuộc tính phản ứng cụ thể. Trong Vue 3, `Dep` là một cấu trúc dữ liệu `Set` chứa các `ReactiveEffect`. Nó có 2 nhiệm vụ cốt lõi: `depend()` (thêm effect hiện tại vào danh sách theo dõi) và `notify()` (lặp qua Set để kích hoạt toàn bộ các effects chạy lại).",
        "deep_dive": """1. Bản đồ phụ thuộc toàn cầu (`targetMap`):
   Vue 3 quản lý toàn bộ dependencies thông qua một `WeakMap`:
   `targetMap: WeakMap<targetObject, Map<propertyKey, Dep>>`
2. Tại sao dùng `WeakMap`: Đảm bảo khi một đối tượng bị hủy, bộ nhớ liên quan đến các dependencies của nó sẽ được Garbage Collector thu hồi tự động, hoàn toàn không bị rò rỉ bộ nhớ.""",
        "code_example": """// Cấu trúc nội bộ của Vue 3 Reactivity
// targetMap (WeakMap)
//    └─ target (Object)
//          └─ key (Thuộc tính)
//                └─ dep (Set các ReactiveEffects)""",
        "tips": "Từ khóa đắt giá nhất câu này: '`WeakMap` targetMap' - việc dùng WeakMap chứng minh sự am hiểu sâu sắc về kiến trúc nội bộ của Vue 3 Core."
    },

    60: {
        "title_vi": "Cách tạo một Writable Computed Property (Computed có cả Getter và Setter)?",
        "level": "Mid",
        "short_answer": "Mặc định, `computed()` chỉ nhận một hàm getter và chỉ có quyền đọc (Read-only). Để tạo một computed property có thể ghi được (Writable Computed), ta truyền vào một Object chứa 2 hàm: `get()` (trả về giá trị tính toán) và `set(newValue)` (xử lý logic khi có hành động gán giá trị mới).",
        "deep_dive": """1. Trường hợp sử dụng phổ biến nhất: Kết hợp với `v-model` trên component con để đồng bộ prop từ component cha mà không vi phạm nguyên tắc một chiều (One-Way Data Flow).""",
        "code_example": """<script setup>
import { ref, computed } from 'vue';

const firstName = ref('Văn');
const lastName = ref('Nguyễn');

// Writable Computed Property
const fullName = computed({
  // Getter: Đọc dữ liệu
  get() {
    return `${lastName.value} ${firstName.value}`;
  },
  // Setter: Kích hoạt khi có lệnh gán fullName.value = '...'
  set(newValue) {
    const names = newValue.split(' ');
    lastName.value = names[0] || '';
    firstName.value = names.slice(1).join(' ') || '';
  }
});

function changeName() {
  fullName.value = 'Trần Thị Mai'; // Kích hoạt hàm setter!
}
</script>

<template>
  <div>
    <input v-model=\"fullName\" />
    <button @click=\"changeName\">Đổi tên thành Mai</button>
  </div>
</template>""",
        "tips": "Sử dụng Writable Computed là kỹ thuật chuẩn mực nhất khi viết custom input component bọc lại một prop nhận từ cha."
    },

    61: {
        "title_vi": "Cách Vue.js xử lý hiệu ứng chuyển động (Transitions) với component `<Transition>`?",
        "level": "Mid",
        "short_answer": "Vue cung cấp component tích hợp sẵn `<Transition>` để tự động áp dụng các hiệu ứng chuyển động (vào/ra) cho bất kỳ phần tử hoặc component nào được kích hoạt bởi `v-if`, `v-show` hoặc component động. Khi trạng thái thay đổi, Vue tự động thêm và gỡ bỏ 6 class CSS tương ứng theo từng giai đoạn.",
        "deep_dive": """Sáu class CSS chuyển động:
1. Giai đoạn Vào (Enter):
   - `v-enter-from`: Trạng thái ban đầu trước khi xuất hiện.
   - `v-enter-active`: Trạng thái đang chuyển động vào (khai báo transition / animation duration).
   - `v-enter-to`: Trạng thái kết thúc khi đã hiển thị hoàn chỉnh.
2. Giai đoạn Rời đi (Leave):
   - `v-leave-from`: Trạng thái ban đầu trước khi biến mất.
   - `v-leave-active`: Trạng thái đang chuyển động ra ngoài.
   - `v-leave-to`: Trạng thái kết thúc khi phần tử bị xóa.
* Đặt tên tùy biến: `<Transition name=\"fade\">` sẽ đổi tiền tố `v-` thành `fade-enter-active`.""",
        "code_example": """<script setup>
import { ref } from 'vue';
const show = ref(true);
</script>

<template>
  <div>
    <button @click=\"show = !show\">Toggle Fade</button>

    <Transition name=\"fade\">
      <p v-if=\"show\" class=\"box\">Khối nội dung chuyển động mượt mà</p>
    </Transition>
  </div>
</template>

<style scoped>
/* Hiệu ứng Fade đẹp mắt */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>""",
        "tips": "Nhớ: `<Transition>` chỉ áp dụng cho DUY NHẤT MỘT phần tử hoặc component con bên trong nó. Nếu muốn áp dụng hiệu ứng cho một danh sách nhiều phần tử, phải dùng `<TransitionGroup>`."
    },

    62: {
        "title_vi": "Cách áp dụng hiệu ứng cho một danh sách phần tử bằng `<TransitionGroup>`?",
        "level": "Mid",
        "short_answer": "Khi áp dụng hiệu ứng cho danh sách tạo bởi `v-for` (thêm mới, xóa bỏ, hoặc sắp xếp lại thứ tự), ta sử dụng `<TransitionGroup>`. Điểm đặc biệt của `<TransitionGroup>` là nó hỗ trợ thêm class `v-move` sử dụng kỹ thuật FLIP để tạo hoạt ảnh di chuyển mượt mà giữa các vị trí trong danh sách.",
        "deep_dive": """1. Bắt buộc thuộc tính `:key`: Mọi phần tử con bên trong `<TransitionGroup>` BẮT BUỘC phải có một `:key` duy nhất (không dùng index).
2. Class `v-move`: Tự động áp dụng CSS transform khi một phần tử thay đổi vị trí do danh sách bị đảo thứ tự hoặc xóa bớt phần tử khác.
3. Thuộc tính `tag`: Có thể quy định phần tử bọc ngoài (mặc định trong Vue 3 không render thẻ bọc).""",
        "code_example": """<script setup>
import { ref } from 'vue';
const items = ref([1, 2, 3, 4, 5]);

function addItem() {
  items.value.splice(2, 0, Date.now() % 100);
}
function remove(index) {
  items.value.splice(index, 1);
}
</script>

<template>
  <div>
    <button @click=\"addItem\">Chèn phần tử ngẫu nhiên</button>

    <TransitionGroup name=\"list\" tag=\"ul\">
      <li v-for=\"(item, index) in items\" :key=\"item\" @click=\"remove(index)\">
        Phần tử: {{ item }} (Bấm để xóa)
      </li>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
/* Hiệu ứng mượt mà khi các phần tử khác dồn chỗ */
.list-move {
  transition: transform 0.5s ease;
}
</style>""",
        "tips": "Kỹ thuật FLIP trong class `.v-move` của Vue giúp các item xung quanh tự động trượt vào vị trí trống của item vừa bị xóa cực kỳ mượt mà mà không tốn công lập trình thủ công."
    },

    63: {
        "title_vi": "So sánh CSS Transitions và CSS Animations trong Vue?",
        "level": "Junior",
        "short_answer": "CSS Transitions chuyển đổi mượt mà giữa 2 trạng thái định sẵn (từ A đến B) dựa trên thời gian và easing function (thường dùng cho hiệu ứng đơn giản như fade, slide). CSS Animations (sử dụng `@keyframes`) cho phép định nghĩa các chuỗi chuyển động phức tạp qua nhiều mốc phần trăm khác nhau (`0%`, `50%`, `100%`) và có thể lặp lại liên tục.",
        "deep_dive": """1. Thuộc tính `type` trong `<Transition>`: Khi một component kết hợp cả CSS transition và animation, Vue cần biết hiệu ứng nào kết thúc sau cùng để tháo bỏ DOM chính xác. Bạn chỉ định `<Transition type=\"animation\">` để Vue lắng nghe sự kiện `animationend` thay vì `transitionend`.""",
        "code_example": """<Transition name=\"bounce\">
  <div v-if=\"show\">Hiệu ứng nảy sinh động</div>
</Transition>

<style scoped>
.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
</style>""",
        "tips": "Dùng CSS Transitions cho các tương tác người dùng vi mô (micro-interactions), dùng `@keyframes` Animation cho các hiệu ứng phức tạp như nảy (bounce), rung lắc (shake)."
    },

    64: {
        "title_vi": "Cách tạo hiệu ứng chuyển động hoàn toàn bằng JavaScript trong Vue?",
        "level": "Mid",
        "short_answer": "Bên cạnh việc dùng CSS, component `<Transition>` của Vue cung cấp đầy đủ các sự kiện JavaScript hooks: `@before-enter`, `@enter`, `@after-enter`, `@before-leave`, `@leave`, `@after-leave`. Bạn có thể gắn các thư viện diễn hoạt JavaScript chuyên nghiệp như GSAP (GreenSock) để tạo các hiệu ứng 3D hoặc vật lý siêu phức tạp.",
        "deep_dive": """1. Bắt buộc gọi `done()`: Trong các hook bất đồng bộ `@enter` và `@leave`, bạn BẮT BUỘC phải gọi hàm callback `done()` khi hiệu ứng hoàn thành, để Vue biết khi nào có thể xóa phần tử khỏi DOM.
2. Tắt kiểm tra CSS: Thêm thuộc tính `:css=\"false\"` vào thẻ `<Transition>` để báo cho Vue bỏ qua việc quét class CSS, giúp tăng nhẹ hiệu năng.""",
        "code_example": """<script setup>
import gsap from 'gsap';

function onEnter(el, done) {
  gsap.fromTo(el, 
    { opacity: 0, scale: 0.8 },
    { opacity: 1, scale: 1, duration: 0.6, onComplete: done }
  );
}

function onLeave(el, done) {
  gsap.to(el, { opacity: 0, y: 50, duration: 0.4, onComplete: done });
}
</script>

<template>
  <Transition :css=\"false\" @enter=\"onEnter\" @leave=\"onLeave\">
    <div v-if=\"show\" class=\"box\">Hoạt cảnh điều khiển bằng GSAP!</div>
  </Transition>
</template>""",
        "tips": "Luôn nhớ thuộc tính `:css=\"false\"` khi sử dụng thuần JavaScript Transition để tránh xung đột với các class CSS vô tình."
    },

    65: {
        "title_vi": "Liệt kê chi tiết toàn bộ các JavaScript Hooks có sẵn trong `<Transition>`?",
        "level": "Senior",
        "short_answer": "Các JavaScript transition hooks gồm 2 nhóm: (1) Nhóm Xuất hiện (Enter): `@before-enter(el)`, `@enter(el, done)`, `@after-enter(el)`, `@enter-cancelled(el)`, và (2) Nhóm Biến mất (Leave): `@before-leave(el)`, `@leave(el, done)`, `@after-leave(el)`, `@leave-cancelled(el)`.",
        "deep_dive": """1. `@enter-cancelled` / `@leave-cancelled`: Kích hoạt khi người dùng thay đổi trạng thái liên tục giữa chừng (ví dụ: đang fade in nửa chừng thì người dùng bấm nút ẩn đi ngay lập tức). Giúp bạn reset lại các thuộc tính CSS inline đang dở dang.""",
        "code_example": """<Transition
  @before-enter=\"(el) => console.log('Chuẩn bị vào')\"
  @enter=\"(el, done) => { /* Xử lý JS */ done(); }\"
  @after-enter=\"(el) => console.log('Đã vào hoàn tất')\"
  @before-leave=\"(el) => console.log('Chuẩn bị rời đi')\"
  @leave=\"(el, done) => { /* Xử lý JS */ done(); }\"
  @after-leave=\"(el) => console.log('Đã rời đi hoàn tất')\"
>
  <div v-if=\"visible\">Nội dung</div>
</Transition>""",
        "tips": "Nắm vững toàn bộ 8 hooks này chứng minh bạn đã làm chủ hoàn toàn hệ thống diễn hoạt hoạt cảnh của Vue."
    },

    66: {
        "title_vi": "Các thực hành tốt nhất về tổ chức cấu trúc mã nguồn trong ứng dụng Vue lớn?",
        "level": "Senior",
        "short_answer": "Để duy trì ứng dụng Vue doanh nghiệp: (1) Tổ chức mã theo Tính năng/Mô-đun (Feature-based Architecture) thay vì gom tất cả components vào 1 folder chung, (2) Tách nhỏ các Single File Components không vượt quá 200-300 dòng code, (3) Tách toàn bộ business logic ra các Custom Composables (`src/composables/`), (4) Sử dụng TypeScript để quản lý Types an toàn, (5) Quản lý trạng thái bằng Pinia chia theo từng store nhỏ độc lập, và (6) Tự động hóa format bằng ESLint + Prettier.",
        "deep_dive": """1. Feature-based Structure:
   `src/features/auth/` (chứa components, composables, api, routes của riêng Auth).
   `src/features/orders/` (chứa các thành phần của riêng Orders).
2. Clean Code Component: Component chỉ nên đóng vai trò hiển thị (Presentation Layer). Logic tính toán phức tạp phải nằm trong Composable.""",
        "code_example": """// Cấu trúc dự án chuẩn Senior:
// src/
// ├── assets/          # Hình ảnh, font chữ, styles toàn cục
// ├── components/      # UI components dùng chung toàn app (Button, Modal, Input)
// ├── composables/     # Logic tái sử dụng (useAuth, useFetch, useDebounce)
// ├── router/          # Cấu hình Vue Router và Navigation Guards
// ├── stores/          # Pinia stores (userStore, cartStore)
// ├── views/           # Các trang ứng với từng URL (HomeView, CartView)
// ├── api/             # Tầng gọi HTTP axios client
// ├── types/           # Định nghĩa TypeScript interfaces/types
// └── App.vue""",
        "tips": "Quy tắc nằm lòng: 'Component lo việc hiển thị UI, Composable lo việc xử lý Business Logic'."
    },

    67: {
        "title_vi": "Tại sao thuộc tính `:key` lại có vai trò sinh tử trong danh sách `v-for`?",
        "level": "Mid",
        "short_answer": "Thuộc tính `:key` cung cấp một định danh duy nhất (Unique Identity) cho mỗi nút Virtual DOM trong danh sách. Nhờ `:key`, thuật toán Diffing của Vue có thể nhận diện chính xác phần tử nào vừa được thêm, sửa, xóa, hoặc đổi chỗ để tái sử dụng đúng DOM node đó. Nếu không có key (hoặc dùng index làm key), Vue sẽ áp dụng chiến lược 'In-place Patch' (vá tại chỗ) gây ra các lỗi hiển thị nghiêm trọng khi danh sách bị xáo trộn hoặc xóa phần tử.",
        "deep_dive": """1. Tác hại của việc dùng `index` làm key (`:key=\"index\"`):
   - Khi bạn xóa phần tử đầu tiên trong mảng, phần tử thứ 2 lập tức bị gán lại `index = 0`. Vue tưởng phần tử thứ 2 chính là phần tử thứ 1 cũ và giữ lại trạng thái form nội bộ (như text trong thẻ `<input>` hoặc checkbox đang tick), dẫn đến việc dữ liệu bị lệch lạc hoàn toàn!
2. Hiệu năng: Key giúp giảm thiểu số lượng thao tác cập nhật DOM thật xuống mức tối thiểu tuyệt đối.""",
        "code_example": """<template>
  <ul>
    <!-- ❌ TỒI: Dùng index làm key khi danh sách có thể thêm/xóa/đảo vị trí -->
    <!-- <li v-for=\"(item, index) in items\" :key=\"index\"> -->

    <!-- ✅ XUẤT SẮC: Luôn dùng ID duy nhất của dữ liệu làm key -->
    <li v-for=\"item in items\" :key=\"item.id\">
      <input type=\"checkbox\" /> {{ item.title }}
    </li>
  </ul>
</template>""",
        "tips": "Tuyệt đối không bao giờ dùng `index` làm `:key` nếu danh sách có tính năng xóa, lọc hoặc sắp xếp."
    },

    68: {
        "title_vi": "Cách cấu trúc các Components để đạt khả năng mở rộng và bảo trì tối đa?",
        "level": "Senior",
        "short_answer": "Cấu trúc theo mô hình phân tầng kim tự tháp: (1) Base / Primitive Components (các khối nguyên tử ở đáy: Button, Input, Icon - không phụ thuộc bất kỳ business logic nào), (2) Pattern / Composite Components (ghép các base components lại: SearchBar, FormField), (3) Domain / Feature Components (gắn liền với nghiệp vụ: ProductCard, UserDropdown), và (4) Page / View Components (ở đỉnh: đóng gói toàn bộ trang và kết nối Router/Pinia).",
        "deep_dive": """1. Đặt tên file component:
   - Các component cơ sở dùng chung: Bắt đầu bằng tiền tố `Base` (`BaseButton.vue`, `BaseInput.vue`).
   - Các component đơn lẻ chỉ dùng 1 lần: Bắt đầu bằng `The` (`TheHeader.vue`, `TheSidebar.vue`).
   - Các component phụ thuộc: Bắt đầu bằng tên component cha (`TodoList.vue`, `TodoListItem.vue`).""",
        "code_example": """// Áp dụng Design System Atomic Design trong Vue:
// Atoms -> Molecules -> Organisms -> Templates -> Pages""",
        "tips": "Đọc qua Style Guide chính thức của Vue (Priority A, B, C rules) để trả lời trôi chảy các quy chuẩn đặt tên component."
    },

    69: {
        "title_vi": "Tại sao cần tránh việc sử dụng từ khóa `this` bên trong template expressions của Vue?",
        "level": "Junior",
        "short_answer": "Trong template của Vue, ngữ cảnh thực thi đã được tự động liên kết với component instance. Bạn có thể truy cập trực tiếp tên biến và hàm (như `{{ count }}`, `@click=\"increment\"`) mà không cần `this`. Việc viết `this.count` trong template là dư thừa, làm giảm tính thẩm mỹ của code và có thể gây xung đột ngữ cảnh trong quá trình biên dịch tối ưu hóa của Vue 3 Compiler.",
        "deep_dive": """1. Đặc biệt trong Vue 3 `<script setup>`: Từ khóa `this` hoàn toàn không tồn tại trong `<script setup>`. Vì vậy việc dùng `this` trong template sẽ tạo ra sự bất nhất và khó hiểu đối với người đọc code.""",
        "code_example": """<template>
  <!-- ❌ Dư thừa, không chuẩn Vue: -->
  <p>{{ this.userName }}</p>

  <!-- ✅ Chuẩn mực và sạch sẽ: -->
  <p>{{ userName }}</p>
</template>""",
        "tips": "Hãy nhớ: Template của Vue luôn tự động truy cập vào scope của instance; không bao giờ cần gõ `this` trong template."
    },

    70: {
        "title_vi": "Cách giữ cho các phương thức và logic trong Vue component luôn ngắn gọn, dễ đọc?",
        "level": "Junior",
        "short_answer": "Để code luôn trong sáng: (1) Tuân thủ quy tắc mỗi hàm không quá 20 dòng và chỉ làm duy nhất một việc (Single Responsibility), (2) Đẩy các tác vụ tính toán phái sinh sang `computed`, (3) Đẩy các hàm tiện ích thuần túy (format tiền tệ, xử lý ngày tháng) ra file `utils/`, và (4) Đóng gói các cụm logic trạng thái phức tạp thành các Custom Composables.",
        "deep_dive": """1. Composable refactoring: Khi một component vượt quá 200 dòng, hãy nhóm các biến và hàm liên quan thành một hàm `useFeature()` riêng biệt. Component chỉ việc gọi composable đó ra dùng.""",
        "code_example": """// Tách logic giỏ hàng ra file riêng: composables/useCart.js
export function useCart() {
  const items = ref([]);
  const total = computed(() => items.value.reduce((s, i) => s + i.price, 0));
  const addItem = (product) => items.value.push(product);

  return { items, total, addItem };
}

// Trong component: Ngắn gọn chỉ 3 dòng!
const { items, total, addItem } = useCart();""",
        "tips": "Nguyên tắc vàng: 'Một component sạch là một component mà người khác chỉ cần đọc 30 giây là hiểu hết nó làm nhiệm vụ gì'."
    },

    71: {
        "title_vi": "Cách viết Unit Test cho một Vue Component sử dụng Vitest và Vue Test Utils?",
        "level": "Mid",
        "short_answer": "Sử dụng thư viện chính thức `@vue/test-utils` kết hợp với test runner `vitest`. Dùng hàm `mount(Component, { props })` để tạo một bản bao bọc (wrapper) của component trong môi trường DOM ảo (jsdom), sau đó kiểm tra các assertions: nội dung văn bản hiển thị đúng (`wrapper.text()`), class CSS tồn tại, sự kiện kích hoạt chính xác (`wrapper.trigger('click')`), và kiểm tra emit sự kiện (`wrapper.emitted()`).",
        "deep_dive": """1. `shallowMount` vs `mount`:
   - `mount`: Render toàn bộ component cùng tất cả các components con của nó.
   - `shallowMount`: Chỉ render component hiện tại, thay thế các components con bằng thẻ giả lập (stubs), giúp bài test chạy nhanh và cô lập hoàn toàn component cần kiểm thử.
2. Kiểm tra bất đồng bộ: Luôn gọi `await wrapper.vm.$nextTick()` sau khi kích hoạt sự kiện để chờ Vue cập nhật DOM trước khi assert!""",
        "code_example": """// tests/Counter.spec.js
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Counter from '@/components/Counter.vue';

describe('Component Counter', () => {
  it('phải hiển thị giá trị khởi tạo và tăng lên khi bấm nút', async () => {
    // 1. Mount component với prop khởi tạo
    const wrapper = mount(Counter, {
      props: { initialValue: 5 }
    });

    // 2. Kiểm tra text ban đầu
    expect(wrapper.text()).toContain('Giá trị: 5');

    // 3. Giả lập người dùng bấm nút tăng
    await wrapper.find('button.btn-increase').trigger('click');

    // 4. Kiểm tra DOM đã cập nhật chính xác
    expect(wrapper.text()).toContain('Giá trị: 6');
  });
});""",
        "tips": "Senior Tip: Luôn nhắc đến `await wrapper.vm.$nextTick()` khi test các tương tác click làm thay đổi giao diện."
    },

    72: {
        "title_vi": "Các framework kiểm thử phổ biến nhất hiện nay cho Vue.js?",
        "level": "Junior",
        "short_answer": "Hệ sinh thái kiểm thử Vue hiện đại gồm: (1) `Vitest` (Test runner thế hệ mới xây dựng trên Vite, nhanh gấp nhiều lần Jest và tương thích 100% với cấu hình vite.config), (2) `@vue/test-utils` (Thư viện tiện ích chính thức để mount và tương tác component), (3) `Playwright` hoặc `Cypress` (Kiểm thử đầu-cuối E2E trên trình duyệt thật), và (4) `Jest` (Framework truyền thống cũ).",
        "deep_dive": """1. Tại sao Vitest chiến thắng Jest trong thế giới Vue: Vitest dùng chung toàn bộ pipeline cấu hình của Vite (plugins, alias `@`, CSS preprocessors). Bạn không cần phải cấu hình lại `babel-jest` hay `ts-jest` phức tạp như trước đây.""",
        "code_example": """# Khởi chạy kiểm thử Vitest ở chế độ theo dõi file (Watch Mode):
npm run test:unit
# Hoặc mở giao diện trực quan tuyệt đẹp của Vitest UI:
npx vitest --ui""",
        "tips": "Nếu bắt đầu dự án mới, hãy luôn chọn bộ ba: `Vitest` + `Vue Test Utils` + `Playwright`."
    },

    73: {
        "title_vi": "Các phương pháp Debug hiệu quả nhất cho ứng dụng Vue.js?",
        "level": "Junior",
        "short_answer": "Các kỹ thuật gỡ lỗi bao gồm: (1) Sử dụng tiện ích Vue DevTools kiểm tra Props, State và Events theo thời gian thực, (2) Đặt từ khóa `debugger` trong code để kích hoạt Breakpoints trên Chrome DevTools, (3) Sử dụng hook `onRenderTracked` và `onRenderTriggered` của Vue 3 để phát hiện biến nào vừa kích hoạt re-render, và (4) Bắt lỗi bằng `onErrorCaptured` hook.",
        "deep_dive": """1. Sức mạnh của `onRenderTriggered`: Cực kỳ đắt giá khi tối ưu hiệu năng! Hook này in ra chính xác thuộc tính nào, giá trị cũ là gì, giá trị mới là gì khiến component bị vẽ lại.""",
        "code_example": """<script setup>
import { ref, onRenderTriggered } from 'vue';

const count = ref(0);

// Công cụ Debugging đỉnh cao của Vue 3:
onRenderTriggered((event) => {
  console.log('Component bị re-render bởi:', event.key, 'từ', event.oldValue, 'thành', event.newValue);
});
</script>""",
        "tips": "Hook `onRenderTriggered` là bảo bối của Senior Developer khi cần điều tra vì sao một trang web bị lag do render thừa."
    },

    74: {
        "title_vi": "Những lưu ý đặc thù của Vue khi viết kiểm thử (Vue-specific Testing Considerations)?",
        "level": "Mid",
        "short_answer": "Khi kiểm thử Vue cần lưu ý: (1) Tính bất đồng bộ của DOM updates: Vue không cập nhật DOM ngay lập tức mà gom vào hàng đợi microtask, do đó BẮT BUỘC phải dùng `await nextTick()` sau mỗi thay đổi state, (2) Mocking các Global Plugins (Vue Router, Pinia) thông qua `global.plugins` trong options của `mount()`, và (3) Sử dụng `data-testid` để chọn phần tử an toàn thay vì dựa vào class CSS dễ thay đổi.",
        "deep_dive": """1. Bẫy CSS class: Nếu viết `wrapper.find('.btn-submit')`, khi designer đổi class sang `.btn-primary` thì bài test bị gãy dù tính năng vẫn chạy tốt. Hãy dùng `wrapper.find('[data-testid=\"submit-btn\"]')`.""",
        "code_example": """import { mount } from '@vue/test-utils';
import { createTestingPinia } from '@pinia/testing';

const wrapper = mount(MyComponent, {
  global: {
    plugins: [createTestingPinia({ stubActions: false })], // Mock Pinia store an toàn
    mocks: {
      $t: (msg) => msg // Mock thư viện đa ngôn ngữ i18n
    }
  }
});""",
        "tips": "Sử dụng `@pinia/testing` giúp bạn mock toàn bộ Pinia store trong các bài test chỉ với một dòng code."
    },

    75: {
        "title_vi": "Cách viết Unit Test cho Pinia Actions?",
        "level": "Mid",
        "short_answer": "Vì Pinia Store là các hàm JavaScript độc lập, việc kiểm thử Actions trong Pinia cực kỳ đơn giản: Khởi tạo một phiên bản Pinia cô lập bằng `setActivePinia(createPinia())`, gọi hàm Action, và kiểm tra trạng thái của State sau khi Action hoàn thành hoặc kiểm tra các lời gọi API giả lập (Mock API).",
        "deep_dive": """1. Độc lập hoàn toàn với Component: Bạn có thể test 100% logic của Store mà không cần phải mount bất kỳ component Vue nào vào DOM!""",
        "code_example": """import { setActivePinia, createPinia } from 'pinia';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAuthStore } from '@/stores/auth';

describe('Auth Store Actions', () => {
  beforeEach(() => {
    // Tạo môi trường Pinia mới tinh cho từng bài test
    setActivePinia(createPinia());
  });

  it('Action login phải cập nhật user và trạng thái isAuthenticated', async () => {
    const authStore = useAuthStore();
    expect(authStore.isAuthenticated).toBe(false);

    // Giả lập gọi action đăng nhập
    await authStore.login({ username: 'dan', token: 'XYZ123' });

    expect(authStore.user.username).toBe('dan');
    expect(authStore.isAuthenticated).toBe(true);
  });
});""",
        "tips": "Điểm mạnh tuyệt đối của Pinia so với Vuex cũ: Viết unit test cho Pinia nhẹ nhàng và trực quan như test một hàm JavaScript thông thường."
    },

    76: {
        "title_vi": "Cách xây dựng một Vue.js Plugin có thể chia sẻ cho cộng đồng?",
        "level": "Senior",
        "short_answer": "Một Vue Plugin là một Object có chứa phương thức `install(app, options)` hoặc đơn giản là một hàm nhận `(app, options)`. Plugin có thể: Đăng ký các Global Components, Directives toàn cục, cung cấp dữ liệu qua `app.provide()`, hoặc gắn các thuộc tính tiện ích vào `app.config.globalProperties`.",
        "deep_dive": """1. Sử dụng trong ứng dụng: Người dùng cài đặt plugin thông qua lệnh `app.use(myPlugin, options)`.
2. Clean Architecture: Khuyên dùng `app.provide()` bên trong plugin kết hợp với một Composable chuyên dụng để component con lấy ra dùng, tránh lạm dụng `globalProperties`.""",
        "code_example": """// plugins/i18n.js
export default {
  install: (app, options) => {
    // Cung cấp hàm dịch ngôn ngữ toàn cục
    const translate = (key) => {
      return key.split('.').reduce((o, i) => (o ? o[i] : key), options.translations);
    };

    // Cung cấp cho toàn bộ app qua provide
    app.provide('i18n', translate);
    
    // Hoặc gắn vào global properties
    app.config.globalProperties.$translate = translate;
  }
};

// Sử dụng trong main.js:
// app.use(i18nPlugin, { translations: { greeting: { hello: 'Xin chào' } } });""",
        "tips": "Mọi thư viện nổi tiếng như Vue Router, Pinia, Vuetify thực chất đều tuân theo đúng khuôn mẫu hàm `install(app)` này."
    },

    77: {
        "title_vi": "Khái niệm Filters trong Vue và giải pháp thay thế chính thức trong Vue 3?",
        "level": "Junior",
        "short_answer": "Filters (cú pháp ống dẫn `{{ message | capitalize }}`) là tính năng trong Vue 2 dùng để định dạng văn bản trong template. Trong Vue 3, Filters ĐÃ BỊ LOẠI BỎ HOÀN TOÀN vì chúng có cú pháp mâu thuẫn với toán tử bitwise của JavaScript, làm tăng độ phức tạp cho trình biên dịch. Giải pháp thay thế chính thức là sử dụng `Computed Properties` hoặc gọi trực tiếp các `Methods` / hàm tiện ích.",
        "deep_dive": """1. Tại sao loại bỏ: `{{ text | filterA | filterB }}` trông giống cú pháp bash script hơn là JavaScript, và việc gọi hàm `{{ formatCurrency(price) }}` trực quan, chuẩn ES và dễ dàng kiểm soát tham số hơn rất nhiều.""",
        "code_example": """<!-- Thay vì dùng Filter Vue 2 cũ: {{ price | toVND }} -->
<!-- Trong Vue 3: Dùng hàm tiện ích JavaScript chuẩn -->
<script setup>
function toVND(amount) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
}
</script>

<template>
  <p>Giá sản phẩm: {{ toVND(150000) }}</p>
</template>""",
        "tips": "Nếu nhà tuyển dụng hỏi về Filters, hãy nói ngay: 'Filters đã deprecated và bị xóa trong Vue 3. Chúng tôi dùng computed hoặc utility functions thay thế'."
    },

    78: {
        "title_vi": "Cách tích hợp một thư viện bên thứ ba không viết riêng cho Vue (như Chart.js, Leaflet, D3)?",
        "level": "Mid",
        "short_answer": "Để tích hợp an toàn một thư viện DOM bên thứ 3: (1) Sử dụng Template Ref (`ref=\"chartCanvas\"`) để lấy tham chiếu DOM thật, (2) Khởi tạo thư viện bên trong lifecycle hook `onMounted()` khi DOM đã sẵn sàng, (3) Dùng `markRaw()` hoặc `shallowRef()` để lưu instance của thư viện, và (4) BẮT BUỘC gọi hàm `destroy()` của thư viện trong `onBeforeUnmount()` để dọn dẹp bộ nhớ.",
        "deep_dive": """1. Bẫy Memory Leak: Nếu bạn không gọi `chartInstance.destroy()` khi component unmount, canvas context và các event listeners của thư viện ngoài sẽ tồn tại vĩnh viễn trong RAM!""",
        "code_example": """<script setup>
import { ref, onMounted, onBeforeUnmount, markRaw } from 'vue';
import Chart from 'chart.js/auto';

const canvasRef = ref(null);
let chartInstance = null;

onMounted(() => {
  // Khởi tạo Chart khi DOM đã xuất hiện
  chartInstance = markRaw(new Chart(canvasRef.value, {
    type: 'bar',
    data: { labels: ['Q1', 'Q2'], datasets: [{ data: [10, 20] }] }
  }));
});

// BẮT BUỘC dọn dẹp chống rò rỉ bộ nhớ
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<template>
  <div>
    <canvas ref=\"canvasRef\"></canvas>
  </div>
</template>""",
        "tips": "Luôn nhớ: Thao tác với thư viện DOM bên ngoài chỉ được phép làm trong `onMounted()` và bắt buộc hủy trong `onBeforeUnmount()`."
    },

    79: {
        "title_vi": "Cách tạo và sử dụng Global Mixin trong Vue 2 và tại sao nó cực kỳ nguy hiểm?",
        "level": "Senior",
        "short_answer": "Trong Vue 2, Global Mixin được đăng ký bằng `Vue.mixin({ ... })`. Nó áp dụng các options cho TẤT CẢ mọi component instance trong toàn bộ ứng dụng (kể cả component của thư viện bên thứ 3). Nó CỰC KỲ NGUY HIỂM vì làm ô nhiễm phạm vi toàn cục, dễ gây lỗi ghi đè thuộc tính ngầm, làm suy giảm hiệu năng nghiêm trọng và khiến việc truy vết nguồn gốc lỗi trở thành cơn ác mộng.",
        "deep_dive": """1. Lời khuyên chính thức: Tài liệu của Vue khuyến cáo người dùng 'Cực kỳ hạn chế hoặc tuyệt đối không dùng Global Mixins'.
2. Thay thế trong Vue 3: Dùng `app.provide()` hoặc các Composables riêng biệt.""",
        "code_example": """// ❌ NGUY HIỂM: Global Mixin trong Vue 2 ảnh hưởng đến hàng nghìn components!
// Vue.mixin({
//   created() {
//     console.log('Chạy trên MỌI component trong app!');
//   }
// });""",
        "tips": "Nếu được hỏi về Global Mixin, câu trả lời chuẩn là: 'Tôi không bao giờ khuyên dùng Global Mixin trong production'."
    },

    80: {
        "title_vi": "Những lưu ý an toàn nếu bắt buộc phải bảo trì hệ thống dùng Mixins?",
        "level": "Mid",
        "short_answer": "Nếu phải bảo trì mã nguồn cũ dùng mixins: (1) Luôn đặt tiền tố (prefix) cho các thuộc tính và methods của mixin (ví dụ `userMixin_isLoading`) để tránh xung đột tên, (2) Viết tài liệu rõ ràng các dependencies mà mixin kỳ vọng component phải cung cấp, và (3) Lên kế hoạch tái cấu trúc (refactor) từng bước chuyển đổi các mixins sang Vue 3 Composables.",
        "deep_dive": """1. Chiến lược Refactoring: Tách logic trong mixin thành hàm `useXxx()` composable độc lập, sau đó trong component cũ chỉ việc gọi composable này.""",
        "code_example": """// Đặt tiền tố rõ ràng nếu buộc phải dùng mixin cũ:
export const cartMixin = {
  data() {
    return {
      cart_items: [],
      cart_totalPrice: 0
    };
  },
  methods: {
    cart_calculateTotal() { ... }
  }
};""",
        "tips": "Việc đề xuất prefix tên biến trong Mixin chứng tỏ bạn đã từng trải qua nỗi đau đụng độ tên biến trong các dự án lớn thực tế."
    },

    81: {
        "title_vi": "Cách quản lý các cuộc gọi API hiệu quả và chuyên nghiệp trong Vue 3?",
        "level": "Senior",
        "short_answer": "Quản lý API chuyên nghiệp đòi hỏi: (1) Xây dựng một HTTP Client tập trung (sử dụng Axios với Interceptors hoặc Fetch wrapper) quản lý Base URL, tự động đính kèm Bearer Token và refresh token tự động, (2) Đóng gói các endpoints thành các API Services độc lập theo nghiệp vụ, (3) Sử dụng Custom Composables (`useFetch` hoặc thư viện TanStack Vue Query) để quản lý tự động trạng thái `data`, `isLoading`, `error` và Caching.",
        "deep_dive": """1. Lợi ích của TanStack Query for Vue: Tự động cache kết quả API, tự động làm mới khi người dùng focus lại màn hình (Window Focus Refetching), tự động retry khi mất mạng, và hủy request cũ khi đổi trang.""",
        "code_example": """// api/axiosClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000
});

// Tự động gắn Token vào mọi request
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default apiClient;""",
        "tips": "Senior Tip: Đề xuất sử dụng TanStack Vue Query (`@tanstack/vue-query`) để biến việc quản lý server state trở nên đơn giản và chuyên nghiệp như các công ty công nghệ lớn."
    },

    82: {
        "title_vi": "Chiến lược Server-Side Rendering (SSR) trong Vue và sự kết hợp với Nuxt.js?",
        "level": "Senior",
        "short_answer": "SSR trong Vue biên dịch các component thành chuỗi HTML trực tiếp trên máy chủ Node.js rồi gửi về cho trình duyệt, giúp tăng tốc First Contentful Paint và tối ưu hóa SEO. Thay vì tự cấu hình phức tạp với `@vue/server-renderer`, cách chuẩn mực tuyệt đối trong ngành công nghiệp hiện nay là sử dụng Nuxt 3 (Full-stack framework dựa trên Vue 3).",
        "deep_dive": """1. Hydration (Thủy hóa): Quá trình JavaScript ở client nạp vào để gắn các event listeners vào cây HTML tĩnh tải về từ server.
2. Hydration Mismatch: Lỗi kinh điển khi HTML render trên server khác với kết quả render trên client (ví dụ dùng `new Date()` hoặc đọc `localStorage` trong lúc render).""",
        "code_example": """// Trong Nuxt 3: SSR được kích hoạt mặc định tự động!
// Chỉ cần tạo file pages/products/[id].vue:
// Nuxt tự động fetch data trên server và render sẵn HTML cho Googlebot!""",
        "tips": "Bất cứ khi nào nhắc đến Vue SSR, hãy lập tức nhắc đến Nuxt 3."
    },

    83: {
        "title_vi": "Nuxt.js là gì và mối quan hệ của nó với Vue.js?",
        "level": "Junior",
        "short_answer": "Nuxt.js là một Meta-Framework cấp cao được xây dựng trên nền tảng của Vue.js (tương tự Next.js đối với React). Nó cung cấp giải pháp toàn diện cho các ứng dụng Vue cấp doanh nghiệp: Tự động hóa định tuyến dựa trên cấu trúc thư mục (File-based Routing), hỗ trợ đa dạng chế độ render (SSR, SSG, SPA), tự động import components và composables, và tích hợp sẵn công cụ máy chủ Nitro backend engine.",
        "deep_dive": """1. Khác biệt cốt lõi: Với Vue thuần, bạn phải tự cài và cấu hình Router, Pinia, Vite, SEO meta tags. Nuxt đóng gói sẵn tất cả theo chuẩn quy ước tối ưu nhất (Convention over Configuration).
2. Universal Rendering: Tải trang đầu tiên bằng SSR nhanh như chớp, các lần bấm link tiếp theo hoạt động như SPA mượt mà không reload.""",
        "code_example": """# Khởi tạo dự án Nuxt 3 nhanh chóng:
npx nuxi@latest init my-nuxt-app""",
        "tips": "Nếu dự án yêu cầu SEO hàng đầu (Thương mại điện tử, Tin tức, Blog), Nuxt là lựa chọn số 1 bắt buộc."
    },

    84: {
        "title_vi": "Quá trình Tạo trang tĩnh (Static Site Generation - SSG) trong Vue?",
        "level": "Mid",
        "short_answer": "Static Site Generation (SSG - còn gọi là Pre-rendering) là quá trình render trước toàn bộ các trang của website thành các file HTML, CSS và JS tĩnh ngay trong thời gian build (`npm run generate`). Các file này có thể được tải lên hosting miễn phí hoặc CDN (như Cloudflare Pages, Vercel, Netlify) với tốc độ phản hồi tính bằng mili-giây và khả năng bảo mật tuyệt đối.",
        "deep_dive": """1. So sánh SSG vs SSR:
   - SSR: Render động trên server Node.js mỗi khi CÓ REQUEST gửi đến (tốn CPU server).
   - SSG: Render trước 1 LẦN DUY NHẤT LÚC BUILD. Khi người dùng truy cập, máy chủ chỉ việc ném file HTML tĩnh có sẵn ra (không tốn CPU, chịu tải hàng triệu người).""",
        "code_example": """# Lệnh build toàn bộ trang thành HTML tĩnh trong Nuxt:
npx nuxi generate""",
        "tips": "SSG là lựa chọn hoàn hảo cho website tài liệu, portfolio, hoặc trang tin tức nơi nội dung ít khi thay đổi theo từng giây."
    },

    85: {
        "title_vi": "Cách xử lý xác thực và phân quyền (Authentication & Authorization) trong Vue Router?",
        "level": "Senior",
        "short_answer": "Xác thực được quản lý thông qua Navigation Guards toàn cục (`router.beforeEach`). Ta khai báo các thuộc tính `meta` trên mỗi route (ví dụ `requiresAuth: true`, `role: 'admin'`). Trước khi chuyển trang, Guard sẽ kiểm tra token trong Pinia store/Cookie. Nếu chưa đăng nhập, tự động chuyển hướng về trang `/login` kèm tham số `redirect` để quay lại sau khi login thành công.",
        "deep_dive": """1. Xử lý Token hết hạn: Kết hợp Navigation Guard với Axios Response Interceptor (nếu nhận mã 401, tự động xóa token và đẩy user về trang login).
2. Tối ưu UX: Lưu lại trang đích `router.push({ path: '/login', query: { redirect: to.fullPath } })` để khi user gõ mật khẩu xong là nhảy ngay về đúng trang họ đang muốn vào.""",
        "code_example": """// router/index.js
import { router } from './router';
import { useAuthStore } from '@/stores/auth';

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Kiểm tra route có yêu cầu đăng nhập không
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Chuyển về login và lưu lại URL đang muốn vào
    return next({ path: '/login', query: { redirect: to.fullPath } });
  }

  // Kiểm tra quyền hạn vai trò (Role check)
  if (to.meta.role && authStore.userRole !== to.meta.role) {
    return next('/403-forbidden');
  }

  next(); // Cho phép đi tiếp
});""",
        "tips": "Navigation Guard `router.beforeEach` là chốt chặn an ninh quan trọng nhất phía frontend trong mọi ứng dụng Vue."
    },

    86: {
        "title_vi": "Single File Component (SFC - `.vue`) là gì và cách hoạt động của nó?",
        "level": "Junior",
        "short_answer": "Single File Component (SFC) là định dạng tệp có đuôi mở rộng `.vue` độc quyền của Vue. Nó đóng gói trọn vẹn cả 3 trụ cột của một thành phần giao diện vào trong cùng một file duy nhất: Logic (`<script>`), Giao diện cấu trúc (`<template>`), và Kiểu dáng thẩm mỹ (`<style>`). Trình biên dịch `@vue/compiler-sfc` của Vite sẽ phân tách và biên dịch file này thành JavaScript và CSS chuẩn.",
        "deep_dive": """1. Khắc phục vấn đề tách rời nhân tạo: Truyền thống tách rời file `HTML`, `CSS`, `JS` riêng biệt khiến bạn phải nhảy qua lại giữa 3 file mỗi khi sửa một nút bấm nhỏ. SFC đưa tất cả các phần tử liên quan mật thiết về cùng một nơi (Colocation).""",
        "code_example": """<!-- MyWidget.vue: Trọn gói trong 1 file duy nhất -->
<script setup>
import { ref } from 'vue';
const count = ref(0);
</script>

<template>
  <button class=\"btn\" @click=\"count++\">Count: {{ count }}</button>
</template>

<style scoped>
.btn { background: #42b883; color: white; padding: 8px 16px; }
</style>""",
        "tips": "Từ khóa định vị: 'Colocation of Concerns' (Gom các mối quan tâm liên quan lại một nơi thay vì chia cắt nhân tạo)."
    },

    87: {
        "title_vi": "Mô tả cấu trúc của một Single File Component chuẩn trong Vue 3?",
        "level": "Junior",
        "short_answer": "Một file SFC chuẩn gồm 3 khối gốc (Top-level Blocks): (1) `<script setup>` chứa logic JavaScript/TypeScript chạy trong thời gian biên dịch, (2) `<template>` chứa cấu trúc HTML mở rộng với các directives của Vue, và (3) `<style scoped>` chứa mã CSS được cô lập chỉ áp dụng riêng cho component hiện tại.",
        "deep_dive": """1. Tùy chọn ngôn ngữ (Pre-processors):
   - `<script setup lang=\"ts\">`: Kích hoạt TypeScript.
   - `<style scoped lang=\"scss\">`: Kích hoạt SCSS.
2. Thứ tự khuyến nghị chính thức: `<script setup>` đặt ở trên cùng, `<template>` ở giữa, và `<style>` ở dưới cùng.""",
        "code_example": """<script setup lang=\"ts\">
// 1. Script block: Types, imports, state và handlers
defineProps<{ title: string }>();
</script>

<template>
  <!-- 2. Template block: Chỉ được chứa 1 hoặc nhiều root nodes -->
  <h1>{{ title }}</h1>
</template>

<style scoped>
/* 3. Style block: CSS cô lập */
h1 { color: #2c3e50; }
</style>""",
        "tips": "Trong Vue 3, template hỗ trợ Fragment (chứa nhiều root elements ngang hàng), không còn bị bắt buộc phải bọc trong duy nhất 1 thẻ `<div>` như Vue 2."
    },

    88: {
        "title_vi": "Những lợi ích vượt trội của việc sử dụng Single File Components (SFC)?",
        "level": "Junior",
        "short_answer": "SFC mang lại các lợi thế: (1) Cú pháp nổi bật và IntelliSense xuất sắc trong IDE (VS Code với Volar / Vue - Official), (2) Hỗ trợ CSS Scoped tự động tránh xung đột style giữa các trang, (3) Biên dịch trước (Pre-compiled Templates) giúp loại bỏ chi phí biên dịch lúc runtime của trình duyệt, (4) Hỗ trợ Hot Module Replacement (HMR) giữ nguyên trạng thái khi sửa code, và (5) Tương thích hoàn hảo với các pre-processors (TypeScript, SCSS, PostCSS).",
        "deep_dive": """1. Compile-time Optimizations: Trình biên dịch có thể phân tích cú pháp tĩnh template của SFC để áp dụng Patch Flags và Hoisting, điều mà các hàm render động không làm được.""",
        "code_example": """// Trải nghiệm phát triển (DX) tuyệt vời với tiện ích mở rộng 'Vue - Official'""",
        "tips": "Nhớ cài extension chính thức 'Vue - Official' (tên cũ là Volar) trên VS Code để có trải nghiệm SFC hoàn hảo nhất."
    },

    89: {
        "title_vi": "Cách hoạt động của Scoped Styles (`<style scoped>`) trong SFC?",
        "level": "Mid",
        "short_answer": "Khi một thẻ `<style>` có thuộc tính `scoped`, PostCSS sẽ tự động can thiệp bằng cách sinh ra một thuộc tính dữ liệu độc nhất (dạng `data-v-xxxxxxx`) và gắn thuộc tính đó vào tất cả các phần tử HTML bên trong component, đồng thời viết lại selector CSS tương ứng (ví dụ `.btn[data-v-xxxxxxx]`). Nhờ đó, style của component này TUYỆT ĐỐI KHÔNG BỊ TRÀN (leak) sang component khác.",
        "deep_dive": """1. Deep Selectors (`:deep()`): Mặc định scoped style không tác động vào các phần tử bên trong component con. Nếu muốn tác động vào class của component con (ví dụ tùy biến style của thư viện Element Plus), bạn dùng cú pháp `:deep(.child-class)` (thay thế cho `>>>` và `/deep/` cũ).
2. Slotted Selectors (`:slotted()`): Tùy biến style cho nội dung truyền vào qua `<slot>`.""",
        "code_example": """<template>
  <div class=\"my-box\">
    <p>Chữ màu xanh chỉ áp dụng ở component này!</p>
  </div>
</template>

<style scoped>
/* PostCSS biên dịch thành: .my-box[data-v-12345] */
.my-box {
  background: #f0fdf4;
}

/* Áp dụng vào phần tử con sâu bên trong */
:deep(.el-button) {
  border-radius: 20px;
}
</style>""",
        "tips": "Nhớ: Dùng `:deep(.class)` thay cho cú pháp cũ `/deep/` hoặc `::v-deep`."
    },

    90: {
        "title_vi": "Custom Blocks trong Vue Single File Components là gì?",
        "level": "Senior",
        "short_answer": "Bên cạnh 3 khối chuẩn (`<script>`, `<template>`, `<style>`), Vue SFC cho phép định nghĩa các khối tùy biến (Custom Blocks) như `<i18n>`, `<docs>`, hoặc `<test>`. Các khối này được xử lý thông qua các plugin tùy chỉnh của Vite/Rollup để nhúng tài liệu, đa ngôn ngữ, hoặc bài test trực tiếp vào cùng file component.",
        "deep_dive": """1. Ví dụ `<i18n>` block: Cho phép nhúng trực tiếp chuỗi JSON dịch ngôn ngữ của riêng component đó ngay trong file, rất tiện lợi cho các component đa ngôn ngữ độc lập.""",
        "code_example": """<!-- Component có Custom Block <i18n> -->
<template>
  <p>{{ t('welcome') }}</p>
</template>

<i18n lang=\"json\">
{
  \"en\": { \"welcome\": \"Welcome to our app!\" },
  \"vi\": { \"welcome\": \"Chào mừng bạn đến với ứng dụng!\" }
}
</i18n>""",
        "tips": "Custom blocks là minh chứng cho thấy thiết kế cực kỳ linh hoạt và mở rộng của trình biên dịch SFC Vue."
    },

    91: {
        "title_vi": "Những tính năng mới đột phá nhất được giới thiệu trong Vue 3?",
        "level": "Junior",
        "short_answer": "Vue 3 là một cuộc cách mạng toàn diện: (1) Composition API (cho phép gom nhóm logic linh hoạt và tái sử dụng vượt trội), (2) Hệ thống Reactivity mới dựa trên JavaScript `Proxy` thay thế `Object.defineProperty`, (3) `<script setup>` tối ưu hóa hiệu năng và giảm boilerplate, (4) Teleport (chuyển vị trí render DOM ra ngoài `#app`), (5) Suspense (xử lý async dependencies), (6) Hỗ trợ Fragments (nhiều root nodes), và (7) Viết lại 100% bằng TypeScript.",
        "deep_dive": """1. Nhẹ hơn và Nhanh hơn: Vue 3 nhẹ hơn Vue 2 khoảng 40% (nhờ Tree-shaking), tốc độ render nhanh hơn gấp đôi và tiêu tốn ít hơn 50% RAM.""",
        "code_example": """<!-- Tận dụng tính năng Fragments mới của Vue 3: Không cần bọc <div> ngoài cùng! -->
<template>
  <header>Header</header>
  <main>Main Content</main>
  <footer>Footer</footer>
</template>""",
        "tips": "Nhớ 4 'từ khóa vàng' của Vue 3: Composition API, Proxy Reactivity, Tree-shakable, và Fragments."
    },

    92: {
        "title_vi": "So sánh chi tiết sự khác biệt giữa Composition API và Options API trong Vue 3?",
        "level": "Junior",
        "short_answer": "Options API tổ chức mã nguồn dựa trên các 'TÙY CHỌN' (Data, Methods, Computed, Mounted) khiến code của một tính năng bị xé nhỏ ra nhiều nơi. Composition API tổ chức mã nguồn dựa trên 'TÍNH NĂNG NGHIỆP VỤ' (Logical Concerns), cho phép toàn bộ code liên quan đến cùng một tính năng nằm gọn bên cạnh nhau hoặc tách ra thành Composable độc lập.",
        "deep_dive": """1. Khả năng tái sử dụng: Composition API cho phép chia sẻ logic dễ dàng mà không gặp các nhược điểm của Mixins.
2. Tương thích TypeScript: Composition API suy luận kiểu dữ liệu tự nhiên 100%, trong khi Options API phải dựa vào cấu trúc `this` rất khó khăn để định kiểu.
3. Cả hai vẫn cùng tồn tại: Vue 3 vẫn hỗ trợ đầy đủ Options API cho những ai yêu thích phong cách truyền thống.""",
        "code_example": """<!-- Composition API với <script setup> gọn gàng và tự nhiên -->
<script setup>
import { ref, computed } from 'vue';

// Toàn bộ logic tính năng A nằm chung 1 chỗ:
const count = ref(0);
const double = computed(() => count.value * 2);
function increment() { count.value++; }

// Toàn bộ logic tính năng B nằm chung 1 chỗ:
const title = ref('Dashboard');
</script>""",
        "tips": "Hãy liên hệ hình ảnh kinh điển: 'Options API giống như phân loại quần áo theo màu sắc (áo, quần, tất để riêng), còn Composition API phân loại theo bộ trang phục đi làm/đi chơi'."
    },

    93: {
        "title_vi": "Hệ thống Reactivity dựa trên `Proxy` của Vue 3 ưu việt hơn `Object.defineProperty` của Vue 2 như thế nào?",
        "level": "Senior",
        "short_answer": "Hệ thống Proxy trong Vue 3 vượt trội tuyệt đối vì: (1) Phát hiện được việc thêm hoặc xóa thuộc tính mới của Object mà không cần `Vue.set()`, (2) Phát hiện được việc thay đổi phần tử mảng bằng index (`arr[0] = val`) và thay đổi `arr.length`, (3) Hỗ trợ tự nhiên các cấu trúc dữ liệu mới `Map`, `Set`, `WeakMap`, `WeakSet`, và (4) Hiệu năng khởi tạo ban đầu nhanh hơn vì Proxy chỉ bọc tầng ngoài, các thuộc tính lồng sâu chỉ được bọc khi thực sự được truy cập (Lazy Reactive Wrap).",
        "deep_dive": """1. Hạn chế của Vue 2: Phải duyệt đệ quy qua toàn bộ cây object lúc khởi tạo component để cài getters/setters cho từng key, gây đơ lag nếu object ban đầu quá lớn.
2. Vue 3: Proxy bọc đối tượng cha, khi bạn gọi `obj.a.b` thì getter của `a` mới kích hoạt tạo reactive cho `a` (Lazy).""",
        "code_example": """const raw = { a: 1 };
const proxy = new Proxy(raw, {
  deleteProperty(target, prop) {
    console.log(`Đã phát hiện xóa thuộc tính: ${prop}`);
    return delete target[prop];
  }
});

delete proxy.a; // Kích hoạt ngay lập tức! Điều mà Vue 2 không thể làm được.""",
        "tips": "Nhớ cụm từ: 'Lazy Reactive Wrapping' - Vue 3 chỉ chuyển đổi các object lồng sâu thành reactive khi người dùng thực sự đọc nó, tiết kiệm RAM khổng lồ."
    },

    94: {
        "title_vi": "Những cải tiến trong Virtual DOM của Vue 3 và tác động đến hiệu năng?",
        "level": "Senior",
        "short_answer": "Virtual DOM trong Vue 3 được thiết kế lại toàn diện nhờ cơ chế 'Compiler-Informed Virtual DOM': (1) Patch Flags (đánh dấu bitwise chính xác phần tử nào động), (2) Static Hoisting (nâng toàn bộ VNodes tĩnh ra ngoài hàm render để tái sử dụng), (3) Cache Event Handlers, và (4) Flattened VNode Tree (cây DOM ảo được làm phẳng thành mảng các nút động). Kết quả là tốc độ diffing nhanh gấp nhiều lần so với Vue 2 và React.",
        "deep_dive": """1. Flattened Tree (Khối Block): Vue 3 chia template thành các Block. Một Block theo dõi trực tiếp một mảng phẳng các con động (`dynamicChildren`), bỏ qua toàn bộ các nút tĩnh trung gian khi so sánh diffing.""",
        "code_example": """// Minh họa Bitwise Patch Flags trong Vue 3:
// 1 = TEXT (chỉ text thay đổi)
// 2 = CLASS (chỉ class thay đổi)
// 8 = PROPS (thuộc tính thay đổi)
// Trình duyệt chỉ cần kiểm tra: if (patchFlag & 1) patchText()""",
        "tips": "Hiểu rõ về Bitwise Patch Flags và Block Tree là bằng chứng đanh thép cho thấy trình độ kỹ thuật cấp Senior Architect của bạn về Vue."
    },

    95: {
        "title_vi": "Cú pháp Slots trong Vue 3 có những cải tiến gì so với Vue 2?",
        "level": "Mid",
        "short_answer": "Vue 3 thống nhất hoàn toàn cú pháp Slots thông qua directive `v-slot` (viết tắt là `#`). Toàn bộ các cú pháp cũ như thuộc tính `slot=\"header\"` và `slot-scope=\"data\"` trong Vue 2 đã bị khai tử. Đồng thời, toàn bộ Slots trong Vue 3 được xử lý dưới dạng các HÀM (Functions) giúp tối ưu hóa hiệu năng: component con thay đổi slot không làm component cha bị re-render không cần thiết.",
        "deep_dive": """1. Viết tắt `#`: `<template #header=\"{ user }\">` thay thế cho `v-slot:header=\"{ user }\"`.
2. Truy cập trong script: Dùng macro `defineSlots()` trong TypeScript hoặc `useSlots()`.""",
        "code_example": """<!-- Component Cha sử dụng cú pháp Vue 3 chuẩn mực -->
<template>
  <MyTable :items=\"users\">
    <!-- Named Slot + Scoped Slot Props với cú pháp # rút gọn -->
    <template #row=\"{ item }\">
      <td>{{ item.name }}</td>
      <td><span class=\"badge\">{{ item.role }}</span></td>
    </template>
  </MyTable>
</template>""",
        "tips": "Nhớ: Cú pháp `slot=\"...\"` và `slot-scope=\"...\"` thuộc về Vue 2 cũ. Trong Vue 3 chỉ dùng `#` hoặc `v-slot`."
    },

    96: {
        "title_vi": "Cách quản lý trạng thái toàn cầu (Global State) mà không cần Vuex trong ứng dụng lớn?",
        "level": "Senior",
        "short_answer": "Trong các ứng dụng quy mô lớn hiện nay, có 2 cách chuẩn mực: (1) Sử dụng `Pinia` (thư viện quản lý state nhẹ, module hóa tự nhiên, chuẩn TypeScript), hoặc (2) Sử dụng mô hình `Stateful Composables` (tạo các file `.ts` chứa `reactive()` / `ref()` kết hợp `readonly()` ở phạm vi module).",
        "deep_dive": """1. Mô hình Module Scope Composable:
   Biến được khởi tạo bên NGOÀI hàm composable sẽ tồn tại như một Singleton dùng chung cho tất cả các components gọi hàm đó!""",
        "code_example": """// composables/useGlobalCart.js (Singleton State)
import { ref, computed, readonly } from 'vue';

// Biến nằm NGOÀI hàm -> Chia sẻ chung cho TOÀN BỘ ứng dụng
const cartItems = ref([]);

export function useGlobalCart() {
  const count = computed(() => cartItems.value.length);
  
  function addToCart(item) {
    cartItems.value.push(item);
  }

  return {
    cartItems: readonly(cartItems),
    count,
    addToCart
  };
}""",
        "tips": "Giải thích được cơ chế biến nằm bên ngoài hàm composable hoạt động như một Singleton State là câu trả lời cực kỳ tinh tế."
    },

    97: {
        "title_vi": "Chiến lược Phân tách mã nguồn (Code-Splitting) trong ứng dụng Vue?",
        "level": "Mid",
        "short_answer": "Code-Splitting chia nhỏ bundle JavaScript khổng lồ thành nhiều file nhỏ (chunks) chỉ được tải về trình duyệt khi người dùng thực sự cần đến. Hai chiến lược cốt lõi trong Vue là: (1) Route-level Code Splitting (Lazy-loading từng trang trong Vue Router qua `() => import('./View.vue')`), và (2) Component-level Code Splitting (Lazy-loading các component nặng qua `defineAsyncComponent()`).",
        "deep_dive": """1. Kết quả: Giảm kích thước tải trang đầu tiên từ 2MB xuống còn 150KB! Trình duyệt hiển thị trang chủ ngay tức thì.
2. Tự động chia vendor chunks: Vite tự động tách các package npm lớn trong `node_modules` thành file vendor riêng biệt để tận dụng HTTP cache của trình duyệt.""",
        "code_example": """// 1. Phân tách theo Route (Router)
const routes = [
  { path: '/admin', component: () => import('@/views/AdminView.vue') }
];

// 2. Phân tách theo Component (defineAsyncComponent)
import { defineAsyncComponent } from 'vue';
const HeavyPdfViewer = defineAsyncComponent(() =>
  import('@/components/HeavyPdfViewer.vue')
);""",
        "tips": "Bất kỳ dự án Vue nào bước vào giai đoạn nghiệm thu đều bắt buộc phải áp dụng Route-level Code Splitting."
    },

    98: {
        "title_vi": "Những cân nhắc quan trọng khi áp dụng Lazy Loading cho Components?",
        "level": "Mid",
        "short_answer": "Khi áp dụng Lazy Loading với `defineAsyncComponent()`, cần cân nhắc: (1) Trải nghiệm người dùng lúc chờ tải mạng (cần cung cấp Loading Component và Error Component nếu mạng mất), (2) Đặt thời gian trễ hiển thị (`delay: 200ms`) để tránh hiện tượng nhấp nháy spinner khi mạng nhanh, (3) Đặt thời gian timeout, và (4) Không nên lạm dụng cho các component nhỏ (< 5KB) vì chi phí gửi thêm một HTTP request tải chunk sẽ tốn thời gian hơn việc gộp chung vào bundle chính.",
        "deep_dive": """1. Cấu hình nâng cao của `defineAsyncComponent`: Cho phép truyền một object cấu hình chi tiết thay vì chỉ truyền một hàm import.""",
        "code_example": """import { defineAsyncComponent } from 'vue';
import LoadingSpinner from './LoadingSpinner.vue';
import ErrorDisplay from './ErrorDisplay.vue';

const AsyncModal = defineAsyncComponent({
  loader: () => import('./LargeModal.vue'),
  loadingComponent: LoadingSpinner,
  delay: 200, // Chỉ hiện spinner nếu tải quá 200ms (tránh nhấp nháy)
  errorComponent: ErrorDisplay,
  timeout: 5000 // Hủy nếu tải quá 5 giây
});""",
        "tips": "Thuộc tính `delay: 200` là chi tiết 'ăn tiền' thể hiện sự quan tâm sâu sắc đến trải nghiệm người dùng (UX)."
    },

    99: {
        "title_vi": "Kỹ thuật quản lý hệ thống định tuyến quy mô lớn (Large-Scale Routing) trong Vue?",
        "level": "Senior",
        "short_answer": "Quản lý hệ thống định tuyến hàng trăm routes trong dự án lớn đòi hỏi: (1) Chia nhỏ file router thành các module theo từng Domain nghiệp vụ (`user.routes.js`, `billing.routes.js`) và gộp lại trong `index.js`, (2) Sử dụng Route Metadata (`meta`) để khai báo tiêu đề trang, layout tương ứng và quyền hạn truy cập, (3) Sử dụng Dynamic Route Registration (`router.addRoute()`) để nạp thêm các routes quản trị chỉ sau khi user đăng nhập thành công, và (4) Kiểm soát cuộn trang tự động (`scrollBehavior`).",
        "deep_dive": """1. `router.addRoute()` (Định tuyến động bảo mật): Thay vì khai báo sẵn các trang admin trong file bundle (kẻ tấn công có thể soi ra URL trong mã nguồn), chỉ khi server trả về role admin thì frontend mới gọi `router.addRoute()` để đăng ký các route bí mật đó!""",
        "code_example": """// router/index.js (Gộp các modules định tuyến)
import { createRouter, createWebHistory } from 'vue-router';
import authRoutes from './modules/auth.routes';
import orderRoutes from './modules/order.routes';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...authRoutes,
    ...orderRoutes,
    { path: '/:pathMatch(.*)*', component: () => import('@/views/NotFound.vue') }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition; // Giữ nguyên vị trí khi bấm nút Back
    return { top: 0 }; // Cuộn lên đầu trang khi sang trang mới
  }
});""",
        "tips": "Kỹ thuật dùng `router.addRoute()` dựa trên quyền hạn người dùng là kiến trúc định tuyến bảo mật tiêu chuẩn cho các hệ thống ERP / CRM quy mô lớn."
    },

    100: {
        "title_vi": "Các quyết định về Kiến trúc và CSS/Styling ảnh hưởng như thế nào đến khả năng mở rộng của ứng dụng Vue?",
        "level": "Senior",
        "short_answer": "Các quyết định kiến trúc và style định hình sự sống còn của dự án khi mở rộng: (1) Sử dụng Utility-First CSS (như Tailwind CSS) hoặc Design System chuẩn mực thay vì viết CSS tự do không kiểm soát, (2) Luôn bật `<style scoped>` hoặc CSS Modules để ngăn ngừa xung đột kiểu dáng giữa các nhóm phát triển, (3) Tách biệt nghiêm ngặt Smart Components (State/API) và Dumb Components (UI thuần), (4) Áp dụng Monorepo (Turborepo / Nx) khi chia sẻ UI Components cho nhiều dự án, và (5) Tự động hóa kiểm tra Type Safety với TypeScript và CI/CD.",
        "deep_dive": """1. Tại sao Tailwind CSS bùng nổ trong Vue: Tailwind loại bỏ hoàn toàn việc phải đau đầu nghĩ tên class CSS, ngăn chặn việc file CSS phình to theo thời gian (kích thước CSS của Tailwind luôn giữ ở mức cố định < 10KB trên production build nhờ Purge/Content analysis).
2. Lời khuyên vàng cho tương lai: Một kiến trúc tốt là kiến trúc cho phép xóa bỏ hoặc thay thế một tính năng mà không làm ảnh hưởng đến phần còn lại của hệ thống.""",
        "code_example": """<!-- Sự kết hợp hoàn hảo giữa Vue 3 <script setup> và Tailwind CSS -->
<template>
  <button class=\"px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg shadow-md transition-all\">
    <slot>Nút chuẩn Design System</slot>
  </button>
</template>""",
        "tips": "Khép lại câu 100 tuyệt đẹp: 'Khả năng mở rộng không nằm ở việc viết code phức tạp, mà nằm ở tính nhất quán, module hóa độc lập, tuân thủ Clean Architecture và sự hỗ trợ mạnh mẽ của hệ thống kiểm thử tự động'."
    }
}
