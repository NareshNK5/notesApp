from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from app.views import user_register,user_login,user_notes_detail,user_notes_list_create

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('user/register/',user_register),
    path('user/login/',user_login),
    
    path('user/notes/',user_notes_list_create),
    path('user/notes/<int:pk>/',user_notes_detail),
    
]
