from django.shortcuts import render,HttpResponse, redirect
from django import views
from app01 import models
from django.utils.decorators import method_decorator
# Create your views here.
# http://ccbv.co.uk/


def auth(func):
    def inner(request, *args, **kwargs):
        print(type(request.session))
        is_login = request.session['is_login']
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('login.html')
    return inner


class Login(views.View):

    def dispatch(self, request, *args, **kwargs):
        ret = super(Login, self).dispatch(request, *args, **kwargs)
        return ret

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'message': ''})

    def post(self, request, *args, **kwargs):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            request.session['user'] = user
            request.session['is_login'] = True
            rep = redirect('index.html')
            return rep
        else:
            message = "用户名或密码不正确"
            return render(request, 'login.html', {'message': message})


@method_decorator(auth, name='dispatch')
class Class(views.View):

    def dispatch(self, request, *args, **kwargs):
        ret = super(Class, self).dispatch(request, *args, **kwargs)
        return ret

    def get(self, request, *args, **kwargs):
        user = request.session['user']
        return render(request, 'addClass.html', {'user': user})

    def post(self, request):
        user = request.session['user']
        caption = request.POST.get('caption')

        if caption:
            models.Classes.objects.create(caption=caption)
            return redirect('classes.html')
        else:
            return render(request, 'classes.html', {'user': user})


def login(request):
    message =''
    # models.Administrator.objects.create(
    #     username='root',
    #     password='123456'
    # )
    # v = request.session
    # print(type(v))
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            request.session['is_login'] = True
            request.session['user'] = user
            rep = redirect('index.html')
            return rep
        else:
            message = "用户名账户密码错误!"
    obj = render(request, 'login.html', {'message': message})
    return obj






def logout(request):
    request.session.clear()
    return redirect('login.html')


@auth
def index(request):
    user = request.session['user']
    return render(request, 'index.html', {'user': user})


@auth
def handle_classes(request):
    # for i in range(300):
    #     caption = "班级"+str(i)
    #     models.Classes.objects.create(caption=caption)
    user = request.session['user']
    if request.method == "GET":
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
            #1 0, 10
            #2 10,20

        items_count_per_page = 10
        page_start = (current_page-1)*items_count_per_page
        page_end = page_start+items_count_per_page
        class_list = models.Classes.objects.all()[page_start:page_end]
        total_count = models.Classes.objects.all().count()
        v,a = divmod(total_count, items_count_per_page)
        if a!=0:
            v+=1
        pager_list = []
        if current_page == 1:
            pager_list.append('<a href="#">上一页</a>')
        else:
            pager_list.append('<a href="classes.html?p=%s">上一页</a>' % (current_page - 1))

        if v <= 11:
            pager_range_start = 1
            pager_range_end = v
        else:
            if current_page < 6:
                pager_range_start = 1
                pager_range_end = 12
            else:
                if current_page+5 < v:
                    pager_range_start = current_page - 5
                    pager_range_end = current_page + 5+1
                else:
                    pager_range_start = v - 10
                    pager_range_end = v+1
        for i in range(pager_range_start, pager_range_end):
            if i == current_page:
                pager_list.append('<a class="active" href="classes.html?p=%s">%s</a>' % (i, i))
            else:
                pager_list.append('<a href="classes.html?p=%s">%s</a>' % (i, i))
        if current_page == v:
            pager_list.append('<a href="#">下一页</a>')
        else:
            pager_list.append('<a href="classes.html?p=%s">下一页</a>' % (current_page + 1))
        pager_str = "".join(pager_list)





        from django.utils.safestring import mark_safe
        return render(request,
                      'classes.html',
                      {'user': user, 'class_list': class_list, 'pager_str': mark_safe(pager_str)}) #可以在前端模板变量后|safe


class PagerHelper():
    def __init__(self):
        pass
    def pager_str(self):
        





@auth
def handle_student(request):
    user = request.session['user']
    return render(request, 'student.html', {'user': user})


@auth
def handle_teacher(request):
    user = request.session['user']
    return render(request, 'teacher.html', {'user': user})


@auth
def handel_add_class(request):
    user = request.session['user']
    return render(request, 'addClass.html', {'user': user})



@auth
def delete_class(request):
    user = request.session['user']
    if request.method=="POST":
        class_id = request.POST.get("class_id")
        print(class_id)
        models.Classes.objects.filter(id=class_id).delete()
        return HttpResponse('OK')


@auth
def edit_class(request):
    user = request.session['user']
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        caption = request.POST.get('caption')
        models.Classes.objects.filter(id=class_id).update(caption=caption)
        return render(request, 'editClass.html', {'user': user})
