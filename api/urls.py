from rest_framework.routers import DefaultRouter

from api.views import UserView, RoleView, PermissionsView

urlpatterns = [
]


router = DefaultRouter()
router.register('user', UserView)
router.register('role', RoleView)
router.register('permission', PermissionsView)

urlpatterns += router.urls