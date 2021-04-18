from abc import ABC, abstractmethod

from django.shortcuts import render
from rest_framework import generics

import os

from django.views import View
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from icd10.storages import MediaStorage
from icd10.core.validation import validate
from .models import (
    ResearchProject,
    ResearchItem,
    ICD10Item,
    ThematicCodeItem
)
from .serializers import (
    ResearchProjectSerializer,
    ResearchItemSerializer,
    ICD10ItemSerializer,
    ThematicCodeItemSerializer
)


class FileUploadView(APIView):
    @csrf_exempt
    def post(self, requests, **kwargs):
        file_obj = requests.FILES.get('file', '')
        validation = validate(file_obj)
        if not validation["valid"]:
            return JsonResponse({
                'message': validation["error"]
            }, status=400)

        file_directory_within_bucket = 'uploads/'

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_obj.name
        )

        media_storage = MediaStorage()

        if not media_storage.exists(file_path_within_bucket): 
            media_storage.save(file_path_within_bucket, file_obj)
            file_url = media_storage.url(file_path_within_bucket)

            return JsonResponse({
                'message': 'OK',
                'fileUrl': file_url,
            })
        else:
            return JsonResponse({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)


class ResearchProjectCreateListView(generics.ListCreateAPIView):
    serializer_class = ResearchProjectSerializer
    queryset = ResearchProject.objects.all()


class ResearchProjectView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResearchProjectSerializer
    queryset = ResearchProject.objects.all()


class ResearchItemCreateListView(generics.ListCreateAPIView):
    serializer_class = ResearchItemSerializer
    queryset = ResearchItem.objects.all()


class ResearchItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResearchItemSerializer
    queryset = ResearchItem.objects.all()


class ICD10ItemCreateListView(generics.ListCreateAPIView):
    serializer_class = ICD10ItemSerializer
    queryset = ICD10Item.objects.all()


class ICD10ItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ICD10ItemSerializer
    queryset = ICD10Item.objects.all()


class PercentView(ABC, APIView):
    research_item_queryset = ResearchItem.objects
    TARGET: str

    @abstractmethod
    def get_in_progress_count(self, pk: int) -> int:
        raise NotImplemented("Please implement the get_in_progress_count method")

    def get(self, request, *args, **kwargs):
        try:
            project_id = kwargs['pk']
        except KeyError:
            return JsonResponse({"error": "Not found"}, status=400)

        total_count = self.research_item_queryset.filter(project_id=project_id).count()
        in_progress_count = self.get_in_progress_count(project_id)

        return JsonResponse({
            "total_count": total_count,
            f"{self.TARGET}_count": in_progress_count,
            "percentage": "{0:.0%}".format(in_progress_count/total_count)
        })


class PredictedPercentView(PercentView):
    TARGET = "predicted"
    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project_id=pk).exclude(icd10item__pk=None).count()


class ValidatedPercentView(PercentView):
    TARGET = "validated"
    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project_id=pk).filter(icd10item__validated=True).count()


class PredictionAcceptedPercentView(PercentView):
    TARGET = "prediction_accepted"
    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project_id=pk)\
            .filter(icd10item__prediction_accepted=True).count()
