from rest_framework.routers import DefaultRouter

from certs.api.viewsets import (
    CertificateViewSet,
    SiteCollectionViewSet,
    SiteViewSet,
)
from onetime.api.viewsets import EntropyViewSet, OneTimeSecretViewSet


router = DefaultRouter(trailing_slash=True)

router.register('entropy', EntropyViewSet, 'entropy')
router.register('one-time-secrets', OneTimeSecretViewSet, 'one-time-secret')
router.register('certificates', CertificateViewSet, 'certificates')
router.register('sites', SiteViewSet, 'sites')
router.register('site-collections', SiteCollectionViewSet, 'site-collections')

urlpatterns = router.urls
