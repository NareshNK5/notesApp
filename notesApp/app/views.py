from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,NoteSerializer
from .models import User,Note

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    print(request.data)
    serializer = RegisterSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        print("valid")
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')    
    password = request.data.get('password')
    print(email, password)
    
    user = authenticate(request, email=email, password=password)
    print(user)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'name': user.name,
            'email': user.email,
        }, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_notes_list_create(request):
    user = request.user
    print("user")
    if request.method == 'GET':
        print("get : user notes get")
        notes = Note.objects.filter(user=user)
        if notes.exists():
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No notes found"}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        print("post : user notes create")
        print(request.data)
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            print("valid")
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_notes_detail(request, pk):
    print("PK : ", pk)
    try:
        note = Note.objects.get(pk=pk, user=request.user)
    except Note.DoesNotExist:
        return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    print("Notes:",note)
    if request.method == 'GET':
        serializer = NoteSerializer(note)
        print("notes:",note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data, partial=True)
        print("serializer:",serializer)
        if serializer.is_valid():
            print("valid data")
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print("delete note")
        note.delete()
        return Response({"detail": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
