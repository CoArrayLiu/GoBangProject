<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h1 v-if="itemId !== null">{{ itemId }}</h1> <!-- 条件渲染 itemId -->
    <button @click="fetchItem">获取 Item</button> <!-- 点击按钮时调用 fetchItem -->
  </div>
</template>

<script>
import api from "../api/http.js"
export default {
  data() {
    return {
      msg: 'Hello World', // 示例消息
      itemId: null, // 存储 itemId
    };
  },
  methods: {
    async fetchItem() {
      try {
        const data = await this.get_item(1); // 调用 get_item，获取 item_id 为 1 的项目
        this.itemId = data.item_id; // 更新 itemId
      } catch (error) {
        console.error(error); // 处理错误
      }
    },
    async get_item(itemId) {
      const res = await api.service.get(`/items/${itemId}`);

      console.log("Response Object:", res);

      // 检查状态码，确保是 2xx
      if (res.status < 200 || res.status >= 300) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      // 获取响应数据
      const data = res.data;
      console.log("Response Data:", data);

      return data; // 返回解析后的 JSON 数据
    }
  }
};
</script>
