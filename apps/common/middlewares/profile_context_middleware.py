from apps.common.constants import ProfileType

class ProfileContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Determine active persona (Header or Cookie)
        persona = request.headers.get('X-Profile-Type') or request.COOKIES.get('active_persona')
        
        # 2. Set Booleans on the request object
        request.is_employer = (persona == ProfileType.EMPLOYER)
        request.is_jobseeker = (persona == ProfileType.JOB_SEEKER)
        
        return self.get_response(request)