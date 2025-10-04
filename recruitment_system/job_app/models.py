from django.db import models

# Create your models here.
class JobPosting(models.Model):
    id = models.IntegerField(primary_key=True)
    job_title = models.CharField(max_length=255, verbose_name='职位名称')
    company_name = models.CharField(max_length=255, verbose_name='公司名称')
    company_logo = models.CharField(max_length=255, null=True, blank=True, verbose_name='公司logo')
    location = models.CharField(max_length=255, verbose_name='工作地点')
    experience = models.CharField(max_length=255, verbose_name='工作经验')
    education = models.CharField(max_length=255, verbose_name='学历要求')
    salary = models.CharField(max_length=255, verbose_name='薪资')
    company_type = models.CharField(max_length=255, verbose_name='公司类型')
    company_size = models.CharField(max_length=255, verbose_name='公司规模')
    industry = models.CharField(max_length=255, verbose_name='行业')
    skills = models.TextField(verbose_name='技能标签')
    
    class Meta:
        managed = False  # 不允许Django管理表的创建和修改
        db_table = 'job_postings'  # 指定对应的数据库表名
        verbose_name = '招聘信息'
        verbose_name_plural = '招聘信息'
