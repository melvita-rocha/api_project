from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import viewsets 
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action


from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.paginator import Paginator


from .models import *
from .serializers import PersonSerializer, LoginSerializer, RegisterAPISerializer

# Create your views here.

@api_view(['GET', 'POST'])
def index(request):
    courses = {
        'course_name': 'Python',
        'learn': [
            'flask', 'Django', 'Tornado', 'FastApi',
        ],
        'course_provider': 'Scaler'
    }
    if request.method == 'GET':
        print("You hit a GET method")
        return Response(courses)   
    elif request.method == 'POST':
        data = request.data
        print("You hit a POST method")
        return Response(courses)


@api_view(['POST'])
def login(request):
    data = request.data 
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message': 'success'})
    
    return Response(serializer.errors)


       
       






@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.all()
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data 
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    elif request.method == 'PATCH':
        data = request.data 
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'Data deleted successfully'})




# Using the class method , APIView
class Employee(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # print(request.user)
        objs = Person.objects.all()
        page = request.GET.get('page', 1)
        page_size = 3
        try:
            paginator = Paginator(objs, page_size)
            print(paginator.page(page))
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Invalid page number'
            })
        serializer = PersonSerializer(paginator.page(page), many=True)
        return Response(serializer.data)

    def post(self, request): 
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def put(self, request):
        data = request.data
        objs = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(objs, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        objs = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(objs, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        objs = Person.objects.get(id=data['id'])
        objs.delete()
        return Response({'message': 'Data deleted successfully'})




class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    http_method_names = ['get', 'post']

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(first_name__startswith=search)
        serializer = PersonSerializer(queryset, many=True)
        return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['POST']) 
    def send_mail_to_person(self, request, pk):
        # print(pk)
        obj = Person.objects.get(pk=pk)
        serializer = PersonSerializer(obj)
        return Response({
            'status': True,
            'message': 'email sent successfully',
            'data': serializer.data
        })




class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterAPISerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors,
            }, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'status': True, 'message': 'User created'}, status.HTTP_201_CREATED)



class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors,
            }, status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'invalid credentials',
            }, status.HTTP_400_BAD_REQUEST)


        token, _ = Token.objects.get_or_create(user=user)

        return Response({'status': True, 
        'message': 'User login', 'token': str(token)}, status.HTTP_201_CREATED)








