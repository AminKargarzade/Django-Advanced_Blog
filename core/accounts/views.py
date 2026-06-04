from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .tasks import sendEmail
import requests

def send_email(request):
    sendEmail.delay()  # This is the syntax how you insert the task into the view! you can give the parameters inside the delay() function like sendEmail.delay(param1, param2)
    return HttpResponse("<h1>Email sent successfully!</h1>")

# def test(request):
#     if cache.get("test_delay_api") is None:
#         response = requests.get("https://755bf7d5-76a0-42f8-a84f-f206c8efc5cf.mock.pstmn.io/test/delay/5")
#         cache.set("test_delay_api", response.json(), 60)  # Cache the response for 60 seconds! You can set it globally in the settings.py file as well using the CACHES variable
#     return JsonResponse(cache.get("test_delay_api"))

@cache_page(60)
def test(request):
    response = requests.get("https://755bf7d5-76a0-42f8-a84f-f206c8efc5cf.mock.pstmn.io/test/delay/5")
    return JsonResponse(response.json())