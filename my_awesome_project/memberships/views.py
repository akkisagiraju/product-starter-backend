from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response

from my_awesome_project.memberships.serializers import CustomRegisterSerializer
from my_awesome_project.memberships.serializers import MembershipSerializer
from my_awesome_project.memberships.serializers import OrganizationSerializer


class SignUpMixin:
    """Common functionality for signup views."""

    def create_user(self, serializer):
        return self.perform_create(serializer)

    @staticmethod
    def set_member_data(request_data, user, organization):
        member_data = request_data.copy()
        member_data["user"] = user.id

        if "organization" not in member_data:
            member_data["organization"] = organization.id

        return member_data

    @staticmethod
    def create_membership(member_data):
        membership_serializer = MembershipSerializer(data=member_data)

        if membership_serializer.is_valid():
            membership = membership_serializer.save()
            return membership, None

        return None, membership_serializer.errors


class CustomRegisterView(RegisterView, SignUpMixin):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom registration logic for creating a new user
        and an associated organization and membership for the user.

        TODO:
        1. Add logic to handle the case where an organization already exists.
        2. Add invitations using django-invitations.
        3. Handle multi tenant setup for organizations and memberships
        """
        serializer = self.get_serializer(data=request.data)
        email = request.data["email"]

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        organization_data = {
            "name": f"{email}'s Org",
        }

        organization_serializer = OrganizationSerializer(data=organization_data)

        if organization_serializer.is_valid():
            # Create the user
            user = self.create_user(serializer)

            # Create the organization
            organization = organization_serializer.save()

            member_data = self.set_member_data(request.data, user, organization)
            # Create the membership for the user and organization
            self.create_membership(member_data)

            headers = self.get_success_headers(serializer.data)
            data = self.get_response_data(user)

            if data:
                response = Response(
                    data,
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            else:
                response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

            return response

        return Response(
            organization_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
