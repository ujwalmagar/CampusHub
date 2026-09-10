from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from students.models import Student
from django.db import transaction

@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):
    """
    Creates a User and a linked Student profile atomically.
    Follows docs/api.md Section 15 EXACTLY.
    """
    data = request.data
    
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    
    if not password or password != password_confirm:
        return Response({"error": "Passwords must match and cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
        
    email = data.get('email')
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=status.HTTP_409_CONFLICT)
        
    try:
        with transaction.atomic():
            # Create the auth user (username can be email for simplicity, or generated)
            user = User.objects.create_user(
                username=email, 
                email=email, 
                password=password
            )
            
            # Create the student profile
            student = Student.objects.create(
                user=user,
                name=data.get('name'),
                email=email,
                phone=data.get('phone'),
                course=data.get('course')
            )
            
        return Response({
            "message": "Account created successfully",
            "user": {
                "id": user.id,
                "email": user.email
            },
            "student": {
                "id": student.student_id,
                "name": student.name,
                "course": student.course
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    Authenticates a user and logs them in via session.
    Follows docs/api.md Section 15 EXACTLY.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    # In Django, authenticate usually takes username. Since we set username=email during signup:
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        login(request, user)
        role = "STAFF" if user.is_staff else "STUDENT"
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": role
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
