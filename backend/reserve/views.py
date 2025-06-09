import datetime

from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .serilizers import ReserveSerializer, Today404OutputSerializer
from accounts.models import Student
from food.models import FoodDate
from .models import Reserve


class ReserveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReserveSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return (
                Reserve.objects.none()
            )  # just for OpenAPI Type hint error of reqquest.user not found

        filters = {"user": self.request.user}

        if self.action == "list":
            start_date_str = self.request.query_params.get("start-date")
            if start_date_str:
                try:
                    start_date = datetime.datetime.fromisoformat(start_date_str).date()
                    end_date = start_date + datetime.timedelta(days=6)
                    filters["date__range"] = [start_date, end_date]
                except ValueError:
                    pass

        return Reserve.objects.filter(**filters).order_by("date")

    def perform_create(self, serializer):
        date_food_count_is_valid = self.validate_date_food_count(serializer)
        if not date_food_count_is_valid:
            raise ValidationError("انتخاب های روزانه شما پر شده است")

        food_date_is_valid = self.validate_food_date(serializer)
        if food_date_is_valid:
            serializer.save()
        else:
            raise ValidationError(
                "تاریخ انتخابی با غذای انتخابی هماهنگ نیست یا تعریف نشده است"
            )

    def validate_food_date(self, serializer: ReserveSerializer):
        food_id = serializer.validated_data["food"].id
        date = serializer.validated_data["date"]

        food_date_is_valid = FoodDate.objects.filter(
            date=date,
            food__pk=food_id,
        ).exists()
        return food_date_is_valid

    def validate_date_food_count(self, serializer: ReserveSerializer):
        date = serializer.validated_data["date"]
        user_date_reserves = Reserve.objects.filter(
            user=self.request.user, date=date
        ).count()

        student = (
            Student.objects.filter(user=self.request.user).only("has_dormitory").first()
        )

        if student is None:
            return user_date_reserves < 1

        has_dormitory = student.has_dormitory
        if has_dormitory:
            return user_date_reserves < 2
        else:
            return user_date_reserves < 1


class TodayView(APIView):
    """reurn today reserved foods"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses={200: ReserveSerializer, 404: Today404OutputSerializer})
    def get(self, request, *args, **kwargs):
        today_reserves = self.get_queryset(request)

        if len(today_reserves) < 1:
            raise NotFound("رزروی برای امروز پیدا نشد")
        else:
            serializer = ReserveSerializer(today_reserves, many=True)
            response = Response(data=serializer.data)

        return response

    def get_queryset(self, request):
        queryset = Reserve.objects.filter(
            user=request.user, date=datetime.datetime.now()
        )
        return queryset
