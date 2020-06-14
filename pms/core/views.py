from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from pms.core.models import Image


@require_POST
@csrf_exempt
def upload_image(request):
    if request.POST.get('oldImage'):
        old_image = Image.objects.get(file=request.POST['oldImage'])
        old_image.delete()

    if request.POST.get('image'):
        image = Image()
        image.file = request.FILES['image']
        image.save()
        return JsonResponse({'image': image.file.name})
    return JsonResponse({})
