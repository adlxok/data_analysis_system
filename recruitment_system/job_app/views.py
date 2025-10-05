from rest_framework import viewsets
from .models import JobPosting
from .serializers import JobPostingSerializer
import re
from django.db.models import Q
from rest_framework import viewsets, decorators, response
from .simple_ml_model import get_simple_model

class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    """招聘信息的只读视图集"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    
    @decorators.action(detail=False, methods=['get'])
    def all_data(self, request):
        """获取所有职位数据（不分页）"""
        # 调用get_queryset方法来应用相同的过滤逻辑
        queryset = self.get_queryset()
        # 序列化数据
        serializer = self.get_serializer(queryset, many=True)
        # 返回未分页的数据
        return response.Response(serializer.data)
    
    @decorators.action(detail=False, methods=['post'])
    def predict_salary(self, request):
        """根据职位信息预测薪资"""
        try:
            # 获取请求数据
            job_info = request.data
            
            # 验证必要的字段
            required_fields = ['experience', 'education', 'location', 'company_type', 'company_size', 'industry']
            for field in required_fields:
                if field not in job_info or not job_info[field]:
                    job_info[field] = 'Unknown'  # 使用默认值
            
            # 获取简化模型实例
            model = get_simple_model()
            
            # 进行薪资预测
            # 从job_info字典中提取各个字段作为单独参数
            predicted_salary = model.predict_salary(
                job_info['experience'],
                job_info['education'],
                job_info['location'],
                job_info['industry']
            )
            
            if predicted_salary is not None:
                # 格式化预测结果
                min_salary = int(predicted_salary * 0.9)  # 预测薪资范围的下限（90%）
                max_salary = int(predicted_salary * 1.1)  # 预测薪资范围的上限（110%）
                
                # 格式化为友好的薪资表示
                def format_salary(salary):
                    if salary >= 10000:
                        return f"{salary/10000:.1f}万"
                    else:
                        return f"{salary/1000:.0f}k"
                
                formatted_min = format_salary(min_salary)
                formatted_max = format_salary(max_salary)
                
                return response.Response({
                    'success': True,
                    'predicted_salary': predicted_salary,
                    'salary_range': f"{formatted_min}-{formatted_max}",
                    'min_salary': min_salary,
                    'max_salary': max_salary
                })
            else:
                return response.Response({
                    'success': False,
                    'error': '无法进行薪资预测，模型可能未正确初始化'
                }, status=500)
                
        except Exception as e:
            return response.Response({
                'success': False,
                'error': str(e)
            }, status=500)
        
    def get_queryset(self):
        # 可以在这里添加过滤逻辑
        queryset = super().get_queryset()
        
        # 构建Q对象用于复杂查询
        q_objects = Q()
        
        # 按职位名称搜索
        job_title = self.request.query_params.get('job_title', None)
        if job_title:
            q_objects &= Q(job_title__icontains=job_title)
        
        # 按公司名称搜索
        company_name = self.request.query_params.get('company_name', None)
        if company_name:
            q_objects &= Q(company_name__icontains=company_name)
        
        # 按地点搜索
        location = self.request.query_params.get('location', None)
        if location:
            q_objects &= Q(location__icontains=location)
        
        # 按技能搜索
        skills = self.request.query_params.get('skills', None)
        if skills:
            q_objects &= Q(skills__icontains=skills)
            
        # 按学历要求搜索
        education = self.request.query_params.get('education', None)
        if education:
            q_objects &= Q(education__icontains=education)
            
        # 按行业搜索
        industry = self.request.query_params.get('industry', None)
        if industry:
            q_objects &= Q(industry__icontains=industry)
            
        # 应用所有过滤条件
        if q_objects:
            queryset = queryset.filter(q_objects)
            
        # 按最低薪资搜索（单独处理，因为需要特殊逻辑解析薪资字符串）
        min_salary = self.request.query_params.get('min_salary', None)
        if min_salary:
            try:
                min_salary = float(min_salary)
                
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
