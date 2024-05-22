from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    RequirementsViewSet,
    RequirementsInformationViewSet,
    FAQViewSet,
    send_email,
    contacts_view,
    CategoriesViewSet,
    PublicationsViewSet,
    PapersViewSet,
    PapersInformationViewSet,
    papers_menu_view,
    reviewers,
)

router = DefaultRouter()
router.register(r'requirements', RequirementsViewSet)
router.register(r'requirementsinformation', RequirementsInformationViewSet)
router.register(r'faq', FAQViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'publications', PublicationsViewSet)
router.register(r'papers', PapersViewSet)
router.register(r'papersinformation', PapersInformationViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('contacts/', contacts_view, name='contacts'),
    path('send-email/', send_email, name='send_email'),
    path('menu/', papers_menu_view, name='menu'),
    path('reviewers/<int:id>', reviewers, name='reviews')
]