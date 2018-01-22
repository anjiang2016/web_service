# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import os
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.styles import STYLE_MAP
from pyh import *
import commands
import re
# Create your views here.
def para_parse(request):
    print 'request:{}'.format(request)
    data_dict={'activity':'open','filepath':'/data1/mingmingzhao/dlib/python_examples/cv2drawlib1.py','content':'default','text_style':'vim'} #返回给客户端的数据
    data_dict1={'face_num':'u need post imageurl to me'}
    if request.method=="POST":
        print('request_post:{}'.format(request.POST)) #<查看客户端发来的请求内容
        #return JsonResponse(data_post) #通过 django内置的Json格式
        return data_dict #通过 django内置的Json格式
    elif request.method=="GET":
        title_list=[u'activity',u'filepath',u'content',u'text_style']
        for title in title_list:
            if title in request.GET:
                
                data_dict[title]=request.GET[title]
        #if u'activity' in request.GET:
        #    activity=request.GET[u'activity']
        #if u'filepath' in request.GET:
        #    filepath=request.GET[u'filepath']
        #if u'url' in request.GET: 
        #    q = request.GET[u'url']
        #    img_url=q
        #    boxstr,img_url_result,face_num=has_object(img_url,obj_str)
        #    data_dict['boxstr']=boxstr
        #    data_dict['img_result']=img_url_result
        #    data_dict['face_num']=face_num
        #return JsonResponse(data_post)
        return data_dict
    else:
        #return JsonResponse({'info':'u send any information!'})
        return {'info':'u send any information!'}
def savefilecontent(filepath,content):
    file_object = open(filepath, 'w')
    file_object.write(content)
    file_object.close()
def highlight_python(python_scripts,activity='open',text_style='vim'):
    #['manni', 'igor', 'lovelace', 'xcode', 'vim', 'autumn', 'abap', 'vs', 'rrt', 'native', 'perldoc', 'borland', 'arduino', 'tango', 'emacs', 'friendly', 'monokai', 'paraiso-dark', 'colorful', 'murphy', 'bw', 'pastie', 'rainbow_dash', 'algol_nu', 'paraiso-light', 'trac', 'default', 'algol', 'fruity']
   
    formatter = HtmlFormatter(encoding='utf-8', style = text_style, linenos = True)
    print STYLE_MAP.keys()
    code=''
    if activity=='run':
        #formatter = HtmlFormatter(encoding='utf-8', style = 'manni', linenos = True)
        p = re.compile(r'<img(.{10,100}) />')
        splitlist=p.split(python_scripts)
        findlist =p.findall(python_scripts)
        for str_ in splitlist:
            if str_ not in findlist:
                 code+=highlight(str_,PythonLexer(),formatter)
            else:
                 code+='<img '+str_+" style='border:3px solid #aaaaaa;'"+'/>'
            print 'split:{},{}'.format(str_,len(p.split(python_scripts)))
        for str_ in findlist:
            print 'findall:{},{}'.format(str_,len(p.findall(python_scripts)))
        #code = highlight(python_scripts, PythonLexer(), formatter)
        #code = highlight(python_scripts, PythonLexer(), formatter)
    else: 
        code = highlight(python_scripts, PythonLexer(), formatter)
        #print code
        #print css
    css = formatter.get_style_defs('.highlight') 
    return code,css
def run(request):
    filepath=''
    data_dict=para_parse(request)
    activity=data_dict['activity']
    text_style=data_dict['text_style']
    print data_dict
    # open script
    filepath=data_dict['filepath']
    content=data_dict['content']
    if data_dict['activity'] == 'open':
        #command='cat /data1/mingmingzhao/dlib/python_examples/cv2drawlib.py'
        command='cat {}'.format(data_dict['filepath'])
    # save script
    if data_dict['activity'] == 'save':
        #command='cat /data1/mingmingzhao/dlib/python_examples/cv2drawlib.py'
        #command="echo  > {}".format(data_dict['content'],data_dict['filepath'])
        savefilecontent(data_dict['filepath'],data_dict['content'])
        command='cat {}'.format(data_dict['filepath'])
    # run script
    if data_dict['activity'] == 'run':
        #command='python /data1/mingmingzhao/dlib/python_examples/cv2drawlib.py'
        command='python {}'.format(data_dict['filepath'])
    # del scrpt
    #command='python /data1/mingmingzhao/dlib/python_examples/cv2drawlib.py'
    #tmp = os.popen(command).readlines()
    print ("command:{}".format(command))
    status,tmp=commands.getstatusoutput(command)
    print 'status:{}'.format(status)
    print 'output:{}'.format(tmp)
    page = PyH('read code page')
    page.addJS('http://192.168.7.37:8393/static/ckeditor/ckeditor/ckeditor.js')
    #page.addJS('jquery.js')
    html=''
    html+='status:{}\noutput:'.format(status)
   
    for tmp_ in tmp:
        #html+=tmp_.replace('\n','<br />')
        html+=tmp_
    html_str=html
    #html,css=highlight_python(html)
    html,css=highlight_python(html_str,activity,text_style)
    if activity=='run':
        content=tmp
    if activity=="open":
        content=tmp
    page<<head('<style>'+css+'</style>')
    mainform=page<<form(name='myform1')
    mainform<<h3('test form')
    mainform<<input(type='text', name='filepath', value=filepath,id='fd1')
    #mainform<<input(type='text', name='content' , value=content,id='fd')
    #mainform<<"<textarea class='ckeditor' cols='80' id='content' name='content' rows='1'>"+content+"</textarea>"
    mainform<<"<textarea  cols='80' id='content' name='content' rows='1'>"+content+"</textarea>"
    #mainform<<textarea(class='ckeditor',name='content',cols='80',rows='10')
    #mainform<<"<script>var editor=CKEDITOR.replace( 'content_' , {uiColor: '#9AB8F3'});editor.setData('"+content+"');function save(){editor.updateElement();var editor_data = CKEDITOR.instances.content.getData();if(editor_data==null||editor_data==''){alert('any content'); }else{if(confirm(editor_data)){document.getElementById('fd').value=editor_data;document.myform1.submit();}}}</script>"
    mainform<<"<script>CKEDITOR.replace('content',{height:800,startupMode:'source',extraPlugins:'codesnippet'});function save(){var editor_data = CKEDITOR.instances.content.getData();if(editor_data==null||editor_data==''){alert('any content'); }else{if(1){document.myform1.submit();}}}</script>"
    #mainform<<"<script>CKEDITOR.replace('content',{height:800,startupMode:'wysiwyg'});function save(){var editor_data = CKEDITOR.instances.content.getData();if(editor_data==null||editor_data==''){alert('any content'); }else{if(1){document.myform1.submit();}}}</script>"
    #mainform<<"<script>function run(){var psel = document.getElementById('fd');alert('get value:' + psel.value+' ,'+$('#fd').val());psel.value = '123';alert('value:' + psel.value);}</script>"
    mainform<<input(type='submit',name='activity',value='open')
    mainform<<input(type='submit',name='activity',value='run')
    mainform<<input(type='submit',name='activity',value='save',onclick='save()')
    text_style_list=['manni', 'igor', 'lovelace', 'xcode', 'vim', 'autumn', 'abap', 'vs', 'rrt', 'native', 'perldoc', 'borland', 'arduino', 'tango', 'emacs', 'friendly', 'monokai', 'paraiso-dark', 'colorful', 'murphy', 'bw', 'pastie', 'rainbow_dash', 'algol_nu', 'paraiso-light', 'trac', 'default', 'algol', 'fruity']
    mainselect=mainform<<select('aaa',name='text_style')
    #selected = "selected"
    for style_ in text_style_list:
        if style_==text_style:
            mainselect<<option(style_,value=style_,selected='selected')
        else:
            mainselect<<option(style_,value=style_)
    # write the ckeditor
    #page<<textarea(name='editor1')
    #page<<"<textarea name='editor1'>"+html+"</textarea>"
    #page<<"<script>CKEDITOR.replace( 'editor1' , {uiColor: '#9AB8F3'});</script>" 
    #if data_dict['activity']=='run':
    page<<html
    #elif data_dict['activity']=='open':
    #    page<<html

    ret_str=page.render()
    #print ret_str
    return HttpResponse(ret_str)
def ckeditor_test():
    """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>CKEditor</title>
            <script src="//cdn.ckeditor.com/4.5.9/standard/ckeditor.js"></script>
        </head>
        <body>
            <textarea name="editor1"></textarea>
            <script>
                CKEDITOR.replace( 'editor1' , {uiColor: '#9AB8F3'});
            </script>
        </body>
    </html>
    """
