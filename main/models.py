from django.db import models

from django.contrib.auth.models import AbstractUser

from django.conf import settings

class User(AbstractUser):
    avatar=models.ImageField(upload_to="avatars/", blank=True, null=True)
    experience=models.IntegerField(default=0)

    class Meta:

        verbose_name='User'

        verbose_name_plural="Users"

    def __str__(self):
        return self.username
    
     

class Exercise(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(
        max_length=50, 
        choices=[
            ("Груди","Груди"),
            ("Спина","Спина"),
            ("Руки","Руки"),
            ("Плечі","Плечі"),
            ("Ноги","Ноги"),
            ("Кор","Кор")

        ]                      
        )
    descriptions=models.TextField(blank=True, null=True)
    dificulty=models.IntegerField(default=1)
    image=models.ImageField(upload_to='media/')


class WorkOut(models.Model):
    user=models.ForeignKey("User", on_delete=models.CASCADE, related_name="workouts")
    date=models.DateField()
    title=models.CharField(max_length=100)


    def __str__(self):
        return f"{self.title} ({self.date})"
    

class WorkoutExercise(models.Model):
    workout=models.ForeignKey(WorkOut, on_delete=models.CASCADE, related_name="media")
    exercise=models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets=models.IntegerField(default=4)
    reps=models.IntegerField(default=8)
    weight=models.FloatField(default=5)


    def __str__(self):
        return f"{self.exercise.name} ({self.sets}x{self.reps})"
    


class Calendar(models.Model):
    STATUS_CHOICES=[
        ("planned", "Заплановано"),
        ("done", "Зроблено"),
        ("skipped", "Пропущено"),
    ]
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="calendar", on_delete=models.CASCADE)
    date=models.DateField()
    note=models.TextField(blank=True, null=True)
    ratings=models.FloatField(default=0)
    status=models.CharField(max_length=30, choices=STATUS_CHOICES, default="planned")

    class Meta:
        unique_together=("user", "date")

    def __str__(self):
        return f"{self.user.username} - {self.date} [{self.status}]"
    


