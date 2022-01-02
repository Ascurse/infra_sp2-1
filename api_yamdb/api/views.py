import uuid
from django.conf import settings
from django.db.models import Avg
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter

from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
)
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin
)
from django_filters.rest_framework import DjangoFilterBackend

from .filters import GenresFilter, CategoriesFilter, TitlesFilter
from .models import Category, Genre, Title, User, Review, Comment
from .serializers import (
    CategorySerializer, GenreSerializer, TitleReadSerializer,
    TitleCreateSerializer, UserSerializer, CommentSerializer,
    ReviewSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsModerator, IsSuperuser, IsAuthorOrReadOnly, IsAdmin
)


class CustomViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    pass


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if user.exist():
            return Response(
                {'message': 'User already registered'},
                status=status.HTTP_200_OK)
        confirmation_code = str(uuid.uuid1()).split('-')[0]
        username = email.split("@")[0]
        data = {
            'username': username,
            'email': email,
            'confirmation_code': confirmation_code
        }
        send_mail(
            subject='Registration',
            message=f'Hello! Your confirm code is {confirmation_code}',
            from_email=settings.FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Registration done',
             'data': data},
            status=status.HTTP_201_CREATED)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        token = AccessToken().for_user(user)
        if user.confirmation_code != request.data.get('confirmation_code'):
            response = {'message': 'Incorrect confirmation_code'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'access': str(token)}
        return Response(response, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperuser)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'username'

    @action(
        detail=False, permission_classes=(IsAuthenticated, ),
        methods=['get', 'patch'], url_path='me',
    )
    def update_self(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name', 'year')
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    search_fields = ('name', 'year')
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    search_fields = ('name',)
    filterset_class = CategoriesFilter
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    search_fields = ('name',)
    filterset_class = GenresFilter
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly | IsModerator | IsAdmin | IsSuperuser
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly | IsModerator | IsAdmin | IsSuperuser
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
