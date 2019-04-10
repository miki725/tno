from cryptography.x509 import NameOID
from django.contrib import admin
from django_countries import countries

from core.admin import site

from .models import Certificate, Site, SiteCollection


class CountryFilter(admin.SimpleListFilter):
    template = 'admin/dropdown_filter.html'
    title = 'country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        return sorted(countries.countries.items(), key=lambda i: i[1])

    def queryset(self, request, queryset):
        v = self.value()
        if v:
            return queryset.filter(subject__contains={NameOID.COUNTRY_NAME._name: v})
        else:
            return queryset


class CertificateAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'common_name',
        'organization',
        'country',
        'valid_not_after',
        'is_root',
        'is_trusted',
    ]

    list_filter = [
        CountryFilter,
        'is_root',
        'is_trusted',
    ]

    raw_id_fields = [
        'trust_certificate',
        'issuer_certificate',
    ]


class SiteAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'certificate',
    ]


class SiteCollectionAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'name',
        'owner',
    ]
    raw_id_fields = [
        'owner',
    ]


site.register(Certificate, CertificateAdmin)
site.register(Site, SiteAdmin)
site.register(SiteCollection, SiteCollectionAdmin)
