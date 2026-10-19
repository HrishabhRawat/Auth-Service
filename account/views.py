from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerilizers
from django.contrib.auth import authenticate
from account.renderers import UserRenderer

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':"Registration Successfull "}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format= None):
        serializer = UserLoginSerilizers(data = request.data)
        if serializer.is_valid(raise_exception= True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password =password)
            if user is not None:
                return Response({'msg':'User logged in Sucessfullly'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Vaild']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    


