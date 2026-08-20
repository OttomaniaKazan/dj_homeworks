from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField автоматически проверит, существует ли продукт с таким ID в базе,
    # и преобразует число из JSON (например, "product": 2) в реальный объект Product для ORM.
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    # Указываем, что поле positions может содержать много объектов и не является обязательным при создании
    positions = ProductPositionSerializer(many=True, required=False)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # 1. "Вынимаем" данные о позициях из общего словаря validated_data.
        # Если их нет, возвращаем пустой список, чтобы избежать ошибки NoneType.
        positions_data = validated_data.pop('positions', [])

        # 2. Создаем сам объект Склада (Stock). 
        # Мы делаем это ДО создания позиций, потому что нам нужен id созданного склада 
        # для привязки к нему товаров в промежуточной таблице.
        stock = super().create(validated_data)

        # 3. Проходимся по каждому словарю с данными позиции и создаем запись в StockProduct.
        # pos_data уже содержит ключи 'product' (как объект модели), 'quantity', 'price'
        for pos_data in positions_data:
            StockProduct.objects.create(stock=stock, **pos_data)

        return stock

    def update(self, instance, validated_data):
        # 1. "Вынимаем" данные о позициях. Используем .pop с дефолтным None, 
        # чтобы отличить ситуацию "поле не пришло в запросе" от "пришел пустой список".
        positions_data = validated_data.pop('positions', None)

        # 2. Обновляем основные поля склада (например, address), если они были переданы.
        stock = super().update(instance, validated_data)

        # 3. Если данные о позициях были переданы в запросе, обновляем их.
        if positions_data is not None:
            for pos_data in positions_data:
                # update_or_create ищет запись по указанным критериям (stock и product).
                # Если находит - обновляет поля из словаря defaults.
                # Если не находит - создает новую запись.
                # Это предотвращает дублирование товаров на одном и том же складе при PATCH-запросах.
                StockProduct.objects.update_or_create(
                    stock=instance,
                    product=pos_data['product'],
                    defaults={
                        'quantity': pos_data.get('quantity', 1),
                        'price': pos_data['price']
                    }
                )
        
        return stock