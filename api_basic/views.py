from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()

    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class GenericAPIDetailView(generics.GenericAPIView,mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()

    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class ArticleAPIView(APIView):

    def get(self, requset):
        articles = Article.objects.all()
        serializer = ArticleSerializers(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        searializer = ArticleSerializers(data=request.data)
        if searializer.is_valid():
            searializer.save()
            return Response(searializer.data, status=status.HTTP_201_CREATED)

        return Response(searializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get_object(self, id):
        try:
            return Article.objects.get(pk=id)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, requset, id):
        article = self.get_object(id)
        serializer = ArticleSerializers(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_object(id)
        searializer = ArticleSerializers(article, data=request.data)

        if searializer.is_valid():
            searializer.save()
            return Response(searializer.data)

        return Response(searializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @csrf_exempt
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializers(articles, many=True)
        # return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data=JSONParser().parse(request)
        # searializer=ArticleSerializers(data=data)
        searializer = ArticleSerializers(data=request.data)
        if searializer.is_valid():
            searializer.save()
            # return JsonResponse(searializer.data,status=201)
            return Response(searializer.data, status=status.HTTP_201_CREATED)

        # return JsonResponse(searializer.errors,status=400)
        return Response(searializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def article_details(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        # return HttpResponse(status=404)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializers(article)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data=JSONParser().parse(request)
        searializer = ArticleSerializers(article, data=request.data)

        if searializer.is_valid():
            searializer.save()
            # return JsonResponse(searializer.data)
            return Response(searializer.data)

        # return JsonResponse(searializer.errors, status=400)
        return Response(searializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        # return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)
