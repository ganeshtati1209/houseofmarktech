from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.core.cache import cache
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        priority = self.request.query_params.get('priority', None)
        status = self.request.query_params.get('status', None)

        cache_key = f"tasks_{user.id}_{priority}_{status}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        queryset = Task.objects.filter(user=user)

        if priority:
            queryset = queryset.filter(priority=priority)

        if status:
            queryset = queryset.filter(status=status)

        cache.set(cache_key, queryset, timeout=60)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
import heapq

class TaskScheduler:
    def __init__(self):
        self.task_queue = []

    def add_task(self, task):
        heapq.heappush(self.task_queue, (self.get_priority_value(task.priority), task.created_at, task))

    def get_tasks(self):
        return [heapq.heappop(self.task_queue)[2] for _ in range(len(self.task_queue))]

    def get_priority_value(self, priority):
        priority_mapping = {'high': 1, 'medium': 2, 'low': 3}
        return priority_mapping.get(priority, 3)

task_scheduler = TaskScheduler()
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        for task in queryset:
            task_scheduler.add_task(task)

        return task_scheduler.get_tasks()
