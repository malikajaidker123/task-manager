from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    # ViewSet for viewing and editing tasks.
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        # This view returns a list of all the tasks for the currently authenticated user.
        return Task.objects.filter(owner=self.request.user)



    def perform_create(self, serializer):
        # The owner is automatically set to the current user when creating a task.
        serializer.save(owner=self.request.user)


    def destroy(self, request, *args, **kwargs):
        # Return a clearer error when the task is not found on DELETE.
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"detail": f"Task with id {kwargs.get('pk')} not found"}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        # Custom action to toggle the completed status of a task.
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
