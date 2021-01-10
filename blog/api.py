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
    #attention:difreent in url.required defind list, create and retrieve, update, destroy or we can just register in router
    serializer_class = PostModelSerializer#required
    queryset = Post.objects.all()#required
    #queryset = Post.objects.filter(draft=False)

    #def get_queryset(self):
    ##we can customize queryset like this
    #    queryset = Post.objects.all()
    #    queryset = queryset.filter(draft=False)
    #    return queryset

    @action(detail=True, methods=['GET'])
    #the 'action' give  us some extra "url".
    #attion this is not show in usuall path url, need to use router
    #'detail=True' means this action is for detail not list
    #we can defind the method this action is work.hear is "GET"
    def comments(self, request, pk=None):
        #this 'action' give us all comments of this post. the url is "http://127.0.0.1:8000/api/posts/pk/comments/"
        #attion:the name of function is add in the end of the url
        #if in 'action' detail=True so you need pass the "pk" to func 
        post = self.get_object()
        #we can get our object like this
        #the query of 'get_object' is "post = Post.objects.get(pk=pk)".'get_object' is bether becuse of it has error response it self
        comments = post.comments.all()
        #we can defind our query like this
        #we can customize that "Comment.objects.filter(post_id=pk)" or "Comment.objects.filter(post=post)"
        serializer = CommentModelSerializer(comments, many=True)
        #read the data from database by serializer.'comments' is our "data"
        return Response(serializer.data)
        #create our JSON wiht Response of restfull

    @action(detail=True, methods=['POST'])
    #attion:this action is just effect on postman not browser
    #the 'action' give  us some extra "url".
    #attion this is not show in usuall path url, need to use router
    #'detail=True' means this action is for detail not list
    #we can defind the method this action is work.hear is "GET"
    def publish(self, request, pk=None):
        #this 'action' give us all of this post. the url is "http://127.0.0.1:8000/api/posts/pk/published/"
        #attion:the name of function is add in the end of the url
        #if in 'action' detail=True so you need pass the "pk" to func 
        post = self.get_object()
        post.draft = False
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    #the 'action' give  us some extra "url".
    #attion this is not show in usuall path url, need to use router
    #'detail=False' means this action is for list not detail
    #we can defind the method this action is work.hear is "POST"
    def get_published(self, request):
        #this 'action' give us all published posts[draft=False]. the url is "http://127.0.0.1:8000/api/posts/get_published/"
        #attion:the name of function is add in the end of the url
        queryset = self.filter_queryset(self.get_queryset())
        #defalt of library
        queryset = queryset.filter(draft=False)
        #filter agane on queryset
        page = self.paginate_queryset(queryset)
        #defaul of library
        #paginating on show comment
        #attion:need configor in settings.py/ go to documetation to see that
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.filter(is_confirmed=True)
    #'is_confirmed' is the models.py obect for the Comment class for confirmed the comment. we add query of this option to limited the comment is not confirmed.



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
    #queryset = Post.objects.filter(draft=False)#we can customize the queryset
    def get(self, request, *args, **kwargs):#required
        return self.list(request, *args, **kwargs)
        #say we want list
    def post(self, request, *args, **kwargs):#required
        return self.create(request, *args, **kwargs)
        #say we want create a post

#use mixin in class based api
class PostDetailMixin(
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.RetrieveModelMixin, 
    generics.GenericAPIView):
    serializer_class = PostSerializer#required
    queryset = Post.objects.all()#required
    #queryset = Post.objects.filter(draft=False)#we can customize the queryset
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
       return self.destroy(request, *args, **kwargs)


#user rest class bassed apiview
class PostList(APIView):
    #like serializer[not ModelSerializer]need define all things
    def get(self, request, format=None):
        #for get data
        posts =Post.objects.all()
        #get all post
        serializer = PostSerializer(posts,many=True)
        #pass the 'posts' in serializers for proceesing the models.py
        return Response(serializer.data)
        #show the restfull response format
    def post(self, request, format=None):
        #for post data
        serializer = PostSerializer(data=request.data)
        #parse the json get from frontEnd and give in serializer for proccessing in the models.py
        if serializer.is_valid():
            #for check validation
            serializer.save()
            #save the serializer
            return Response(serializer.data, status.HTTP_201_CREATED)
            #show the restfull response format
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # show the error response of frstfurll


class PostDetail(APIView):
    #like serializer[not ModelSerializer]need define all things
    def get_object(self, pk):
    #for show detail of post of we want to do on it
    #get 'pk' from url. attention:if in url the name is 'slug' we should use slug hear instead of pk or any thing else
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    def get(self, request, pk , format=None):
        #get detail of post
        #'pk' get from url. attention:if in url the name is 'slug' we should use slug hear instead of pk or any thing else
        post =self.get_object(pk)#return detail of post
        serializer = PostSerializer(post)
        #pass the detail of post in Models.py by PostSerializer
        return Response(serializer.data)
    def put(self, request, pk , format=None):
        #for edit the post
        post =self.get_objects(pk)
        serializer = PostSerializer(post, data=request.data)
        #'request.data' is for get request of 'put' in json from frontEnd
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk , format=None):
        post =self.get_objects(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
#this is a restfull tool.this is decorator.need defind the method.
#this decorator do  not need defind the data from json this do parse() automation.
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        #get all comments
        serializer = CommentSerializer(comments, many=True)
        #modifi all comments whit serializer.
        #many=True means this is list and have morthan one comment
        return Response(serializer.data)
        #hear we don`t use 'JsonResponse' and just use 'Response' from restfull.they gove use some tools in browser
        #we should import 'Response'
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        #the data is the dictionary from json how 'api_view' parse that.
        #'request.data' means 'data = JSONParser().parse(request)'.
        #attion:'request.data' work when we have '@api_view'.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #status was defind in restfull. we can import and use it.


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
#def comment_list(request):
# #the function way for use serilizer.this is function base of view in api 
#    if request.method == 'GET':
#        comments = Comment.objects.all()
#        serializer = CommentSerializer(comments, many=True)
#        return JsonResponse(serializer.data, safe=False)
        #this is the anser of our procces. we shoud post that whit json so use 'django JsonResponse'.in browser the show just raw json
#    elif request.method == 'POST':
#        data = JSONParser().parse(request)
        #like 'json.loads()' this get the dictionery of json from json
#        serializer = CommentSerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=201)
#        return JsonResponse(serializer.errors, status=400)


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
