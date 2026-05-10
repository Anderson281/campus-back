
from django.http import JsonResponse
from django.views import View  

class BaseDjangoView(View):
    """
    DJANGO CLASS BASED VIEW

    This class is a class based view that will handle the insert, 
    update, delete and select operations over the Buildings model.

    The class has the following methods:
        -get() -> Handles the select operation. It will return the record with the id.
        -post() -> Handles the insert, update, and delete operations.

    To use this view:
        1. Inherit from this class.
        2. Implement the methods selectone, selectall, insert, update, and delete.
        3. Register the view in the urls.py file. For example for the building model:
            [...
                path('buildings_view/<str:action>/', views.BuildigsView.as_view(), name='buildings_views'),  # POST requests
                path('buildings_view/<str:action>/<int:id>/', views.BuildigsView.as_view(), name='buildings_views'),  # POST requests            
             ...
            ]
        4. To use the view, the URL must be like:
            To get a record, the URL must be like:
                GET /buildings_view/selectone/<id>/
            To get all the records, the URL must be like:
                GET /buildings_view/selectall/
            To insert a record, the URL must be like:
                POST /buildings_view/insert/ --> The data must be sent in the body of the request.
            To update a record, the URL must be like:
                POST /buildings_view/update/<id>/ --> The data must be sent in the body of the request.
            To delete a record, the URL must be like:
                POST /buildings_view/delete/<id>/

        You can add more methods to this class by redefining the get and post methods. To add
        the new get method and new post method methods, you can do the following:

            def get(self, request, *args, **kwargs):
                action=kwargs.get('action')
                if action == 'newgetmethod':
                    return self.newgetmethod()
                else:            
                    return super().get(request, *args, **kwargs)
                
            def post(self, request, *args, **kwargs):
                action = kwargs.get('action')
                if action == 'newpostmethod':
                    return self.newpostmethod()
                else:            
                    return super().get(request, *args, **kwargs)
                    
        To call them, the URL must be like:
            GET /buildings_view/newgetmethod/
            POST /buildings_view/newpostmethod/       
    """
    def get(self, request, *args, **kwargs):
        """Handles the 'select' method with a GET request."""

        action=kwargs.get('action')
        if action == 'selectone':
            id = kwargs.get('id')
            return self.selectone(id)
        elif action == 'selectall':
            return self.selectall()
        else:            
            return JsonResponse({"message": "Invalid operation option"}, status=400)

    def post(self, request, *args, **kwargs):
        """Handles insert, update, and delete depending on the URL parameter."""
        
        action = kwargs.get('action')
        print(f"action father: {action}")
        if action == 'insert':
            return self.insert(request)
        elif action == 'update':
            id = kwargs.get('id')
            return self.update(request, id)
        elif action == 'delete':
            id = kwargs.get('id')
            return self.delete(id)
        else:
            JsonResponse({"message": "Invalid operation option"}, status=400)
    
    #GET OPERATIONS
    def selectone(self, id):
        return JsonResponse({'ok':True, 'message': 'Method selectone called: GET', 'data': []}, status=200)

    def selectall(self):
        return JsonResponse({'ok':True, 'message': 'Method selectall called: GET', 'data': []}, status=200)

    #POST OPERATIONS
    def insert(self, request):
        return JsonResponse({'ok':True, 'message': 'Method insert called: POST', 'data': []}, status=200)
    def update(self, request, id):
        return JsonResponse({'ok':True, 'message': 'Method update called: POST', 'data': []}, status=200)
    def delete(self, id):
        return JsonResponse({'ok':True, 'message': 'Method delete called: POST', 'data': []}, status=200)
