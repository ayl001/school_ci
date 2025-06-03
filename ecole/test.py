import datetime

from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
from main import *


def test_course():
    z = TeacherDao()
    tx = z.read(6)
    print(tx)
    print(tx.courses_teached)
    tx.hiring_date = date.today()
    std = StudentDao()
    #assert std.create(Student("Z","ZZ",0)) != 0
    #assert z.update(tx) is True
    assert std.read(1) is not None
    x = CourseDao()
    cr = x.read(1)

    assert cr.teacher is not None



test_course()
