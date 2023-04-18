from rest_framework.response import Response


class CustomResponse():
    '''
    Custom Response Classs
    '''
    def Success(data, status=200, headers=None):
        data1 = {
            "data": data,
            "errors": "",
            "code": status,
            "status": "Success"
        }
        return Response(data1, status, headers=headers)

    def Failure(error, status=400, headers=None):
        data1 = {
            'data': [],
            'errors': error,
            'code': status,
            'status': 'Failed'
        }
        return Response(data1, status, headers=headers)
