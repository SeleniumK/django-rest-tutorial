from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse


# root api endpoint
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         # reverse returns fully-qualified urls
#         # identified by convenience names from urls.py
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format),
#     })


# replace all three snippet views with one viewset
class SnippetViewSet(viewsets.ModelViewSet):
    """Automatically provides list/create/retrieve/update/destroy actions.

    Provide extra highlight with detail route.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    # decorator responds to GET request by default, but can use method argument to get POST
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        """Override perform create method, associate user with snippet."""
        serializer.save(owner=self.request.user)


# replaces two views. allows read only list and detail views
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides list and detail actions for user view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


# class SnippetHighlight(generics.GenericAPIView):
#     """Highlight Snippet."""

#     queryset = Snippet.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)

#     def get(self, request, *args, **kwargs):
#         """Get method for highlight."""
#         snippet = self.get_object()
#         return Response(snippet.highlighted)


# # generic class based views
# class SnippetList(generics.ListCreateAPIView):
#     """List all snippets, or create a new snippet."""

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         IsOwnerOrReadOnly,
#     )

#     def perform_create(self, serializer):
#         """Override perform create method, associate user with snippet."""
#         serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     """Snippet detail view, or create a new snippet."""

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         IsOwnerOrReadOnly,
#     )



# replace with view sets
# class UserList(generics.ListAPIView):
#     """List all users."""

#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     """User detail view."""

#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.http import Http404
# from rest_framework import status
# from rest_framework import mixins, generics


# with mixins
# class SnippetList(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     generics.GenericApiView
# ):
#     """List all snippets, or create a new snippet."""

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         """Snippet List get method."""
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         """Snippet List post method."""
#         return self.create(request, *args, **kwargs)


# class SnippetDetail(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView
# ):
#     """Retrieve, update, or delete snippet instance."""

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         """Snippet Detail get method."""
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         """Snippet Detail put method."""
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         """Snippet Detail delete method."""
#         return self.destroy(request, *args, **kwargs)

# basic restful class views
# class SnippetList(APIView):
#     """List all snippets, or create a new snippet."""

#     def get(self, request, format=None):
#         """Snippet List get method."""
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         """Snippet List post method."""
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
#     """Retrieve, update, or delete snippet instance."""

#     def get_object(self, pk):
#         """Get requested object."""
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         """Snippet detail get method."""
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         """Snippet detail put method."""
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         """Snippet detail delete method."""
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# function api view
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     """List all code snippets, or create new."""
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     """Retrieve, update, or delete Code Snippet."""
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# replace with restful view
# class JSONResponse(HttpResponse):
#     """An Http Response that Renders content to JSON."""

#     def __init__(self, data, **kwargs):
#         """Init Json Response class."""
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


# not good practice, rest framework has better things for posting without a token
# @csrf_exempt
# def snippet_list(request):
#     """List all code snippets, or create new."""
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JSONResponse(serializer.data)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#         return JSONResponse(serializer.errors, status=400)


# @csrf_exempt
# def snippet_detail(request, pk):
#     """Retrieve, update, or delete Code Snippet."""
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JSONResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)
# It's worth noting that there are a couple of edge cases we're not
# dealing with properly at the moment. If we send malformed json,
# or if a request is made with a method that the view doesn't handle,
# then we'll end up with a 500 "server error" response.
