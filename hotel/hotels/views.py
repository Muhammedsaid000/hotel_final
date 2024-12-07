from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import viewsets, generics, status
from rest_framework import permissions
from .permission import CheckOwner, CheckClient, IsOwnerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from .filters import *




class RegisterView(generics.CreateAPIView):
    serializer_class=ProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail: Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user=serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh токен отсутствует."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Ошибка обработки токена."}, status=status.HTTP_400_BAD_REQUEST)




class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CountryListApiView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer


class CountryDetailApiView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializer
    permission_classes = [IsAuthenticated, CheckOwner,IsOwnerOrReadOnly]


class HotelListViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    permission_classes = [IsAuthenticated, CheckOwner,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend,]
    filterset_class=HotelListFilter


class HotelDetailViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer
    permission_classes = [IsAuthenticated, CheckOwner, IsOwnerOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, CheckOwner,]
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RoomListFilter


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class RoomPhotosViewSet(viewsets.ModelViewSet):
    queryset = RoomPhotos.objects.all()
    serializer_class = RoomPhotosSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, CheckClient]