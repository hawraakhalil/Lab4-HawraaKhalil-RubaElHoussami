from .person import Person

class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def _register_course(self, course_id: int):
        self.registered_courses.append(course_id)
    
    def _unregister_course(self, course_id: int):
        self.registered_courses.remove(course_id)

    def __repr__(self):
        """
        This method returns a string representation of the object which will be needed for pickling.
        """
        return f"Student(name={self.name}, age={self.age}, email={self._email}, student_id={self.student_id}, registered_courses={self.registered_courses})"
    