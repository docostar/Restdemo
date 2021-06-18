from django.urls import path, include
from .views import article_list,article_details,ArticleAPIView,ArticleDetails,GenericAPIView,GenericAPIDetailView,ArticleViewSet, GenericViewSet
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('article', ArticleViewSet,basename='article')
router.register('generic',GenericViewSet)

urlpatterns = [

    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>',include(router.urls)),
    path('',ArticleAPIView.as_view(),name="Article_API_View" ),
    path('detail/<int:id>',ArticleDetails.as_view(),name="Article_Detail_View" ),
    path('article',article_list,name="Article_list" ),
    path('dt/<int:pk>',article_details,name="Article_Details" ),
    path('generic',GenericAPIView.as_view(),name="Genric_API_View_all" ),
    path('generic/<int:id>',GenericAPIDetailView.as_view(),name="Generic_Article"),

    ]