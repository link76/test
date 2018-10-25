from django.shortcuts import render
from last.models import Notice


def index(request):
    notices = Notice.objects.all()
    return render(request, 'index.html', {'notices': notices})


def search_name(request):
    search_name = request.GET.get("title", "")
    title_list = Notice.objects.filter(notice_title__contains=search_name)
    return render(request, 'result.html', {"title_list": title_list})
