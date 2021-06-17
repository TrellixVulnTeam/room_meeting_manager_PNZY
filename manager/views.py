from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from manager.models import MeetingRoom


class AddMeetingRoom(View):
    def get(self, request):
        return render(request, 'add_meeting_room.html')

    def post(self, request):
        name = request.POST.get('name')
        seats = int(request.POST.get('seats'))
        if name is None:
            return render(request, 'add_meeting_room.html', context={'information': 'Invalid name'})
        if seats < 0:
            return render(request, 'add_meeting_room.html', context={'information': 'Invalid seats data'})
        projector = request.POST.get('projector') == 'on'
        check = MeetingRoom.objects.all()
        check = check.filter(name=name)
        if len(check) != 0:
            return render(request, 'add_meeting_room.html', context={'information': 'Name is in use'})
        MeetingRoom.objects.create(name=name, seats=seats, projector=projector)
        return render(request, 'add_meeting_room.html', context={'information': 'Added'})


class MeetingRoomsList(View):
    def get(self, request):
        rooms = MeetingRoom.objects.all()
        return render(request, 'meeting_rooms_list.html', context={'meeting_rooms': rooms})

    def post(self, request):
        pass


class DeleteMeetingRoom(View):
    def get(self, request, room_id):
        room = MeetingRoom.objects.get(id=room_id)
        room.delete()
        return redirect('/room/')


class ModifyMeetingRoom(View):
    def get(self, request, room_id):
        room = MeetingRoom.objects.get(id=room_id)
        seats = int(room.seats)
        projector = 'on' if room.projector is True else ''
        return render(request, 'modify_meeting_room.html', context={'name_value': room.name,
                                                                    'seat_value': seats,
                                                                    'checked_projector': projector})

    def post(self, request, room_id):
        def render_response(response):
            return render(request, 'modify_meeting_room.html', context={'name_value': room.name,
                                                                        'seat_value': seats,
                                                                        'checked_projector': projector,
                                                                        'information': str(response)})

        room = MeetingRoom.objects.get(id=room_id)
        name = request.POST.get('name')
        seats = int(request.POST.get('seats'))
        projector = request.POST.get('projector') == 'on'
        if seats < 0:
            return render_response('Invalid seats data!')
        if name is None:
            return render_response('Invalid name data!')
        find_room = MeetingRoom.objects.all()
        find_room = find_room.filter(name=name)
        if room.id in find_room:
            return render_response('That name is in use!')
        room.name = name
        room.seats = seats
        room.projector = projector
        room.save()
        return redirect('/room/')
