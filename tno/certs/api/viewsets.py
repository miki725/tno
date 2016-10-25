from functools import partial

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from ..models import Certificate, Site
from ..openssl import x509_text_from_x509
from .renderers import PlainTextRenderer
from .serializer import CertificateNestedSerializer, SiteSerializer


class SpecifiedPageNumberPagination(PageNumberPagination):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class CertificateViewSet(ListModelMixin,
                         RetrieveModelMixin,
                         GenericViewSet):
    model = Certificate
    queryset = (
        Certificate.objects
        .select_related(
            'trust_certificate',
            'issuer_certificate',
        )
        .all()
    )

    lookup_field = 'fingerprint_sha2'
    lookup_url_kwarg = 'fingerprint_sha2'

    serializer_class = CertificateNestedSerializer
    pagination_class = partial(
        SpecifiedPageNumberPagination,
        page_size=100,
    )

    @detail_route(methods=['get'], renderer_classes=[PlainTextRenderer])
    def text(self, request, *args, **kwargs):
        object = self.get_object()
        return Response(
            data=x509_text_from_x509(object.x509.encode('utf-8')),
        )


class SiteViewSet(ListModelMixin,
                  DestroyModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    model = Site
    queryset = (
        Site.objects
        .select_related(
            'certificate',
        )
        .all()
    )

    lookup_field = 'host'
    lookup_url_kwarg = 'host'
    lookup_value_regex = r'[^/]+'

    serializer_class = SiteSerializer
    pagination_class = partial(
        SpecifiedPageNumberPagination,
        page_size=100,
    )

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def update(self, request, host, **kwargs):
        try:
            self.get_object()
        except Http404:
            pass
        else:
            raise MethodNotAllowed(request.method)

        serializer = self.get_serializer(
            data={'host': host, 'port': 443},
            writable_fields=[
                'host',
                'port',
            ],
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data

        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(data),
        )
