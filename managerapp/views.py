from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin, RetrieveModelMixin
from .serializers import TransactionSerializer, TransactionAdminSerializer
from .models import Transaction
from .filters import TransactionFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView

class TransactionViewSet(GenericViewSet, 
                  ListModelMixin, 
                  UpdateModelMixin,
                  DestroyModelMixin,
                  CreateModelMixin,
                  RetrieveModelMixin):

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    filterset_class = TransactionFilter
    search_fields = ('id')
    ordering_fields = ('datetime', 'money_amount')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        Transaction.objects.get(id=serializer.data['id']).set_user(user=request.user)
        request.user.recount_balance()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        request.user.recount_balance()
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return TransactionAdminSerializer
        return TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(user__id=self.request.user.id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        request.user.recount_balance()
        return super().destroy(request, *args, **kwargs)

class StatisticsAPIView(APIView):
    def get(self, request):
        statistics = request.user.get_statistics()
        return Response(statistics)