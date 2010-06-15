from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed


class CallableClass(type):
    def __new__(cls, name, bases, dct):
        if 'HEAD' not in dct and 'GET' in dct:
            # XXX: this function could possibly be moved out
            # to the global namespace to save memory.
            def HEAD(self, request, *args, **kwargs):
                response = self.GET(request, *args, **kwargs)
                response.content = u''
                return response
            dct['HEAD'] = HEAD

        dct['permitted_methods'] = []
        for method in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE'):
            if hasattr(dct.get(method, None), '__call__'):
                dct['permitted_methods'].append(method)

        return type.__new__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if args and isinstance(args[0], HttpRequest):
            instance = super(CallableClass, cls).__call__()
            return instance.__call__(*args, **kwargs)
        else:
            instance = super(CallableClass, cls).__call__(*args, **kwargs)
            return instance


class View(object):
    __metaclass__ = CallableViewClass

    def __call__(self, request, *args, **kwargs):
        if request.method in self.permitted_methods:
            handler = getattr(self, request.method)
            # XXX: Could possibly check if 'before' returns a response
            # and return that instead.
            self.before(request, args, kwargs)
            return handler(request, *args, **kwargs)

        return HttpResponseNotAllowed(self.permitted_methods)

    def before(self, request, args, kwargs):
        """Override this method to add common functionality to all HTTP method handlers.

        args and kwargs are passed as regular arguments so you can add/remove arguments:
            def before(self, request, args, kwargs):
                kwargs['article'] = get_object_or_404(Article, id=kwargs.pop('article_id')
            def GET(self, request, article): # <== 'article' instead of 'article_id'
                ...
            def POST(delf, request, article): # <== 'article' instead of 'article_id'
                ...
        """
        pass