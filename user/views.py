from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import logging
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.generics import ListCreateAPIView
from .common import err_msg
from .rbac import IsManager, IsAdmin
# Create your views here.

logger = logging.getLogger("django")

def index(request):
    return JsonResponse({"message": "Welcome !"})

# User registration view
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                # user.save()
                # Success part of the code # Single line dictionary for response with info logs
                # UserProfileSerializer(user, context=self.get_serializer_context()).data, }

                res_data = {"success": True, "message": "Registration Successful, Please Login",
                            "data": {"id": user.id, "username": user.username}}
                logger.info(f"Successfully created user {user}")
                return Response(res_data, status=status.HTTP_201_CREATED)
            else:
                # Error handling part of the code # Single line dictionary for response with error logs
                err_data = str(serializer.errors)
                res_data = {"success": False, "message": "Something weBnt wrong", "data": {"error": err_data}}
                logger.warning(err_data)
                return Response(res_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            # Exception handling part of the code # Single line dictionary for response with error logs
            logger.error(ex)
            res_data = {"success": False, "message": " Something went wrong !", "data": {"error": str(ex)}, }
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Logout view for logged users
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                blacklisted = token.blacklist()
                res_data = {"success": True, "message": "Logout Successfully !", "data": {}}
                return Response(res_data, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"message": "Invalid token ", "success": False, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            res_data = {"success": False, "message": "Something went wrong !", "data": {"error": str(ex)}, }
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    # Identify which user is to be updated using Request
    def get_object(self):
        user = self.request.user
        if user.is_deleted:
            return None
        return user

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            # Check for user is exist
            if user:
                serializer = self.get_serializer(user)
                return Response({'success': True, 'message': 'User details fetched successfully', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response({'success': False, 'message': 'User Not Found', 'data': {}},
                status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'success': True, 'message': 'User details updated successfully', 'data': serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.is_deleted = True
            user.save()
            return Response({'success': True, 'message': 'User deleted successfully', 'data': {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# User change password
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.update(request.user, serializer.validated_data)
                return Response({'success': True, 'message': 'Password updated successfully', 'data': {}},
                                status=status.HTTP_200_OK)

            res_data = {"error": err_msg(serializer.errors)}
            return Response({'success': False, 'message': 'Failed to updated Password', 'data': res_data},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_400_BAD_REQUEST)
        



# List and create users
class UserListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,IsManager | IsAdmin)
    queryset = User.objects.all()
    serializer_class = UserSerializer