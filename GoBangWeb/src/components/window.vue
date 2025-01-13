<template>
    <div v-if="isVisible" class="modal">
      <div class="modal-content">
        <p>{{ content }}</p>
        <button @click="closeModal">OK</button>
      </div>
    </div>
</template>
  
<script>
  export default {
    props:{
        content:{
            type:String,
            Required:true,
        }
    },
    data() {
      return {
        isVisible: false
      };
    },
    methods: {
      openModal() {
        this.isVisible = true;
      },
      closeModal() {
        this.isVisible = false;
      }
    }
  }
</script>
  
<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* 深色背景，透明度稍高 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 确保模态框在最上层 */
}

.modal-content {
  background-color: #fff; /* 白色背景 */
  padding: 30px; /* 增加内边距 */
  border-radius: 10px; /* 圆角 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 更柔和的阴影 */
  max-width: 500px; /* 最大宽度限制 */
  width: 90%; /* 自适应宽度 */
  animation: fadeIn 0.3s; /* 添加淡入效果 */
}

button {
  background-color: #007bff; /* Bootstrap 蓝色 */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s; /* 添加过渡效果 */
}

button:hover {
  background-color: #0056b3; /* 鼠标悬停颜色 */
  transform: scale(1.05); /* 悬停时轻微放大 */
}

/* 添加淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
