from datetime import timedelta, datetime, date

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from local_extentions.permisions import IsAdminOrReadOnly
from .serializer import FoodDateSerializer
from .models import FoodDate


class FoodsView(ListAPIView):
    """در ریسپانس غذاهای ابتدای هفته تا هفت روز بعد ان را برمیگرداند\n
    اگر ابتدای هفته در پارامتر url به نام start-date مشخص نشود زمان لحظه درخواست به عنوان پارامتر در نظر گرفته میشود
    تاریخ باید با فرمت iso به بکند ارسال شود
    """

    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )
    serializer_class = FoodDateSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get("start-date")

        if start_date is None:
            today = date.today()
            # Calculate previous Saturday
            start_date = today - timedelta(days=(today.weekday() + 2) % 7)
        else:
            start_date = datetime.fromisoformat(start_date).date()
            # Adjust to previous Saturday
            start_date = start_date - timedelta(days=(start_date.weekday() + 2) % 7)

        # Get or create all 7 days (Saturday to Friday)
        dates = [start_date + timedelta(days=i) for i in range(7)]
        for day_date in dates:
            FoodDate.objects.get_or_create(date=day_date)

        return (
            FoodDate.objects.filter(
                date__gte=start_date, date__lte=start_date + timedelta(days=6)
            )
            .order_by("date")
            .prefetch_related("food_set")
        )
