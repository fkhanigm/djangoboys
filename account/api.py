from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
	
class UserViewSet(ModelViewSet):
	queryset = User.objects.all()
	#usually we need queryset
	serializer_class = UserSerializer
	#we allways need serializer class to change json to table
		