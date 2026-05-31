from django.http import HttpResponse
from .tasks import sendEmail


def send_email(request):
    sendEmail.delay()  # This is the syntax how you insert the task into the view! you can give the parameters inside the delay() function like sendEmail.delay(param1, param2)
    return HttpResponse("<h1>Email sent successfully!</h1>")
