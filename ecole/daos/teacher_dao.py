from __future__ import annotations


import copy
from dataclasses import dataclass
from typing import Optional, Dict, Any, TYPE_CHECKING

#from daos.course_dao import CourseDao
from daos.dao import Dao
from daos.person_dao import PersonDao
from models.person import Person
from models.student import Student
from models.teacher import Teacher

#if TYPE_CHECKING:
#    from course_dao import CourseDao


@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, person: Teacher) -> int:
        """Crée en BD l'entité Course correspondant au cours obj

        :param person: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            x = PersonDao().create(person)
            sql = "INSERT INTO teacher VALUES (%s,%s,%s)"
            cursor.execute(sql, (person.id_teacher, person.hiring_date, person.id_teacher, x))
            return x

    def read(self, id: int | None) -> Optional[Teacher]:
        from daos.course_dao import CourseDao
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        if id is None:
            return None
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM teacher WHERE id_teacher=%s"

            cursor.execute(sql, (id,))
            query : Dict[str,Any] = cursor.fetchone()
            if query is None:
                return query
            pers = PersonDao().read(query["id_person"])

            out = Teacher(pers.first_name, pers.last_name, pers.age,query["start_date"])

            out.id = pers.id

            out.id_teacher = id

            for i in CourseDao().all():
                e = CourseDao().read(i,False)
                if e.teacher is not None and e.teacher == out.id_teacher:
                    out.courses_teached.append(e)

            return out

        return None

    def update(self, person: Teacher) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param person: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            PersonDao().update(person)

            sql = "UPDATE teacher SET start_date = %s WHERE id_teacher=%s"


            return cursor.execute(sql, (person.hiring_date, person.id_teacher,)) != 0





    def delete(self, student: Teacher) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            PersonDao().delete(student)

            sql = "DELETE FROM TABLE teacher WHERE id_person=%s"

            return cursor.execute(sql, (student.id_teacher,)) != 0

