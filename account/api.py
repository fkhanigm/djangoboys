from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



class UserViewSet(ModelViewSet):
	queryset = User.objects.all()
	#usually we need queryset
	serializer_class = UserSerializer
	#we allways need serializer class to change json to table
	#authentication_classes = [SessionAuthentication, BasicAuthentication]
	# #attion:this is for developing not deploy

	#permission_classes = [IsAuthenticated]

	
	#def get_queryset(self):
	#we can customize queryset like this
		#queryset = Post.objects.all()
		#queryset = queryset.filter(draft=False)
		#return User.objects.filter(email=self.request.user.email)
		#return just show the post this user write