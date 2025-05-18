import logging
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, NoteSerializer
from .models import User, Note

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    logger.info("Registration attempt: %s", request.data.get('email'))
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info("User registered successfully: %s", serializer.data.get('email'))
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    logger.error("Registration failed: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    logger.info("Login attempt: %s", email)
    user = authenticate(request, email=email, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        logger.info("Login successful: %s", email)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'name': user.name,
            'email': user.email,
        }, status=status.HTTP_200_OK)
    logger.warning("Login failed for: %s", email)
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_notes_list_create(request):
    user = request.user
    cache_key = f"user_notes_{user.id}"
    
    if request.method == 'GET':
        logger.info("Fetching notes for: %s", user.email)
        notes_data = cache.get(cache_key)
        if notes_data:
            logger.debug("Notes served from cache for: %s", user.email)
            return Response(notes_data, status=status.HTTP_200_OK)
        notes = Note.objects.filter(user=user)
        if not notes.exists():
            logger.info("No notes found for: %s", user.email)
            return Response({"detail": "No notes found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteSerializer(notes, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 5)
        logger.debug("Notes cached for: %s", user.email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        logger.info("Creating note for: %s", user.email)
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            cache.delete(cache_key)
            logger.info("Note created for: %s", user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Note creation failed for: %s - %s", user.email, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_notes_detail(request, pk):
    user = request.user
    cache_key = f"user_notes_{user.id}"

    try:
        note = Note.objects.get(pk=pk, user=user)
    except Note.DoesNotExist:
        logger.warning("Note not found: pk=%s, user=%s", pk, user.email)
        return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(cache_key)
            logger.info("Note updated: pk=%s, user=%s", pk, user.email)
            return Response(serializer.data)
        logger.error("Note update failed: pk=%s, user=%s, errors=%s", pk, user.email, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        note.delete()
        cache.delete(cache_key)
        logger.info("Note deleted: pk=%s, user=%s", pk, user.email)
        return Response({"detail": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
