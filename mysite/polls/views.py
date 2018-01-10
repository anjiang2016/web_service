# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Template
import sys
sys.path.append("/home/mingmingzhao/MTCNN-Tensorflow/test/")
sys.path.append("/home/mingmingzhao/MTCNN-Tensorflow/")
#from home.mingmingzhao.MTCNN-Tensorflow.test import face_detect
import face_detect
# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
import os
def get_bodystr(rlist):
    if len(rlist)<3:
        rlist=[]
        rlist.append('1')
        rlist.append('100')
        rlist.append(u'video/teacher_images_rate_10/')
    #bodystr="<p><img src='{{urlstr1}}' alt='merge' /><br /></p>"
    static_dir='/data1/mingmingzhao/data_sets/test/'
    dirname=static_dir+u'video/teacher_images_rate_10/'
    dirname=static_dir+rlist[2]
    remote_url_pre=u'http://192.168.7.37:8393/static/'+rlist[2]
    img_url='no_run_https://vodp.vipkid.com.cn/cltvprocess/cover/jz66f1d49d97d048fe9e4a62004199d0b2/jz66f1d49d97d048fe9e4a62004199d0b2_1_for_trail.jpg'
    bodystr=u"<p><img src='%s' /><br/></p>"%(img_url)
    count=0
    start_num=int(rlist[0])
    length=int(rlist[1])
    for rt, dirs, files in os.walk(dirname):
        for f in files:
            count+=1
            if count<start_num:
                continue
            
            fname = os.path.splitext(f)
            print remote_url_pre+f
            local_name="["+str(count)+"]"+dirname+f
            bodystr+=u"%s<p><img src='%s' alt='%s' title='%s'/></p><br />"%(local_name,remote_url_pre+f,local_name,local_name)
            if count>=start_num+length:
                return bodystr
    return bodystr     
def show_face_datasets(request):
    print 'host:'
    print request.get_host() 
    #templatestr="Hello {{ name }}!...<br/><img src='{{urlstr1}}' alt='merge' /><br/><img src='{{urlstr2}}' alt='merge' />"
    templatestr=create_body_show()
    #bodystr="<p><img src='{{urlstr1}}' alt='merge' /><br /></p>"
    
    vlist=[u'start_num',u'length',u'dirname']
    rlist=sparse_request(request,vlist)
    bodystr=get_bodystr(rlist)
    template = Template(templatestr)
    html=template.render(body=bodystr)
    #return HttpResponse("Hello, world. You're at the polls index. and i want to send some html")
    return HttpResponse(html)
def apis(request):
    data_post={'face_num':1,'boxstr':'','img_result':''} #返回给客户端的数据
    data_get={'face_num':'u need post imageurl to me'}
    if request.method=="POST":
        print(request.POST) #<查看客户端发来的请求内容
        return JsonResponse(data_post) #通过 django内置的Json格式
    elif request.method=="GET":
        if u'url' in request.GET: 
            q = request.GET[u'url']
            img_url=q
            boxstr,img_url_result=has_face(img_url)
            data_post['boxstr']=boxstr
            data_post['img_result']=img_url_result
        return JsonResponse(data_post)
    else:
        return JsonResponse({'info':'u send any information!'})
def create_body_show():
    html = """
    <html>
    <body>
         <form method="GET" >
            <p>
            start_num: <input type="text" name="start_num" style="width: 20%; height:2%;border:5px solid blue;padding:5px;background-color:transparent;">
            length: <input type="text" name="length" style="width: 20%; height:2%;border:5px solid blue;padding:5px;background-color:transparent;">
            </p>
            <p>
            dirname: <input type="text" name="dirname" style="width: 100%; height:2%;border:5px solid blue;padding:5px;background-color:transparent;">
</p>
            <p>
            <input type="submit" style="width:100%;height:4%;" value="get image">
            </p>

    "show images :"
    {{body}}
    </body>
    </html>
    """
    return html
def create_body():
    html = """
    <html>
    <body>
        <form method="GET" >
            <p>
            Image url: <input type="text" name="url" style="width: 100%; height:7%;border:5px solid blue;padding:5px;background-color:transparent;">
            </p>
            <p>
            <input type="submit" style="width:100%;height:4%;" value="face detect">
            </p>
            <p>"Hello {{ name }}!...<br/><img src='{{urlstr1}}' alt='merge' /><br/>"src img:"<br /><img src='{{urlstr2}}' alt='merge' />"
              
            </p>
            <p>"result:{{bbox}}"<br /><img src='{{url_result}}' alt='face detect result' title='face detect result' />"
    </body>
    </html>
    """
    return html
def has_face(img_url):
    return face_detect.face_detc(img_url)
    face_num=3
    return "img:%s has %d faces"%(img_url,face_num)
def sparse_request(request,vlist):
    #vlist=[u'start_num',u'length']
    rlist=[]
    if request.method=="GET":
        for i in range(0,len(vlist)):
            if vlist[i] in request.GET:
                if request.GET[vlist[i]] is not '':
                    rlist.append(request.GET[vlist[i]])
                    print rlist
    return rlist

def index(request):
    print 'host:'
    print request.get_host() 
    #templatestr="Hello {{ name }}!...<br/><img src='{{urlstr1}}' alt='merge' /><br/><img src='{{urlstr2}}' alt='merge' />"
    templatestr=create_body()
    img_url='https://vodp.vipkid.com.cn/cltvprocess/cover/jz66f1d49d97d048fe9e4a62004199d0b2/jz66f1d49d97d048fe9e4a62004199d0b2_1_for_trail.jpg'
    gif_url='https://vodp.vipkid.com.cn/cltvprocess/cover/5244262/5244262_24509715_24509715_0.123419_for_yearbook.gif'
    img_url_result=img_url
    boxstr='boxstr'
    if request.method == 'GET':
        templatestr+='get'
        if u'url' in request.GET: 
            q = request.GET[u'url']
            img_url=q
            boxstr,img_url_result=has_face(img_url)
            #templatestr+=boxstr
        templatestr+='[get]'
    elif request.method == 'POST':
        templatestr+='[post]'
    template = Template(templatestr)
    html=template.render(name='Zhao mingming',urlstr1=gif_url,urlstr2=img_url,url_result=img_url_result,bbox=boxstr)
    #return HttpResponse("Hello, world. You're at the polls index. and i want to send some html")
    return HttpResponse(html)

