from django.http import HttpResponseRedirect


class RedirectMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Verificar si la solicitud se hace a 127.0.0.1:8000
    if request.META['HTTP_HOST'] == '127.0.0.1:8000':
      # Verificar si la solicitud no está en /admin/
      if not (request.path.startswith('/admin/')):
        return HttpResponseRedirect('/admin/')

    return self.get_response(request)
