from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (UserRegistrationSerializer, 
                          UserLoginSerilizers, 
                          UserProfileSerializer, 
                          UserPasswordChangeSerializer, 
                          SendUserPasswordEmailSerializer, 
                          UserResetPasswordSerializer)
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate tokens Manually
def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token ,'msg':"Registration Successfull "}, status=status.HTTP_201_CREATED)
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
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'User logged in Sucessfullly'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Vaild']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


    
class UserPasswordchangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        serializer = UserPasswordChangeSerializer(data = request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class SendUserPasswordEmailview(APIView):
    renderer_classes = [UserRenderer]
    def post(self, requeset, format = None):
        serializer = SendUserPasswordEmailSerializer(data = requeset.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link send. Please check the your email'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format = None):
        serializer = UserResetPasswordSerializer(data = request.data, context = {'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        










