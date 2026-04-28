from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import base64
import json
from PIL import Image
import io

FACE_RECOGNITION_AVAILABLE = False
try:
    import importlib
    importlib.util.find_spec('face_recognition')
    FACE_RECOGNITION_AVAILABLE = True
except Exception:
    FACE_RECOGNITION_AVAILABLE = False
from .models import CustomUser, FaceLogin
from .serializers import UserSerializer, RegisterSerializer


class RegisterView(CreateView):
    model = CustomUser
    template_name = 'accounts/register.html'
    fields = ['username', 'email', 'password', 'phone', 'role']
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
        return super().form_valid(form)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Username yoki parol noto\'g\'ri'}, status=status.HTTP_401_UNAUTHORIZED)


class FaceRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not FACE_RECOGNITION_AVAILABLE:
            return Response({'error': 'Yuz aniqlash tizimi mavjud emas'}, status=400)
        image_data = request.data.get('image')
        if not image_data:
            return Response({'error': 'Rasm yuklanmadi'}, status=400)
        try:
            image_data = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            encodings = face_recognition.face_encodings(image_array)
            if not encodings:
                return Response({'error': 'Yuz topilmadi'}, status=400)
            encoding = encodings[0].tolist()
            request.user.face_encoding = json.dumps(encoding)
            request.user.save()
            return Response({'success': 'Yuz muvaffaqiyatli ro\'yxatdan o\'tdi'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class FaceLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not FACE_RECOGNITION_AVAILABLE:
            return Response({'error': 'Yuz aniqlash tizimi mavjud emas'}, status=400)
        image_data = request.data.get('image')
        if not image_data:
            return Response({'error': 'Rasm yuklanmadi'}, status=400)
        try:
            image_data = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            unknown_encoding = face_recognition.face_encodings(image_array)
            if not unknown_encoding:
                return Response({'error': 'Yuz topilmadi'}, status=400)
            unknown_encoding = unknown_encoding[0]
            users = CustomUser.objects.exclude(face_encoding__isnull=True).exclude(face_encoding='')
            for user in users:
                known_encoding = np.array(json.loads(user.face_encoding))
                results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.6)
                if results[0]:
                    FaceLogin.objects.create(user=user, success=True)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': UserSerializer(user).data
                    })
            return Response({'error': 'Yuz tanilmadi'}, status=401)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)