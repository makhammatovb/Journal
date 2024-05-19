from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    RequirementsViewSet,
    RequirementsInformationViewSet,
    FAQViewSet,
    send_email,
    CategoriesViewSet,
    PublicationsViewSet,
    PapersViewSet,
    PapersInformationViewSet,
    ReviewersViewSet,
    MenuViewSet
)

router = DefaultRouter()
router.register(r'requirements', RequirementsViewSet)
router.register(r'requirementsinformation', RequirementsInformationViewSet)
router.register(r'faq', FAQViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'publications', PublicationsViewSet)
router.register(r'papers', PapersViewSet)
router.register(r'papersinformation', PapersInformationViewSet)
router.register(r'reviewers', ReviewersViewSet)
router.register(r'menu', MenuViewSet, basename='menu')

urlpatterns = router.urls

urlpatterns += [
    path('send-email/', send_email, name='send_email'),
]