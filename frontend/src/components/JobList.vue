<template>
  <div class="job-list-container">
    <h2 class="page-title">招聘信息列表</h2>
    
    <!-- 搜索和筛选区域 -->
    <div class="search-filter">
      <input
        v-model="searchParams.job_title"
        placeholder="搜索职位名称"
        class="search-input"
      />
      <input
        v-model="searchParams.company_name"
        placeholder="搜索公司名称"
        class="search-input"
      />
      <input
        v-model="searchParams.location"
        placeholder="搜索工作地点"
        class="search-input"
      />
      <input
        v-model="searchParams.skills"
        placeholder="搜索技能标签"
        class="search-input"
      />
      <input
        v-model.number="searchParams.min_salary"
        type="number"
        placeholder="最低薪资"
        class="search-input"
      />
      <input
        v-model="searchParams.education"
        placeholder="搜索学历要求"
        class="search-input"
      />
      <input
        v-model="searchParams.industry"
        placeholder="搜索行业"
        class="search-input"
      />
      <button @click="fetchJobs" class="search-button">搜索</button>
    </div>
    
    <!-- 招聘列表 -->
    <div class="job-cards">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="jobs.length === 0" class="no-data">暂无数据</div>
      <div v-else>
        <div class="job-card" v-for="job in jobs" :key="job.id">
          <div class="job-header">
            <div class="company-info">
              <img 
                :src="job.company_logo || 'https://via.placeholder.com/60'" 
                alt="公司Logo"
                class="company-logo"
                v-if="job.company_logo"
              />
              <div v-else class="no-logo">暂无Logo</div>
              <div class="company-details">
                <h3 class="job-title">{{ job.job_title }}</h3>
                <p class="company-name">{{ job.company_name }}</p>
              </div>
            </div>
            <div class="salary">{{ job.salary }}</div>
          </div>
          
          <div class="job-info">
            <span class="info-item">{{ job.location }}</span>
            <span class="info-item">{{ job.experience }}</span>
            <span class="info-item">{{ job.education }}</span>
          </div>
          
          <div class="company-info-row">
            <span class="info-item">{{ job.company_type }}</span>
            <span class="info-item">{{ job.company_size }}</span>
            <span class="info-item">{{ job.industry }}</span>
          </div>
          
          <div class="skills">
            <span class="skill-tag" v-for="skill in getSkillsArray(job.skills)" :key="skill">
              {{ skill }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分页 -->
    <div class="pagination" v-if="totalJobs > 0">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1"
        class="pagination-btn"
      >
        上一页
      </button>
      <span class="page-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      <div class="page-jump">
        <input 
          v-model.number="jumpPage" 
          type="number" 
          min="1" 
          :max="totalPages"
          class="jump-input"
        />
        <button @click="gotoPage" class="jump-button">跳转</button>
      </div>
      <button 
        @click="nextPage" 
        :disabled="currentPage === totalPages"
        class="pagination-btn"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script>
import { getJobList } from '../api/jobService';

export default {
  name: 'JobList',
  data() {
    return {
      jobs: [],
      loading: false,
      error: '',
      currentPage: 1,
      pageSize: 20,
      totalJobs: 0,
      jumpPage: 1,
      searchParams: {
        job_title: '',
        company_name: '',
        location: '',
        skills: '',
        min_salary: null,
        education: '',
        industry: '',
      },
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalJobs / this.pageSize);
    },
  },
  mounted() {
    this.fetchJobs();
  },
  methods: {
    async fetchJobs() {
      this.loading = true;
      this.error = '';
      
      try {
        const params = {
          ...this.searchParams,
          page: this.currentPage,
          page_size: this.pageSize,
        };
        
        const data = await getJobList(params);
        
        // 处理响应数据
        if (Array.isArray(data)) {
          // 如果返回的是数组，直接使用
          this.jobs = data;
          this.totalJobs = data.length;
        } else if (data.results) {
          // 如果返回的是分页数据
          this.jobs = data.results;
          this.totalJobs = data.count;
        } else {
          this.jobs = [];
          this.totalJobs = 0;
        }
      } catch (err) {
        this.error = '获取数据失败，请稍后重试';
        console.error('获取招聘数据失败:', err);
      } finally {
        this.loading = false;
      }
    },
    
    // 解析技能标签为数组
    getSkillsArray(skills) {
      if (!skills) return [];
      // 假设技能标签是以逗号分隔的字符串
      return skills.split(',').map(skill => skill.trim()).filter(skill => skill);
    },
    
    // 上一页
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.jumpPage = this.currentPage;
        this.fetchJobs();
      }
    },
    
    // 下一页
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.jumpPage = this.currentPage;
        this.fetchJobs();
      }
    },
    
    // 跳转到指定页码
    gotoPage() {
      let page = parseInt(this.jumpPage);
      if (page && page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchJobs();
      } else {
        this.jumpPage = this.currentPage;
      }
    },
  },
};
</script>

<style scoped>
.job-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.page-title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
}

.search-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.search-button:hover {
  background-color: #0056b3;
}

.job-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.job-card {
  padding: 20px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.job-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.company-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.company-logo {
  width: 60px;
  height: 60px;
  object-fit: contain;
  border-radius: 4px;
}

.no-logo {
  width: 60px;
  height: 60px;
  background-color: #f5f5f5;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 12px;
}

.company-details {
  flex: 1;
}

.job-title {
  margin: 0 0 5px 0;
  font-size: 18px;
  color: #333;
}

.company-name {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.salary {
  font-size: 20px;
  font-weight: bold;
  color: #ff6b35;
}

.job-info,
.company-info-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
}

.info-item {
  font-size: 14px;
  color: #666;
}

.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  padding: 4px 12px;
  background-color: #e3f2fd;
  color: #1976d2;
  border-radius: 16px;
  font-size: 12px;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 30px;
    padding: 20px;
  }

  .pagination-btn {
    padding: 8px 16px;
    background-color: #000000;
    color: white;
    border: 1px solid #000000;
    border-radius: 4px;
    cursor: pointer;
  }

  .pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .pagination-btn:not(:disabled):hover {
    background-color: #333333;
  }
  
  .page-jump {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .jump-input {
    width: 60px;
    padding: 6px 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    text-align: center;
  }
  
  .jump-button {
    padding: 6px 12px;
    background-color: #000000;
    color: white;
    border: 1px solid #000000;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .jump-button:hover {
    background-color: #333333;
  }

.page-info {
  font-size: 14px;
  color: #666;
}

.loading,
.error,
.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #dc3545;
}
</style>