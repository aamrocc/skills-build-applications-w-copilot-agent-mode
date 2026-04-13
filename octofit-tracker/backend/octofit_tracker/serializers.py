from rest_framework import serializers
from .models import User, Team, Activity, Workout, LeaderboardEntry

class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        # Access the MongoDB _id directly
        return getattr(obj, '_id', obj.pk)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        # Access the MongoDB _id directly
        return getattr(obj, '_id', obj.pk)
    
    class Meta:
        model = Team
        fields = ['id', 'name']

class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        # Access the MongoDB _id directly
        return getattr(obj, '_id', obj.pk)
    
    def get_user_name(self, obj):
        try:
            return obj.user.username if obj.user else None
        except:
            return None
    
    def get_team_name(self, obj):
        try:
            return obj.team.name if obj.team else None
        except:
            return None
    
    class Meta:
        model = Activity
        fields = ['id', 'activity_type', 'duration', 'date', 'user_name', 'team_name']

class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        # Access the MongoDB _id directly
        return getattr(obj, '_id', obj.pk)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description']

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        # Access the MongoDB _id directly
        return getattr(obj, '_id', obj.pk)
    
    def get_user_name(self, obj):
        try:
            return obj.user.username if obj.user else None
        except:
            return None
    
    def get_team_name(self, obj):
        try:
            return obj.team.name if obj.team else None
        except:
            return None
    
    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'user_name', 'team_name', 'total_duration']

