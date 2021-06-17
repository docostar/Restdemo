from django.urls import path
from . import views

urlpatterns = [
    path('',views.article_list,name="Article_list" ),
    path('detail/<int:pk>/',views.article_details,name="Article_Details" )
]
