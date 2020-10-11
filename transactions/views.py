from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Transaction
from .permissions import HaveAccountPermission
from .serializers import TransactionSerializer


class TransactionViewSet(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    list:
    API View that receives a GET

    Returns a list of transactions made by authenticated user

    retrieve:
    API View that receives a GET

    Returns the transaction's JSON object

    create:
    API View that receives a POST and creates a new transaction

    transaction_type = 1 for withdraw, 2 for deposit

    """
    serializer_class = TransactionSerializer
    permission_classes = [HaveAccountPermission]

    def get_queryset(self):
        return Transaction.objects.filter(account=self.request.user.account)
