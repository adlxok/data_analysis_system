import numpy as np
import pandas as pd
import re
import json
import os
from datetime import datetime

class SimpleSalaryPredictionModel:
    """简化版薪资预测模型，不依赖scikit-learn和scipy"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimpleSalaryPredictionModel, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.weights = {
                'experience': 3000,  # 每增加1年经验，薪资增加3000
                'education': {'大专': 5000, '本科': 8000, '硕士': 12000, '博士': 18000, '其他': 5000},  # 不同学历的基础薪资
                'location': {'北京': 12000, '上海': 11000, '广州': 8000, '深圳': 9000, '杭州': 7000, '其他': 5000},  # 不同城市的基础薪资
                'industry': {'互联网': 10000, '金融': 9000, '教育': 6000, '医疗': 7000, '其他': 5000},  # 不同行业的基础薪资
            }
            self.bias = 3000  # 基础偏差值
            self.is_trained = False
            self.model_path = os.path.join(os.path.dirname(__file__), 'simple_model_weights.json')
            self.load_model()
    
    def load_model(self):
        """加载预训练的模型权重"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'r', encoding='utf-8') as f:
                    model_data = json.load(f)
                    self.weights = model_data.get('weights', self.weights)
                    self.bias = model_data.get('bias', self.bias)
                    self.is_trained = True
                    print(f"模型已从{self.model_path}加载")
        except Exception as e:
            print(f"加载模型失败: {str(e)}")
    
    def save_model(self):
        """保存模型权重"""
        try:
            model_data = {
                'weights': self.weights,
                'bias': self.bias,
                'train_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            with open(self.model_path, 'w', encoding='utf-8') as f:
                json.dump(model_data, f, ensure_ascii=False, indent=2)
            print(f"模型已保存到{self.model_path}")
        except Exception as e:
            print(f"保存模型失败: {str(e)}")
    
    def train(self, data=None):
        """训练模型"""
        # 这里使用简化的训练逻辑
        # 在实际应用中，你可以根据真实数据调整权重
        print("开始训练简化版薪资预测模型...")
        
        # 如果没有提供数据，生成一些模拟数据来调整权重
        if data is None:
            data = self._generate_sample_data()
        
        # 这里使用简单的启发式方法调整权重
        # 在实际应用中，你可以使用更复杂的优化算法
        self._adjust_weights_based_on_data(data)
        
        self.is_trained = True
        self.save_model()
        print("模型训练完成！")
        return True
    
    def _generate_sample_data(self, num_samples=200):
        """生成模拟数据用于训练"""
        # 生成不同经验值的样本
        experiences = np.random.randint(1, 10, num_samples)
        
        # 生成不同学历的样本
        education_levels = ['大专', '本科', '硕士', '博士']
        education = np.random.choice(education_levels, num_samples)
        
        # 生成不同城市的样本
        locations = ['北京', '上海', '广州', '深圳', '杭州', '其他']
        location = np.random.choice(locations, num_samples)
        
        # 生成不同行业的样本
        industries = ['互联网', '金融', '教育', '医疗', '其他']
        industry = np.random.choice(industries, num_samples)
        
        # 创建DataFrame
        data = pd.DataFrame({
            'experience': experiences,
            'education': education,
            'location': location,
            'industry': industry
        })
        
        # 根据权重生成薪资
        data['salary'] = data.apply(lambda row: self._calculate_salary(row) + np.random.normal(0, 2000), axis=1)
        data['salary'] = data['salary'].apply(lambda x: max(3000, int(x)))  # 确保薪资不为负
        
        return data
    
    def _adjust_weights_based_on_data(self, data):
        """根据数据调整权重"""
        # 这是一个简化的权重调整方法
        # 在实际应用中，你可以使用更复杂的算法
        
        # 计算不同特征组合下的平均薪资
        for edu in self.weights['education'].keys():
            for loc in self.weights['location'].keys():
                for ind in self.weights['industry'].keys():
                    mask = (data['education'] == edu) & (data['location'] == loc) & (data['industry'] == ind)
                    subset = data[mask]
                    if len(subset) > 0:
                        # 计算经验系数
                        if subset['experience'].std() > 0:
                            exp_coef = (subset['salary'].mean() - self.weights['education'][edu] - \
                                       self.weights['location'][loc] - self.weights['industry'][ind] - self.bias) / \
                                      subset['experience'].mean()
                            if not np.isnan(exp_coef) and exp_coef > 0:
                                self.weights['experience'] = (self.weights['experience'] + exp_coef) / 2
    
    def _extract_experience_years(self, experience_str):
        """从经验字符串中提取年数"""
        import re
        # 尝试提取数字
        match = re.search(r'(\d+)', str(experience_str))
        if match:
            return float(match.group(1))
        # 处理特殊情况
        if '应届生' in str(experience_str):
            return 0
        if '1年以下' in str(experience_str):
            return 0.5
        # 默认返回平均经验值
        return 3.0  # 假设平均经验为3年

    def _calculate_salary(self, row):
        """根据特征计算薪资"""
        # 经验影响
        exp_years = self._extract_experience_years(row['experience'])
        exp_effect = exp_years * self.weights['experience']
        
        # 学历影响
        edu_effect = self.weights['education'].get(row['education'], self.weights['education']['其他'])
        
        # 城市影响
        loc_effect = self.weights['location'].get(row['location'], self.weights['location']['其他'])
        
        # 行业影响
        ind_effect = self.weights['industry'].get(row['industry'], self.weights['industry']['其他'])
        
        # 计算总薪资
        total_salary = exp_effect + edu_effect + loc_effect + ind_effect + self.bias
        
        return total_salary
    
    def predict_salary(self, experience, education, location, industry):
        """预测薪资"""
        if not self.is_trained:
            print("警告: 模型尚未训练，使用默认权重进行预测")
        
        # 创建一行数据
        row = pd.Series({
            'experience': experience,
            'education': education,
            'location': location,
            'industry': industry
        })
        
        # 计算薪资
        predicted_salary = self._calculate_salary(row)
        
        # 添加一些随机波动使预测更真实
        predicted_salary += np.random.normal(0, 1500)
        predicted_salary = max(3000, int(predicted_salary))  # 确保薪资不为负
        
        return predicted_salary

    def get_model_info(self):
        """获取模型信息"""
        return {
            'model_type': 'Simple Linear Model',
            'is_trained': self.is_trained,
            'weights': self.weights,
            'bias': self.bias
        }

def get_simple_model():
    """获取简化版模型的单例实例"""
    model = SimpleSalaryPredictionModel()
    return model