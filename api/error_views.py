from django.http import HttpResponse
import json


def not_found(request, template_name = ""):
    response = {}
    response['status'] = 404
    response['message'] = "not found"
    return HttpResponse(json.dumps(response), content_type="application/json", status=404)

def forbidden(request, template_name = ""):
    response = {}
    response['status'] = 401
    response['message'] = "forbidden"
    return HttpResponse(json.dumps(response), content_type="application/json", status=401)

def server_error(request, template_name = ""):
    response = {}
    response['status'] = 500
    response['message'] = "internal server error"
    return HttpResponse(json.dumps(response), content_type="application/json", status=500)