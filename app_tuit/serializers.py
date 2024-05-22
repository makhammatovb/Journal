from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from users.models import CustomUser
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


class RequirementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requirements
        fields = '__all__'


class RequirementsInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequirementsInformation
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'


class FAQGETSerializer(serializers.ModelSerializer):
    question = SerializerMethodField(method_name='get_question', read_only=True)
    answer = SerializerMethodField(method_name='get_answer', read_only=True)

    class Meta:
        model = FAQ
        fields = ('question', 'answer')

    def get_question(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.question_en
            return obj.question_uz
        except:
            return obj.question_uz

    def get_answer(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.answer_en
            return obj.answer_uz
        except:
            return obj.answer_uz


class SendEmailSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=255)
    subject = serializers.CharField(max_length=255)


class ContactsSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=500)

    def create(self, validated_data):
        contact = Contacts.objects.create(**validated_data)
        return contact


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['name',]


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class ReviewerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviewers
        fields = ['first_name', 'last_name']


class PublicationsGETSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField(method_name='get_description', read_only=True)
    file = serializers.SerializerMethodField(method_name='get_file', read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Publications
        fields = ['image', 'description','description_en', 'file', 'category', 'author']
        read_only_fields = ['author']

    def get_description(self,obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.description_en
            return obj.description_uz
        except:
            return obj.description_uz

    def get_file(self, obj):
        lang = self.context['request'].GET.get('lang', 'uz')
        file_field = obj.file_en if lang == 'en' else obj.file_uz
        if file_field:
            return f"http://127.0.0.1:8000/{file_field.url}"
        return None


class PublicationsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Publications
        fields = ['image', 'description_uz', 'file_uz', 'category', 'author']
        read_only_fields = ['author']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super(PublicationsSerializer, self).create(validated_data)


class PapersSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    references = serializers.SerializerMethodField(method_name='get_references', read_only=True)

    class Meta:
        model = Papers
        fields = ['id', 'category', 'name', 'author', 'pub_date', 'views', 'description', 'references']
        read_only_fields = ['author']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super(PapersSerializer, self).create(validated_data)

    def get_references(self, obj):
        papers_info = obj.papersinformation_set.first()
        return papers_info.references if papers_info else None


class PapersInformationSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    reviews = ReviewerSerializer(read_only=True, many=True)

    class Meta:
        model = PapersInformation
        fields = ['name_uz','pub_date', 'author', 'views',  'reviews', 'description_uz', 'keywords', 'article_uz', 'file_uz', 'references_count', 'references']
        read_only_fields = ['author']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super(PapersInformationSerializer, self).create(validated_data)


class PapersInformationGETSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_name', read_only=True)
    description = serializers.SerializerMethodField(method_name='get_description', read_only=True)
    file = serializers.SerializerMethodField(method_name='get_file', read_only=True)
    article = serializers.SerializerMethodField(method_name='get_article', read_only=True)
    author = AuthorSerializer(read_only=True)
    reviews = ReviewerSerializer(read_only=True, many=True)

    class Meta:
        model = PapersInformation
        fields = ['name','pub_date', 'author', 'views',  'reviews', 'description', 'keywords', 'article', 'file', 'references_count', 'references']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super(PapersInformationSerializer, self).create(validated_data)

    def get_name(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.name_en
            return obj.name_uz
        except:
            return obj.name_uz

    def get_description(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.description_en
            return obj.description_uz
        except:
            return obj.description_uz

    def get_file(self, obj):
        lang = self.context['request'].GET.get('lang', 'uz')
        file_field = obj.file_en if lang == 'en' else obj.file_uz
        if file_field:
            return f"http://127.0.0.1:8000{file_field.url}"
        return None

    def get_article(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.article_en
            return obj.article_uz
        except:
            return obj.article_uz


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviewers
        fields = '__all__'

    def validate(self, data):
        if not self.context['request'].user.is_reviewer:
            raise serializers.ValidationError('You are not allowed to review this paper')
        return data


class LastEditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PapersInformation
        fields = ['name_uz', 'description_uz']


class LastPaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = PapersInformation
        fields = ['pub_date', 'name_uz', 'description_uz']


class MostReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = PapersInformation
        fields = ['name_uz', 'description_uz', 'views']


