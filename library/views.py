# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView


class AuthView(APIView):

    """
    Very simple API authentication view that logs in an user.
    """

    authentication_classes = (BasicAuthentication,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)