from rest_framework import mixins, viewsets


class CreateDestroyListModelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет, предоставляющий возможности для создания и удаления
    экземпляров моделей, а также для получения их в виде списка .
    Доступные методы: `create()`, `destroy()`, `list()`.
    """
    pass
