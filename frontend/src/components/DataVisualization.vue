<template>
  <div class="data-visualization">
    <h2 class="page-title">招聘数据分析</h2>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="charts-container">
      <!-- 薪资分布图 -->
      <div class="chart-card">
        <h3>薪资分布</h3>
        <div class="chart-wrapper">
          <VChart :option="salaryOption" height="400px" />
        </div>
      </div>
      
      <!-- 学历分布图 -->
      <div class="chart-card">
        <h3>学历要求分布</h3>
        <div class="chart-wrapper">
          <VChart :option="educationOption" height="400px" />
        </div>
      </div>
      
      <!-- 行业分布图 -->
      <div class="chart-card">
        <h3>行业分布</h3>
        <div class="chart-wrapper">
          <VChart :option="industryOption" height="400px" />
        </div>
      </div>
      
      <!-- 工作经验分布图 -->
      <div class="chart-card">
        <h3>工作经验要求分布</h3>
        <div class="chart-wrapper">
          <VChart :option="experienceOption" height="400px" />
        </div>
      </div>
      
      <!-- 技能词云 -->
      <div class="chart-card">
        <h3>热门技能词云</h3>
        <div class="chart-wrapper">
          <VChart :option="skillsWordCloudOption" height="400px" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getJobList, getAllJobData } from '../api/jobService';
import * as echarts from 'echarts';
import 'echarts-wordcloud'; // 导入词云组件
import VChart from 'vue-echarts';

export default {
  name: 'DataVisualization',
  components: {
    VChart
  },
  data() {
    return {
      jobs: [],
      loading: false,
      error: '',
      salaryData: [],
      educationData: [],
      industryData: [],
      experienceData: [],
      skillsData: []
    };
  },
  computed: {
    // 薪资分布图表配置
    salaryOption() {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            return `${params[0].name}: ${params[0].value} 个职位`;
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.salaryData.map(item => item.range),
          axisLabel: {
            interval: 0,
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '职位数量'
        },
        series: [{
          data: this.salaryData.map(item => item.count),
          type: 'bar',
          itemStyle: {
            color: '#007bff'
          }
        }]
      };
    },
    
    // 学历分布图表配置
    educationOption() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: this.educationData.map(item => item.name)
        },
        series: [
          {
            name: '学历分布',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.educationData.map(item => ({
              value: item.count,
              name: item.name
            }))
          }
        ]
      };
    },
    
    // 行业分布图表配置
    industryOption() {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.industryData.slice(0, 10).map(item => item.name),
          axisLabel: {
            interval: 0,
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '职位数量'
        },
        series: [{
          data: this.industryData.slice(0, 10).map(item => item.count),
          type: 'bar',
          itemStyle: {
            color: '#28a745'
          }
        }]
      };
    },
    
    // 工作经验分布图表配置
    experienceOption() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: this.experienceData.map(item => item.name)
        },
        series: [
          {
            name: '经验分布',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.experienceData.map(item => ({
              value: item.count,
              name: item.name
            }))
          }
        ]
      };
    },
    
    // 技能词云配置
    skillsWordCloudOption() {
      return {
        tooltip: {},
        series: [
          {
            type: 'wordCloud',
            shape: 'circle',
            left: 'center',
            top: 'center',
            width: '80%',
            height: '80%',
            right: null,
            bottom: null,
            sizeRange: [12, 40],
            rotationRange: [-45, 45],
            rotationStep: 45,
            gridSize: 8,
            drawOutOfBound: false,
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              color: function() {
                return 'rgb(' + [
                  Math.round(Math.random() * 150 + 50),
                  Math.round(Math.random() * 150 + 50),
                  Math.round(Math.random() * 150 + 50)
                ].join(',') + ')';
              }
            },
            emphasis: {
              textStyle: {
                shadowBlur: 10,
                shadowColor: '#333'
              }
            },
            data: this.skillsData.slice(0, 100)
          }
        ]
      };
    }
  },
  mounted() {
    this.fetchAllData();
  },
  methods: {
    async fetchAllData() {
      this.loading = true;
      this.error = '';
      
      try {
        // 使用专门的接口获取所有数据（不分页）
        const params = {}; // 可以传递过滤参数，但不进行分页
        
        const data = await getAllJobData(params);
        
        // 由于all_data接口直接返回数组，不需要处理分页结构
        if (Array.isArray(data)) {
          this.jobs = data;
        } else {
          this.jobs = [];
        }
        
        // 处理数据生成各类统计信息
        this.processData();
      } catch (err) {
        this.error = '获取数据失败，请稍后重试';
        console.error('获取招聘数据失败:', err);
      } finally {
        this.loading = false;
      }
    },
    
    // 处理数据生成各类统计信息
    processData() {
      // 处理薪资分布数据
      this.processSalaryData();
      
      // 处理学历分布数据
      this.processEducationData();
      
      // 处理行业分布数据
      this.processIndustryData();
      
      // 处理工作经验分布数据
      this.processExperienceData();
      
      // 处理技能词云数据
      this.processSkillsData();
    },
    
    // 处理薪资分布数据
    processSalaryData() {
      const salaryRanges = [
        { min: 0, max: 5000, range: '0-5k' },
        { min: 5000, max: 10000, range: '5-10k' },
        { min: 10000, max: 15000, range: '10-15k' },
        { min: 15000, max: 20000, range: '15-20k' },
        { min: 20000, max: 30000, range: '20-30k' },
        { min: 30000, max: 50000, range: '30-50k' },
        { min: 50000, max: Infinity, range: '50k以上' }
      ];
      
      const salaryDistribution = salaryRanges.map(range => ({
        range: range.range,
        count: 0
      }));
      
      this.jobs.forEach(job => {
        const avgSalary = this.parseSalary(job.salary);
        if (avgSalary) {
          for (let i = 0; i < salaryRanges.length; i++) {
            const range = salaryRanges[i];
            if (avgSalary >= range.min && avgSalary < range.max) {
              salaryDistribution[i].count++;
              break;
            }
          }
        }
      });
      
      this.salaryData = salaryDistribution;
    },
    
    // 解析薪资字符串，返回平均薪资数值
    parseSalary(salaryStr) {
      if (!salaryStr) return null;
      
      // 提取所有可能的薪资数值
      const matches = salaryStr.match(/(\d+(?:\.\d+)?)/g);
      if (!matches || matches.length === 0) return null;
      
      // 转换为数字
      const numbers = matches.map(match => parseFloat(match));
      
      // 判断单位并转换
      let multiplier = 1;
      if (salaryStr.includes('k') || salaryStr.includes('K')) {
        multiplier = 1000;
      } else if (salaryStr.includes('万')) {
        multiplier = 10000;
      }
      
      // 计算平均值
      const avg = numbers.reduce((sum, num) => sum + num, 0) / numbers.length;
      
      return avg * multiplier;
    },
    
    // 处理学历分布数据
    processEducationData() {
      const educationMap = new Map();
      
      this.jobs.forEach(job => {
        if (job.education) {
          const key = job.education.trim();
          educationMap.set(key, (educationMap.get(key) || 0) + 1);
        }
      });
      
      this.educationData = Array.from(educationMap.entries())
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count);
    },
    
    // 处理行业分布数据
    processIndustryData() {
      const industryMap = new Map();
      
      this.jobs.forEach(job => {
        if (job.industry) {
          const key = job.industry.trim();
          industryMap.set(key, (industryMap.get(key) || 0) + 1);
        }
      });
      
      this.industryData = Array.from(industryMap.entries())
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count);
    },
    
    // 处理工作经验分布数据
    processExperienceData() {
      const experienceMap = new Map();
      
      this.jobs.forEach(job => {
        if (job.experience) {
          const key = job.experience.trim();
          experienceMap.set(key, (experienceMap.get(key) || 0) + 1);
        }
      });
      
      this.experienceData = Array.from(experienceMap.entries())
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count);
    },
    
    // 处理技能词云数据
    processSkillsData() {
      const skillsMap = new Map();
      
      this.jobs.forEach(job => {
        if (job.skills) {
          // 假设技能标签是以逗号分隔的字符串
          const skills = job.skills.split(',')
            .map(skill => skill.trim())
            .filter(skill => skill);
          
          skills.forEach(skill => {
            skillsMap.set(skill, (skillsMap.get(skill) || 0) + 1);
          });
        }
      });
      
      // 转换为词云所需格式
      this.skillsData = Array.from(skillsMap.entries())
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value);
    }
  }
};
</script>

<style scoped>
.data-visualization {
  max-width: 1400px;
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

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
}

.chart-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: box-shadow 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.chart-card h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 20px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.chart-wrapper {
  width: 100%;
  height: 400px;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #dc3545;
}

@media (max-width: 600px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    padding: 15px;
  }
  
  .chart-wrapper {
    height: 300px;
  }
}
</style>