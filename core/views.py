# import json
# from django.http import JsonResponse
# from django.shortcuts import render
# from imagekitio import ImageKit
#
#
# def get_image_kit_signature(request):
#     image_kit = ImageKit(
#         private_key='private_7zgXhRBx6JkdbiffUrT6Iz+RC70=',
#         public_key='public_7/xIjAxG2LvxezZFcU5XVjHQv50=',
#         url_endpoint=' https://ik.imagekit.io/quava'
#     )
#     return JsonResponse(data=image_kit.get_authentication_parameters())
