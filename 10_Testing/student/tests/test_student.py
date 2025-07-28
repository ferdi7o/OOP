from unittest import TestCase, main

from project.student import Student


class TestStudent(TestCase):
    def setUp(self):
        self.student1 = Student("Student 1",
                                {"Python": ["n1", "n2", "n3"],
                                 "Java": ["n4", "n5", "n6"],})

        self.student2 = Student("Student 2")

    def test_init_with_courses(self):
        self.assertEqual("Student 1", self.student1.name)
        self.assertEqual({"Python": ["n1", "n2", "n3"],
                          "Java": ["n4", "n5", "n6"]}, self.student1.courses)

    def test_init_with_courses2(self):
        self.assertEqual("Student 2", self.student2.name)
        self.assertEqual({}, self.student2.courses)

    def test_enroll_existing_course(self):
        result = self.student1.enroll("Python", ["n4", "n5", "n6"], "y")
        self.assertEqual("Course already added. Notes have been updated.", result)
        self.assertEqual({"Python": ["n1", "n2", "n3","n4", "n5", "n6",],
                                 "Java": ["n4", "n5", "n6"]}, self.student1.courses)

    def test_enroll_not_existing_course(self):
        result = self.student1.enroll("C#", ["n4", "n5", "n6"], "")
        self.assertIn("C#", self.student1.courses)
        self.assertEqual("Course and course notes have been added.", result)
        self.assertEqual(["n4", "n5", "n6"], self.student1.courses["C#"])

    def test_enroll_not_exiisting_course_not_adding_notes(self):
        result = self.student2.enroll("C#", ["n4", "n5", "n6"], "y")
        self.assertIn("C#", self.student2.courses)
        self.assertEqual("Course has been added.", result)
        self.assertEqual([], self.student2.courses["C#"])

    def test_add_notes(self):
        result = self.student1.add_notes("Java", "n3")
        self.assertEqual("Notes have been updated", result)
        self.assertIn("n3", self.student1.courses["Java"])

    def test_add_notes_to_not_existing_course(self):
        with self.assertRaises(Exception) as e:
            self.student2.add_notes("JS", "n3")
        self.assertEqual("Cannot add notes. Course not found.", str(e.exception))

    def test_leave_course(self):
        result = self.student1.leave_course("Python")
        self.assertEqual("Course has been removed", result)
        self.assertNotIn("Python", self.student1.courses)

    def test_leave_not_existing_course(self):
        with self.assertRaises(Exception) as e:
            self.student1.leave_course("C#")

        self.assertEqual("Cannot remove course. Course not found.", str(e.exception))



if __name__ == '__main__':
    main()