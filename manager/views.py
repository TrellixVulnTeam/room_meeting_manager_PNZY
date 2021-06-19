from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from manager.models import MeetingRoom, Reservation
from datetime import timedelta, date


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
        today_reservations = Reservation.objects.filter(date=date.today())
        reserved_rooms = []
        for today_reservation in today_reservations:
            reserved_rooms.append(today_reservation.id_meeting_room.id)
        return render(request, 'meeting_rooms_list.html', context={'meeting_rooms': rooms,
                                                                   'reserved_rooms': reserved_rooms})


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


class MakeReservation(View):
    def get(self, request, room_id):
        room = MeetingRoom.objects.get(id=room_id)
        reservations = Reservation.objects.filter(id_meeting_room__name=room.name).order_by('date')
        return render(request, 'meeting_room_reservation.html', context={'reservations': reservations})

    def post(self, request, room_id):
        reservation_date = date.fromisoformat(request.POST.get('date'))
        if reservation_date < date.today():
            return redirect('/room/')
        comment = request.POST.get('comment')
        room = MeetingRoom.objects.get(id=room_id)
        reservations = Reservation.objects.filter(id_meeting_room__name=room.name)
        for reservation in reservations:
            if reservation_date == reservation.date:
                return redirect('/room/')
            else:
                Reservation.objects.create(date=reservation_date, comment=comment, id_meeting_room_id=room_id)
                return redirect('/room/')


class MeetingRoomDetails(View):
    def get(self, request, room_id):
        room = MeetingRoom.objects.get(id=room_id)
        reservations = Reservation.objects.filter(id_meeting_room__name=room.name).order_by('date')
        return render(request, 'meeting_room_details.html', context={'room': room, 'reservations': reservations})
