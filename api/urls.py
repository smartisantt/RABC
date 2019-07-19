from rest_framework.routers import DefaultRouter

from api.views import UserView

urlpatterns = [
]


router = DefaultRouter()
router.register('user', UserView)

urlpatterns += router.urls