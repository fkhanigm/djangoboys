from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, CommentSerializer, PostModelSerializer, PostSettingModelSerializer, CommentModelSerializer, CategoryModelSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Post, PostSetting, Comment, Category
from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.decorators import action



#best ever
#use instead for bout listviewgeneric and detailviewgeneric
class PostViewSet(ModelViewSet):
    serializer_class = PostModelSerializer#required
    queryset = Post.objects.filter(draft=False)#required
    #attention:difreent in url.required defind list, create and retrieve, update, destroy
    
    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentModelSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def published(self, request, pk=None):
        post = self.get_object()
        post.draft = False
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_published(self, request):
        queryset = self.filter_queryset(self.get_queryset())#get_queryset get queryset we defind in class in uper
        queryset = queryset.filter(draft=False)#filter agane on queryset
        page = self.paginate_queryset(queryset)#paginating on show comment
        #attion:need configor in settings.py/ go to documetation to see that
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.filter(is_confirmed=True)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()#required


#use for list view whith out set get , put , delete , post
class PostListGeneric(generics.ListCreateAPIView):
    serializer_class = PostSerializer#required
    queryset = Post.objects.all()#required
    

#use for detail view whith out set get , put , delete , post
class PostdetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer#required
    queryset = Post.objects.all()#required


#use mixin in class based api
class PostListMixin(
                    mixins.CreateModelMixin, 
                    mixins.ListModelMixin, 
                    generics.GenericAPIView):
    serializer_class = PostSerializer#required
    queryset = Post.objects.all()#required
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


#use mixin in class based api
class PostDetailMixin(
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.RetrieveModelMixin, 
    generics.GenericAPIView):
    serializer_class = PostSerializer#required
    queryset = Post.objects.all()#required
    #queryset = Post.objects.ilter(deraft=False)#required
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
       return self.destroy(request, *args, **kwargs)



#user rest class bassed apiview
class PostList(APIView):
    def get(self, request, format=None):
        posts =Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    def get(self, request, pk , format=None):
        post =self.get_object(pk)#return detail of post
        serializer = PostSerializer(post)
        return Response(serializer.data)
    def put(self, request, pk , format=None):
        post =self.get_objects(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk , format=None):
        post =self.get_objects(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
#use api_view decorators and give some futar for example defind the json automatic
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#def post_list(request):
#    if request.method == 'GET':
#        posts = Post.objects.all()
#        serializer = PostSerializer(posts, many=True)
#        #posts is a data
#        #many=True means the post is more than one the django should return array
#        return JsonResponse(serializer.data, safe=False)
#        #.data important to reform seralizer to data
#        #JsonResponse change the data from binery to text
#        #safe mean you say JsonResponse i know the data is array and some browser do not know that but i want it.
#    elif request.method == 'POST':
#        data = JSONParser().parse(request)
#        #get data from reques
#        #like in view go an do 'data = json.loads(request.body)'
#        serializer = PostSerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            #save() call the create func in serializer.py/PostSerializer
#            return JsonResponse(serializer.data, status=201)
#            #in export we return JSON instance
#        return JsonResponse(serializer.errors, status=400)




@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':#PUT means update
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=204)

#@csrf_exempt
#def post_detail(request, pk):
#
#    try:
#        post = Post.objects.get(pk=pk)
#
#    except Post.DoesNotExist:
#        return HttpResponse(status=404)
#
#    if request.method == 'GET':
#        serializer = PostSerializer(post)
#        return JsonResponse(serializer.data)
#
#    elif request.method == 'PUT':#PUT means update
#        data = JSONParser().parse(request)
#        serializer = PostSerializer(post, data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return JsonResponse(serializer.error, status=400)
#
#    elif request.metrhod == 'DELET':
#        post.delete()
#        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@csrf_exempt
#def comment_list(request):
#    if request.method == 'GET':
#        comments = Comment.objects.all()
#        serializer = CommentSerializer(comments, many=True)
#        return JsonResponse(serializer.data, safe=False)
#    elif request.method == 'POST':
#        data = JSONParser().parse(request)
#        serializer = CommentSerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=201)
#        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)

    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return HttpResponse(status=204)

#@csrf_exempt
#def comment_detail(request, pk):
#    try:
#        comment = Comment.objects.get(pk=pk)
#
#    except Post.DoesNotExist:
#        return HttpResponse(status=404)
#
#    if request.method == 'GET':
#        serializer = CommentSerializer(comment)
#        return JsonResponse(serializer.data)
#
#    elif request.method == 'PUT':
#        data = JSONParser().parse(request)
#        serializer = CommentSerializer(comment, data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return JsonResponse(serializer.error, status=400)
#
#    elif request.metrhod == 'DELET':
#        comment.delete()
#        return HttpResponse(status=204)

