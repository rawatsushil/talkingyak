import operator

from django.db import models
from django.shortcuts import get_object_or_404
from functools import reduce

from rest_framework import generics, status, views
from rest_framework.response import Response

from .helpers import get_tiny_url
from .models import Link
from .serializer import LinkSerializer

SEARCH_FIELDS = {'original_url': 'string'}


class AbstractView(object):
    def search_query_list(self, queryset, search):
        """
        Return a tuple containing a queryset to implement the search
        """
        orm_lookups = [
            {'%s__icontains' % str(field_name): search}
            for field_name, field_type in self.search_fields.items()
        ]
        or_queries = [models.Q(**orm_lookup) for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.or_, or_queries)).distinct()
        return queryset


class CreateTinyUrlView(generics.ListCreateAPIView, AbstractView):
    search_fields = SEARCH_FIELDS
    serializer_class = LinkSerializer

    def get_queryset(self):
        queryset = Link.objects.all()
        search = self.request.query_params.get('search', '')
        if search and self.search_fields:
            return self.search_query_list(queryset, search)
        return queryset

    def get(self, request, *args, **kwargs):
        response = super(CreateTinyUrlView, self).get(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        original_url = request.data.get('url')
        tiny_url = get_tiny_url(request, original_url)
        return Response(
            data=tiny_url, status=status.HTTP_200_OK
        )


class ShortUrlMetaInfo(views.APIView):
    def get(self, request, *args, **kwargs):
        short_id = kwargs.get('short_id')
        link = get_object_or_404(Link, tiny_id=short_id)
        link.total_hits += 1
        link.save()
        return Response(
            {
                'total_hits': link.total_hits,
                'hourly_hits': link.hourly_hits

             }, status=status.HTTP_200_OK
        )

