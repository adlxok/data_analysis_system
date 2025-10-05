#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
薪资预测模型训练脚本
用于训练和保存机器学习模型，以便系统启动时可以直接加载使用
"""
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recruitment_system.settings')
import django
django.setup()

from job_app.simple_ml_model import get_simple_model


def main():
    """主函数，训练并保存薪资预测模型"""
    print("===== 开始训练薪资预测模型 =====")
    
    try:
        # 获取模型实例（这会自动加载已训练的模型或训练新模型）
        model = get_simple_model()
        
        # 训练模型
        model.train()
        
        # 获取模型信息
        model_info = model.get_model_info()
        print("\n模型训练成功！")
        print("\n模型信息:")
        print(f"- 模型类型: {model_info['model_type']}")
        print(f"- 是否已训练: {'是' if model_info['is_trained'] else '否'}")
        print(f"- 经验权重: {model_info['weights']['experience']}")
        print(f"- 基础偏差值: {model_info['bias']}")
        
        # 测试预测功能
        experience = 4  # 4年经验
        education = '本科'
        location = '北京'
        industry = '互联网'
        
        predicted_salary = model.predict_salary(experience, education, location, industry)
        print(f"\n测试预测结果:")
        print(f"- 测试职位信息: 经验={experience}年, 学历={education}, 地点={location}, 行业={industry}")
        print(f"- 预测薪资: {predicted_salary} 元")
            
    except Exception as e:
        print(f"训练模型时发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n===== 模型训练脚本执行完毕 =====")


if __name__ == '__main__':
    main()