from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, response, status
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Participant
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from .models import *
from .serializers import *

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })

class RegistrationView(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)


        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)


            return Response({
                'message':'User is registered successfully',
                'access':access_token,
                'refresh':str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParticipantView(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = Participant.objects.filter(id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.id == request.user.id:
            return super().retrieve(request, *args, **kwargs)
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response({'error': 'You can only modify your own profile.'}, status=status.HTTP_403_FORBIDDEN)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id != request.user.id:
         return Response({'error': 'You can only update your own account.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        required_fields = ['name', 'surname', 'age', 'phoneNumber']
        for field in required_fields:
           if field not in data:
             return Response({'error': f"Missing field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id != request.user.id:
            return Response({'error': 'You can only delete your own account.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({'message': 'Participant deleted'}, status=status.HTTP_204_NO_CONTENT)
  

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(event)
        response_data = serializer.data

        # Участники
        event_participant = EventParticipant.objects.filter(event=event).first()
        participants = event_participant.eventParticipants.all() if event_participant else []
        response_data['participants'] = ParticipantSerializer(participants, many=True).data

        # Список ожидающих — только для создателя
        if request.user.id == event.creator.id:
            waiting_list = ListOfWaitingParticipant.objects.filter(event=event)
            response_data['waiting_list'] = ListOfWaitingParticipantSerializer(waiting_list, many=True).data

        # Флаг: может ли текущий пользователь подать заявку
        participant = Participant.objects.filter(user=request.user).first()  # Преобразуем User в Participant
        already_joined = event_participant and event_participant.eventParticipants.filter(id=participant.id).exists()
        already_waiting = ListOfWaitingParticipant.objects.filter(event=event, participant=participant).exists()
        is_creator = request.user.id == event.creator.id
        response_data['can_apply'] = not already_joined and not already_waiting and not is_creator

        return Response(response_data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='join')
    def join_event(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if user == event.creator:
            return Response({'error': 'Creator cannot join their own event.'}, status=status.HTTP_400_BAD_REQUEST)

        event_participant, _ = EventParticipant.objects.get_or_create(event=event)

        if event_participant.eventParticipants.filter(id=user.id).exists():
            return Response({'error': 'Already a participant.'}, status=status.HTTP_400_BAD_REQUEST)

        if ListOfWaitingParticipant.objects.filter(event=event, participant=user).exists():
            return Response({'error': 'Already in waiting list.'}, status=status.HTTP_400_BAD_REQUEST)

        ListOfWaitingParticipant.objects.create(event=event, participant=user)
        return Response({'message': 'Added to waiting list.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='leave')
    def leave_event(self, request, pk=None):
        event = self.get_object()
        user = request.user

        event_participant = EventParticipant.objects.filter(event=event).first()
        if event_participant:
            event_participant.eventParticipants.remove(user)

        ListOfWaitingParticipant.objects.filter(event=event, participant=user).delete()

        return Response({'message': 'You have left the event.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='approve')
    def approve_participant(self, request, pk=None):
        event = self.get_object()

        if request.user.id != event.creator.id:
            return Response({'error': 'Only the creator can approve participants.'}, status=status.HTTP_403_FORBIDDEN)

        participant_id = request.data.get('participant_id')
        if not participant_id:
            return Response({'error': 'participant_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = Participant.objects.get(id=participant_id)
        except Participant.DoesNotExist:
            return Response({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

        event_participant, _ = EventParticipant.objects.get_or_create(event=event)
        if event_participant.eventParticipants.count() >= event.capacity:
            return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)

        ListOfWaitingParticipant.objects.filter(event=event, participant=participant).delete()

        if event_participant.eventParticipants.filter(id=participant.id).exists():
            return Response({'error': 'Already a participant'}, status=status.HTTP_400_BAD_REQUEST)

        event_participant.eventParticipants.add(participant)

        return Response({'message': 'Participant approved and added to event'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='reject')
    def reject_participant(self, request, pk=None):
        event = self.get_object()

        if request.user.id != event.creator.id:
            return Response({'error': 'Only the creator can reject participants.'}, status=status.HTTP_403_FORBIDDEN)

        participant_id = request.data.get('participant_id')
        if not participant_id:
            return Response({'error': 'participant_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = Participant.objects.get(id=participant_id)
        except Participant.DoesNotExist:
            return Response({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = ListOfWaitingParticipant.objects.filter(event=event, participant=participant).delete()
        if deleted:
            return Response({'message': 'Participant rejected and removed from waiting list'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Participant was not in the waiting list'}, status=status.HTTP_400_BAD_REQUEST)


class EventParticipantView(viewsets.ModelViewSet):    
    queryset = EventParticipant.objects.all()   
    serializer_class = EventParticipantSerializer
    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        participant_id = request.data.get('participant')

        try:
            event = Event.objects.get(id=event_id)
            participant = Participant.objects.get(id=participant_id)
        except (Event.DoesNotExist, Participant.DoesNotExist):
            return Response({'error': 'Event or Participant does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if event.creator.id != request.user.id:
            return Response({'error': 'Only creator can add participants'}, status=status.HTTP_403_FORBIDDEN)

        event_participant, created = EventParticipant.objects.get_or_create(event=event)

        if event_participant.eventParticipants.filter(id=participant.id).exists():
            return Response({'error': 'This participant is already in the event'}, status=status.HTTP_400_BAD_REQUEST)

        event_participant.eventParticipants.add(participant)

        return Response({'message': 'Participant added to event'}, status=status.HTTP_201_CREATED)

    

    
    def destroy(self, request, *args, **kwargs):
        event_participant = self.get_object()
        event = event_participant.event
        creator = event.creator

        if creator.id != request.user.id:
            return Response({'error': 'Only the creator can remove participants.'}, status=status.HTTP_403_FORBIDDEN)
        
        participant_id = request.data.get('participant_id')
        try:
            participant = Participant.objects.get(id=participant_id)
            event_participant.eventParticipants.remove(participant)
        except(Participant.DoesNotExist, Event.DoesNotExist):
                return Response({'error':'Event or Participant does not exist'}, status=status.HTTP_404_NOT_FOUND)

                
        return Response({'message': 'Participant removed from event.'}, status=status.HTTP_204_NO_CONTENT)

    
    def list(self, request, *args, **kwargs):
        print('All event participants')
        event_id = self.kwargs.get('id')
        try:
            event = Event.objects.get(id = event_id)
        except(Event.DoesNotExist):
            return Response({'error':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        event_participant = EventParticipant.objects.filter(event=event).first()
        if not event_participant:
            return Response({'participants': []})

        participants = event_participant.eventParticipants.all()
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class ListOfWaitingParticipantView(viewsets.ModelViewSet):
    queryset = ListOfWaitingParticipant.objects.all()
    serializer_class = ListOfWaitingParticipantSerializer
    permission_classes = [IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     event_id = self.kwargs.get('event_id')
    #     try:
    #         event = Event.objects.get(id=event_id)
    #     except Event.DoesNotExist:
    #         return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    #     if event.creator.id != request.user.id:
    #         return Response({'error': 'Only the creator can manage the waiting list.'}, status=status.HTTP_403_FORBIDDEN)

    #     waiting_participants = ListOfWaitingParticipant.objects.filter(event=event)
    #     serializer = self.get_serializer(waiting_participants, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        if not event.isActive:
            return Response({'error': 'Event is inactive, you cannot join.'}, status=status.HTTP_400_BAD_REQUEST)
                
        participant_id = request.data.get('participant_id')
        if not participant_id:
            return Response({'error': 'participant_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = Participant.objects.get(id=participant_id)
        except Participant.DoesNotExist:
            return Response({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

        if ListOfWaitingParticipant.objects.filter(event=event, participant=participant).exists():
            return Response({'error': 'Participant is already on the waiting list'}, status=status.HTTP_400_BAD_REQUEST)

        ListOfWaitingParticipant.objects.create(event=event, participant=participant)
        return Response({'message': 'Participant added to waiting list'}, status=status.HTTP_201_CREATED)

    
