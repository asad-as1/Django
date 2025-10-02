from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Blog
from django.contrib.auth.models import User
import json

def index(request):
    blogs = Blog.objects.all()
    return render(request, "core/index.html", {"blogs": blogs})

@csrf_exempt
def blogs(request):
    if request.method == "GET":
        blogs = Blog.objects.all().values("id", "title", "content", "author__username", "created_at")
        return JsonResponse(list(blogs), safe=False)

    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        try:
            author = User.objects.first()  
            if not author:
                return JsonResponse({"error": "No users found. Create a user first."}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=400)
        
        blog = Blog.objects.create(
            title=data.get("title"),
            content=data.get("content"),
            author=author
        )
        return JsonResponse({"message": "Blog created", "id": blog.id})

    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Blog not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "author": blog.author.username,
            "created_at": blog.created_at
        })

    elif request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        blog.title = data.get("title", blog.title)
        blog.content = data.get("content", blog.content)
        blog.save()
        return JsonResponse({"message": "Blog updated"})

    elif request.method == "DELETE":
        blog.delete()
        return JsonResponse({"message": "Blog deleted"})

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])
