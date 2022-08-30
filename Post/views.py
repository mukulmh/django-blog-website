from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import auth, messages
from django.db.models import Count
from .models import Category, Featured, Like, Post

# Create your views here.

def index(request):
    top_authors = Post.objects.values('author').annotate(no_of_post=Count('id')).order_by('-no_of_post')[:3]
    top_posts = Like.objects.values('liked_on').annotate(likes=Count('liked_by')).order_by('-likes')[:3]
    for post in top_posts:
        top_post = Post.objects.all().filter(id=post['liked_on'])
        print(top_post)
    posts = Post.objects.all().order_by('-created_at')[:3]
    featured = Featured.objects.all()
    
    return render(request, 'blog/index.html',{'posts':posts,'featured':featured,'top_posts':top_posts})



def blogs(request):

    posts = Post.objects.all().order_by('-created_at')

    return render(request,'blog/blog.html',{'posts':posts})



def categories(request):

    categories = Category.objects.all()

    return render(request,'blog/categories.html',{'categories': categories})



def single(request, id):
    post = Post.objects.get(id=id)
    return render(request,'blog/single.html',{'post':post})



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
            post.save()
        categories = Category.objects.all()
        return render(request, 'blog/create.html',{'categories': categories})
    return redirect('index')



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
                return redirect('profile')
            else:
                post.title = request.POST['title']
                post.description = request.POST['description']
                post.category_id = request.POST.get('category')
                post.author_id = request.user.id
                post.save()
                return redirect('profile')
        categories = Category.objects.all()
        return render(request, 'blog/edit.html',{'categories': categories,'post':post})
    return redirect('index')



def delete(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('profile')
    return redirect('index')



def profile(request):
    if request.user.is_authenticated:

        posts = Post.objects.filter(author_id=request.user.id).all().order_by('-created_at')

        return render(request,'blog/profile.html',{'posts': posts})

    return redirect('index')
    