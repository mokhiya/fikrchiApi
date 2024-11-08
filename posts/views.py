from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import PostModel
from .serializers import PostSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        object = super().get_object()
        if object.user != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this post.")
        return object