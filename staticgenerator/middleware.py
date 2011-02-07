import re
from django.conf import settings
from staticgenerator import StaticGenerator

class StaticGeneratorMiddleware(object):
    """
    This requires settings.STATIC_GENERATOR_URLS tuple to match on URLs
    
    Example::
        
        STATIC_GENERATOR_URLS = (
            r'^/$',
            r'^/blog',
        )
        
    """
    urls = tuple([re.compile(url) for url in settings.STATIC_GENERATOR_URLS])
    excluded_urls = tuple([re.compile(url) for url in getattr(settings, 'STATIC_GENERATOR_EXCLUDE_URLS', [])])
    gen = StaticGenerator()
    
    def process_response(self, request, response):
        if response.status_code == 200:
            if getattr(settings, 'STATIC_GENERATOR_ANONYMOUS_ONLY', False) and not request.user.is_anonymous():
                return response

            if not getattr(settings, 'STATIC_GENERATOR_IGNORE_GET_PARAMS', False) and len(request.GET) is not 0:
                return response

            excluded = False
            for url in self.excluded_urls:
                if url.match(request.path_info):
                    excluded = True
                    break

            if not excluded:
                for url in self.urls:
                    if url.match(request.path_info):
                        self.gen.publish_from_path(request.path_info, response.content)
                        break

        return response
