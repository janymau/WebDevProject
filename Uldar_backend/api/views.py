from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework import mixins
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *
from .serializers import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_classes = [UserSerializer, RegisterSerializer]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return RegisterSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UpdateUserSerializer
    lookup_field = 'username'


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    lookup_field = 'username'


class QuestionListView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def question_detail(request, pk):
    try:
        question = Question.objects.get(id=pk)
    except Question.DoesNotExist as e:
        return Response({'message': str(e)}, status=404)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = QuestionSerializer(instance=question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        question.delete()
        return Response({'message': 'deleted'}, status=204)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def question_messages(request, pk):
    try:
        question = Question.objects.get(id=pk)
    except Question.DoesNotExist as e:
        return Response({'message': str(e)}, status=404)

    if request.method == 'GET':
        messages = question.message_set.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, question=question)
        return Response(serializer.data)


# class TagListView(generics.ListCreateAPIView):
#     queryset = Tag.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = TagSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def tag_list(request):
    if request.method == 'GET':
        companies = Tag.objects.all()
        serializer = TagSerializer(companies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TagDetailView(generics.RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    lookup_field = 'name'
    serializer_class = TagSerializer
