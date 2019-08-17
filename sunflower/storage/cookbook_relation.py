from sunflower.models.cookbook_relation import CookBookRelation
from sunflower.storage.base_query import BaseQuery


class CookBookRelationQuery(BaseQuery):

    def add(self, cookbook_relation: CookBookRelation) -> CookBookRelation:
        return BaseQuery.add(cookbook_relation)

    def get(self, relation_id: int) -> CookBookRelation:
        return BaseQuery.get(CookBookRelation, relation_id)

    def update(self, relation_id: int, kwargs):
        return BaseQuery.update(CookBookRelation, relation_id, kwargs)

    def delete(self, relation_id: int):
        return BaseQuery.delete(CookBookRelation, relation_id)

    @staticmethod
    def get_by_cookbook(cookbook_id: int, subcookbook_id: int):
        return CookBookRelation.objects.filter(cookbook_id=cookbook_id,
                                               subcookbook_id=subcookbook_id)

    @staticmethod
    def get_all_by_parent(cookbook_id: int):
        return CookBookRelation.objects.filter(cookbook_id=cookbook_id)

    @staticmethod
    def get_all_by_child(subcookbook_id: int):
        return CookBookRelation.objects.filter(subcookbook_id=subcookbook_id)
