#Django imports
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Codelist. Hello world", "data":[]})