from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.db.models import Count
from .models import Category, Comment, Featured, Like, Post

# Create your views here.

# blog main page
def index(request):
    posts = Post.objects.all()[:3]

    likes = Like.objects.values('liked_on').annotate(count=Count('liked_by')).order_by('-count')[:3]
    tops=[]
    for post in likes:
        top = Post.objects.get(id=post['liked_on'])
        tops.append(top)

    featured = Featured.objects.all()
    
    return render(request, 'blog/index.html',{'posts':posts,'featured':featured,'tops':tops,'likes':likes})


# all blogs page
def blogs(request):
    posts = Post.objects.all()

    return render(request,'blog/blog.html',{'posts':posts})


# blogs categories page
def categories(request):
    categories = Category.objects.all()
    return render(request,'blog/categories.html',{'categories':categories})


# filter posts by category
def blogFilter(request, id):
    posts = Post.objects.filter(category_id=id)
    return render(request,'blog/blog.html',{'posts':posts})


# filter single post
def single(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(comment_on=id)
    counts = Comment.objects.filter(comment_on = id).values('comment_on').annotate(count=Count('comment_by'))
    likes = Like.objects.filter(liked_on_id = id).values('liked_on').annotate(count=Count('liked_by')).order_by('-count')
    
    like = Like.objects.filter(liked_by_id=request.user.id, liked_on_id = id)
    if like.exists():
        like = 'True'
    if request.method=='POST':
        if request.user.is_authenticated:
            comment = request.POST['comment']
            query = Comment(comment=comment,comment_by=request.user, comment_on=post)
            query.save()
            return redirect('single', id = id)
    related = Post.objects.filter(category_id=post.category_id)[:3]
    return render(request,'blog/single.html',{'post':post, 'related':related, 'comments':comments, 'counts':counts, 'like':like,'likes':likes})


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
        posts = Post.objects.filter(author_id=request.user.id).all()
        return render(request,'blog/yourblog.html',{'posts':posts})
    return redirect('index')
    

# blogs of an author
def profile(request,id):
    author = User.objects.get(id=id)
    posts = Post.objects.filter(author_id=id)
    return render(request,'blog/profile.html',{'posts':posts,'author':author})
    

# filter posts by search
def searchBlog(request):
    if request.method=='POST':
        value = request.POST['s']
        posts = Post.objects.filter(title__icontains=value)
        return render(request,'blog/blog.html',{'posts':posts})
    return redirect('blogs')


# like post
def likepost(request, id):
    if request.user.is_authenticated:
        like = Like.objects.filter(liked_by_id=request.user.id, liked_on_id = id)
        if like.exists():
            like.delete()
            return redirect('single', id=id)
        click = Like(liked_by_id = request.user.id, liked_on_id = id)
        click.save()
        return redirect('single', id=id)
        

# user profile setting
def setting(request):
    return render(request,'blog/user.html')


# delete comment
def deleteComment(request, id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id = id)
        if request.user.id == comment.comment_by_id:
            pid = comment.comment_on_id
            comment.delete()
            return redirect('single', pid)
        return redirect('yourblog')
    return redirect('index')


# edit comment
def editComment(request, id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=id)
        if request.user.id == comment.comment_by_id:
            comment.comment = request.POST['comment']
            comment.save()
        return redirect('single', comment.comment_on_id)
    return redirect('index')