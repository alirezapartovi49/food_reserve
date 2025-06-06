import datetime

from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serilizers import ReserveSerializer
from accounts.models import Student
from food.models import FoodDate
from .models import Reserve


class ReserveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReserveSerializer

    def get_queryset(self):
        queryset = Reserve.objects.filter(user=self.request.user)
        return queryset

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

        has_dormitory: bool = student.has_dormitory
        if has_dormitory:
            return user_date_reserves < 2
        else:
            return False


class TodayView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        today_reserves = self.get_queryset(request)

        if len(today_reserves) < 1:
            response = Response(data={"status": 404})
            response.status_code = 404
        else:
            serializer = ReserveSerializer(today_reserves, many=True)
            response = Response(data=serializer.data)

        return response

    def get_queryset(self, request):
        queryset = Reserve.objects.filter(
            user=request.user, date=datetime.datetime.now()
        )
        return queryset
