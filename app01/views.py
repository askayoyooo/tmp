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

        items_count_per_page = 5
        total_count = models.Classes.objects.all().count()
        base_url = "classes.html"
        from app01.utils.page import PagerHelper
        obj = PagerHelper(total_count, current_page, items_count_per_page, base_url)
        pager_str = obj.pager_str()
        class_list = models.Classes.objects.all()[obj.page_start:obj.page_end]

        from django.utils.safestring import mark_safe
        return render(request,
                      'classes.html',
                      {'user': user, 'class_list': class_list, 'pager_str': mark_safe(pager_str)}) #可以在前端模板变量后|safe




        





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
