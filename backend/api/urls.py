from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CurrentUserView, ListOfWaitingParticipantView, ParticipantView, RegistrationView, EventView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import EventParticipantView


waiting_list = ListOfWaitingParticipantView.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})


router = DefaultRouter()
router.register(r'events', EventView, basename='events')
router.register(r'register', RegistrationView, basename='register')
router.register(r'participants', ParticipantView, basename='participant')
router.register(r'event-participants', EventParticipantView, basename='event-participants')
router.register(r'event-waiting-list', ListOfWaitingParticipantView, basename='event-waiting-list')


urlpatterns = [
    path('api/user/', CurrentUserView.as_view(), name='user-profile'),
    path('', include(router.urls))
]
