from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        request = self.context.get('request')
        
        if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
            return data

        user = request.user
        status = data.get('status', AdvertisementStatusChoices.OPEN)

        if status == AdvertisementStatusChoices.OPEN:
            # Считаем открытые объявления текущего пользователя
            open_ads_queryset = Advertisement.objects.filter(
                creator=user, 
                status=AdvertisementStatusChoices.OPEN
            )
            
            # Если это обновление существующего объявления, исключаем его из подсчета
            if self.instance:
                open_ads_queryset = open_ads_queryset.exclude(pk=self.instance.pk)

            if open_ads_queryset.count() >= 10:
                raise serializers.ValidationError(
                    "У вас уже есть 10 открытых объявлений. Закройте одно из них, прежде чем создавать новое или менять статус на 'Открыто'."
                )

        return data
