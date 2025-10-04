from rest_framework import viewsets
from .models import JobPosting
from .serializers import JobPostingSerializer
import re
from django.db.models import Q
from rest_framework import viewsets

class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    """招聘信息的只读视图集"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    
    def get_queryset(self):
        # 可以在这里添加过滤逻辑
        queryset = super().get_queryset()
        # 示例：按职位名称搜索
        job_title = self.request.query_params.get('job_title', None)
        if job_title:
            queryset = queryset.filter(job_title__icontains=job_title)
        # 示例：按公司名称搜索
        company_name = self.request.query_params.get('company_name', None)
        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)
        # 示例：按地点搜索
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        # 示例：按技能搜索
        skills = self.request.query_params.get('skills', None)
        if skills:
            queryset = queryset.filter(skills__icontains=skills)
            
        # 按学历要求搜索
        education = self.request.query_params.get('education', None)
        if education:
            queryset = queryset.filter(education__icontains=education)
            
        # 按行业搜索
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
            
        # 按最低薪资搜索
        min_salary = self.request.query_params.get('min_salary', None)
        if min_salary:
            try:
                min_salary = float(min_salary)
                # 构建Q对象进行复杂查询
                salary_queries = Q()
                
                # 从已过滤的queryset中获取所有职位
                valid_job_ids = []
                
                # 优化查询：只获取必要的字段
                for job in queryset.values('id', 'salary'):
                    # 尝试从薪资字符串中提取数值
                    salary_str = job['salary'] or ''
                    # 改进正则表达式，支持更多薪资格式
                    # 提取所有可能的薪资数值，如'15k-25k', '15000-25000', '15000元/月', '25k'等
                    salary_matches = re.findall(r'(\d+(?:\.\d+)?)\s*[kK]?', salary_str)
                    
                    if salary_matches:
                        try:
                            # 使用最低薪资数值作为比较依据
                            # 或者取所有匹配数值的最小值
                            min_salary_value = float('inf')
                            
                            for match in salary_matches:
                                salary_value = float(match)
                                # 如果薪资包含'k'或'K'，则乘以1000
                                if 'k' in salary_str.lower():
                                    salary_value *= 1000
                                # 如果薪资包含'万'，则乘以10000
                                elif '万' in salary_str:
                                    salary_value *= 10000
                                
                                if salary_value < min_salary_value:
                                    min_salary_value = salary_value
                            
                            # 保留薪资大于等于最低薪资的职位
                            if min_salary_value <= float('inf') and min_salary_value >= min_salary:
                                valid_job_ids.append(job['id'])
                        except ValueError:
                            pass
                
                # 过滤出符合条件的职位
                if valid_job_ids:
                    queryset = queryset.filter(id__in=valid_job_ids)
                else:
                    # 如果没有符合条件的职位，返回空查询集
                    queryset = queryset.none()
            except ValueError:
                # 如果min_salary不是有效的数字，则忽略该过滤条件
                pass
                
        return queryset
