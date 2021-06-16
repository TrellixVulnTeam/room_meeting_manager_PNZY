from django.shortcuts import render

# Create your views here.
from django.views import View
from manager.models import MeetingRoom


class AddMeetingRoom(View):
    def get(self, request):
        return render(request, 'add_meeting_room.html')

    def post(self, request):
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        projector = request.POST.get('projector') == 'on'
        return render(request, 'add_meeting_room.html', context={'information': 'Added'})
