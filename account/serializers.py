from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
User = get_user_model()
#in hear we have Serializer and ModelSerializer

class UserSerializer(serializers.ModelSerializer):
#hear just like forms we just pass the model and fields
	
	class Meta:
		model = User
		fields = '__all__'
		
		
class UserSerializer2(serializers.Serializer):
#hear just like the forms we should defien all field and actions
	email = serializers.EmailField(required=True)
	full_name = serializers.CharField(max_length=150)
	avatar = serializers.ImageField()
	is_staff = serializers.BooleanField(default=False)
	is_active = serializers.BooleanField(default=True)
	
	def validate_email(self, email):
	#for clean the email or any others field we do like this
	#	.... do some thing ....
		return email
	
	def create(self, validated_data):
    #for clreate the account
		user = user.objects.create_user(**validated_data)
		return user
	
	def update(self, validated_data):
    #for update the account
		instance.update(**validated_data)
		instance.save()
		
		
