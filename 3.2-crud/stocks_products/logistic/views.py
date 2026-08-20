from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


# Настраиваем класс пагинации
class CustomPagination(PageNumberPagination):
    page_size = 10  # Количество элементов на одной странице
    page_size_query_param = 'page_size' # Позволяет клиенту менять размер страницы (?page_size=20)
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # Получаем базовый queryset
        queryset = super().get_queryset()
        
        # Проверяем, есть ли в URL параметр ?search=...
        search_query = self.request.query_params.get('search')
        
        if search_query:
            # Q-объекты позволяют использовать логическое ИЛИ (|) в фильтрах.
            # __icontains означает "содержит подстроку" без учета регистра.
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
            
        return queryset


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_query = self.request.query_params.get('search')
        # В файле requests-examples.http указан параметр ?products=2 для поиска по ID
        product_id = self.request.query_params.get('products')

        # 1. Поиск по ID продукта (базовое требование из примера запросов)
        if product_id:
            queryset = queryset.filter(positions__product_id=product_id)

        # 2. Поиск по названию или описанию продукта (дополнительное задание)
        # Мы идем через связующую модель 'positions' к полям связанного продукта
        if search_query:
            queryset = queryset.filter(
                Q(positions__product__title__icontains=search_query) |
                Q(positions__product__description__icontains=search_query)
            )

        # ВАЖНО: distinct() удаляет дубликаты из результата.
        # Если на одном складе есть два разных товара, подходящих под поиск "помид",
        # без distinct() этот склад вернется в ответе дважды. distinct() гарантирует уникальность строк.
        if search_query or product_id:
            queryset = queryset.distinct()

        return queryset