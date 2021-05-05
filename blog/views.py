from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.

def index(request):
    blogs = Blogpost.objects.all()
    bloglist = [];
    for blog in blogs:
        bloglist.append(blog)

    return render(request,'blog/index.html',{'blogs':bloglist})

def blogPost(request,myid):
    postid = myid
    cur = Blogpost.objects.filter(post_id=postid)[0]
    try:
        prev =  Blogpost.objects.filter(post_id=postid - 1)[0]
    except Exception as e:
        prev=False
        pass
    try:
        nex= Blogpost.objects.filter(post_id=postid + 1)[0]
    except Exception as e:
        nex = False
        pass

    return render(request,'blog/blogPost.html',{'current':cur,'previous': prev,'next': nex })
