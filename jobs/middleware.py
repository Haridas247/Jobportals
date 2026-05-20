import time 

# Request logger middleware
class RequestLoggerMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        # __init__ run oce when Django runs, get response is the  next middleware

    def __call__(self,request):
        # runs before the view
        print(f"REQUEST  --. Method: {request.method} | URL: {request.path}")
        response = self.get_response(request)
        print (f"RESPONSE  -->STATUS: {response.status_code} | URL: {request.path}")
        return response

#block IP middleware
BLOCKED_IPS =['192.168.1.100', '10.0.0.1']

class BlockIPMiddleware:
    def __init__(self,get_response):   
        self.get_response = get_response
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip in BLOCKED_IPS:
            # block this IP — never reaches the view
            from django.http import HttpResponseForbidden
            print(f"BLOCKED IP --> {ip} tried to access {request.path}")
            return HttpResponseForbidden("You are blocked from this site.")

    
        response = self.get_response(request)
        return response
#execution timee middleware


class ExecutionTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #record time BEFORE view runs
        start_time = time.time()
        response = self.get_response(request)
        #record time AFTER view runs
        end_time = time.time()
        #calculate how long it took
        duration = end_time - start_time
        print(f"EXECUTION TIME --> {request.path} took {duration:.4f} seconds")

        return response
