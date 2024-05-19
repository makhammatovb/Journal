from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

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


class ContactSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=255)
    subject = serializers.CharField(max_length=255)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class PublicationsGETSerializer(serializers.ModelSerializer):
    publication = serializers.SerializerMethodField(method_name='get_publication_name', read_only=True)
    file = serializers.SerializerMethodField(method_name='get_file', read_only=True)

    class Meta:
        model = Publications
        fields = ('publication', 'file')

    def get_publication_name(self,obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.description_en
            return obj.description_uz
        except:
            return obj.description_uz

    def get_file(self,obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.file_en
            return obj.file_uz
        except:
            return obj.file_uz

class PublicationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publications
        fields = '__all__'


class PapersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Papers
        fields = '__all__'


class PapersInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PapersInformation
        fields = '__all__'


class PapersInformationGETSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_name', read_only=True)
    description = serializers.SerializerMethodField(method_name='get_description', read_only=True)
    file = serializers.SerializerMethodField(method_name='get_file', read_only=True)
    article = serializers.SerializerMethodField(method_name='get_article', read_only=True)

    class Meta:
        model = PapersInformation
        fields = ('name', 'description', 'file', 'article')


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
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.file_en.url if obj.file_en else None
            return obj.file_uz if obj.file_uz else None
        except:
            return obj.file_uz if obj.file_uz else None

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


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = PapersInformation
        fields = ['id', 'name_uz', 'name_en', 'pub_date', 'views', 'file_uz', 'file_en']

