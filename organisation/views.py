from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Site, Organisation
from .serializers import SiteSerializer, OrganisationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class SiteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SiteSerializer,
        responses={201: SiteSerializer},
    )
    def get(self, request):
        sites = Site.objects.filter(created_by=request.user)
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=SiteSerializer,
        responses={201: SiteSerializer},
    )
    def post(self, request):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        site = self.get_object(pk)
        serializer = SiteSerializer(site)
        return Response(serializer.data)

    @extend_schema(
        request=SiteSerializer,
        responses={201: SiteSerializer},
    )
    def get_object(self, pk):
        try:
            return Site.objects.get(pk=pk, created_by=self.request.user)
        except Site.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    @extend_schema(
        request=SiteSerializer,
        responses={201: SiteSerializer},
    )
    def put(self, request, pk):
        site = self.get_object(pk)
        serializer = SiteSerializer(site, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=SiteSerializer,
        responses={201: SiteSerializer},
    )
    def delete(self, request, pk):
        site = self.get_object(pk)
        site.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=OrganisationSerializer,
        responses={201: OrganisationSerializer},
    )
    def get(self, request):
        organisation = Organisation.objects.filter(created_by=request.user)
        serializer = OrganisationSerializer(organisation, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=OrganisationSerializer,
        responses={201: OrganisationSerializer},
    )
    def post(self, request):
        if not request.user.has_perm('organisation.add_organisation'):
            return Response({"error": "You don't have permission to create an organization."}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            organization_data = serializer.data
            site_data = {
                'organization': organization_data['id'],
                'created_by': request.user,
                'site': organization_data['site']
            }

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Organisation.objects.get(pk=pk, created_by=self.request.user)
        except Organisation.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    @extend_schema(
        request=OrganisationSerializer,
        responses={201: OrganisationSerializer},
    )
    def get(self, request, pk):
        organisation = self.get_object(pk)
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data)

    @extend_schema(
        request=OrganisationSerializer,
        responses={201: OrganisationSerializer},
    )
    def put(self, request, pk):
        organisation = self.get_object(pk)
        serializer = OrganisationSerializer(organisation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=OrganisationSerializer,
        responses={201: OrganisationSerializer},
    )
    def delete(self, request, pk):
        organisation = self.get_object(pk)
        organisation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


