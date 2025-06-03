import copy
from dataclasses import dataclass
from typing import Optional, Dict, Any

from daos.dao import Dao
from daos.person_dao import PersonDao
from models.person import Person
from models.student import Student


@dataclass
class StudentDao(Dao[Student]):
    def create(self, person: Student) -> int:
        """Crée en BD l'entité Course correspondant au cours obj

        :param person: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            x = PersonDao().create(person)
            sql = "INSERT INTO student VALUES (%s,%s)"
            cursor.execute(sql, (person.student_nbr,x))
            res: Dict[str, Any] = cursor.fetchone()
            if res is None:
                return res

            w = PersonDao().read(res["id_person"])
            assert w is not None
            out = Student(w.first_name,w.last_name,w.age)
            out.id = res["id_person"]
            out.student_nbr = person.student_nbr
        return 0

    def read(self, nbr: int) -> Optional[Student]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM student WHERE student_nbr=%s"
            cursor.execute(sql, (nbr,))
            result : Dict[str,Any] = cursor.fetchone()
            if result is None:
                return result
            st = PersonDao().read(result["id_person"])

            std = Student(st.first_name,st.last_name,st.age)

            std.address = st.address

            std.student_nbr = nbr

            std.id = st.id

            return st

    def update(self, person: Student) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param person: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:

            PersonDao().update(person)
            sql = "UPDATE student SET student_nbr = %(student_nbr) WHERE student_nbr=%s AND id_person=%s"

            return cursor.execute(sql, (person.student_nbr,person.id,)) != 0

    def delete(self, student : Student) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:

            PersonDao().delete(student)

            sql = "DELETE FROM TABLE takes WHERE student_nbt=%s"

            cursor.execute(sql, (student.student_nbr,))

            sql = "DELETE FROM TABLE student WHERE id_person=%s"

            return cursor.execute(sql, (student.id,)) != 0

