
from rest_framework.renderers import JSONRenderer


class MyJsonRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:

            code = data.pop('code')
            msg = data.pop('msg')
            res = {
                'code': code,
                'msg': msg,
            }
            renderer_context['response'].status_code = 400
        except:
            # 表示程序是正常运行的，需自己组装code和msg参数
            code = 200
            msg = 'OK'
            renderer_context['response'].status_code = 200
            res = {
                'code': code,
                'msg': msg,
                'data': data
            }
        return super().render(res)

