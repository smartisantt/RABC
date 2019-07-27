from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:

        response.data['code'] = response.data.get('code') or response.status_code
        if response.data.get('detail'):
            response.data['msg'] = response.data.get('detail')
        if response.data.get('msg'):
            response.data['msg'] = response.data.get('msg')
        else:
            response.data['msg'] = '参数有误'
    return response