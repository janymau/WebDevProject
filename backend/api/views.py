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
        if instance.id != request.user.id:
            return Response({'error': 'You can only access your own data.'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'], url_path='waiting-list')
    def waiting_list(self, request, pk=None):
        event = self.get_object()
        if event.creator.id != request.user.id:
            return Response({'error': 'Only the creator can see waiting list.'}, status=status.HTTP_403_FORBIDDEN)
        
        waiting = ListOfWaitingParticipant.objects.filter(event=event)
        serializer = ListOfWaitingParticipantSerializer(waiting, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'], url_path='waiting-list/delete/')
    def delete_from_waiting_list(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        if event.creator.id != request.user.id:
            return Response({'error': 'Only the creator can remove from the waiting list'}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  
        required_fields = ['type', 'place', 'date', 'description', 'capacity']
        
        for field in required_fields:
            if field not in data:
                return Response({'error': f"Missing field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        participant_id = data.get('creator')  
        if not participant_id:
            return Response({'error': 'Missing creator'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            creator = Participant.objects.get(id=participant_id)
        except Participant.DoesNotExist:
            return Response({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        event = serializer.instance
        
        event_participant = EventParticipant.objects.create(event=event)
        event_participant.eventParticipants.add(creator)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def list(self, request, *args, **kwargs):
        print('All events')
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        event = self.get_object()
        if 'isActive' in request.data:
            if event.creator.id != request.user.id:
                return Response({'error': 'Only the creator can deactivate the event.'}, status=status.HTTP_403_FORBIDDEN)
            event.isActive = request.data['isActive']
            event.save()
            return Response({'message': f"Event status updated to {'active' if event.isActive else 'inactive'}."}, status=status.HTTP_200_OK)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event.creator.id != request.user.id:
                return Response({'error': 'Only the creator can destroy the event.'}, status=status.HTTP_403_FORBIDDEN)    
        return super().destroy(request, *args, **kwargs)

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

    
