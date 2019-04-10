from django.db.models import Prefetch
from django.http import Http404
from drf_braces.mixins import MultipleSerializersViewMixin
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from ..models import Certificate, Site, SiteCollection
from .renderers import CertificateOpenSSLTextRenderer, CertificatePEMRenderer
from .serializer import (
    CertificateNestedSerializer,
    CertificateSerializer,
    SiteCollectionSerializer,
    SiteNestedSerializer,
)


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

    @property
    def renderer_classes(self):
        renderers = super(CertificateViewSet, self).renderer_classes[:]
        renderers.append(CertificatePEMRenderer)
        if self.lookup_url_kwarg in self.kwargs:
            renderers.append(CertificateOpenSSLTextRenderer)
        return renderers


class SiteViewSet(ListModelMixin,
                  DestroyModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    model = Site
    queryset = (
        Site.objects
        .select_related(
            'certificate',
            'certificate__trust_certificate',
            'certificate__issuer_certificate',
        )
        .all()
    )

    lookup_field = 'host'
    lookup_url_kwarg = 'host'
    lookup_value_regex = r'[^/]+'

    serializer_class = SiteNestedSerializer

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
            data={'host': host},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data

        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(data),
        )


class SiteCollectionViewSet(ListModelMixin,
                            RetrieveModelMixin,
                            MultipleSerializersViewMixin,
                            GenericViewSet):
    model = SiteCollection
    queryset = (
        SiteCollection.objects
        .select_related(
            'owner',
        )
        .prefetch_related(
            Prefetch('sites', SiteViewSet.queryset),
        )
        .all()
    )

    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    serializer_class = SiteCollectionSerializer

    @property
    def is_detail(self):
        return bool(self.kwargs.get(self.lookup_url_kwarg))

    def get_queryset(self):
        qs = super(SiteCollectionViewSet, self).get_queryset()
        # in list view, only allow owners to list their site collections
        # otherwise raise permission denied
        # note that since UUID is unique enough, users can still
        # query any site collection via specific UUID regardless
        # if they are signed in
        if not self.is_detail:
            if self.request.user.is_authenticated:
                qs = qs.filter(owner=self.request.user)
            else:
                raise PermissionDenied
        return qs

    @detail_route(methods=['get'],
                  url_path='trust-certificates',
                  renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES + [CertificatePEMRenderer])
    def trust_certificates(self, request, uuid, *args, **kwargs):
        certificates = (
            Certificate.objects
            .filter(leaf_certificates__sites__site_collections__in=self.get_queryset())
            .all()
        )

        page = self.paginate_queryset(certificates)

        serializer = self.get_serializer(
            serializer_class=CertificateSerializer,
            instance=page,
            many=True,
        )

        response = self.get_paginated_response(serializer.data)
        response['Certificates-Length'] = response.data['count']
        return response
