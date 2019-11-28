from django.db import models

# Create your models here.


# 创建用户权限表
class User(models.Model):
    uname = models.CharField(max_length=50,verbose_name="用户名")
    upwd = models.CharField(max_length=200,verbose_name="密码")
    A_q = models.CharField(max_length=30, null=True, blank=True,verbose_name="A平台权限")
    B_q = models.CharField(max_length=30, null=True, blank=True, verbose_name="B平台权限")
    C_q = models.CharField(max_length=30, null=True, blank=True, verbose_name="C平台权限")


    def __str__(self):
        return self.uname


    class Meta:
        db_table = "user"
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


#创建反馈数据表
class FankuiInfo(models.Model):
    fankuiyonghu  = models.CharField(max_length=30,verbose_name="反馈用户")
    pingtai = models.CharField(max_length=30,verbose_name="赛事来源")
    match_id =models.CharField(max_length=50,verbose_name="赛事ID")
    match_name =models.CharField(max_length=100,verbose_name="赛事名称")
    mat_time = models.CharField(max_length=80,verbose_name="赛事时间")
    team_a = models.CharField(max_length=200,verbose_name="主队")
    team_a_en = models.CharField(max_length=200, null=True, blank=True,verbose_name="主队外语")
    team_b = models.CharField(max_length=200,verbose_name="客队")
    team_b_en = models.CharField(max_length=200, null=True, blank=True,verbose_name="客队外语")
    tijiao_time = models.CharField(max_length=100,verbose_name="提交时间")
    leixing = models.CharField(max_length=30,verbose_name="赛事类型")
    saishiwenti = models.CharField(max_length=100, verbose_name="赛事问题")
    fankui_id = models.CharField(max_length=30,null=True, blank=True,verbose_name="反馈赛事ID")
    chulijieguo = models.CharField(max_length=20, null=True, blank=True,verbose_name="运营处理状态")
    chuli_time = models.CharField(max_length=100, null=True, blank=True,verbose_name="运营处理时间")

    def __str__(self):
        return self.fankuiyonghu

    class Meta:
        db_table = "fankuiinfo"
        verbose_name = '反馈信息'
        verbose_name_plural = verbose_name


#各个平台赛事表
class MatchInfo(models.Model):
    pingtai = models.CharField(max_length=30,verbose_name="赛事平台")
    match_id =models.CharField(max_length=50,verbose_name="赛事ID")
    match_name =models.CharField(max_length=100,verbose_name="赛事名称")
    start_time = models.CharField(max_length=80,verbose_name="赛事时间")
    team_a = models.CharField(max_length=200,verbose_name="主队")
    team_a_en = models.CharField(max_length=200, null=True, blank=True,verbose_name="主队外语")
    team_b = models.CharField(max_length=200,verbose_name="客队")
    team_b_en = models.CharField(max_length=200, null=True, blank=True,verbose_name="客队外语")
    leixing = models.CharField(max_length=30,verbose_name="赛事类型")

    def __str__(self):
        return self.pingtai

    class Meta:
        db_table = "matchinfo"
        verbose_name = '各平台赛事信息'
        verbose_name_plural = verbose_name

