from rest_framework import serializers

from .models import User, Exercise, WorkOut, WorkoutExercise, Calendar

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'password']
        extra_kwargs={
            'password': {'write_only': True}
            }
        
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class WorkOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOut
        fields = '__all__'

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = WorkoutExercise
        fields= '__all__'

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'