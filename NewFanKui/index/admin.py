from django.contrib import admin

# Register your models here.
from index.models import *

#定义高级管理类

class UserAdmin(admin.ModelAdmin):
  search_fields = ('uname',)
  # #2.定义过滤器筛选字段
  # list_filter = ('',)
  # 3.定义列表页中显示的数据字段们
  list_display = ('uname','upwd','A_q','B_q','C_q')

class FankuiInfoAdmin(admin.ModelAdmin):
  #1.定义搜索字段
  search_fields = ('match_id',)
  # #2.定义过滤器筛选字段
  # list_filter = ('',)
  #3.定义列表页中显示的数据字段们
  list_display = ('fankuiyonghu','pingtai','match_id','match_name','mat_time','team_a','team_b','tijiao_time','leixing','saishiwenti','fankui_id','chulijieguo','chuli_time')


class MatchInfoAdmin(admin.ModelAdmin):
  #1.定义搜索字段
  search_fields = ('pingtai',)
  # #2.定义过滤器筛选字段
  # list_filter = ('',)
  #3.定义列表页中显示的数据字段们
  list_display = ('pingtai','match_id','match_name','start_time','team_a','team_a_en','team_b','team_b_en','leixing')

admin.site.register(FankuiInfo,FankuiInfoAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(MatchInfo,MatchInfoAdmin)