
from django.forms import ValidationError
from rest_framework import serializers


def subtitle_validator(file):
    if not file.name.endswith(".srt"):
        raise ValidationError("file should be srt formated")
    return file

