from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SiteSettings


class SiteSettingsAPI(APIView):
    def get(self, request):
        settings = SiteSettings.objects.first()
        if not settings:
            return Response({})

        data = {
            'site_name': settings.site_name,
            'logo': settings.logo.url if settings.logo else None,
            'icons': {
                icon.icon_type: icon.get_svg()
                for icon in settings.icons.all()
            }
        }
        return Response(data)
