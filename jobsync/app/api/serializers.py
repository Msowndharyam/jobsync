from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ..models import User, JobListing, JobApplication, Skill

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'password', 'role', 'job_title']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class JobListingSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True)

    class Meta:
        model = JobListing
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobListingSerializer()

    class Meta:
        model = JobApplication
        fields = '__all__'
class JobRecommendationSerializer(serializers.ModelSerializer):
    match_count = serializers.IntegerField(required=False)

    class Meta:
        model = JobListing
        fields = ['id', 'title', 'company', 'location', 'description', 'match_count']

class DashboardSerializer(serializers.Serializer):
    total_jobs_posted = serializers.IntegerField()
    total_applications_received = serializers.IntegerField()
    total_applications_sent = serializers.IntegerField()
