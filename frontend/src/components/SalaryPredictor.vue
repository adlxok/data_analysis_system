<template>
  <div class="salary-predictor-container">
    <h2>薪资预测工具</h2>
    
    <div class="predictor-content">
      <!-- 左侧表单区域 -->
      <div class="form-section">
        <form @submit.prevent="handlePrediction" class="prediction-form">
          <div class="form-group">
            <label for="experience">工作经验</label>
            <select id="experience" v-model="formData.experience" required>
              <option value="应届生">应届生</option>
              <option value="1-3年">1-3年</option>
              <option value="3-5年">3-5年</option>
              <option value="5-10年">5-10年</option>
              <option value="10年以上">10年以上</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="education">学历要求</label>
            <select id="education" v-model="formData.education" required>
              <option value="大专及以上">大专及以上</option>
              <option value="本科及以上">本科及以上</option>
              <option value="硕士及以上">硕士及以上</option>
              <option value="博士及以上">博士及以上</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="location">工作地点</label>
            <select id="location" v-model="formData.location" required>
              <option value="北京">北京</option>
              <option value="上海">上海</option>
              <option value="广州">广州</option>
              <option value="深圳">深圳</option>
              <option value="杭州">杭州</option>
              <option value="成都">成都</option>
              <option value="武汉">武汉</option>
              <option value="西安">西安</option>
              <option value="南京">南京</option>
              <option value="其他">其他</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="company_type">公司类型</label>
            <select id="company_type" v-model="formData.company_type" required>
              <option value="互联网">互联网</option>
              <option value="金融">金融</option>
              <option value="教育">教育</option>
              <option value="制造业">制造业</option>
              <option value="医疗健康">医疗健康</option>
              <option value="电子商务">电子商务</option>
              <option value="人工智能">人工智能</option>
              <option value="外资企业">外资企业</option>
              <option value="国有企业">国有企业</option>
              <option value="民营企业">民营企业</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="company_size">公司规模</label>
            <select id="company_size" v-model="formData.company_size" required>
              <option value="50人以下">50人以下</option>
              <option value="50-100人">50-100人</option>
              <option value="100-500人">100-500人</option>
              <option value="500-1000人">500-1000人</option>
              <option value="1000-5000人">1000-5000人</option>
              <option value="5000人以上">5000人以上</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="industry">行业</label>
            <select id="industry" v-model="formData.industry" required>
              <option value="互联网">互联网</option>
              <option value="金融">金融</option>
              <option value="人工智能">人工智能</option>
              <option value="医疗健康">医疗健康</option>
              <option value="教育培训">教育培训</option>
              <option value="电子商务">电子商务</option>
              <option value="云计算">云计算</option>
              <option value="软件服务">软件服务</option>
              <option value="游戏">游戏</option>
              <option value="移动互联网">移动互联网</option>
            </select>
          </div>
          
          <button type="submit" class="predict-button" :disabled="loading">
            {{ loading ? '预测中...' : '预测薪资' }}
          </button>
        </form>
      </div>
      
      <!-- 右侧结果展示区域 -->
      <div class="result-section">
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>正在预测薪资，请稍候...</p>
        </div>
        
        <div v-else-if="predictionResult" class="prediction-result">
          <h3>预测结果</h3>
          <div class="result-card">
            <div class="salary-range">
              <span class="salary-label">预计薪资范围：</span>
              <span class="salary-value">{{ predictionResult.salary_range }}</span>
            </div>
            
            <div class="prediction-details">
              <p>该预测基于机器学习模型分析大量招聘数据得出，仅供参考</p>
              <div class="prediction-factors">
                <h4>影响薪资的主要因素：</h4>
                <ul>
                  <li>工作经验：{{ formData.experience }}</li>
                  <li>学历要求：{{ formData.education }}</li>
                  <li>工作地点：{{ formData.location }}</li>
                  <li>行业领域：{{ formData.industry }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="initial-state">
          <p>请填写左侧表单信息，点击"预测薪资"按钮获取基于机器学习的薪资预测结果</p>
          <div class="tips">
            <h4>使用提示：</h4>
            <ul>
              <li>预测结果基于历史招聘数据分析</li>
              <li>选择越准确的信息，预测结果越可靠</li>
              <li>薪资范围仅供参考，实际薪资可能因个人能力和公司差异有所不同</li>
            </ul>
          </div>
        </div>
        
        <div v-if="error" class="error-message">
          <p>{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { predictSalary } from '../api/jobService';

export default {
  name: 'SalaryPredictor',
  data() {
    return {
      formData: {
        experience: '1-3年',
        education: '本科及以上',
        location: '北京',
        company_type: '互联网',
        company_size: '100-500人',
        industry: '互联网'
      },
      predictionResult: null,
      loading: false,
      error: null
    };
  },
  
  methods: {
    async handlePrediction() {
      this.loading = true;
      this.error = null;
      
      try {
        const result = await predictSalary(this.formData);
        if (result.success) {
          console.log('API返回结果:', result);
          this.predictionResult = result;
        } else {
          this.error = result.error || '预测失败，请稍后重试';
        }
      } catch (err) {
        this.error = '预测过程中发生错误，请稍后重试';
        console.error('预测错误:', err);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.salary-predictor-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.salary-predictor-container h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

.predictor-content {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
}

.form-section {
  flex: 1;
  min-width: 300px;
}

.result-section {
  flex: 1;
  min-width: 400px;
}

.prediction-form {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s;
}

.form-group select:focus {
  outline: none;
  border-color: #36cfc9;
}

.predict-button {
  width: 100%;
  padding: 12px;
  background: #36cfc9;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.predict-button:hover:not(:disabled) {
  background: #31b8b3;
}

.predict-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #36cfc9;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.prediction-result {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.prediction-result h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 20px;
}

.result-card {
  background: white;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 25px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.salary-range {
  text-align: center;
  margin-bottom: 20px;
}

.salary-label {
  font-size: 16px;
  color: #666;
  margin-right: 10px;
}

.salary-value {
  font-size: 32px;
  font-weight: bold;
  color: #36cfc9;
}

.prediction-details p {
  color: #666;
  margin-bottom: 15px;
  font-size: 14px;
  line-height: 1.5;
}

.prediction-factors h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 16px;
}

.prediction-factors ul {
  list-style: none;
  padding: 0;
}

.prediction-factors li {
  background: #f0f9f8;
  padding: 8px 12px;
  margin-bottom: 5px;
  border-radius: 4px;
  font-size: 14px;
  color: #555;
}

.initial-state {
  background: #f8f9fa;
  padding: 40px 25px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.initial-state p {
  color: #666;
  margin-bottom: 25px;
  line-height: 1.6;
  font-size: 16px;
}

.tips {
  text-align: left;
  background: white;
  padding: 20px;
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.tips h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 16px;
}

.tips ul {
  list-style: none;
  padding: 0;
}

.tips li {
  color: #666;
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
  font-size: 14px;
  line-height: 1.5;
}

.tips li::before {
  content: "•";
  color: #36cfc9;
  position: absolute;
  left: 0;
  font-weight: bold;
}

.error-message {
  background: #fee;
  border: 1px solid #fcc;
  color: #c00;
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .predictor-content {
    flex-direction: column;
  }
  
  .salary-predictor-container h2 {
    font-size: 20px;
  }
  
  .salary-value {
    font-size: 24px;
  }
}
</style>