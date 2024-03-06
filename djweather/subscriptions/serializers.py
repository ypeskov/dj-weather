from datetime import datetime, timezone, timedelta

from rest_framework import serializers

from icecream import ic

from core.responses.exceptions.exceptions import ApiException
from .models import Subscription
from .models import period_choices


class SubscriptionSerializer(serializers.ModelSerializer):
    period_hours = serializers.IntegerField()

    class Meta:
        model = Subscription
        fields = ['id', 'city', 'period_hours']

    def validate_period_hours(self, value):
        if value not in [choice[0] for choice in period_choices]:
            possible_period_hours = ','.join([str(choice[0]) for choice in period_choices])
            raise ApiException(
                error_code='INVALID_INPUT',
                status_code=400,
                message=f'Period hours must be one of the following: {possible_period_hours}',
                details={'period_hours': value}
            )
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        city = attrs['city']

        if Subscription.objects.filter(user=user, city=city).exists():
            raise ApiException(
                error_code='SUBSCRIPTION_ALREADY_EXISTS',
                status_code=400,
                message='Subscription with this user, already exists',
                details={'username': user.username, 'city': city}
            )
        return attrs

    def save(self, **kwargs):
        request = self.context.get('request')
        user = request.user
        city = self.validated_data['city']
        period_hours = self.validated_data['period_hours']

        current_datetime = datetime.now(timezone.utc)
        next_notification_datetime = current_datetime + timedelta(hours=period_hours)

        subscription = Subscription(user=user,
                                    city=city,
                                    next_notification_datetime=next_notification_datetime,
                                    period_hours=period_hours)
        subscription.save()

        return subscription
