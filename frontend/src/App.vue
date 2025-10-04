<script setup>
import JobList from './components/JobList.vue'
</script>

<template>
  <header class="app-header">
    <h1>招聘信息管理系统</h1>
  </header>
  <main class="app-main">
    <JobList />
  </main>
</template>

<style scoped>
.app-header {
  background-color: #007bff;
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 24px;
}

.app-main {
  min-height: calc(100vh - 80px);
  background-color: #f5f7fa;
}
</style>
