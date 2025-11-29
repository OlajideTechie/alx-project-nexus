from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

class HealthCheck(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=200)


@extend_schema(tags=["Health"])
@api_view(["GET"])
@permission_classes([AllowAny]) 
def db_health(request):
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

        if not result:
            raise Exception("Database returned no value")

        return Response({"database": "ok"}, status=200)

    except Exception as e:
        return Response({
            "database": "error",
            "details": str(e)
        }, status=500)
