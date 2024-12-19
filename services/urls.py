from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicesViewSet, SpecialistsViewSet, ScheduleViewSet, CreateAppointmentView, AppointmentViewSet,SalonViewSet

router = DefaultRouter()
router.register(r'services', ServicesViewSet, basename='services')
router.register(r'specialists', SpecialistsViewSet, basename='specialists')
router.register(r'schedules', ScheduleViewSet, basename='schedules')
router.register(r'appointments', AppointmentViewSet, basename='appointments')
router.register(r'salons', SalonViewSet, basename='salons')

urlpatterns = [
    path('', include(router.urls)),
    path('appointments-new/create/', CreateAppointmentView.as_view(), name='create-appointment'),
]
