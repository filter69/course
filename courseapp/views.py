import json
import time
import traceback

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse


from courseapp.models import TCategory
from courseapp.models import Title

# Create your views here.

#渲染主界面
def home(request):
    username = request.session.get('username')
    title = Title.objects.all()
    course = TCategory.objects.filter(level=1)
    course_type = TCategory.objects.filter(level=2)
    num = int(request.GET.get('num', 1))
    pagtor = Paginator(title, per_page=5)
    if num < 1:
        num = 1
    elif num > pagtor.num_pages:#最后一页
        num = pagtor.num_pages
    num = str(num)
    page = pagtor.page(num)
    return render(request,'courseapp/index.html',{'username':username,'page':page,'titles':title,'course':course,'course_type':course_type})



def home1(request):
    username = request.session.get('username')
    id = request.GET.get('id')
    level = request.GET.get('level')
    course_type = TCategory.objects.filter(level=2)
    course = TCategory.objects.filter(level=1)
    list = []
    list1 = []
    if level =='2':
        id = int(id)
        data = TCategory.objects.filter(id=id)
        for i in data:
            list.append(i)
            pt = Title.objects.filter(cate__id=i.id)  # 查文章对象
            for i in pt:
                list1.append(i)
    else:
        id = int(id)
        data = TCategory.objects.filter(parnt_elevel=id)
        for i in data:
            list.append(i)
            pt = Title.objects.filter(cate__id=i.id)  # 查文章对象
            for i in pt:
                list1.append(i)

    num = int(request.GET.get('num', 1))
    pagtor = Paginator(list1, per_page=5)
    if num < 1:
        num = 1
    elif num > pagtor.num_pages:
        num = pagtor.num_pages
    page = pagtor.page(num)
    return render(request, 'courseapp/pythonBase.html', {'username':username,'id': id,'page': page,'level': level,
                'list1': list1,'list': list,'course':course,'course_type':course_type })


def course_add(request):
    course = TCategory.objects.filter(level=1)
    course_type = TCategory.objects.filter(level=2)
    return render(request,'courseapp/addCourse.html',{'course':course,'course_type':course_type})

#添加课程/课程分类
def course_add1(request):
    title = request.POST.get('name')
    level = request.POST.get('title')
    cate_sel = request.POST.get('cate_sel')  #获取课程名称
    try:
        level = int(level)
        #添加课程分类
        if level == 2:
            u = TCategory.objects.filter(titles=cate_sel)
            with transaction.atomic():
                category = TCategory(titles=title,level=level,parnt_elevel=u[0].id)
                category.save()
                data = TCategory.objects.get(titles=title)
                print(data,999)
                return HttpResponse('添加成功!'+str(data.id)+"!"+str(level))
        else:
            #添加课程
            with transaction.atomic():
                category = TCategory(titles=title, level=level,)
                category.save()
                data = TCategory.objects.get(titles=title)
                return HttpResponse('添加成功!'+str(data.id)+"!"+str(level))
    except:
        traceback.print_exc()
        return HttpResponse('添加失败!')

#渲染添加课程界面
def course_add_title(request):
    course = TCategory.objects.filter(level=1)
    course_type = TCategory.objects.filter(level=2)
    return render(request, 'courseapp/addArticle.html', {'course': course, 'course_type': course_type})


def my_default(t):
    if isinstance(t, Title):
        return {'id': t.id, 'title': t.title, 'content': t.content, 'publish_time': t.publish_time.strftime('%Y-%m-%d %H-%M-%S'),'count':t.count,'cate_id':t.cate_id}
    if isinstance(t, TCategory):
        return {'id': t.id, 'titles': t.titles, 'level': t.level, 'parnt_elevel': t.parnt_elevel}

#查询二级目录返回json对象
def addAritcle(request):
    course_id = request.POST.get("course")
    course = TCategory.objects.filter(parnt_elevel=course_id)
    if course:
        return JsonResponse({"course":list(course)},json_dumps_params={"default":my_default})
    return HttpResponse('error!')

#添加课程逻辑
def addAritcle_btn(request):
    title = request.POST.get("title")
    # course_sel = request.POST.get("course_sel")#所属课程
    cate_sel = request.POST.get("cate_sel")#所属课程分类
    id = TCategory.objects.filter(titles=cate_sel)
    publish_time = request.POST.get("time")
    txt = request.POST.get("txt")
    try:
        if not publish_time:
            publish_time = time.strftime("%Y-%m-%d %H:%M:%S")
        t = Title(title=title,content=txt,count=0,publish_time=publish_time,cate_id=id[0].id)
        t.save()
        data = Title.objects.filter(cate_id=id[0].id)
        if len(data)<5:
            num = 1
        else:
            if len(data)//5 == 0:
                num = int(len(data)/5)
            else:
                num = int(len(data)/5)+1
        return HttpResponse("添加成功!"+str(id[0].id)+"!"+str(id[0].level)+"!"+str(num))
    except:
        traceback.print_exc()
        return HttpResponse("添加失败!")

#删除
def delete(request):
    del_id = request.POST.get("del_id")
    id = request.POST.get("id")
    level = request.POST.get("level")
    num = request.POST.get("num")
    title = Title.objects.filter(id=del_id)
    title.delete()
    if id and level:
        print(111)
        return HttpResponse("删除成功!" + num+"!"+ id+"!"+ level)
    return HttpResponse("删除成功!" + num)

#更新文章
def update(request):
    id=request.GET.get('id')
    if isinstance(id, str):
        id = int(id)
    request.session['id'] = id
    data = Title.objects.get(id=id)#文章
    data1 = TCategory.objects.get(id=data.cate_id) #查文章的二级目录
    data2 = TCategory.objects.get(id=data1.parnt_elevel)#查文章的一级目录
    course = TCategory.objects.filter(level=1)
    course_type = TCategory.objects.filter(level=2)
    return render(request, 'courseapp/update.html', {'data1': data1,'data2': data2,'course': course, 'course_type': course_type,'data':data})

#更新逻辑
def updata_title(request):
    id = request.session.get('id')
    title = request.POST.get("title")
    cate_sel = request.POST.get("cate_sel")  # 所属课程分类
    t_id = TCategory.objects.filter(titles=cate_sel)
    publish_time = request.POST.get("time")
    txt = request.POST.get("txt")
    t = Title.objects.get(id=id)
    try:
        if not publish_time:
            publish_time = time.strftime("%Y-%m-%d %H:%M:%S")
        t.title = title
        t.content = txt
        t.publish_time = publish_time
        t.cate_id = t_id[0].id
        t.save()
        data = Title.objects.filter(cate_id=t_id[0].id)
        if len(data) < 5:
            num = 1
        else:
            if len(data) // 5 == 0:
                num = int(len(data) / 5)
            else:
                num = int(len(data) / 5) + 1
        return HttpResponse("添加成功!" + str(t_id[0].id) + "!" + str(t_id[0].level) + "!" + str(num))
    except:
        traceback.print_exc()
        return HttpResponse("添加失败!")

#排序
def read_sort(request):
    id = request.GET.get('id')
    level = request.GET.get('level')
    read = request.GET.get('read')
    time = request.GET.get('time')
    list1 = []
    if level == '2':
        id = int(id)
        data = TCategory.objects.filter(id=id)
        for i in data:
            if read == 'true':
                pt = Title.objects.filter(cate__id=i.id).order_by('count')[0:5]  # 查文章对象
            elif read == 'false':
                pt = Title.objects.filter(cate__id=i.id).order_by('-count')[0:5]
            elif time == 'true':
                pt = Title.objects.filter(cate__id=i.id).order_by('publish_time')[0:5]  # 查文章对象
            else:
                pt = Title.objects.filter(cate__id=i.id).order_by('-publish_time')[0:5]
            for i in pt:
                    list1.append(i)
        return JsonResponse({"list1": list1, 'data': list(data)}, json_dumps_params={"default": my_default})
    elif level == '1':
        id = int(id)
        data = TCategory.objects.filter(parnt_elevel=id)
        for i in data:
            if read == 'true':
                pt = Title.objects.filter(cate__id=i.id).order_by('count')[0:5]  # 查文章对象
            elif read == 'false':
                pt = Title.objects.filter(cate__id=i.id).order_by('-count')[0:5]
            elif time == 'true':
                pt = Title.objects.filter(cate__id=i.id).order_by('publish_time')[0:5]  # 查文章对象
            else:
                pt = Title.objects.filter(cate__id=i.id).order_by('-publish_time')[0:5]
            for i in pt:
                list1.append(i)
        return JsonResponse({"list1": list1, 'data': list(data)}, json_dumps_params={"default": my_default})
    else:
        if read == 'true':
            title = Title.objects.all().order_by('count')[0:5]  # 查文章对象
        elif read == 'false':
            title = Title.objects.all().order_by('-count')[0:5]
        elif time == 'true':
            title = Title.objects.all().order_by('publish_time')[0:5]  # 查文章对象
        else:
            title = Title.objects.all().order_by('-publish_time')[0:5]
        course_type = TCategory.objects.filter(level=2)
        return JsonResponse({"title": list(title),'course_type':list(course_type)}, json_dumps_params={"default": my_default})
    # return JsonResponse(list(list1),safe=False, json_dumps_params={"default": my_default1})




def home9(request):
    t_all = Title.objects.all()
    t_all2 = TCategory.objects.filter(level=2)
    paginator = Paginator(t_all,5)
    if request.method == "GET":
        present_all = paginator.page(1)
        return render(request,'courseapp/index.html',{'present_all':present_all})
    if request.is_ajax():
        page = request.GET.get("page")
        try:
            present_all = paginator.page(page)
        except PageNotAnInteger:
            present_all = paginator.page(1)
        except InvalidPage:
            present_all = paginator.page(paginator.num_pages)
        present_list = list(present_all.object_list.values())
        result = {}
    return JsonResponse({"t_all": list(t_all),"t_all2":t_all2},json_dumps_params={"default": my_default})





# Paginator
# per_page： 每页显示记录数量
# count：数据总个数
# num_pages：总页数
# page_range：总页数的索引范围，如: (1,10),(1,200)
# page：page对象  page(2)  代表第二页数据的对象
#
#
# Page
# has_next：是否有下一页
# has_previous：是否有上一页
# next_page_number：下一页页码
# previous_page_number：上一页页码
# object_list：分页之后的当前页数据列表
# number：当前页
# paginator：paginator对象，父类对象
















