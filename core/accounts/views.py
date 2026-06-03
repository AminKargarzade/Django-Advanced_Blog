from django.http import HttpResponse, JsonResponse
from .tasks import sendEmail
import requests

def send_email(request):
    sendEmail.delay()  # This is the syntax how you insert the task into the view! you can give the parameters inside the delay() function like sendEmail.delay(param1, param2)
    return HttpResponse("<h1>Email sent successfully!</h1>")

def test(request):
    response = requests.get("https://755bf7d5-76a0-42f8-a84f-f206c8efc5cf.mock.pstmn.io/test/delay/5")
    return JsonResponse(response.json())