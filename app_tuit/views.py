from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from config import settings
from django.utils import timezone
from datetime import timedelta

from .models import (
    RequirementsInformation,
    Requirements,
    FAQ,
    Contacts,
    SendEmail,
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
    SendEmailSerializer,
    ContactsSerializer,
    CategoriesSerializer,
    PublicationsSerializer, PublicationsGETSerializer,
    PapersSerializer,
    PapersInformationSerializer, PapersInformationGETSerializer,
    ReviewSerializer,
    LastEditionSerializer, LastPaperSerializer, MostReadSerializer
)

from .filters import (
    RequirementsFilter,
    FAQFilter,
    PublicationsFilter,
    PapersInfoFilter,
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
        serializer = SendEmailSerializer(data=request.data)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contacts_view(request):
    serializer = ContactsSerializer(data=request.data)
    if serializer.is_valid():
        first_name = serializer.validated_data.get('first_name')
        email = serializer.validated_data.get('email')
        message = serializer.validated_data.get('message')


        subject = 'New Contact Message'
        email_message = (
            f"First Name: {first_name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )
        from_email = email
        recipient_list = [settings.EMAIL_HOST_USER]

        send_mail(subject, email_message, from_email, recipient_list)

        return Response({'message': 'Message sent successfully'}, status=200)
    return Response(serializer.errors, status=400)


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = PapersInfoFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        view_cookie_key = f'viewed_{instance.id}'
        view_cookie = request.COOKIES.get(view_cookie_key)
        if not view_cookie:
            instance.views += 1
            instance.save()
            response = Response(self.get_serializer(instance).data)
            expires = timezone.now() + timedelta(seconds=10)
            response.set_cookie(view_cookie_key, 'true', expires=expires)
        else:
            response = Response(self.get_serializer(instance).data)
        return response


class PapersInformationViewSet(viewsets.ModelViewSet):
    queryset = PapersInformation.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        view_cookie_key = f'viewed_{instance.id}'
        view_cookie = request.COOKIES.get(view_cookie_key)
        if not view_cookie:
            instance.views += 1
            instance.save()
            response = Response(self.get_serializer(instance).data)
            expires = timezone.now() + timedelta(seconds=10)
            response.set_cookie(view_cookie_key, 'true', expires=expires)
        else:
            response = Response(self.get_serializer(instance).data)
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PapersInformationGETSerializer
        return PapersInformationSerializer


@api_view(['GET'])
def papers_menu_view(request):
    latest_papers = PapersInformation.objects.all().order_by('-pub_date')[:5]
    most_read = PapersInformation.objects.all().order_by('-views')[:5]
    last_edition = PapersInformation.objects.all().order_by('-pub_date')[:1]

    latest_papers_serializer = LastPaperSerializer(latest_papers, many=True, context={'request': request})
    most_read_serializer = MostReadSerializer(most_read, many=True, context={'request': request})
    last_edition_serializer = LastEditionSerializer(last_edition, many=True, context={'request': request})

    return Response({
        'last_edition': last_edition_serializer.data,
        'latest_papers': latest_papers_serializer.data,
        'most_read': most_read_serializer.data,
    }, status=200)


@api_view(['GET'])
def reviewers(request, id):
    paperinformation = PapersInformationSerializer(PapersInformation.objects.get(id=id)).data
    reviews = ReviewSerializer(Reviewers.objects.filter(paper=id), many=True).data
    return Response(
        {
            'reviews': reviews,
            'paper_infromation': paperinformation
        }
    )