from pyexpat.errors import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, Users


def index(request) :
    return render(request, 'index.html')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list.html', {'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.nickName = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.nickName = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form' : form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def register(request):
    if request.method =='GET':
        return render(request, 'registration/register.html')
    elif request.method == 'POST':
        userEmail = request.POST.get('userEmail', None)
        nickName = request.POST.get('nickName', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)
        photo = request.FILES['photo']
        guardianName = request.POST.get('guardianName', None)
        guardianCallNum = request.POST.get('guardianCallNum', None)
        guardianBasicMsg = request.POST.get('guardianBasicMsg', None)
        res_data = {}
        if not (userEmail and password and re_password and nickName):
            res_data['error']='아이디 또는 패스워드를 입력해주세요.'
        elif password != re_password:
            res_data['error']='비밀번호가 다릅니다.'
        else:
            users = Users(
                userEmail=userEmail,
                nickName=nickName,
                password=make_password(password),
                photo=photo,
                guardianName=guardianName,
                guardianCallNum=guardianCallNum,
                guardianBasicMsg=guardianBasicMsg
            )
            users.save()
        return render(request, 'registration/register.html', res_data)

def login(request):
    context = None
    if request.method == "POST":
        userEmail = request.POST.get('userEmail', None)
        password = request.POST.get('password', None)
        try :
            user = Users.objects.get(userEmail=userEmail)
        except Users.DoesNotExist :
            context = {'error': '계정을 확인하세요'}
        else :
            if check_password(password, user.password):
                request.session['user'] = userEmail
                return redirect('post_list')
            else :
                context = { 'error' : '패스워드를 확인하세요'}
    else :
        if 'user' in request.session:
            context = {'msg': '이미 %s 로그인 하셨습니다.' % request.session['user'] }
    return render(request, 'registration/login.html', context)

def logout(request):
    if 'user' in request.session :
        del request.session['user']
        context = {'msg' : '로그아웃 완료'}
    else :
        context = {'msg': '로그인 상태가 아닙니다!'}
    return render(request, 'registration/logout.html', context)


