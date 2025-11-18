from django.contrib import admin

from .models import User, Exercise, Calendar, WorkOut, WorkoutExercise

admin.site.register(User)
admin.site.register(Calendar)
admin.site.register(WorkOut)
admin.site.register(Exercise)
admin.site.register(WorkoutExercise)