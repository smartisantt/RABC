from rest_framework.routers import DefaultRouter

from api.views import UserView, RoleView

urlpatterns = [
]


router = DefaultRouter()
router.register('user', UserView)
router.register('role', RoleView)

urlpatterns += router.urls