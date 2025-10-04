<template>
  <div class="app">
    <header class="navbar">
      <h1>招聘信息管理系统</h1>
    </header>
    <nav class="navigation">
      <ul>
        <li :class="{ active: currentView === 'jobList' }" @click="switchView('jobList')">职位列表</li>
        <li :class="{ active: currentView === 'dataVisualization' }" @click="switchView('dataVisualization')">数据分析</li>
      </ul>
    </nav>
    <main class="main-content">
      <JobList v-if="currentView === 'jobList'" />
      <DataVisualization v-if="currentView === 'dataVisualization'" />
    </main>
  </div>
</template>

<script>
import JobList from './components/JobList.vue'
import DataVisualization from './components/DataVisualization.vue'

export default {
  name: 'App',
  components: {
    JobList,
    DataVisualization
  },
  data() {
    return {
      currentView: 'jobList' // 默认显示职位列表
    }
  },
  methods: {
    switchView(view) {
      this.currentView = view
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #4a6fa5;
  color: white;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navigation {
  background-color: white;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.navigation ul {
  display: flex;
  list-style: none;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.navigation li {
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  font-weight: 500;
  color: #666;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
}

.navigation li:hover {
  color: #4a6fa5;
}

.navigation li.active {
  color: #4a6fa5;
  border-bottom-color: #4a6fa5;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>