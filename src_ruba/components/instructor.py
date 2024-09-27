from .person import Person

class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def _add_course(self, course_id: int):
        self.assigned_courses.append(course_id)
    
    def _remove_course(self, course: int):
        self.assigned_courses.remove(course)
    
    def __repr__(self):
        """
        This method returns a string representation of the object which will be needed for pickling.
        """
        return f"Instructor(name={self.name}, age={self.age}, email={self._email}, instructor_id={self.instructor_id}, assigned_courses={self.assigned_courses})"