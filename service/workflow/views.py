# -*- coding: utf-8 -*-
"""Workflow Views"""



from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_json_api.views import RelationshipView
from rest_framework.exceptions import APIException

import json

from workflow import models
from workflow import serializers
from workflow import operations


class Workflow(viewsets.ModelViewSet):
    queryset = models.Workflow.objects.all()
    serializer_class = serializers.Workflow

    #def list(self, request, *args, **kwargs):
    #     
    #    return Response('No Available Workflows.')

    #def retrieve(self, request, *args, **kwargs):
    #    return Response('This is not a workflow.')


class Operation(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'run']
    queryset = models.Operation.objects.all()
    serializer_class = serializers.Operation


    def run(self, request, *args, **kwargs):

        user_parameters = json.loads(request.body)
        #context = models.context.objects.get(pk=params.pop('context', none))
        #if not context.exists():
        #    return response({
        #        "status": "404",
        #        "title": "context does not exist",
        #        "description": "the requested context does not currently exist"
        #    }, status=status.http_404_not_found)
        operation = models.Operation.objects.get(pk=kwargs['pk'])
        parameters = dict(operation.parameters.all())
        result = getattr(operations, operation.operation)(**parameters)

        message = models.Message()
        message.message_type = ''
        message.operation = operation
        message.content = {
            "parameters": parameters,
            "result": result
        }
        message.save()

        return Response(message)

    def get_queryset(self):
        queryset=self.queryset
        #if 'operation_pk' in self.kwargs:
        #    import ipdb; ipdb.set_trace()
        #    queryset = queryset.filter(prerequisites=None)
        #    return queryset
        #if 'prerequisites' in self.request.query_params:
        #    queryset = queryset.filter(prerequisites=None)
        #    return queryset
            #return queryset.filter(prerequisites__pk=self.kwargs['operation_pk'])
        return queryset


class OperationRelationship(RelationshipView):
    queryset = models.Operation.objects.all()
    serializer_class = models.Operation


class Value(viewsets.ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = serializers.Value


class Context(viewsets.ModelViewSet):
    queryset = models.Context.objects.all()
    serializer_class = serializers.Context


class Message(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.Message

    def get_queryset(self):
        queryset = self.queryset
        return queryset


class Service(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.Service


class ServiceRelationship(RelationshipView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.Service


class Resource(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.Resource


class Role(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.Role


class User(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.User


class Group(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.Group