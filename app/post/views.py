from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.post.models import Post
from app.post.serializers import PostSerializer, PostDisplaySerializer
from common.util import is_missing_param_in_request, is_empty
from constants import constants
from constants.api_mandatory_field_lists import APIMandatoryFieldList


def update_blog_post(data):
    post_serializer_data = {
        'email': data['email'],
        'title': data['title'],
        'story': data['story']
    }
    post_serializer = PostSerializer (data=post_serializer_data)
    if post_serializer.is_valid ():
        post = post_serializer.save ()
        return True, post
    else:
        return False, post_serializer.errors


def is_valid_post_request(data):
    if not data:
        return False, "payload can not be empty"
    mandatory_fields = APIMandatoryFieldList.get_mandatory_field_list (key='post')
    is_missing_param, message = is_missing_param_in_request (dict=data, key_list=mandatory_fields)
    if is_missing_param:
        return False, message
    return True, None


@api_view (['POST'])
@permission_classes ((AllowAny,))
@authentication_classes ([])
def blog_post(request):
    data = request.data
    is_valid_request, message = is_valid_post_request (data=data)
    if not is_valid_request:
        return Response ({'status': constants.API_ERROR, 'message': message}, status=status.HTTP_400_BAD_REQUEST)

    is_success, message = update_blog_post(data=data)
    if not is_success:
        return Response ({'status': constants.API_ERROR, 'message': message},
                         status=status.HTTP_400_BAD_REQUEST)

    return Response ({'status': constants.API_SUCCESS, 'message': 'Successfully created a post'},
                     status=status.HTTP_201_CREATED)


@api_view (['GET'])
@permission_classes ((AllowAny,))
@authentication_classes ([])
def display_post(request):
    posts = Post.objects.filter (is_deleted=False)
    if not len (posts):
        return Response ({'status': constants.API_ERROR, 'message': 'No one has posted yet'},
                         status=status.HTTP_204_NO_CONTENT)
    if 2 > len ((posts)) > 0:
        message = " {0} blogpost found".format (len (posts))
    else:
        message = " {0} blogposts found".format (len (posts))
    return Response (
        {'status': constants.API_SUCCESS, 'message': message, 'data': PostDisplaySerializer (posts,
                                                                                             many=True).data},
        status=status.HTTP_200_OK)


@api_view (['DELETE'])
@permission_classes ((AllowAny,))
@authentication_classes ([])
def delete_post(request, post_id):
    try:
        post = Post.objects.get (id=post_id, is_deleted=False)
    except Post.DoesNotExist:
        return Response ({'status': constants.API_ERROR, 'message': 'given id {0} does not exist'.format (post_id)},
                         status=status.HTTP_400_BAD_REQUEST)
    post.is_deleted = True
    post.save ()
    return Response ({'status': constants.API_ERROR, 'message': 'given id post has been deleted'},
                     status=status.HTTP_200_OK)


def is_valid_update_request(data):
    if not data:
        return False, "payload can not be empty"
    mandatory_fields = APIMandatoryFieldList.get_mandatory_field_list (key='id')
    is_missing_param, message = is_missing_param_in_request (dict=data, key_list=mandatory_fields)
    if is_missing_param:
        return False, message
    return True, None


@api_view (['PUT'])
@permission_classes ((AllowAny,))
@authentication_classes ([])
def update_post(request):
    data = request.data
    is_valid_request, message = is_valid_update_request (data=data)
    if not is_valid_request:
        return Response ({'status': constants.API_ERROR, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
    post_id = data['id']
    try:
        post = Post.objects.get (id=post_id, is_deleted=False)
    except Post.DoesNotExist:
        return Response ({'status': constants.API_ERROR, 'message': 'given id {0} does not exist'.format (post_id)},
                         status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.get (id=post_id)
    if not is_empty (dict=data, key='email'):
        post.email = data['email']
        post.save ()
    if not is_empty (dict=data, key='title'):
        post.title = data['title']
        post.save ()
    if not is_empty (dict=data, key='story'):
        post.story = data['story']
        post.save ()
    return Response ({'status': constants.API_SUCCESS, 'message': 'given id post has been updated'},
                     status=status.HTTP_200_OK)
