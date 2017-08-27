from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from campaigns.views import CampaignViewSet, CustomActionViewSet, RecurrentSubscribersViewSet

router = routers.DefaultRouter()
router.register(r'campaigns', CampaignViewSet, base_name='campaigns')
router.register(r'custom_actions', CustomActionViewSet, base_name='custom_actions')

campaigns_router = NestedSimpleRouter(router, r'campaigns', lookup='campaign')
campaigns_router.register(r'subscribers', RecurrentSubscribersViewSet, base_name='campaign-subscribers')

custom_actions_router = NestedSimpleRouter(router, r'custom_actions', lookup='custom_action')
custom_actions_router.register(r'subscribers', RecurrentSubscribersViewSet, base_name='custom_action-subscribers')

campaigns_activate = CampaignViewSet.as_view({
    'get': 'activate'
})

campaigns_deactivate = CampaignViewSet.as_view({
    'get': 'deactivate'
})

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(campaigns_router.urls)),
    url(r'^', include(custom_actions_router.urls)),
    url(r'^campaigns/(?P<uuid>[0-9a-f-]+)/activate/$', campaigns_activate, name='campaigns-activate'),
    url(r'^campaigns/(?P<uuid>[0-9a-f-]+)/deactivate/$', campaigns_deactivate, name='campaigns-deactivate'),
]
