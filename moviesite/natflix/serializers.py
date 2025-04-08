from .models import Movie
from rest_framework import serializers
import base64

class MovieSerializer(serializers.ModelSerializer):
    movie_file = serializers.FileField(write_only=True, required=True)  # Accept binary file on input
    movie_file_base64 = serializers.SerializerMethodField(read_only=True)  # Base64 string on output

    class Meta:
        model = Movie
        fields = ["id", "title", "movie_file", "movie_file_base64", "description", "date_added"]

    def get_movie_file_base64(self, obj):
        request = self.context.get('request')
        if request and request.parser_context.get('kwargs', {}).get('pk'):
            if obj.movie_file:
                return base64.b64encode(obj.movie_file).decode('utf-8')
        return None

    def create(self, validated_data):
        uploaded_file = validated_data.pop('movie_file')
        validated_data['movie_file'] = uploaded_file.read()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        uploaded_file = validated_data.pop('movie_file', None)
        if uploaded_file:
            instance.movie_file = uploaded_file.read()
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
