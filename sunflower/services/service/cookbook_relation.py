""" This module provides a class CookBookRelationService for working with
    cookbook relation data at a higher level (with error handling)

    Classes:
    ----------------
        CookBookRelationService
            working with cookbook relation data in database at a higher level
            (with logical error handling)
"""
from typing import List, Set

from sunflower.models.cookbook import CookBook
from sunflower.models.cookbook_relation import CookBookRelation
from sunflower.services import exceptions
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.storage.cookbook_relation import CookBookRelationQuery


class CookBookRelationService(metaclass=LogAllMethods):

    @staticmethod
    def _get_by_cookbooks(cookbook_id: int, subcookbook_id: int):
        return CookBookRelationQuery.get_by_cookbook(cookbook_id,
                                                     subcookbook_id)

    @staticmethod
    def is_duplicated(new_relation: CookBookRelation) -> bool:
        if CookBookRelationService._get_by_cookbooks(new_relation.cookbook_id,
                                                     new_relation.subcookbook_id
                                                     ):
            raise exceptions.DuplicationException(f"Such relation with id "
                                                  f"{new_relation.pk}"
                                                  f" is already exists!")
        return False

    @staticmethod
    def add(cookbook_relation: CookBookRelation) -> CookBookRelation:
        CookBookRelationService.is_duplicated(cookbook_relation)
        return BaseService.add(cookbook_relation)

    @staticmethod
    def get(relation_id: int) -> CookBookRelation:
        return BaseService.get(CookBookRelation, relation_id)

    @staticmethod
    def update(user_id: int, relation_id: int, kwargs) -> CookBookRelation:
        return BaseService.update(CookBookRelation, user_id, relation_id,
                                  kwargs)

    @staticmethod
    def delete(user_id: int, relation_id: int):
        return BaseService.delete(CookBookRelation, user_id, relation_id)

    @staticmethod
    def _get_all_by_parent(cookbook_id: int) -> List[CookBookRelation]:
        return CookBookRelationQuery.get_all_by_parent(cookbook_id)

    @staticmethod
    def _get_all_by_child(subcookbook_id: int) -> List[CookBookRelation]:
        return CookBookRelationQuery.get_all_by_child(subcookbook_id)

    @staticmethod
    def get_all_children(user_id: int, parent_cookbook_id: int) -> Set[int]:

        BaseService.is_object_exist(CookBook, parent_cookbook_id)
        BaseService.is_has_rights(CookBook, user_id, parent_cookbook_id)

        cookbook_relations = CookBookRelationService._get_all_by_parent(
            parent_cookbook_id)

        child_cookbooks = set()
        for relation in cookbook_relations:
            child_cookbooks.add(relation.subcookbook_id)
        return child_cookbooks

    @staticmethod
    def get_all_parent(user_id: int, subcookbook_id: int) -> Set[int]:

        BaseService.is_object_exist(CookBook, subcookbook_id)
        BaseService.is_has_rights(CookBook, user_id, subcookbook_id)

        cookbook_relation = CookBookRelationService._get_all_by_child(
            subcookbook_id)

        parent_cookbook = set()
        for relation in cookbook_relation:
            parent_cookbook.add(relation.cookbook_id)
        return parent_cookbook

    @staticmethod
    def delete_all_relations(user_id: int, cookbook_id: int):
        parent_relations = CookBookRelationService._get_all_by_child(
            cookbook_id)
        for relation in parent_relations:
            CookBookRelationService.delete(user_id, relation.pk)

        child_relations = CookBookRelationService._get_all_by_parent(
            cookbook_id)
        for relation in child_relations:
            CookBookRelationService.delete(user_id, relation.pk)
