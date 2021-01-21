'''
we can make our owne permision in hear.this make our api.py clean.
'''
from rest_framework.permissions import BasePermission, SAFE_METHODS
#the `BasePermission` is base and we should inhariet in our class
#`SAFR_METHODS` are the just get methods not put methods

class IsPostAuthorOrReadOnly(BasePermission):
    #for author to edit or anothor for read
    def has_permission(self, request, view):
        '''
        this is for list of objects for example list of post
        Return `True` if permission is granted, `False` otherwise.
        '''
        return bool(
            request.method in SAFE_METHODS or
            #if my method in SAFE_METHODS [get,heed,option ] do it or
            request.user and
            #check user is log in and
            request.user.is_authenticated
            #user is authenticated
        )

    def has_object_permission(self, request, view, obj):
        '''
        this is for detail of object for example detail of post
        Return `True` if permission is granted, `False` otherwise.
        '''
        return bool(
            request.method in SAFE_METHODS or
            #if my method in SAFE_METHODS [get,heed,option ] do it or
            request.user == obj.author or
            #this log in user is author of our object get them all permissions or
            request.user.is_staff
            #this means user is log in is admin permission
        )
    