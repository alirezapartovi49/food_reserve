from datetime import timedelta, datetime

from rest_framework.generics import ListAPIView

from local_extentions.permisions import IsAdminOrReadOnly
from .serializer import FoodDateSerializer
from .models import FoodDate


class FoodsView(ListAPIView):
    """get list of active foods from now to 30 days"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = FoodDateSerializer

    def get_queryset(self):
        now = datetime.now()
        past_30_days = now + timedelta(days=30)
        return FoodDate.objects.filter(
            date__gte=now, date__lte=past_30_days
        ).prefetch_related("food_set")
