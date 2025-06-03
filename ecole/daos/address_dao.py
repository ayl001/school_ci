import copy
from dataclasses import dataclass
from typing import Optional, Dict, Any

#from daos.addresse_dao import addresseDao
from daos.dao import Dao
from daos.person_dao import PersonDao
from models.address import Address
from models.person import Person
from models.student import Student
from models.teacher import Teacher


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité addresse correspondant au cours obj

        :param address: à créer sous forme d'entité addresse en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO address (street,city,postal_code) VALUES (%s,%s,%s)"
            cursor.execute(sql, (address.street, address.city, address.postal_code))
            return cursor.lastrowid

    def read(self, id: int | None) -> Optional[Address]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_addresse
           (ou None s'il n'a pu être trouvé)"""
        if id is None:
            return None
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address=%s"

            cursor.execute(sql, (id,))
            query: Dict[str, Any] = cursor.fetchone()
            if query is None:
                return query
            out = Address(query["street"], query["city"], query["postal_code"])
            out.id = query["id_address"]

            return out


    def update(self, addr: Address) -> bool:
        """Met à jour en BD l'entité addresse correspondant à addresse, pour y correspondre

        :param addr: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = "UPDATE address SET street = %(street)s , city = %(city)s, postal_code = %(postal_code)s WHERE id_teacher=%s"

            return cursor.execute(sql, addr.__dict__) != 0

    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité addresse correspondant à addresse

        :param address: cours dont l'entité addresse correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:

            sql = "DELETE FROM TABLE address WHERE id_address=%s"

            return cursor.execute(sql, (address.id,)) != 0
