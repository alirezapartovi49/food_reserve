from datetime import timedelta, datetime, date

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from local_extentions.permisions import IsAdminOrReadOnly
from .serializer import FoodDateSerializer
from .models import FoodDate


class FoodsView(ListAPIView):
    """در ریسپانس غذاهای ابتدای هفته تا هفت روز بعد ان را برمیگرداند
    اگر ابتدای هفته در پارامتر url به نام start-date مشخص نشود زمان لحظه درخواست به عنوان پارامتر در نظر گرفته میشود
    تاریخ باید با فرمت iso به بکند ارسال شود
    """

    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )
    serializer_class = FoodDateSerializer

    def get_queryset(self):
        filters = {}
        start_date = self.request.query_params.get("start-date")

        if start_date is None:
            today = date.today()
            start_date = today - timedelta(days=(today.weekday() + 2) % 7)
        else:
            start_date = datetime.fromisoformat(start_date).date()

        filters["date__gte"] = start_date
        filters["date__lte"] = start_date + timedelta(days=6)

        return FoodDate.objects.filter(**filters).prefetch_related("food_set")
