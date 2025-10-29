from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ========== ZONE ==========
class Zone(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# ========== BUILDING ==========
class Building(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=150)
    floors = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('zone', 'name')  # same zone cannot contain two buildings with same name

    def __str__(self):
        return f"{self.name} ({self.zone})"

# ========== DIVISION ==========
class Division(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='divisions')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    # Management assistant assignment:
    # Stores which user (staff/assistant) is responsible for this division.
    assistant = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='assigned_divisions',
        help_text="Management assistant assigned to this division (optional)."
    )

    def __str__(self):
        return f"{self.name} - {self.building.name}"

# ========== TASK (under Division) ==========
class Task(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # status/priority fields can be added later (e.g., completed boolean, priority int)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.division})"

# ========== SUBTASK (under Task) ==========
class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title} [{self.task.title}]"
