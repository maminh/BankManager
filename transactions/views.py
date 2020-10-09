from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Transaction
from .permissions import HaveAccountPermission
from .serializers import TransactionSerializer


class TransactionViewSet(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [HaveAccountPermission]

    def get_queryset(self):
        return Transaction.objects.filter(account=self.request.user.account)
