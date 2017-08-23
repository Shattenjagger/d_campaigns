from django.conf.urls import include, url
from rest_framework import routers

from campaigns.views import CampaignViewSet

router = routers.DefaultRouter()
router.register(r'campaigns', CampaignViewSet, base_name='campaigns')

campaigns_activate = CampaignViewSet.as_view({
    'get': 'activate'
})

campaigns_deactivate = CampaignViewSet.as_view({
    'get': 'deactivate'
})

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^campaigns/(?P<pk>[0-9a-f-]+)/activate/$', campaigns_activate, name='campaigns-activate'),
    url(r'^campaigns/(?P<pk>[0-9a-f-]+)/deactivate/$', campaigns_deactivate, name='campaigns-deactivate'),
]
