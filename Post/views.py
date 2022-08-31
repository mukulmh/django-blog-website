from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.db.models import Count
from .models import Category, Comment, Featured, Like, Post

# Create your views here.

# blog main page
def index(request):
    posts = Post.objects.all().order_by('-created_at')[:3]
    featured = Featured.objects.all()
    
    return render(request, 'blog/index.html',{'posts':posts,'featured':featured})


# all blogs page
def blogs(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request,'blog/blog.html',{'posts':posts})


# blogs categories page
def categories(request):
    categories = Category.objects.all()
    return render(request,'blog/categories.html',{'categories':categories})


# filter posts by category
def blogFilter(request, id):
    posts = Post.objects.filter(category_id=id).order_by('-created_at')
    return render(request,'blog/blog.html',{'posts':posts})


# filter single post
def single(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(comment_on=id).annotate(count=Count('id')).order_by()
    counts = Comment.objects.raw('SELECT id, COUNT(id) as count FROM post_comment WHERE comment_on_id = %s',[id])
    if request.method=='POST':
        if request.user.is_authenticated:
            comment = request.POST['comment']
            query = Comment(comment=comment,comment_by=request.user, comment_on=post)
            back = request.POST.get('back', '/')
            query.save()
            return redirect(back)
    related = Post.objects.filter(category_id=post.category_id).order_by('-created_at')[:3]
    return render(request,'blog/single.html',{'post':post, 'related':related, 'comments':comments, 'counts':counts})


# create post
def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['image']:
            title = request.POST['title']
            description = request.POST['description']
            category = request.POST['category']
            file = request.FILES['image']
            fs = FileSystemStorage()
            image = fs.save(file.name, file)
            author = request.user.id
            post = Post(title=title, description=description, category_id=category, author_id = author, image=image)
            print(post)
            post.save()
        categories = Category.objects.all()
        return render(request, 'blog/create.html',{'categories':categories})
    return redirect('index')


# edit post
def edit(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        if request.method == 'POST':
            if request.FILES.get('image', False):
                post.title = request.POST['title']
                post.description = request.POST['description']
                post.category_id = request.POST.get('category')
                file = request.FILES['image']
                fs = FileSystemStorage()
                post.image = fs.save(file.name, file)
                post.author_id = request.user.id
                post.save()
                return redirect('yourblog')
            else:
                post.title = request.POST['title']
                post.description = request.POST['description']
                post.category_id = request.POST.get('category')
                post.author_id = request.user.id
                post.save()
                return redirect('yourblog')
        if int(request.user.id) != int(post.author_id):
            return redirect('index')
        categories = Category.objects.all()
        return render(request, 'blog/edit.html',{'categories':categories, 'post':post})
    return redirect('index')


# delete post
def delete(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        if int(request.user.id) != int(post.author_id):
            return redirect('index')
        post.delete()
        return redirect('yourblog')
    return redirect('index')


# blog created by the logged in user
def yourBlog(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author_id=request.user.id).all().order_by('-created_at')
        return render(request,'blog/yourblog.html',{'posts':posts})
    return redirect('index')
    

# profile of an user
def profile(request,id):
    author = User.objects.get(id=id)
    posts = Post.objects.filter(author_id=id).order_by('-created_at')
    return render(request,'blog/profile.html',{'posts':posts,'author':author})
    
