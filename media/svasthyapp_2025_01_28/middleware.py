from django.utils.deprecation import MiddlewareMixin

class RemoveServerHeaderMiddleware(MiddlewareMixin):
    # def process_response(self, request, response):
    #     # Remove the 'Server' header
    #     print(response, 'responseresponseresponse')
        
    #     response.headers.pop('Server', None)
    #     # Optionally, set a custom value
    #     # response['Server'] = 'Custom Server Name'  # Uncomment to set a custom server name

    #     return response
    def process_response(self, request, response):
        # print(type(response), 'response.headers')
        if 'Content-Type' in response.headers:
            # print(True, 'data right')
            del response.headers['Content-Type']

        else:
            pass
            # print(False, 'Data false')

        # if 'Server' in response.headers:
        #     del response.headers['Server']
        
        return response


