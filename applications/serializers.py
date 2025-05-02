from rest_framework import serializers
from django.shortcuts import get_object_or_404
from accounts.serializers import AttachmentSerializer
from applications.models import Application
from common.serializers import EducationPlaceSerializer, ProgramBaseSerializer
from common.models import EducationPlace
from rest_framework.exceptions import NotAcceptable
from .constants import StatusChoices

class ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application


class ApplicationCreateSerializer(serializers.Serializer):
    education_place = serializers.IntegerField()

    def save(self, **kwargs):
        user = self.context['request'].user
        education_place = get_object_or_404(EducationPlace, pk=self.validated_data['education_place'])
        program = education_place.degrees.filter(name=user.degree).first()
        if not user.degree:
            raise NotAcceptable('Программа в профиле пользователя не выбрана')
        if not program:
            raise NotAcceptable(f'В выбранном университете отсутствует программа "{user.degree}"')
        application = Application.objects.filter(program=program,owner=user,
                                      status__in=[StatusChoices.draft, StatusChoices.accepted,
                                                  StatusChoices.for_consideration, StatusChoices.for_revision,
                                                  StatusChoices.in_progress]).first()
        if application:
            return application
        application = Application.objects.create(program=program, **kwargs)

        application.name = f'Заявка №{application.id}'
        application.save()
        return application


class ApplicationListSerializer(ApplicationBaseSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    program = ProgramBaseSerializer(read_only=True)
    education_place = serializers.SerializerMethodField()

    class Meta(ApplicationBaseSerializer.Meta):
        fields = '__all__'

    def get_education_place(self, obj):
        return EducationPlaceSerializer(
            obj.program.education_place).data


class ApplicationRetrieveUpdateSerializer(ApplicationBaseSerializer):
    class Meta(ApplicationBaseSerializer.Meta):
        fields = '__all__'
