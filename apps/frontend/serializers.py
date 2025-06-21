from rest_framework import serializers
from .models import SiteSettings, Icon


class IconSerializer(serializers.ModelSerializer):
    svg = serializers.SerializerMethodField()

    class Meta:
        model = Icon
        fields = ['icon_type', 'svg']

    def get_svg(self, obj):
        return obj.get_svg()


class SiteSettingsSerializer(serializers.ModelSerializer):
    icons = IconSerializer(many=True, read_only=True)

    class Meta:
        model = SiteSettings
        fields = ['site_name', 'logo', 'icons']
