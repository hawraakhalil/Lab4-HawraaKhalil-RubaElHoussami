from src_ruba.components.instructor import Instructor
from src_ruba.components.student import Student
from src_ruba.components.course import Course

import pickle
import os
import json

class DataManager:
    def __init__(self, path: str):
        assert os.path.isdir(path), 'The path specified is not a folder.'
        self.path = path

    def pickle_data(self, students: dict[int, Student], instructors: dict[int, Instructor], courses: dict[int, Course]) -> None:
        """
        This function pickles the data to the specified path into 'data.pkl' file.
        """
        cvs_path = os.path.join(self.path, 'data.cvs')
        json_path = os.path.join(self.path, 'data.json')
        
        if os.path.isfile(cvs_path):
            os.remove(cvs_path)
        
        if os.path.isfile(json_path):
            os.remove(json_path)
            
        with open(os.path.join(self.path, 'data.pkl'), 'wb') as file:
            pickle.dump(students, file)
            pickle.dump(instructors, file)
            pickle.dump(courses, file)

    def unpickle_data(self) -> tuple:
        """
        This function unpickles the data from the specified path from 'data.pkl' file.
        """
        assert os.path.isfile(os.path.join(self.path, 'data.pkl')), 'The path specified does not contain a file named data.pkl.'
        with open(os.path.join(self.path, 'data.pkl'), 'rb') as file:
            students = pickle.load(file)
            instructors = pickle.load(file)
            courses = pickle.load(file)
        return students, instructors, courses

    def save_to_csv(self, students: dict[int, Student], instructors: dict[int, Instructor], courses: dict[int, Course]) -> None:
        """
        This function saves the data to the specified path into 'data.csv' file.
        """
        pkl_path = os.path.join(self.path, 'data.pkl')
        json_path = os.path.join(self.path, 'data.json')
        
        if os.path.isfile(pkl_path):
            os.remove(pkl_path)
        
        if os.path.isfile(json_path):
            os.remove(json_path)

        with open(os.path.join(self.path, 'data.csv'), 'w') as file:
            file.write('Courses\n')
            for course in courses.values():
                file.write(f'{course}\n')
            file.write('\nStudents\n')
            for student in students.values():
                file.write(f'{student}\n')
            file.write('\nInstructors\n')
            for instructor in instructors.values():
                file.write(f'{instructor}\n')

    def load_from_csv(self) -> tuple:
        """
        This function loads the data from the specified path from 'data.csv' file.
        """
        assert os.path.isfile(os.path.join(self.path, 'data.csv')), 'The path specified does not contain a file named data.csv.'
        students = {}
        instructors = {}
        courses = {}
        with open(os.path.join(self.path, 'data.csv'), 'r') as file:
            data = file.read().split('\n')
            course_section = data.index('Courses') + 1
            student_section = data.index('Students') + 1
            instructor_section = data.index('Instructors') + 1

            for i in range(course_section, student_section - 1):
                if data[i].strip():
                    course = Course.from_string(data[i])
                    courses[course.id] = course

            for i in range(student_section, instructor_section - 1):
                if data[i].strip():
                    student = Student.from_string(data[i])
                    students[student.id] = student

            for i in range(instructor_section, len(data)):
                if data[i].strip():
                    instructor = Instructor.from_string(data[i])
                    instructors[instructor.id] = instructor

        return students, instructors, courses

    def save_to_json(self, students: dict[int, Student], instructors: dict[int, Instructor], courses: dict[int, Course]) -> None:
        """
        This function saves the data to the specified path into 'data.json' file.
        """
        
        pkl_path = os.path.join(self.path, 'data.pkl')
        csv_path = os.path.join(self.path, 'data.csv')
        
        if os.path.isfile(pkl_path):
            os.remove(pkl_path)
        
        if os.path.isfile(csv_path):
            os.remove(csv_path)

        with open(os.path.join(self.path, 'data.json'), 'w') as file:
            json.dump(students, file, default=lambda x: x.__dict__)
            file.write('\n')
            json.dump(instructors, file, default=lambda x: x.__dict__)
            file.write('\n')
            json.dump(courses, file, default=lambda x: x.__dict__)

    def load_from_json(self) -> tuple:
        """
        This function loads the data from the specified path from 'data.json' file.
        """
        assert os.path.isfile(os.path.join(self.path, 'data.json')), 'The path specified does not contain a file named data.json.'
        with open(os.path.join(self.path, 'data.json'), 'r') as file:
            data = file.read().split('\n')
            students = json.loads(data[0])
            instructors = json.loads(data[1])
            courses = json.loads(data[2])
        return students, instructors, courses

    def boot(self) -> tuple:
        """
        This function boots the data from the specified path.
        """
        if os.path.isfile(os.path.join(self.path, 'data.pkl')):
            return self.unpickle_data()
        elif os.path.isfile(os.path.join(self.path, 'data.csv')):
            return self.load_from_csv()
        elif os.path.isfile(os.path.join(self.path, 'data.json')):
            return self.load_from_json()
        return {}, {}, {}
