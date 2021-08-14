from rest_framework import routers
from rest_framework.permissions import AllowAny


class APIRootView(routers.APIRootView):
    """
    The root view which handles listing available API's
    """
    permission_classes = (AllowAny,)
    pass


class DefaultRouter(routers.DefaultRouter):
    """
    Extends DefaultRouter class to add a method for extending url routes from another router.
    """
    APIRootView = APIRootView

    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)
