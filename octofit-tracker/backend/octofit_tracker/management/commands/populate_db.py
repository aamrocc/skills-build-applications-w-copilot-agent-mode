from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        try:
            client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
            db = client['octofit_db']
            
            # Drop collections to reset
            db.octofit_tracker_team.drop()
            db.octofit_tracker_activity.drop()
            db.octofit_tracker_workout.drop()
            db.octofit_tracker_leaderboardentry.drop()
            db.octofit_tracker_user.delete_many({'is_superuser': False})
            
            self.stdout.write('✓ Cleared existing data')
            
            # Create Teams with integer IDs
            teams_data = [
                {'_id': 1, 'name': 'Team Marvel'},
                {'_id': 2, 'name': 'Team DC'},
            ]
            db.octofit_tracker_team.insert_many(teams_data)
            self.stdout.write('✓ Created teams: Marvel, DC')

            # Create Users with integer IDs
            users_data = [
                {
                    '_id': 1,
                    'username': 'spiderman',
                    'email': 'spiderman@marvel.com',
                    'first_name': 'Peter',
                    'last_name': 'Parker',
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False,
                    'password': 'pbkdf2_sha256$720000$dummy',
                    'last_login': None,
                    'date_joined': date.today().isoformat()
                },
                {
                    '_id': 2,
                    'username': 'ironman',
                    'email': 'ironman@marvel.com',
                    'first_name': 'Tony',
                    'last_name': 'Stark',
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False,
                    'password': 'pbkdf2_sha256$720000$dummy',
                    'last_login': None,
                    'date_joined': date.today().isoformat()
                },
                {
                    '_id': 3,
                    'username': 'wonderwoman',
                    'email': 'wonderwoman@dc.com',
                    'first_name': 'Diana',
                    'last_name': 'Prince',
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False,
                    'password': 'pbkdf2_sha256$720000$dummy',
                    'last_login': None,
                    'date_joined': date.today().isoformat()
                },
                {
                    '_id': 4,
                    'username': 'batman',
                    'email': 'batman@dc.com',
                    'first_name': 'Bruce',
                    'last_name': 'Wayne',
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False,
                    'password': 'pbkdf2_sha256$720000$dummy',
                    'last_login': None,
                    'date_joined': date.today().isoformat()
                },
            ]
            db.octofit_tracker_user.insert_many(users_data)
            self.stdout.write('✓ Created 4 users')

            # Create Activities with integer IDs
            activities_data = [
                {'_id': 1, 'user_id': 1, 'activity_type': 'Running', 'duration': 30, 'date': date.today().isoformat(), 'team_id': 1},
                {'_id': 2, 'user_id': 2, 'activity_type': 'Cycling', 'duration': 45, 'date': date.today().isoformat(), 'team_id': 1},
                {'_id': 3, 'user_id': 3, 'activity_type': 'Swimming', 'duration': 25, 'date': date.today().isoformat(), 'team_id': 2},
                {'_id': 4, 'user_id': 4, 'activity_type': 'Yoga', 'duration': 40, 'date': date.today().isoformat(), 'team_id': 2},
            ]
            db.octofit_tracker_activity.insert_many(activities_data)
            self.stdout.write('✓ Created 4 activities')

            # Create Leaderboard Entries with integer IDs
            leaderboard_data = [
                {'_id': 1, 'user_id': 1, 'team_id': 1, 'total_duration': 100},
                {'_id': 2, 'user_id': 2, 'team_id': 1, 'total_duration': 90},
                {'_id': 3, 'user_id': 3, 'team_id': 2, 'total_duration': 110},
                {'_id': 4, 'user_id': 4, 'team_id': 2, 'total_duration': 95},
            ]
            db.octofit_tracker_leaderboardentry.insert_many(leaderboard_data)
            self.stdout.write('✓ Created 4 leaderboard entries')

            # Create Workouts with integer IDs
            workouts_data = [
                {'_id': 1, 'name': 'Full Body', 'description': 'Full body workout with cardio and strength training'},
                {'_id': 2, 'name': 'Cardio Blast', 'description': 'Intense cardio workout to boost endurance'},
                {'_id': 3, 'name': 'Yoga Flow', 'description': 'Relaxing yoga session for flexibility'},
                {'_id': 4, 'name': 'HIIT Training', 'description': 'High-intensity interval training for maximum burn'},
            ]
            db.octofit_tracker_workout.insert_many(workouts_data)
            self.stdout.write('✓ Created 4 workouts')

            self.stdout.write(self.style.SUCCESS('✓ Database populated successfully with sample data!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            import traceback
            traceback.print_exc()

