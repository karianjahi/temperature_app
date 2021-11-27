from rest_framework.response import Response

from temperature import models
from temperature.lib.serializer import data_by_deserializer_and_model


def errorRespStatusCode(error_msg, status):
    return Response({"message": "error", "details": error_msg}, status=status)


def errorResp(error_msg):
    return Response({"message": "error", "details": error_msg})


def successResp(data, kwargs={}):
    data = {**{"message": "success", "data": data}, **kwargs}
    return Response(data)


def showResp(data, is_empty):
    return Response({"message": "success",
                     "data": data,
                     "isEmpty": is_empty})


def onlySuccessResp():
    return Response({"message": "success"})


