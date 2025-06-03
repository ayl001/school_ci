# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""
from copy import copy

from daos.teacher_dao import TeacherDao
from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours obj

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO course VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, (course.id,course.name,course.start_date,course.end_date,None if course.teacher is None else course.teacher.id_teacher))
            return cursor.lastrowid


    def all(self) -> List[int]:
        with Dao.connection.cursor() as cursor:
            sql = "SELECT id_course FROM course"
            cursor.execute(sql)
            ls = []
            for i in cursor.fetchall():
                ls.append(i["id_course"])
            return ls



    def read(self, id_course: int,with_teacher : bool =True) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            result : Dict[str,Any] = cursor.fetchone()
            if result is None:
                return result
            course = Course(result["name"],result["start_date"],result["end_date"])
            if with_teacher:
                course.teacher = TeacherDao().read(result["id_teacher"])
            else:
                course.teacher = result["id_teacher"]
            return course

    def _init_assoc(self,course : Course):
        with Dao.connection.cursor() as cursor:
            sql = "DELETE FROM takes WHERE id_course=%s"

            cursor.execute(sql,(course.id,))
            for i in course.students_taking_it:
                req = "INSERT INTO takes (course_id,student_nbr) VALUES (%s,%s)"
                cursor.execute(req,(course.id,i.student_nbr))


    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = "UPDATE course SET name = %(name), start_date = %(start_date), end_date = %(end_date), teacher = %(teacher) WHERE id_course=%(id)"

            self._init_assoc(course)

            vals = copy(course.__dict__)

            vals["adress"] = course.teacher.id_teacher if course.teacher is not None else None

            return cursor.execute(sql, course.__dict__) != 0

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:

            sql = "DELETE FROM takes WHERE id_course=%s"
            cursor.execute(sql,(course.id,))




            sql = "DELETE FROM TABLE course WHERE id_course=%s"

            cursor.execute(sql,(course.id,))


        return True
