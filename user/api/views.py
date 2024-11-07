from django.shortcuts import render
from user.api.serializers import RegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
# Create your views here.

@api_view(["POST",])
def logout_user(request):
    if request.method=="POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(["POST",])
def register_user(request):
    if request.method=="POST":
        serializer = RegistrationSerializer(data=request.data)
        data ={}
        if serializer.is_valid():
            account = serializer.save()
            token, created=Token.objects.get_or_create(user=account)
            data["token"]=token.key
            data["username"]=account.username
            data["email"]=account.email
            data["response"]="Registration Successfull"
        else:
            data=serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)
            
            