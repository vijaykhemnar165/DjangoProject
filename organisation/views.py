from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Site
from .serializers import SiteSerializer
from rest_framework.permissions import IsAuthenticated

class SiteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sites = Site.objects.filter(owner=request.user)
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SiteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Site.objects.get(pk=pk, owner=self.request.user)
        except Site.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        site = self.get_object(pk)
        serializer = SiteSerializer(site)
        return Response(serializer.data)

    def put(self, request, pk):
        site = self.get_object(pk)
        serializer = SiteSerializer(site, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        site = self.get_object(pk)
        site.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
