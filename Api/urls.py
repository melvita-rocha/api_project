from django.urls import path,include  
from App.views import index, person, login, Employee, StudentViewSet, RegisterAPI, LoginAPI 

from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'student', StudentViewSet, basename='user')
urlpatterns = router.urls


urlpatterns = [
    path('index/', index),
    path('person/', person),
    path('login/', login),
    path('employee/', Employee.as_view()),
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('login-token/', LoginAPI.as_view()),
]