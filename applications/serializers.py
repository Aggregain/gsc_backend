from rest_framework import serializers

from accounts.serializers import AttachmentSerializer
from applications.models import Application
from common.serializers import EducationPlaceSerializer, ProgramBaseSerializer


class ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application


class ApplicationCreateSerializer(ApplicationBaseSerializer):
    class Meta(ApplicationBaseSerializer.Meta):
        exclude = ('owner', 'assignee', 'status', 'name',)

    def save(self, **kwargs):
        application = super().save(**kwargs)
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
