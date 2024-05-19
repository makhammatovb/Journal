from django.contrib import admin

from .models import (
    Requirements,
    RequirementsInformation,
    FAQ,
    Contacts,
    Categories,
    Publications,
    Papers,
    PapersInformation,
    Reviewers,
)

# Register your models here.
admin.site.register(Requirements)
admin.site.register(RequirementsInformation)
admin.site.register(FAQ)
admin.site.register(Contacts)
admin.site.register(Categories)
admin.site.register(Publications)
admin.site.register(Papers)
admin.site.register(PapersInformation)
admin.site.register(Reviewers)