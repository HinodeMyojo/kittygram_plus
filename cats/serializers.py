import datetime as dt
import webcolors

from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat, Owner


class Hex2NameColor(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени!')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name') 


class CatSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    color = Hex2NameColor()

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements', 'age')

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
            # Если в исходном запросе не было поля achievements
            if 'achievements' not in self.initial_data:
                # То создаём запись о котике без его достижений
                cat = Cat.objects.create(**validated_data)
                return cat

            # Иначе делаем следующее:
            # Уберём список достижений из словаря validated_data и сохраним его
            achievements = validated_data.pop('achievements')
            # Сначала добавляем котика в БД
            cat = Cat.objects.create(**validated_data)
            # А потом добавляем его достижения в БД
            for achievement in achievements:
                current_achievement, status = Achievement.objects.get_or_create(
                    **achievement)
                # И связываем каждое достижение с этим котиком
                AchievementCat.objects.create(
                    achievement=current_achievement, cat=cat)
            return cat


class OwnerSerializer(serializers.ModelSerializer):

    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')

