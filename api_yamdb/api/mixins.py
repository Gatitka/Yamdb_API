from rest_framework import mixins


class CreateDestroyListModelMixin(mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.ListModelMixin):
    """
    Миксин, предоставляющий возможности для создания и удаления
    экземпляров моделей, а также для получения их в виде списка .
    Доступные методы: `create()`, `destroy()`, `list()`.
    """
    pass
