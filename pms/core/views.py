from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from cloudinary import uploader as cloudinary_uploader


@require_POST
@csrf_exempt
def upload_file(request):
    # if request.POST.get('oldImage'):

    response = {}
    if request.FILES.get('file'):
        response = cloudinary_uploader.upload(request.FILES.get('file'))
    return JsonResponse(response)
