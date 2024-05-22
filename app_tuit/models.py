from django.db import models
from users.models import CustomUser
from config import settings
from ckeditor.fields import RichTextField

# Create your models here.
class Requirements(models.Model):
    req_list = models.CharField(max_length=255)

    def __str__(self):
        return self.req_list

    class Meta:
        db_table = 'requirements_list'
        verbose_name = 'Requirement List'
        verbose_name_plural = 'Requirements List'



class RequirementsInformation(models.Model):
    requirement = models.ForeignKey(Requirements, on_delete=models.CASCADE)
    req_title = models.CharField(max_length=255)
    req_description = models.TextField()

    def __str__(self):
        return self.req_title

    class Meta:
        db_table = 'requirements_information'
        verbose_name = 'Requirement Information'
        verbose_name_plural = 'Requirements Information'


class FAQ(models.Model):
    question_uz = models.CharField(max_length=255)
    answer_uz = models.CharField(max_length=255)
    question_en = models.CharField(max_length=255, null=True, blank=True)
    answer_en = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.question_uz} - {self.answer_uz}"

    class Meta:
        db_table = 'faq'
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'


class Contacts(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    message = models.TextField()

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class SendEmail(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    message = models.TextField()

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'send_email'
        verbose_name = 'Send Email'
        verbose_name_plural = 'Send Emails'


class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Publications(models.Model):
    image = models.ImageField(upload_to='publications/')
    description_uz = models.CharField(max_length=255)
    description_en = models.CharField(max_length=255, null=True, blank=True)
    file_uz = models.FileField(upload_to='publications/')
    file_en = models.FileField(upload_to='publications/', null=True, blank=True)
    category = models.ManyToManyField(Categories, related_name='publications')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description_uz} - {self.description_en}"

    class Meta:
        db_table = 'publications'
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'


class Papers(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'papers'
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'


class PapersInformation(models.Model):
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    reviews = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reviews')
    description_uz = models.TextField()
    description_en = models.TextField(null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    article_uz = models.TextField()
    article_en = models.TextField()
    file_uz = models.FileField(upload_to='papers/uz')
    file_en = models.FileField(upload_to='papers/en', null=True, blank=True)
    references_count = models.PositiveIntegerField(default=0)
    references = RichTextField(null=True, blank=True)
    papers = models.ForeignKey(Papers, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name_uz} - {self.name_en}"

    class Meta:
        db_table = 'papers_information'
        verbose_name = 'Papers Information'


class Reviewers(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    paper = models.ForeignKey(PapersInformation, on_delete=models.CASCADE)
    reviewer = models.ManyToManyField(CustomUser, related_name='reviewers')
    review_text = models.TextField()
    review_file = models.FileField(upload_to='review/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review

    class Meta:
        db_table = 'reviewers'
        verbose_name = 'Reviewer'