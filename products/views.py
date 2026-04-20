from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework import status


class ListCreateMixin:
    """
    A mixin to handle both single and multiple object creation for a given serializer.

    This mixin extends the default behavior of viewsets to allow creating
    either a single object or a list of objects in a single request.
    If the request data is a list, it will attempt to create multiple objects.
    Otherwise, it will proceed with creating a single object as usual.
    """
    def create(self, request, *args, **kwargs):
        """
        Handles the creation of objects. Accepts either a single object's data
        or a list of objects' data in the request.

        Args:
            request: The incoming request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A Response object with the serialized data of the created
                      object(s) and the appropriate HTTP status code.
        """
        if isinstance(request.data, list):
            # Handle creation of multiple objects
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle creation of a single object (normal case)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# Create your views here.

# view for product
class ProductViewSet(ListCreateMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling Product-related operations.

    This viewset provides CRUD (Create, Retrieve, Update, Destroy) operations
    for the Product model. It utilizes the ListCreateMixin to support
    creating products either individually or in bulk via a list.

    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


# view for category
class CategoryViewSet(ListCreateMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling Category-related operations.

    This viewset provides CRUD (Create, Retrieve, Update, Destroy) operations
    for the Category model. It leverages the ListCreateMixin to enable
    creating categories either one by one or as a list in a single request.

    """
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

# view for publisher
class PublisherViewSet(ListCreateMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling Publisher-related operations.

    This viewset offers CRUD (Create, Retrieve, Update, Destroy) functionality
    for the Publisher model. It incorporates the ListCreateMixin, allowing
    for the creation of publishers either individually or through a bulk list
    in a single API call.

    """
    queryset = models.Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer