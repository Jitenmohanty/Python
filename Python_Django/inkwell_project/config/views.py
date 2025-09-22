from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Welcome to Inkwell API",
        "endpoints": {
            "blog": "http://127.0.0.1:8000/api/blog/",
            "users": "http://127.0.0.1:8000/api/users/",
            "admin": "http://127.0.0.1:8000/admin/"
        }
    })