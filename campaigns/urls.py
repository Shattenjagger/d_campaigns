from django.conf.urls import include, url
from rest_framework import routers

from campaigns.views import CampaignViewSet

router = routers.DefaultRouter()
router.register(r'campaigns', CampaignViewSet, base_name='campaigns')

urlpatterns = [
    url(r'^', include(router.urls)),
]
