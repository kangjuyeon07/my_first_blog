from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post, Category

def add_params_to_context(request):
    categories = Category.objects.all()
    return {"categories": categories}


def post_list(request):
    post_list = Post.objects.all().order_by('-id')
    
    return render(request, "blog/post_list.html", {"post_list": post_list})


def post_detail(request, pk):
    post_detail = get_object_or_404(Post, id=pk)
    
    return render(request, "blog/post_detail.html", {"post_detail":post_detail})


def post_write(request):
    if request.method == "POST":
        form_data = request.POST
        
        if form_data["title"] !="" and form_data["text"]  !="":
            
            if form_data["category"] !="":
                category=Category.objects.get(id=form_data["category"])
            else:
                category = None
            
            post = Post.objects.create(
                title=form_data["title"],
                text=form_data["text"],
                category=category,
                author=request.user,
                published_date=timezone.now()
            )
            
            return redirect('post_detail', pk=post.id)
            
    categories = Category.objects.all()
            
    return render(request, "blog/post_edit.html", {"categories": categories})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("post_list")
        
    return render(request, "blog/login.html")


def user_logout(request):
    
    logout(request)
    
    return redirect("post_list")


def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user_already = User.objects.filter(username=username)
        
        if len(user_already) > 0:
            None
        else:    
            if username != "" and password !="":
                user = User.objects.create_user(username, "", password)
                login(request, user)

                return redirect("post_list")
        
    return render(request, "blog/signup.html")
    
    
def post_edit(request, pk):
    
    post = Post.objects.get(id=pk)
    
    if request.method == "POST":
        
        title=request.POST["title"]
        text=request.POST["text"]
        category_id=request.POST["category"]
        
        if category_id != "":
            category = Category.objects.get(id=category_id)
        else:
            category = None
        
        post.title = title
        post.text = text
        post.category = category
        
        post.save()
        
        return redirect("post_detail", pk=post.id)
    
    categories = Category.objects.all()
    
    return render(request,"blog/post_edit.html", {"post": post, "categories": categories})