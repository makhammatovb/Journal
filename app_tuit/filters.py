# -*- coding: utf-8 -*-
from django_filters import CharFilter, FilterSet
from django.db.models import Q

from .models import (
    RequirementsInformation,
    FAQ,
    Publications,
    Papers,
)


class RequirementsFilter(FilterSet):
    keyword = CharFilter(method="filter_keyword", label="Search")

    class Meta:
        model = RequirementsInformation
        fields = ['keyword']

    def filter_keyword(self, queryset, name, value):
        title_queryset = queryset.filter(Q(req_title__icontains=value))
        if title_queryset.exists():
            return title_queryset
        return queryset.filter(Q(req_description__icontains=value))

class FAQFilter(FilterSet):
    faq = CharFilter(method="faq_keyword", label="Search FAQ")

    class Meta:
        model = FAQ
        fields = []

    def faq_keyword(self, queryset, name, value):
        faq_queryset = queryset.filter(Q(question_uz__icontains=value))
        if faq_queryset.exists():
            return faq_queryset
        return queryset.filter(Q(answer_uz__icontains=value))


class PublicationsFilter(FilterSet):
    publications = CharFilter(method="publications_keyword", label="Search publications")

    class Meta:
        model = Publications
        fields = []

    def publications_keyword(self, queryset, name, value):
        publications_queryset = queryset.filter(Q(description_uz__icontains=value))
        if publications_queryset.exists():
            return publications_queryset
        return queryset.filter(Q(description_en__icontains=value))


class PapersInfoFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains")
    author = CharFilter(field_name="author__first_name", lookup_expr="icontains")
    description = CharFilter(lookup_expr="icontains")
    category = CharFilter(field_name="category__name", lookup_expr="icontains")
    references = CharFilter(field_name="papersinformation__references", lookup_expr="icontains")

    class Meta:
        model = Papers
        fields = ['name', 'author', 'description', 'category', 'references']
