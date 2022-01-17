from rest_framework import permissions
from config.settings import CREATE_INFRACTION_EVENT_KEY

class IsPredictionServiceRequest(permissions.BasePermission):
  def has_permission(self, request, _):
    print('poop')
    if 'HTTP_X_CREATE_INFRACTION_EVENT_KEY' in request.META:
      return request.META['HTTP_X_CREATE_INFRACTION_EVENT_KEY'] == CREATE_INFRACTION_EVENT_KEY
    return False
