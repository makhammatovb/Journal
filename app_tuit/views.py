from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail

from .models import (
    RequirementsInformation,
    Requirements,
    FAQ,
    Contacts,
    Categories,
    Publications,
    Papers,
    PapersInformation,
    Reviewers
)

from .serializers import (
    RequirementsSerializer,
    RequirementsInformationSerializer,
    FAQSerializer, FAQGETSerializer,
    ContactSerializer,
    CategoriesSerializer,
    PublicationsSerializer, PublicationsGETSerializer,
    PapersSerializer,
    PapersInformationSerializer, PapersInformationGETSerializer,
    ReviewSerializer,
    MenuSerializer
)

from .filters import (
    RequirementsFilter,
    FAQFilter,
    PublicationsFilter
)
from .permissions import IsAuthorOrReadOnly, IsSuperUser


# Create your views here.
class RequirementsViewSet(viewsets.ModelViewSet):
    queryset = Requirements.objects.all()
    serializer_class = RequirementsSerializer
    permission_classes = [IsSuperUser]


class RequirementsInformationViewSet(viewsets.ModelViewSet):
    queryset = RequirementsInformation.objects.all()
    serializer_class = RequirementsInformationSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RequirementsFilter
    permission_classes = [IsSuperUser]


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = FAQFilter
    permission_classes = [IsSuperUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FAQGETSerializer
        return FAQSerializer


@api_view(['POST'])
def send_email(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            try:
                send_mail(
                    subject=serializer.validated_data['subject'],
                    message=serializer.validated_data['message'],
                    from_email="fmetube01@gmail.com",
                    recipient_list=[serializer.validated_data['email']],
                )
                contact_info = Contacts(
                    email=serializer.validated_data['email'],
                    first_name=serializer.validated_data['first_name'],
                    message=serializer.validated_data['message']
                )
                contact_info.save()
                return Response(
                    {'message': 'Email sent successfully'},
                    status=200
                )
            except Exception as e:
                return Response(
                    {'message': f'Failed to send email: {str(e)}'},
                    status=500
                )
        else:
            return Response(
                {'message': 'Invalid data', 'errors': serializer.errors},
                status=400
            )
    return Response(
        {'message': 'Method not allowed'},
        status=405
    )


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsSuperUser]


class PublicationsViewSet(viewsets.ModelViewSet):
    queryset = Publications.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicationsFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PublicationsGETSerializer
        return PublicationsSerializer


class PapersViewSet(viewsets.ModelViewSet):
    queryset = Papers.objects.all()
    serializer_class = PapersSerializer
    permission_classes = [IsAuthorOrReadOnly]


class PapersInformationViewSet(viewsets.ModelViewSet):
    queryset = PapersInformation.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PapersInformationGETSerializer
        return PapersInformationSerializer


class ReviewersViewSet(viewsets.ModelViewSet):
    queryset = Reviewers.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]


class MenuViewSet(viewsets.ModelViewSet):

    def list(self, request):
        last_papers = PapersInformation.objects.all().order_by('-pub_date')[:-5]
        most_read = PapersInformation.objects.all().order_by('-views')[:-5]

        last_papers_serializer = MenuSerializer(last_papers, many=True, context={'request': request})
        most_read_papers_serializer = MenuSerializer(most_read, many=True, context={'request': request})

        return Response(
            data={'last_papers': last_papers_serializer.data,
                  'most_read': most_read_papers_serializer.data,},
            status=200)