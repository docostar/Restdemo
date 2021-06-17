from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializers

# Create your views here.
@csrf_exempt
def article_list(request):
    if request.method=='GET':
        articles=Article.objects.all()
        serializer=ArticleSerializers(articles,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method== 'POST':
        data=JSONParser().parse(request)
        searializer=ArticleSerializers(data=data)

        if searializer.is_valid():
            searializer.save()
            return JsonResponse(searializer.data,status=201)

        return JsonResponse(searializer.errors,status=400)

@csrf_exempt
def article_details(request,pk):
    try:
        article=Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer=ArticleSerializers(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data=JSONParser().parse(request)
        searializer = ArticleSerializers(article,data=data)

        if searializer.is_valid():
            searializer.save()
            return JsonResponse(searializer.data)

        return JsonResponse(searializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)