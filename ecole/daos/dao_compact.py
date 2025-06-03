# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""
import abc

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple, TypeVar





@dataclass
class DaoCompact[T](Dao[T]):


    def from_dao(self) -> Optional[Dao[Any]]:
        ...

    @abc.abstractmethod
    def get_table(self) -> str:
        """Obtient le nom de la table, non protégé contre les injections sql"""
        ...

    @abc.abstractmethod
    def get_primary_key(self) -> str:
        """Obtient le nom de la clé primaire, non protégé contre les injections sql"""
        ...

    @abc.abstractmethod
    def get_fields(self, with_id: bool) -> List[str]:
        """Get field's names, non protégé contre les injections les injections sql"""
        ...

    def _values_replace(self, with_id: bool) -> str:
        fs = []
        for e in self.get_fields(with_id):
            fs.append(f"%({e})")
        return ",".join(fs)

    def _values(self, object: T, with_id: bool) -> Dict[str, Any]:
        fs = {}
        for e in self.get_fields(with_id):
            if "id" in object.__getattribute__(e).__dict__:
                fs[e] = object.__getattribute__(e).__getattribute__("id")
            else:
                fs[e] = object.__getattribute__(e)
        return fs


    def _columns(self, with_id: bool) -> str:
        return str.join(",", self.get_fields(with_id))

    def create(self, course: T) -> int:
        """Crée en BD l'entité Course correspondant au cours obj

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = f"INSERT INTO {self.get_table()} ({self._columns(False)}) VALUES ({self._values_replace(False)})"
            cursor.execute(sql, self._values(course, False))
            result: Dict[str, Any] = cursor.fetchone()
            return result[self.get_primary_key()]


    def update(self, course: T) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sets = []
            for z in self.get_fields(False):
                sets.append(f"{z} = '%({z})'")
            sql = f"UPDATE {self.get_table()} SET {",".join(z)} WHERE {self.get_primary_key()}=%(id)"
            return cursor.execute(sql, (id,)) != 0

    def delete(self, course: T) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sets = []
            for z in self.get_fields(False):
                sets.append(f"{z} = '%({z})'")
            sql = f"DELETE FROM {self.get_table()} WHERE {self.get_primary_key()}=%s"
            return cursor.execute(sql, (course.__getattribute__(self.get_primary_key()),)) != 0
