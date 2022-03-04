from django.http import Http404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from . import serializers
from prediction_models.serializers import PredictionModelSerializer
from prediction_models.prediction_service_client import PredictionServiceClient
from .models import Device
from prediction_models.models import PredictionModel
from infraction_types.models import InfractionType
from infraction_events.permissions import IsPredictionServiceRequest
import boto3
from botocore.config import Config
from django_eventstream import send_event

class RetrieveUpdateDeleteDeviceAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'serial_number'
    serializer_class = serializers.DeviceSerializer
    queryset = Device.objects.all()

    def perform_destroy(self, instance):
        try:
            region = 'us-east-1'
            client = boto3.client(
                'kinesisvideo',
                config=Config(region_name=region),
            )

            client.delete_stream(
                StreamARN=instance.stream_arn
            )
        except:
            raise ValidationError("Failed to delete device stream")
        else:
            instance.infraction_type_models.clear()
            instance.description = ''
            instance.location = None
            instance.stream_arn = ''
            instance.save()

class ListCreatePredictionModelAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PredictionModelSerializer

    def get_queryset(self):
        try:
            account = self.request.user.account
            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=self.kwargs['serial_number'])

            return PredictionModel.objects.filter(device=device)
        except:
            raise Http404('Device not found')

class RetrieveDeletePredictionModelAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PredictionModelSerializer

    def get_queryset(self):
        return PredictionModel.objects.filter(device__location__account=self.request.user.account)

    def get_object(self):
        try:
            account = self.request.user.account

            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=self.kwargs['serial_number'])

            infraction_types = InfractionType.objects.filter(account=account)
            infraction_type = infraction_types.get(id=self.kwargs['infraction_type'])

            return PredictionModel.objects.get(device=device, infraction_type=infraction_type)
        except:
            raise Http404('Could not get prediction model')

class StartCommitInfraction(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, serial_number, infraction_type):
        try:
            account = request.user.account
            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=serial_number)
            infraction_types = InfractionType.objects.filter(account=account)
            infraction_type = infraction_types.get(id=infraction_type)
            prediction_model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)
            isFirstPhase = prediction_model.training_state == PredictionModel.TrainingState.INITIALIZED
            isSecondPhase = prediction_model.training_state == PredictionModel.TrainingState.FIRST_DONE_NOT_COMMITTING_INFRACTION
            if isFirstPhase:
                prediction_model.training_state = PredictionModel.TrainingState.FIRST_COMMITTING_INFRACTION
            elif isSecondPhase:
                prediction_model.training_state = PredictionModel.TrainingState.SECOND_COMMITTING_INFRACTION
            else:
                raise Exception()

            client = PredictionServiceClient(device=device, infraction_type=infraction_type)
            success = client.start_positive()
            if not success:
                raise Exception()

            prediction_model.save()
            return Response({"success": True})
        except:
            raise Http404('Training error')

class DoneCommitInfraction(APIView):
    permission_classes = [IsPredictionServiceRequest]
    authentication_classes = []

    def post(self, request, serial_number, infraction_type):
        try:
            device = Device.objects.get(serial_number=serial_number)
            infraction_type = InfractionType.objects.get(id=infraction_type)
            model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)

            isFirstPhase = model.training_state == PredictionModel.TrainingState.FIRST_COMMITTING_INFRACTION
            isSecondPhase = model.training_state ==  PredictionModel.TrainingState.SECOND_COMMITTING_INFRACTION

            if isFirstPhase:
                model.training_state = PredictionModel.TrainingState.FIRST_DONE_COMMITTING_INFRACTION
            elif isSecondPhase:
                model.training_state = PredictionModel.TrainingState.SECOND_DONE_COMMITTING_INFRACTION
            else:
                raise Exception()
            model.save()

            send_event(
                f'{device.serial_number}_{infraction_type.id}_training_events',
                'message',
                {'update': 'commit_1_done' if isFirstPhase else 'commit_2_done'}
            )

            return Response({"success": True})
        except:
            raise Http404('Training error')

class StartNotCommitInfraction(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, serial_number, infraction_type):
        try:
            account = request.user.account
            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=serial_number)
            infraction_types = InfractionType.objects.filter(account=account)
            infraction_type = infraction_types.get(id=infraction_type)
            prediction_model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)
            isFirstPhase = prediction_model.training_state == PredictionModel.TrainingState.FIRST_DONE_COMMITTING_INFRACTION
            isSecondPhase = prediction_model.training_state == PredictionModel.TrainingState.SECOND_DONE_COMMITTING_INFRACTION
            if isFirstPhase:
                prediction_model.training_state = PredictionModel.TrainingState.FIRST_NOT_COMMITTING_INFRACTION
            elif isSecondPhase:
                prediction_model.training_state = PredictionModel.TrainingState.SECOND_NOT_COMMITTING_INFRACTION
            else:
                raise Exception()

            client = PredictionServiceClient(device=device, infraction_type=infraction_type)
            success = client.start_negative()
            if not success:
                raise Exception()

            prediction_model.save()
            return Response({"success": True})
        except:
            raise Http404('Training error')

class DoneNotCommitInfraction(APIView):
    permission_classes = [IsPredictionServiceRequest]
    authentication_classes = []

    def post(self, request, serial_number, infraction_type):
        try:
            device = Device.objects.get(serial_number=serial_number)
            infraction_type = InfractionType.objects.get(id=infraction_type)
            model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)

            isFirstPhase = model.training_state == PredictionModel.TrainingState.FIRST_NOT_COMMITTING_INFRACTION
            isSecondPhase = model.training_state ==  PredictionModel.TrainingState.SECOND_NOT_COMMITTING_INFRACTION

            if isFirstPhase:
                model.training_state = PredictionModel.TrainingState.FIRST_DONE_NOT_COMMITTING_INFRACTION
            elif isSecondPhase:
                model.training_state = PredictionModel.TrainingState.SECOND_DONE_NOT_COMMITTING_INFRACTION
            else:
                raise Exception()
            model.save()

            send_event(
                f'{device.serial_number}_{infraction_type.id}_training_events',
                'message',
                {'update': 'not_commit_1_done' if isFirstPhase else 'not_commit_2_done'}
            )

            return Response({"success": True})
        except:
            raise Http404('Training error')

class TrainingComplete(APIView):
    permission_classes = [IsPredictionServiceRequest]
    authentication_classes = []

    def post(self, request, serial_number, infraction_type):
        try:
            device = Device.objects.get(serial_number=serial_number)
            infraction_type = InfractionType.objects.get(id=infraction_type)
            model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)

            if model.training_state != PredictionModel.TrainingState.SECOND_DONE_NOT_COMMITTING_INFRACTION:
                raise Exception()

            model.training_state = PredictionModel.TrainingState.TRAINED
            model.save()

            send_event(
                f'{device.serial_number}_{infraction_type.id}_training_events',
                'message',
                {'update': 'model_training_complete'}
            )

            return Response({"success": True})
        except:
            raise Http404('Training error')

class NeedsRetraining(APIView):
    permission_classes = [IsPredictionServiceRequest]
    authentication_classes = []

    def post(self, request, serial_number, infraction_type):
        try:
            device = Device.objects.get(serial_number=serial_number)
            infraction_type = InfractionType.objects.get(id=infraction_type)
            model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)

            if model.training_state != PredictionModel.TrainingState.SECOND_DONE_NOT_COMMITTING_INFRACTION:
                raise Exception()

            model.training_state = PredictionModel.TrainingState.INITIALIZED
            model.save()

            send_event(
                f'{device.serial_number}_{infraction_type.id}_training_events',
                'message',
                {'update': 'model_needs_retraining'}
            )

            return Response({"success": True})
        except:
            raise Http404('Training error')

class StartPredicting(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, serial_number, infraction_type):
        try:
            account = request.user.account
            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=serial_number)
            infraction_types = InfractionType.objects.filter(account=account)
            infraction_type = infraction_types.get(id=infraction_type)
            model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)

            if model.training_state != PredictionModel.TrainingState.TRAINED:
                raise Exception()

            if not model.is_predicting:
                model.is_predicting = True
                model.save()

            client = PredictionServiceClient(device=device, infraction_type=infraction_type)
            success = client.restart_predicting()
            if not success:
                raise Exception()

            return Response({"success": True})
        except:
            raise Http404('Training error')

class PausePredicting(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, serial_number, infraction_type):
        try:
            account = request.user.account
            devices = Device.objects.filter(location__account=account)
            device = devices.get(serial_number=serial_number)
            infraction_types = InfractionType.objects.filter(account=account)
            infraction_type = infraction_types.get(id=infraction_type)
            model = PredictionModel.objects.get(device=device, infraction_type=infraction_type)

            if model.training_state != PredictionModel.TrainingState.TRAINED:
                raise Exception()

            if model.is_predicting:
                model.is_predicting = False
                model.save()

            client = PredictionServiceClient(device=device, infraction_type=infraction_type)
            success = client.stop_predicting()
            if not success:
                raise Exception()

            return Response({"success": True})
        except:
            raise Http404('Training error')
