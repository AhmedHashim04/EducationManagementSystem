from django.shortcuts import render
from rest_framework import viewsets
from .models import Assignment , Grade
from .serializer import AssignmentSerializer #, GradeSerializer
# Create your views here.



class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    lookup_field = 'id'