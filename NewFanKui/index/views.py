from django.shortcuts import render,redirect
from django.http import HttpResponse
import hashlib
import requests
from index.models import *
import json
from django.core import serializers #转换json数据
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail #第三方邮件发送模块
import os
import time,datetime
from dwebsocket.decorators import accept_websocket


# #首页登录接口函数
def index(request):
    if request.method == 'GET':
        return render(request, "index.html")
    else:
        uname = request.POST.get('uname')
        print(uname)
        upwd = request.POST.get('upwd')
        print(upwd)
        user = User.objects.filter(uname=uname, upwd=upwd)
        print(user)
        if user:
            # 登录成功
            uid = user[0].id
            request.session['uid'] = uid
            request.session['uname'] = uname
            return HttpResponse("/fankuiye/")
        else:
            # 登录失败
            errMsg = 0
            return HttpResponse(errMsg)

#=========测试session====
def sessioninfo(request):
    # 获取登录信息
    if 'uid' in request.session and 'uname' in request.session:
        # user_session = User.objects.filter(id=request.session.get('uid'))
        # print(user_session)
        uid = request.session.get('uid')
        print(uid)
        uname = User.objects.get(id=uid).uname
        print(uname)
        return HttpResponse("ok")

# ======================
#反馈页接口函数
def fankuiye(request):
    return render(request, "xiangqing.html")

#提交反馈数据给运营并发送邮件
def tijiaofankui(request):
    if 'uid' in request.session and 'uname' in request.session:
        uid = request.session.get('uid')
        uname = User.objects.get(id=uid).uname
        print(uname)
        if request.method == "GET":
            pingtai = request.GET.get("pingtai")  # 反馈勾选的id
            print(pingtai)
            match_id = request.GET.get("jiemu")#反馈勾选的id
            print(match_id)
            saishiwenti = request.GET.get("problem")#反馈勾选的视频问题
            print(saishiwenti)

            fankuitijiao = MatchInfo.objects.filter(pingtai=pingtai,match_id=match_id)
            for tj in fankuitijiao:
                print(tj.match_id,tj.match_name,tj.start_time,tj.team_a,tj.team_b,tj.leixing)
        # ========反馈数据提交到数据库============
                dic = {
                    "fankuiyonghu": uname,
                    "pingtai":pingtai,
                    "match_id": tj.match_id,
                    "match_name": tj.match_name,
                    "mat_time": tj.start_time,
                    "team_a": tj.team_a,
                    "team_b": tj.team_b,
                    "tijiao_time": time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())),
                    "leixing": tj.leixing,
                    "saishiwenti":saishiwenti,
                }
                user = FankuiInfo(**dic)
                user.save()
                print("提交数据库成功")
                print(dic)
                # #反馈信息发送邮件
                subject = '反馈信息'  #主题
                message = str(dic)  #内容
                sender = settings.EMAIL_HOST_USER  # 发送邮箱，已经在settings.py设置，直接导入
                receiver = ("zhugy66@163.com",)  #目标邮箱
                send_mail(subject, message, sender, receiver, html_message=False)


                return HttpResponse(1) #邮件接收成功
                # return redirect("/fankuiye/")


# =========================
#反馈处理接口函数
def fankuijieguo(request):
    return render(request, "fankuixiangqing.html")


#获取运营处理数据－－＞存入数据库
def addyunyingdata(request):
    a_data = requests.get("http://222.187.222.143:8084/chulishuju/")
    a_data = a_data.text
    array = json.loads(a_data)
    for i in array:
        fankui_id = i["fankui_id"]
        chuliinfo = i["chuliinfo"]
        chulitime = i["chulitime"]
    # return HttpResponse(a_data) #测试用

        fankuitijiao = FankuiInfo.objects.filter(match_id=fankui_id)
        if fankuitijiao:
            for fan in fankuitijiao:
                fan.fankuiid = fankui_id
                fan.chulijieguo = chuliinfo
                fan.chuli_time = chulitime
                fan.save()
        print("运营提交数据库成功")

    return redirect("/fankuijieguo/")


#前端反馈结果显示接口
def fjieguo(request):
    if 'uid' in request.session and 'uname' in request.session:
        id = request.session.get('uid')
        uname = User.objects.get(id=id).uname
        total = FankuiInfo.objects.filter(fankuiyonghu=uname).count()
        total = int(total)
        print("共%s条" % total)

        if request.method == "GET":
            pag = request.GET.get("pageNum")  # 向前端获取页数
            print(pag)
            size = int(12)  # 代表每页显示数量
            n = int(pag) - 1
            n = n * size
            m = int(pag) * size

            jieguo = FankuiInfo.objects.filter(fankuiyonghu=uname)[n:m]
            all_list = []
            for jie in jieguo:
                dict = {
                    "total": total,  # 代表总记录数
                    "size": size,  # 代表每页显示数量
                    "pages": pag,  # 代表当前页
                    "current": total // 12 + 1,  # 代表总页数
                    "data": {
                        "fankuiyonghu": jie.fankuiyonghu,
                        "pingtai": jie.pingtai,
                        "match_id": jie.match_id,
                        "match_name": jie.match_name,
                        "mat_time": jie.mat_time,
                        "team_a": jie.team_a,
                        "team_a_en": jie.team_a_en,
                        "team_b": jie.team_b,
                        "team_b_en": jie.team_b_en,
                        "tijiao_time": jie.tijiao_time,
                        "leixing": jie.leixing,
                        "fankui_id": jie.fankui_id,
                        "chulijieguo": jie.chulijieguo,
                        "chuli_time":jie.chuli_time
                    }
                }

                all_list.append(dict)

            return HttpResponse(json.dumps(all_list))

#权限平台数据
def quanxian(request):
    if 'uid' in request.session and 'uname' in request.session:
        id = request.session.get('uid')
        uname = User.objects.get(id=id).uname
        print(uname)
        yonghuquanxian = User.objects.filter(uname=uname)  # 查询MatchFootball表中id=1的信息
        for q in yonghuquanxian:
            print(q.A_q,q.B_q,q.C_q)
            dic = [{
                "A":q.A_q,
                "B":q.B_q,
                "C":q.C_q,
            }]
            return HttpResponse(json.dumps(dic))

def pingtaishuju(request):
    if request.method == "GET":
        pingtai = request.GET.get('pingtai')
        print(pingtai)
        leixing = request.GET.get("fenlei")
        print(leixing)
        pag = request.GET.get("pageNum") #向前端获取页数
        print(pag)

        total = MatchInfo.objects.filter(pingtai=pingtai, leixing=leixing).count()
        total = int(total)
        print("共%s条" %total)

        size = int(12)# 代表每页显示数量
        n = int(pag)-1
        n = n*size
        m = int(pag) * size

        # if size % 11 == 0:
        #     size =

        matches = MatchInfo.objects.filter(pingtai=pingtai, leixing=leixing)[n:m]#[(pag-1)*size:pag*size]
        all_list = []
        for mat in matches:
            dict = {
                "total": total,  # 代表总记录数
                "size": size,  # 代表每页显示数量
                "pages": pag,  # 代表当前页
                "current": total // 12 + 1,  # 代表总页数
                "data" : {
                    "pingtai": mat.pingtai,
                    "match_id": mat.match_id,
                    "match_name": mat.match_name,
                    "start_time": mat.start_time,
                    "team_a": mat.team_a,
                    "team_a_en": mat.team_a_en,
                    "team_b": mat.team_b,
                    "team_b_en": mat.team_b_en,
                    "leixing": mat.leixing,
                }
            }

            all_list.append(dict)

        return HttpResponse(json.dumps(all_list))

# 搜索功能数据映射
def sousuo(request):
    if request.method == "GET":
        pingtai = request.GET.get("pingtai")
        print("搜索平台：", pingtai)
        sousuo = request.GET.get("keywords")
        print("搜索内容：", sousuo)
        pag = request.GET.get("pageNum")
        print("yeshu:", pag)

        total = MatchInfo.objects.filter(Q(pingtai__contains=pingtai),
                                         Q(leixing__contains=sousuo) | Q(match_name__contains=sousuo) | Q(
                                             team_a__contains=sousuo) | Q(team_b__contains=sousuo) | Q(
                                             start_time__contains=sousuo)).count()
        total = int(total)
        print("共%s条" % total)

        size = int(12)  # 代表每页显示数量
        n = int(pag) - 1
        n = n * size
        print("ddd", n)
        m = int(pag) * size
        print("ddd", m)

        match = MatchInfo.objects.filter(Q(pingtai__contains=pingtai),
                                         Q(leixing__contains=sousuo) | Q(match_name__contains=sousuo) | Q(
                                             team_a__contains=sousuo) | Q(team_b__contains=sousuo) | Q(
                                             start_time__contains=sousuo))[n:m]
        all_list = []
        for mat in match:
            dict = {
                "total": total,  # 代表总记录数
                "size": size,  # 代表每页显示数量
                "pages": pag,  # 代表当前页
                "current": total // 12 + 1,  # 代表总页数
                "data": {
                    "pingtai": mat.pingtai,
                    "match_id": mat.match_id,
                    "match_name": mat.match_name,
                    "start_time": mat.start_time,
                    "team_a": mat.team_a,
                    "team_a_en": mat.team_a_en,
                    "team_b": mat.team_b,
                    "team_b_en": mat.team_b_en,
                    "leixing": mat.leixing,
                }
            }

            all_list.append(dict)

        return HttpResponse(json.dumps(all_list))

#运营接收反馈的接口函数
def tijiaoinfo(request):
    tijiao = FankuiInfo.objects.all().distinct()
    all_list = []
    for tj in tijiao:
        dic = {
            "fankuiyonghu": tj.fankuiyonghu,
            "pingtai": tj.pingtai,
            "leixing": tj.leixing,
            "match_id": tj.match_id,
            "match_name": tj.match_name,
            "mat_time": tj.mat_time,
            "team_a": tj.team_a,
            "team_b": tj.team_b,
            "saishiwenti": tj.saishiwenti,
            "tijiao_time": tj.tijiao_time,
        }
        all_list.append(dic)

    return HttpResponse(json.dumps(all_list))


# =========================
# A平台数据接口函数
def Ashuju(request):
    a_data = requests.get("http://api.iptvjam.com/livejbb.php")
    # a_data = requests.get("http://www.sdton.com/video/api/list.php")
    return HttpResponse(a_data)

#B平台数据接口函数
def Bshuju(request):
    b_data = requests.get("http://api.iptvjam.com/liveim.php")
    return HttpResponse(b_data)

#C平台数据接口函数
def Cshuju(request):
    c_data = requests.get("http://api.iptvjam.com/livesba.php")
    c_data = c_data.text
    c_data = eval(c_data)
    # c_data = c_data["data"][:5]  #前五条数据
    c_data = c_data["data"]
    n = len(c_data)
    print(n)

    return HttpResponse(json.dumps({"data": c_data}))
    # return HttpResponse(c_data)
# =========================

#==================================================================
#测试B平台数据参数
def testajax(request):
    if request.method == "GET":
        data1 = request.GET.get('value')
        print(data1)
        # data2 = request.GET.get("jiemu")
        # print(data2)
        #
        # data3 = request.GET.get("problem")
        # print(data3)
        return HttpResponse(json.dumps({"value":data1}))

#测试多条件查询
def duo(request):
    s = MatchInfo.objects.filter(pingtai="A",leixing="篮球")[:1]
    print(s)
    jieguo_jsonStr = serializers.serialize("json", s, ensure_ascii=False)
    return HttpResponse(jieguo_jsonStr)



#测试数据格式处理
def dd(request):
    sousuo = "杯"
    match = MatchInfo.objects.filter(Q(pingtai__contains="C"),
                                     Q(leixing__contains=sousuo) | Q(match_name__contains=sousuo) | Q(
                                         team_a__contains=sousuo) | Q(team_b__contains=sousuo) | Q(
                                         start_time__contains=sousuo))# [n:m]

    all_list = []
    for mat in match:
        data = {
            "pingtai": mat.pingtai,
            "match_id": mat.match_id,
            "match_name": mat.match_name,
            "start_time": mat.start_time,
            "team_a": mat.team_a,
            "team_a_en": mat.team_a_en,
            "team_b": mat.team_b,
            "team_b_en": mat.team_b_en,
            "leixing": mat.leixing,
        }
        all_list.append(data)
    dict = {"code": "1",
            "message": "查询成功",
            # "total": total,  # 代表总记录数
            # "size": size,  # 代表每页显示数量
            # "pages": pag,  # 代表当前页
            # "current": total // 11 + 1,  # 代表总页数
            "data": all_list,
            }

    return HttpResponse(json.dumps(dict))


#ws协议
def getoIndex(request):
    return render(request,"ws.html")

clients = []
@accept_websocket
def echo(request):
    if request.is_websocket:
        try:
            clients.append(request.websocket)
            for message in request.websocket:
                print(message)
                mes = eval(message) #将字符串类型的消息转换为字典型
                print(mes)
                data = mes["data"]#前端传递过来的数据
                print(data)

                #获取当前时间作为反馈提交的时间
                t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                print("接收到data的时间为:%s" %t)

                dt = datetime.datetime.now()
                s1 = {"data": str(dt)}
                s1 = json.dumps(s1).encode()
                request.websocket.send(s1)
                #
                # onames = SportObject.objects.all()
                # jsonStr = serializers.serialize("json", onames)
                # print(jsonStr)
                # s11 = {"data": str(jsonStr)}
                # s11 = json.dumps(s11).encode()
                # request.websocket.send(s11)


                s2 = {"data": "收到"}
                s2 = json.dumps(s2).encode()
                request.websocket.send(s2)

                time.sleep(0.1)  # 间隔0.1秒

                for client in clients:
                    client.send(message)#前端发送的数据返回到前端
        finally:
             clients.remove(request.websocket)




