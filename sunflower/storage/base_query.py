class BaseQuery:

    @staticmethod
    def add(model_object):
        model_object.save()
        return model_object

    @staticmethod
    def get(model, object_id: int):
        return model.objects.get(pk=object_id)

    @staticmethod
    def get_or_create(model, kwargs):
        return model.objects.get_or_create(**kwargs)

    @staticmethod
    def get_all(model):
        return model.objects.all()

    @staticmethod
    def _get_query(model, object_id: int):
        return model.objects.filter(pk=object_id)

    @staticmethod
    def update(model, object_id: int, kwargs: dict):
        object_query = BaseQuery._get_query(model, object_id)
        object_query.update(**kwargs)
        return object_query[0]

    @staticmethod
    def _delete_object(object_):
        object_.delete()

    @staticmethod
    def delete(model, object_id: int):
        object_ = BaseQuery.get(model, object_id)
        return BaseQuery._delete_object(object_)

    @staticmethod
    def is_duplication(model, kwargs):
        return model.objects.filter(**kwargs).first() is not None
