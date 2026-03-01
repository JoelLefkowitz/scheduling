from dataclasses import asdict

from drf_yasg.openapi import TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from services.payloads.procedures import ProcedurePayload

from .serializers import ProcedureSerializer


class ProcedureIngestView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        consumes=["text/plain"],
        request_body=Schema(
            type=TYPE_STRING,
            example=(
                "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
                "SCH|A1001|PROC123|20250102|093000|120000\n"
                "PID|123456|DOE^JOHN"
            ),
        ),
        responses={
            201: "Procedure created successfully",
            400: "Parsing or validation error occurred",
        },
    )
    def post(self, request):
        """
        Ingest and persist an HL7 procedure scheduling message.

        Returns:
            Response: created procedure and nested patient data
        """
        body = request.body.decode("utf-8")
        parsed = ProcedurePayload.parse(body)

        serializer = ProcedureSerializer(data=asdict(parsed))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
