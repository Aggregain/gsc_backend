from collections import defaultdict
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        fields_err = defaultdict(str)
        if isinstance(exc.detail, dict):
            for field, detail in exc.detail.items():
                if isinstance(detail, list) and detail:
                    fields_err[field] = str(detail[0])
                else:
                    fields_err[field] = str(detail)
        elif isinstance(exc.detail, list):
            fields_err['non_field_errors'] = str(exc.detail[0])

        return Response({'detail': fields_err}, status=status.HTTP_400_BAD_REQUEST)

    return response
