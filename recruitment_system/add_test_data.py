import os
import sys
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recruitment_system.settings')
django.setup()

from job_app.models import JobPosting

# 创建测试数据
def create_test_jobs():
    # 清除现有数据
    print("正在清除现有数据...")
    JobPosting.objects.all().delete()
    
    # 职位数据
    jobs_data = [
        {
            'id': 1,
            'job_title': '高级前端开发工程师',
            'company_name': '科技创新有限公司',
            'company_logo': 'logo1.png',
            'location': '北京',
            'salary': '25k-35k',
            'experience': '3-5年',
            'education': '本科及以上',
            'company_type': '民营企业',
            'company_size': '500-1000人',
            'industry': '互联网',
            'skills': 'Vue, React, JavaScript, TypeScript',
        },
        {
            'id': 2,
            'job_title': '后端开发工程师',
            'company_name': '大数据科技有限公司',
            'company_logo': 'logo2.png',
            'location': '上海',
            'salary': '20k-30k',
            'experience': '2-3年',
            'education': '本科及以上',
            'company_type': '合资企业',
            'company_size': '1000-2000人',
            'industry': '大数据',
            'skills': 'Python, Django, MySQL',
        },
        {
            'id': 3,
            'job_title': '产品经理',
            'company_name': '智能科技有限公司',
            'company_logo': 'logo3.png',
            'location': '广州',
            'salary': '18k-28k',
            'experience': '3-5年',
            'education': '本科及以上',
            'company_type': '外资企业',
            'company_size': '100-500人',
            'industry': '人工智能',
            'skills': '产品设计, 用户研究, 数据分析',
        },
        {
            'id': 4,
            'job_title': 'UI设计师',
            'company_name': '创意设计有限公司',
            'company_logo': 'logo4.png',
            'location': '深圳',
            'salary': '15k-25k',
            'experience': '1-3年',
            'education': '本科及以上',
            'company_type': '民营企业',
            'company_size': '50-100人',
            'industry': '设计',
            'skills': 'Photoshop, Illustrator, Figma',
        },
        {
            'id': 5,
            'job_title': '数据分析师',
            'company_name': '金融科技有限公司',
            'company_logo': 'logo5.png',
            'location': '杭州',
            'salary': '18k-28k',
            'experience': '2-3年',
            'education': '硕士及以上',
            'company_type': '金融科技',
            'company_size': '500-1000人',
            'industry': '金融',
            'skills': 'Python, SQL, 数据分析, 机器学习',
        },
        {
            'id': 6,
            'job_title': '测试工程师',
            'company_name': '软件测试服务有限公司',
            'company_logo': 'logo6.png',
            'location': '成都',
            'salary': '12k-20k',
            'experience': '1-3年',
            'education': '本科及以上',
            'company_type': '服务外包',
            'company_size': '100-500人',
            'industry': '软件服务',
            'skills': '自动化测试, 性能测试, Selenium',
        },
        {
            'id': 7,
            'job_title': '运维工程师',
            'company_name': '云计算服务有限公司',
            'company_logo': 'logo7.png',
            'location': '武汉',
            'salary': '15k-25k',
            'experience': '2-3年',
            'education': '本科及以上',
            'company_type': '互联网',
            'company_size': '500-1000人',
            'industry': '云计算',
            'skills': 'Linux, Docker, Kubernetes',
        },
        {
            'id': 8,
            'job_title': '算法工程师',
            'company_name': '人工智能研究院',
            'company_logo': 'logo8.png',
            'location': '南京',
            'salary': '30k-50k',
            'experience': '3-5年',
            'education': '博士及以上',
            'company_type': '研究机构',
            'company_size': '100-500人',
            'industry': '人工智能',
            'skills': 'Python, TensorFlow, 深度学习',
        },
        {
            'id': 9,
            'job_title': '前端开发工程师',
            'company_name': '移动互联网有限公司',
            'company_logo': 'logo9.png',
            'location': '西安',
            'salary': '15k-25k',
            'experience': '1-3年',
            'education': '本科及以上',
            'company_type': '民营企业',
            'company_size': '50-100人',
            'industry': '移动互联网',
            'skills': 'React, Redux, JavaScript',
        },
        {
            'id': 10,
            'job_title': 'Java开发工程师',
            'company_name': '企业软件有限公司',
            'company_logo': 'logo10.png',
            'location': '重庆',
            'salary': '18k-28k',
            'experience': '2-3年',
            'education': '本科及以上',
            'company_type': '软件公司',
            'company_size': '100-500人',
            'industry': '企业软件',
            'skills': 'Java, Spring Boot, MySQL',
        },
        # 添加更多数据以测试分页
        {
            'id': 11,
            'job_title': 'DevOps工程师',
            'company_name': '敏捷科技有限公司',
            'company_logo': 'logo11.png',
            'location': '苏州',
            'salary': '20k-30k',
            'experience': '3-5年',
            'education': '本科及以上',
            'company_type': '互联网',
            'company_size': '500-1000人',
            'industry': '互联网',
            'skills': 'CI/CD, Docker, Kubernetes',
        },
        {
            'id': 12,
            'job_title': '数据科学家',
            'company_name': '数据智能有限公司',
            'company_logo': 'logo12.png',
            'location': '长沙',
            'salary': '25k-40k',
            'experience': '3-5年',
            'education': '博士及以上',
            'company_type': '高科技',
            'company_size': '100-500人',
            'industry': '人工智能',
            'skills': 'Python, R, 机器学习, 深度学习',
        },
    ]
    
    # 创建职位数据
    print("正在创建测试数据...")
    for job_data in jobs_data:
        JobPosting.objects.create(**job_data)
    
    print(f"成功创建{len(jobs_data)}条测试数据。")

if __name__ == '__main__':
    create_test_jobs()