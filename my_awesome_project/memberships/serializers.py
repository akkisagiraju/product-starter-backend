from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from my_awesome_project.memberships.models import Membership
from my_awesome_project.memberships.models import Organization
from my_awesome_project.utils import consts


class CustomRegisterSerializer(RegisterSerializer):
    def validate_password1(self, password):
        if len(password) < consts.MINIMUM_PASSWORD_LENGTH:
            msg = "Password must be at least 8 characters long"
            raise serializers.ValidationError(msg)
        return super().validate_password1(password)


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):
    memberships = MembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = "__all__"
