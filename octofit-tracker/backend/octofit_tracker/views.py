from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import User, Team, Activity, Workout, LeaderboardEntry
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, WorkoutSerializer, LeaderboardEntrySerializer
from pymongo import MongoClient

# MongoDB connection
def get_mongodb():
    client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
    return client['octofit_db']

def paginate_results(data, page=1, page_size=10):
    """Simple pagination helper"""
    start = (page - 1) * page_size
    end = start + page_size
    paginated = data[start:end]
    
    return {
        'count': len(data),
        'next': None if end >= len(data) else f'?page={page + 1}',
        'previous': None if page == 1 else f'?page={page - 1}',
        'results': paginated
    }

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': '/api/users/',
        'teams': '/api/teams/',
        'activities': '/api/activities/',
        'workouts': '/api/workouts/',
        'leaderboard': '/api/leaderboard/',
    })

@api_view(['GET'])
def get_users(request):
    """Get all users with direct MongoDB query"""
    db = get_mongodb()
    users = list(db.octofit_tracker_user.find({'is_superuser': False}))
    
    # Convert ObjectIds to strings and format response
    for user in users:
        user['id'] = user.pop('_id')
    
    page = int(request.query_params.get('page', 1))
    return Response(paginate_results(users, page))

@api_view(['GET'])
def get_teams(request):
    """Get all teams with direct MongoDB query"""
    db = get_mongodb()
    teams = list(db.octofit_tracker_team.find({}))
    
    # Convert ObjectIds to strings and format response
    for team in teams:
        team['id'] = team.pop('_id')
    
    page = int(request.query_params.get('page', 1))
    return Response(paginate_results(teams, page))

@api_view(['GET'])
def get_activities(request):
    """Get all activities with direct MongoDB query"""
    db = get_mongodb()
    activities = list(db.octofit_tracker_activity.find({}))
    
    # Convert _id to id and get user/team names from references
    for activity in activities:
        activity['id'] = activity.pop('_id')
        
        # Get user name
        if 'user_id' in activity:
            user = db.octofit_tracker_user.find_one({'_id': activity['user_id']})
            activity['user_name'] = user.get('username') if user else None
        else:
            activity['user_name'] = None
        
        # Get team name
        if 'team_id' in activity:
            team = db.octofit_tracker_team.find_one({'_id': activity['team_id']})
            activity['team_name'] = team.get('name') if team else None
        else:
            activity['team_name'] = None
    
    page = int(request.query_params.get('page', 1))
    return Response(paginate_results(activities, page))

@api_view(['GET'])
def get_workouts(request):
    """Get all workouts with direct MongoDB query"""
    db = get_mongodb()
    workouts = list(db.octofit_tracker_workout.find({}))
    
    # Convert ObjectIds to strings and format response
    for workout in workouts:
        workout['id'] = workout.pop('_id')
    
    page = int(request.query_params.get('page', 1))
    return Response(paginate_results(workouts, page))

@api_view(['GET'])
def get_leaderboard(request):
    """Get leaderboard entries with direct MongoDB query"""
    db = get_mongodb()
    entries = list(db.octofit_tracker_leaderboardentry.find({}).sort('total_duration', -1))
    
    # Convert _id to id and get user/team names from references
    for entry in entries:
        entry['id'] = entry.pop('_id')
        
        # Get user name
        if 'user_id' in entry:
            user = db.octofit_tracker_user.find_one({'_id': entry['user_id']})
            entry['user_name'] = user.get('username') if user else None
        else:
            entry['user_name'] = None
        
        # Get team name
        if 'team_id' in entry:
            team = db.octofit_tracker_team.find_one({'_id': entry['team_id']})
            entry['team_name'] = team.get('name') if team else None
        else:
            entry['team_name'] = None
    
    page = int(request.query_params.get('page', 1))
    return Response(paginate_results(entries, page))

# Keep ViewSets for any other functionality
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny]

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.AllowAny]

class LeaderboardEntryViewSet(viewsets.ModelViewSet):
    queryset = LeaderboardEntry.objects.all().order_by('-total_duration')
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [permissions.AllowAny]
