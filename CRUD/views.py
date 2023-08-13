from django.shortcuts import render

def homePage(request):
    context={}
    return render(request,'index.html',context)
