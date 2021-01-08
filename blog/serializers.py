from rest_framework import serializers
from .models import Post, PostSetting, Category, Comment
from account.models import User
from account.serializers import UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()



class PostSerializer(serializers.Serializer):
    #this is serializer for post and use Serializer
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length= 250)
    slug = serializers.SlugField(read_only=True, required=False)
    text = serializers.CharField(required=False)
    created_date = serializers.DateTimeField(read_only=True)
    update_date = serializers.DateTimeField(read_only=True)
    published_date = serializers.DateTimeField(required=False)
    draft = serializers.BooleanField(required=False)
    image_title = serializers.ImageField(read_only=True)
    #read_only is somting like we did not give that
    #in model need have default for this or null=True
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        required=False)
    #category and author for relations need defin another way

#    allow_discussion = serializers.BooleanField()
    #we can use PostSetting hear

    #author = UserSerializer(read_only=True)#get full data of auther instead of just author_id
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        required=False)#hear we just get author_id

    def validate_slug(self, slug):
        #slug can be all objects in uper
        try :
            q = Post.objects.get(slug=slug)
            raise serializers.ValidationError('slug must be uniqe')
        except Post.DoesNotExist:
            return slug

    def create(self, validated_data):
    #in form we do this:
    #form = PostForm(request.POST)
    #if form.is_valid:
    #   title = form.cleaned_data['title']
    #   ....
    #   ....
    #   post = Post.objects.create(title=form.cleaned_data['title'], slug=form.cleaned_data['slug'],.....)
    #   return render('base/post_detail.html', {post:post})
    #hear we can do esear
        return Post.objects.create(**validated_data)
        #**validated_data is a func that get object PostSerializer one by one
        #  like (title=validated_data['title'], slug=validated_data['slug'], ....).
        # "**" is python metod for get the all feild on top.
#        PostSetting.objects.create(
#            post=post, 
#            allow_discussion=validated_data['allow_discussion']
#            )#chang PostSertting
        

    def update (self, instance, validated_data):
        #for update the data
        #instanse that the object we want update
        #validated_data is uper object
        instance.title = validated_data.get('title', instance.title)
        #means if exist get it [the first purameter in prantesis] or not put the default[the second parameter in pratisis] 
        #instance.slug = validated_data.get('slug', instance.slug)
        #instance.text = validated_data.get('text', instance.text)
        #instance.created_date = validated_data.get('created_date', instance.created_date)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.draft = validated_data.get('draft', instance.draft)
        #instance.image_title = validated_data.get('image_title', instance.image_title)
        instance.save()#for save the uper fields
        return instance #return the instance



class CommentSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source='author', read_only=True)
    #for time we 'GET' comments show the full datail of author.this just show in detail and in 'POST' method we just need send id of auther not more
    
    #post = PostSerializer(read_only=True)
    #get full post information in this json.actuly we over write author from defual as just id

    #author = UserSerializer(read_only=True)
    #get full user information in this json.actuly we over write author from defual as just id
    class Meta:
        model = Comment
        fields = '__all__'
        #exclude = ('post')
        #for exclude one of all


class PostSettingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSetting
        fields = '__all__'


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostModelSerializer(serializers.ModelSerializer):
    comments = CommentModelSerializer(many=True, read_only=True)#show comment in post list and post detail
    class Meta:
        model = Post
        fields = '__all__'