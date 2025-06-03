import copy
from dataclasses import dataclass
from typing import Optional, Dict, Any

from daos.dao import Dao
from models.person import Person


@dataclass
class PersonDao(Dao[Person]):
    def create(self, person: Person) -> int:
        """Crée en BD l'entité Course correspondant au cours obj

        :param person: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO person (first_name,last_name,age,id_address) VALUES (%s,%s,%s,%s)"
            if cursor.execute(sql, (person.first_name, person.last_name, person.age,
                                    None if person.address is None else person.address.id)) == 1:
                return cursor.lastrowid

        return 0

    def read(self, id_course: int) -> Optional[Person]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM person WHERE id_person=%s"
            cursor.execute(sql, (id_course,))
            result : Dict[str,Any] = cursor.fetchone()
            if result is None:
                return None

            out = Person(result["first_name"],result["last_name"],result["age"])
            out.id = id_course
            return out


    def update(self, person: Person) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param person: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = "UPDATE person SET first_name = %(first_name)s , last_name = %(last_name)s , age = %(age)s , id_address = %(address)s WHERE id_person=%(id)s"
            vals = copy.copy(person.__dict__)

            vals["address"] = person.address.id if person.address is not None else None

            return cursor.execute(sql, vals) != 0

    def delete(self, course: Person) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:

            sql = "DELETE FROM TABLE person WHERE id_person=%s"

            return cursor.execute(sql, (course.id,)) != 0


