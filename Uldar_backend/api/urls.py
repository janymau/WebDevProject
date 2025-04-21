from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from .views import *

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view()),
    path('users/', UserView.as_view()),
    # path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/<str:username>/', UserDetailView.as_view()),
    # path('users/<int:pk>/change_password/', ChangePasswordView.as_view()),
    path('users/<str:username>/change_password/', ChangePasswordView.as_view()),

    path('questions/', QuestionListView.as_view()),
    path('questions/<int:pk>/', question_detail),
    path('questions/<int:pk>/messages/', question_messages),


    path('tags/', tag_list),
    # path('tags/<int:pk>/', TagDetailView.as_view()),
    path('tags/<str:name>/', TagDetailView.as_view()),
]
