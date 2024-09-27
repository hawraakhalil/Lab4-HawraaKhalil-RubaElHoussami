import os
from src_ruba.managers.data_manager import DataManager
from src_ruba.utils.controllers import terminate
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QComboBox, QMessageBox, QDialog)
from PyQt5.QtCore import QTimer, pyqtSlot, Qt
from src_ruba.utils.controllers import (
    register_student, remove_student_from_course, register_instructor, remove_instructor_from_course, 
    add_course, add_student_to_course, add_instructor_to_course, remove_student, remove_instructor, 
    remove_course, get_students, get_instructors, get_courses, get_instructors_by_course, get_students_by_course,
    search_students, search_instructors, get_student_courses, get_instructor_courses, 
)


class SchoolManagementSystem(QMainWindow):
    """A class to manage the school management system interface and functionalities.

    This class creates a GUI application for managing students, instructors, and courses.
    It provides functionalities to register, delete, and view students and instructors, as well
    as managing courses and their enrollments.

    Attributes:
        central_widget (QWidget): The central widget for the main window.
        layout (QVBoxLayout): The main layout of the application.
        tab_widget (QTabWidget): The tab widget containing different management tabs.
        message_label (QLabel): Label to display messages to the user.
        timer (QTimer): Timer to clear messages after a specified duration.
    """

    def __init__(self):
        """Initialize the SchoolManagementSystem instance and set up the GUI components."""
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()

        self.tab_widget.addTab(self.student_tab, "Students")
        self.tab_widget.addTab(self.instructor_tab, "Instructors")
        self.tab_widget.addTab(self.course_tab, "Courses")

        self.setup_student_tab()
        self.setup_instructor_tab()
        self.setup_course_tab()

        self.message_label = QLabel()
        self.layout.addWidget(self.message_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_message)

        self.update_dropdowns()
        
        self.terminate_button = QPushButton("Terminate")
        self.terminate_button.clicked.connect(self.on_closing)
        self.layout.addWidget(self.terminate_button)

    @pyqtSlot()
    def on_closing(self):
        """Prompt to save session before closing the application."""
        save_window = SaveSessionWindow(self)
        result = save_window.exec_()
        if result == QDialog.Accepted:
            self.close()

    def closeEvent(self, event):
        """Handle the close event of the main window.

        This method prompts the user to save the session before closing.

        Args:
            event (QCloseEvent): The close event triggered by the window.
        """
        self.on_closing()
        event.ignore()
        
    def setup_student_tab(self):
        """Set up the student management tab with the necessary GUI components."""
        layout = QVBoxLayout(self.student_tab)

        register_layout = QHBoxLayout()
        layout.addLayout(register_layout)

        register_layout.addWidget(QLabel("Name:"))
        self.student_name_entry = QLineEdit()
        self.student_name_entry.textChanged.connect(self.validate_register_student_fields)
        register_layout.addWidget(self.student_name_entry)

        register_layout.addWidget(QLabel("Age:"))
        self.student_age_entry = QLineEdit()
        self.student_age_entry.textChanged.connect(self.validate_register_student_fields)
        register_layout.addWidget(self.student_age_entry)

        register_layout.addWidget(QLabel("Email:"))
        self.student_email_entry = QLineEdit()
        self.student_email_entry.textChanged.connect(self.validate_register_student_fields)
        register_layout.addWidget(self.student_email_entry)

        self.register_student_button = QPushButton("Register Student")
        self.register_student_button.clicked.connect(self.register_student_command)
        self.register_student_button.setEnabled(False)
        register_layout.addWidget(self.register_student_button)

        delete_layout = QHBoxLayout()
        layout.addLayout(delete_layout)

        delete_layout.addWidget(QLabel("Student ID:"))
        self.delete_student_id_entry = QLineEdit()
        self.delete_student_id_entry.textChanged.connect(self.validate_delete_student_fields)
        delete_layout.addWidget(self.delete_student_id_entry)

        self.delete_student_button = QPushButton("Delete Student")
        self.delete_student_button.clicked.connect(self.delete_student_command)
        self.delete_student_button.setEnabled(False)
        delete_layout.addWidget(self.delete_student_button)


        select_delete_layout = QHBoxLayout()
        layout.addLayout(select_delete_layout)

        self.select_delete_student_combo = QComboBox()
        self.select_delete_student_combo.currentTextChanged.connect(self.validate_select_delete_student_fields)
        select_delete_layout.addWidget(self.select_delete_student_combo)

        self.select_delete_student_button = QPushButton("Delete Selected Student")
        self.select_delete_student_button.clicked.connect(self.select_delete_student_command)
        self.select_delete_student_button.setEnabled(False)
        select_delete_layout.addWidget(self.select_delete_student_button)

        add_to_course_layout = QHBoxLayout()
        layout.addLayout(add_to_course_layout)

        self.select_student_combo = QComboBox()
        self.select_student_combo.currentTextChanged.connect(self.validate_select_add_student_to_course_fields)
        add_to_course_layout.addWidget(self.select_student_combo)

        self.select_course_combo = QComboBox()
        self.select_course_combo.currentTextChanged.connect(self.validate_select_add_student_to_course_fields)
        add_to_course_layout.addWidget(self.select_course_combo)

        self.add_student_to_course_button = QPushButton("Add Student to Course")
        self.add_student_to_course_button.clicked.connect(self.select_add_student_to_course_command)
        self.add_student_to_course_button.setEnabled(False)
        add_to_course_layout.addWidget(self.add_student_to_course_button)

        remove_from_course_layout = QHBoxLayout()
        layout.addLayout(remove_from_course_layout)

        self.select_student_remove_combo = QComboBox()
        self.select_student_remove_combo.currentTextChanged.connect(self.validate_select_remove_student_from_course_fields)
        remove_from_course_layout.addWidget(self.select_student_remove_combo)

        self.select_course_remove_combo = QComboBox()
        self.select_course_remove_combo.currentTextChanged.connect(self.validate_select_remove_student_from_course_fields)
        remove_from_course_layout.addWidget(self.select_course_remove_combo)

        self.remove_student_from_course_button = QPushButton("Remove Student from Course")
        self.remove_student_from_course_button.clicked.connect(self.select_remove_student_from_course_command)
        self.remove_student_from_course_button.setEnabled(False)
        remove_from_course_layout.addWidget(self.remove_student_from_course_button)

        search_layout = QHBoxLayout()
        layout.addLayout(search_layout)

        search_layout.addWidget(QLabel("Name:"))
        self.search_student_name_entry = QLineEdit()
        self.search_student_name_entry.textChanged.connect(self.validate_student_search_fields)
        search_layout.addWidget(self.search_student_name_entry)

        search_layout.addWidget(QLabel("ID:"))
        self.search_student_id_entry = QLineEdit()
        self.search_student_id_entry.textChanged.connect(self.validate_student_search_fields)
        search_layout.addWidget(self.search_student_id_entry)

        search_layout.addWidget(QLabel("Email:"))
        self.search_student_email_entry = QLineEdit()
        self.search_student_email_entry.textChanged.connect(self.validate_student_search_fields)
        search_layout.addWidget(self.search_student_email_entry)

        self.search_student_button = QPushButton("Search Students")
        self.search_student_button.clicked.connect(self.search_students_command)
        self.search_student_button.setEnabled(False)
        search_layout.addWidget(self.search_student_button)

        view_layout = QVBoxLayout()
        layout.addLayout(view_layout)

        self.view_students_list = QListWidget()
        view_layout.addWidget(self.view_students_list)

        self.view_students_button = QPushButton("View All Students")
        self.view_students_button.clicked.connect(self.view_students)
        view_layout.addWidget(self.view_students_button)

    def setup_instructor_tab(self):
        """Set up the instructor management tab with the necessary GUI components.

        This method initializes the layout and widgets required for managing instructors,
        including registration, deletion, and searching functionalities.

        :return: None
        :rtype: None
        """
        layout = QVBoxLayout(self.instructor_tab)

        register_layout = QHBoxLayout()
        layout.addLayout(register_layout)

        register_layout.addWidget(QLabel("Name:"))
        self.instructor_name_entry = QLineEdit()
        self.instructor_name_entry.textChanged.connect(self.validate_register_instructor_fields)
        register_layout.addWidget(self.instructor_name_entry)

        register_layout.addWidget(QLabel("Age:"))
        self.instructor_age_entry = QLineEdit()
        self.instructor_age_entry.textChanged.connect(self.validate_register_instructor_fields)
        register_layout.addWidget(self.instructor_age_entry)

        register_layout.addWidget(QLabel("Email:"))
        self.instructor_email_entry = QLineEdit()
        self.instructor_email_entry.textChanged.connect(self.validate_register_instructor_fields)
        register_layout.addWidget(self.instructor_email_entry)

        self.register_instructor_button = QPushButton("Register Instructor")
        self.register_instructor_button.clicked.connect(self.register_instructor_command)
        self.register_instructor_button.setEnabled(False)
        register_layout.addWidget(self.register_instructor_button)

        delete_layout = QHBoxLayout()
        layout.addLayout(delete_layout)

        delete_layout.addWidget(QLabel("Instructor ID:"))
        self.delete_instructor_id_entry = QLineEdit()
        self.delete_instructor_id_entry.textChanged.connect(self.validate_delete_instructor_fields)
        delete_layout.addWidget(self.delete_instructor_id_entry)

        self.delete_instructor_button = QPushButton("Delete Instructor")
        self.delete_instructor_button.clicked.connect(self.delete_instructor_command)
        self.delete_instructor_button.setEnabled(False)
        delete_layout.addWidget(self.delete_instructor_button)

        select_delete_layout = QHBoxLayout()
        layout.addLayout(select_delete_layout)

        self.select_delete_instructor_combo = QComboBox()
        self.select_delete_instructor_combo.currentTextChanged.connect(self.validate_select_delete_instructor_fields)
        select_delete_layout.addWidget(self.select_delete_instructor_combo)

        self.select_delete_instructor_button = QPushButton("Delete Selected Instructor")
        self.select_delete_instructor_button.clicked.connect(self.select_delete_instructor_command)
        self.select_delete_instructor_button.setEnabled(False)
        select_delete_layout.addWidget(self.select_delete_instructor_button)

        add_to_course_layout = QHBoxLayout()
        layout.addLayout(add_to_course_layout)

        self.select_instructor_combo = QComboBox()
        self.select_instructor_combo.currentTextChanged.connect(self.validate_select_add_instructor_to_course_fields)
        add_to_course_layout.addWidget(self.select_instructor_combo)

        self.select_course_instructor_combo = QComboBox()
        self.select_course_instructor_combo.currentTextChanged.connect(self.validate_select_add_instructor_to_course_fields)
        add_to_course_layout.addWidget(self.select_course_instructor_combo)

        self.add_instructor_to_course_button = QPushButton("Add Instructor to Course")
        self.add_instructor_to_course_button.clicked.connect(self.select_add_instructor_to_course_command)
        self.add_instructor_to_course_button.setEnabled(False)
        add_to_course_layout.addWidget(self.add_instructor_to_course_button)

        remove_from_course_layout = QHBoxLayout()
        layout.addLayout(remove_from_course_layout)

        self.select_instructor_remove_combo = QComboBox()
        self.select_instructor_remove_combo.currentTextChanged.connect(self.validate_select_remove_instructor_from_course_fields)
        remove_from_course_layout.addWidget(self.select_instructor_remove_combo)

        self.select_course_instructor_remove_combo = QComboBox()
        self.select_course_instructor_remove_combo.currentTextChanged.connect(self.validate_select_remove_instructor_from_course_fields)
        remove_from_course_layout.addWidget(self.select_course_instructor_remove_combo)

        self.remove_instructor_from_course_button = QPushButton("Remove Instructor from Course")
        self.remove_instructor_from_course_button.clicked.connect(self.select_remove_instructor_from_course_command)
        self.remove_instructor_from_course_button.setEnabled(False)
        remove_from_course_layout.addWidget(self.remove_instructor_from_course_button)

        search_layout = QHBoxLayout()
        layout.addLayout(search_layout)

        search_layout.addWidget(QLabel("Name:"))
        self.search_instructor_name_entry = QLineEdit()
        self.search_instructor_name_entry.textChanged.connect(self.validate_instructor_search_fields)
        search_layout.addWidget(self.search_instructor_name_entry)

        search_layout.addWidget(QLabel("ID:"))
        self.search_instructor_id_entry = QLineEdit()
        self.search_instructor_id_entry.textChanged.connect(self.validate_instructor_search_fields)
        search_layout.addWidget(self.search_instructor_id_entry)

        search_layout.addWidget(QLabel("Email:"))
        self.search_instructor_email_entry = QLineEdit()
        self.search_instructor_email_entry.textChanged.connect(self.validate_instructor_search_fields)
        search_layout.addWidget(self.search_instructor_email_entry)

        self.search_instructor_button = QPushButton("Search Instructors")
        self.search_instructor_button.clicked.connect(self.search_instructors_command)
        self.search_instructor_button.setEnabled(False)
        search_layout.addWidget(self.search_instructor_button)

        view_layout = QVBoxLayout()
        layout.addLayout(view_layout)

        self.view_instructors_list = QListWidget()
        view_layout.addWidget(self.view_instructors_list)

        self.view_instructors_button = QPushButton("View All Instructors")
        self.view_instructors_button.clicked.connect(self.view_instructors)
        view_layout.addWidget(self.view_instructors_button)

    def setup_course_tab(self):
        """Set up the course management tab with the necessary GUI components.

        This method initializes the layout and widgets required for managing courses,
        including adding, deleting, and viewing functionalities.

        :return: None
        :rtype: None
        """
        layout = QVBoxLayout(self.course_tab)

        add_course_layout = QHBoxLayout()
        layout.addLayout(add_course_layout)

        add_course_layout.addWidget(QLabel("Course Name:"))
        self.add_course_name_entry = QLineEdit()
        self.add_course_name_entry.textChanged.connect(self.validate_add_course_fields)
        add_course_layout.addWidget(self.add_course_name_entry)

        add_course_layout.addWidget(QLabel("Description:"))
        self.add_course_description_entry = QTextEdit()
        self.add_course_description_entry.textChanged.connect(self.validate_add_course_fields)
        add_course_layout.addWidget(self.add_course_description_entry)

        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course_command)
        self.add_course_button.setEnabled(False)
        add_course_layout.addWidget(self.add_course_button)

        delete_course_layout = QHBoxLayout()
        layout.addLayout(delete_course_layout)

        delete_course_layout.addWidget(QLabel("Course ID:"))
        self.remove_course_id_entry = QLineEdit()
        self.remove_course_id_entry.textChanged.connect(self.validate_remove_course_fields)
        delete_course_layout.addWidget(self.remove_course_id_entry)

        self.remove_course_button = QPushButton("Delete Course")
        self.remove_course_button.clicked.connect(self.remove_course_command)
        self.remove_course_button.setEnabled(False)
        delete_course_layout.addWidget(self.remove_course_button)

        select_delete_course_layout = QHBoxLayout()
        layout.addLayout(select_delete_course_layout)

        self.select_delete_course_combo = QComboBox()
        self.select_delete_course_combo.currentTextChanged.connect(self.validate_select_delete_course_fields)
        select_delete_course_layout.addWidget(self.select_delete_course_combo)

        self.select_delete_course_button = QPushButton("Delete Selected Course")
        self.select_delete_course_button.clicked.connect(self.select_delete_course_command)
        self.select_delete_course_button.setEnabled(False)
        select_delete_course_layout.addWidget(self.select_delete_course_button)

        view_course_layout = QVBoxLayout()
        layout.addLayout(view_course_layout)

        self.course_listbox = QListWidget()
        view_course_layout.addWidget(self.course_listbox)

        self.populate_courses_button = QPushButton("View All Courses")
        self.populate_courses_button.clicked.connect(self.populate_courses)
        view_course_layout.addWidget(self.populate_courses_button)

        course_details_layout = QVBoxLayout()
        layout.addLayout(course_details_layout)

        course_details_layout.addWidget(QLabel("Course Details"))

        self.course_details_text = QTextEdit()
        self.course_details_text.setReadOnly(True)
        course_details_layout.addWidget(self.course_details_text)

    @pyqtSlot()
    def register_student_command(self):
        """Register a new student based on user input.

        Retrieves the student details (name, age, email) entered in the 
        Student tab, registers the student, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the registration fails, an appropriate message is shown.
        """
        name = self.student_name_entry.text().strip()
        age = self.student_age_entry.text().strip()
        email = self.student_email_entry.text().strip()
        message, status = register_student(name, age, email)

        if status == 200:
            self.student_name_entry.clear()
            self.student_age_entry.clear()
            self.student_email_entry.clear()
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def delete_student_command(self):
        """Delete a student based on the entered student ID.

        Retrieves the student ID from the input field, attempts to remove the
        student, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the student deletion fails, an appropriate message is shown.
        """
        student_id = self.delete_student_id_entry.text().strip()
        message, status = remove_student(int(student_id))

        if status == 200:
            self.delete_student_id_entry.clear()
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def select_delete_student_command(self):
        """Delete a selected student from the combo box.

        Retrieves the student ID from the selected combo box item, attempts to
        remove the student, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the selected student deletion fails, an appropriate message is shown.
        """
        student_id = self.select_delete_student_combo.currentText().split(":")[1].strip()
        message, status = remove_student(int(student_id))

        if status == 200:
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def select_add_student_to_course_command(self):
        """Add a selected student to a selected course.

        Retrieves the selected student and course IDs, attempts to register the
        student for the course, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the student registration fails, an appropriate message is shown.
        """
        student_id = self.select_student_combo.currentText().split(":")[1].strip()
        course_id = self.select_course_combo.currentText().split(":")[1].strip()
        message, status = add_student_to_course(int(student_id), int(course_id))

        if status == 200:
            self.show_message(message["message"], "green")
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def select_remove_student_from_course_command(self):
        """Remove a selected student from a selected course.

        Retrieves the selected student and course IDs, attempts to remove the
        student from the course, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the student removal fails, an appropriate message is shown.
        """
        student_id = self.select_student_remove_combo.currentText().split(":")[1].strip()
        course_id = self.select_course_remove_combo.currentText().split(":")[1].strip()
        message, status = remove_student_from_course(int(student_id), int(course_id))

        if status == 200:
            self.show_message(message["message"], "green")
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def register_instructor_command(self):
        """Register a new instructor based on user input.

        Retrieves the instructor details (name, age, email) entered in the 
        Instructor tab, registers the instructor, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the registration fails, an appropriate message is shown.
        """
        name = self.instructor_name_entry.text().strip()
        age = self.instructor_age_entry.text().strip()
        email = self.instructor_email_entry.text().strip()
        message, status = register_instructor(name, age, email)

        if status == 200:
            self.instructor_name_entry.clear()
            self.instructor_age_entry.clear()
            self.instructor_email_entry.clear()
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def delete_instructor_command(self):
        """Delete an instructor based on the entered instructor ID.

        Retrieves the instructor ID from the input field, attempts to remove the
        instructor, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the instructor deletion fails, an appropriate message is shown.
        """
        instructor_id = self.delete_instructor_id_entry.text().strip()
        message, status = remove_instructor(int(instructor_id))

        if status == 200:
            self.delete_instructor_id_entry.clear()
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def select_delete_instructor_command(self):
        """Delete a selected instructor from the combo box.

        Retrieves the instructor ID from the selected combo box item, attempts to
        remove the instructor, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the selected instructor deletion fails, an appropriate message is shown.
        """
        instructor_id = self.select_delete_instructor_combo.currentText().split(":")[1].strip()
        message, status = remove_instructor(int(instructor_id))

        if status == 200:
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def select_add_instructor_to_course_command(self):
        """Add a selected instructor to a selected course.

        Retrieves the selected instructor and course IDs, attempts to register the
        instructor for the course, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the instructor registration fails, an appropriate message is shown.
        """
        instructor_id = self.select_instructor_combo.currentText().split(":")[1].strip()
        course_id = self.select_course_instructor_combo.currentText().split(":")[1].strip()
        message, status = add_instructor_to_course(int(instructor_id), int(course_id))

        if status == 200:
            self.show_message(message["message"], "green")
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def select_remove_instructor_from_course_command(self):
        """Remove a selected instructor from a selected course.

        Retrieves the selected instructor and course IDs, attempts to remove the
        instructor from the course, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the instructor removal fails, an appropriate message is shown.
        """
        instructor_id = self.select_instructor_remove_combo.currentText().split(":")[1].strip()
        course_id = self.select_course_instructor_remove_combo.currentText().split(":")[1].strip()
        message, status = remove_instructor_from_course(int(instructor_id), int(course_id))

        if status == 200:
            self.show_message(message["message"], "green")
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def add_course_command(self):
        """Add a new course based on user input.

        Retrieves the course name and description entered in the Course tab, 
        attempts to register the course, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the course registration fails, an appropriate message is shown.
        """
        name = self.add_course_name_entry.text().strip()
        description = self.add_course_description_entry.toPlainText().strip()
        message, status = add_course(name, description)

        if status == 200:
            self.add_course_name_entry.clear()
            self.add_course_description_entry.clear()
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def remove_course_command(self):
        """Remove a course based on the entered course ID.

        Retrieves the course ID from the input field, attempts to remove the
        course, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the course removal fails, an appropriate message is shown.
        """
        course_id = self.remove_course_id_entry.text().strip()
        message, status = remove_course(int(course_id))

        if status == 200:
            self.remove_course_id_entry.clear()
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def select_delete_course_command(self):
        """Delete a selected course from the combo box.

        Retrieves the course ID from the selected combo box item, attempts to
        remove the course, and updates the UI accordingly.

        :return: None
        :rtype: None
        :raises ValueError: If the course deletion fails, an appropriate message is shown.
        """
        course_id = self.select_delete_course_combo.currentText().split(":")[1].strip()
        message, status = remove_course(int(course_id))

        if status == 200:
            self.show_message(message["message"], "green")
            self.update_dropdowns()
        else:
            self.show_message(message["message"], "red")

    @pyqtSlot()
    def view_students(self):
        """View all registered students and update the UI accordingly.

        Retrieves the list of students and populates the students' list widget.
        
        :return: None
        :rtype: None
        :raises ValueError: If the retrieval fails, an appropriate message is shown.
        """
        students, status = get_students()
        self.view_students_list.clear()
        
        if status == 200 and students:
            for student in students['students'].values():
                courses = get_student_courses(student.student_id)
                course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                self.view_students_list.addItem(f"Name: {student.name}, ID: {student.student_id}, Email: {student._email}")
                self.view_students_list.addItem(f"Courses: {course_names}")
                self.view_students_list.addItem("")
            self.show_message("Students retrieved successfully", "green")
        else:
            self.show_message("No students found", "red")

    @pyqtSlot()
    def view_instructors(self):
        """View all registered instructors and update the UI accordingly.

        Retrieves the list of instructors and populates the instructors' list widget.
        
        :return: None
        :rtype: None
        :raises ValueError: If the retrieval fails, an appropriate message is shown.
        """
        instructors, status = get_instructors()
        self.view_instructors_list.clear()
        
        if status == 200 and instructors:
            for instructor in instructors['instructors'].values():
                courses = get_instructor_courses(instructor.instructor_id)
                course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                self.view_instructors_list.addItem(f"Name: {instructor.name}, ID: {instructor.instructor_id}, Email: {instructor._email}")
                self.view_instructors_list.addItem(f"Courses: {course_names}")
                self.view_instructors_list.addItem("")
            self.show_message("Instructors retrieved successfully", "green")
        else:
            self.show_message("No instructors found", "red")

    @pyqtSlot()
    def populate_courses(self):
        """Populate the courses list with all registered courses.

        Retrieves the list of courses and updates the courses' list widget.
        
        :return: None
        :rtype: None
        :raises ValueError: If the retrieval fails, an appropriate message is shown.
        """
        courses, status = get_courses()
        self.course_listbox.clear()
        
        if status == 200 and courses:
            for course in courses['courses'].values():
                self.course_listbox.addItem(f"{course.name}: {course.course_id}")
            self.show_message("Courses retrieved successfully", "green")
        else:
            self.show_message("No courses found", "red")

    @pyqtSlot()
    def search_students_command(self):
        """Search for students based on the provided criteria.

        Retrieves the search criteria (name, student ID, email) and updates the 
        students' list widget with matching results.

        :return: None
        :rtype: None
        :raises ValueError: If the search fails, an appropriate message is shown.
        """
        name = self.search_student_name_entry.text().strip()
        student_id = self.search_student_id_entry.text().strip()
        email = self.search_student_email_entry.text().strip()
        
        students, status = search_students(name, student_id, email)
        self.view_students_list.clear()
        
        if status == 200 and students:
            for student in students['students']:
                courses = get_student_courses(student.student_id)
                course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                self.view_students_list.addItem(f"Name: {student.name}, ID: {student.student_id}, Email: {student._email}")
                self.view_students_list.addItem(f"Courses: {course_names}")
                self.view_students_list.addItem("")
            self.show_message("Students found", "green")
        else:
            self.show_message("No students found", "red")

    @pyqtSlot()
    def search_instructors_command(self):
        """Search for instructors based on the provided criteria.

        Retrieves the search criteria (name, instructor ID, email) and updates the 
        instructors' list widget with matching results.

        :return: None
        :rtype: None
        :raises ValueError: If the search fails, an appropriate message is shown.
        """
        name = self.search_instructor_name_entry.text().strip()
        instructor_id = self.search_instructor_id_entry.text().strip()
        email = self.search_instructor_email_entry.text().strip()
        
        instructors, status = search_instructors(name, instructor_id, email)
        self.view_instructors_list.clear()
        
        if status == 200 and instructors:
            for instructor in instructors['instructors']:
                courses = get_instructor_courses(instructor.instructor_id)
                course_names = ", ".join([course.name for course in courses]) if courses else "No courses"
                self.view_instructors_list.addItem(f"Name: {instructor.name}, ID: {instructor.instructor_id}, Email: {instructor._email}")
                self.view_instructors_list.addItem(f"Courses: {course_names}")
                self.view_instructors_list.addItem("")
            self.show_message("Instructors found", "green")
        else:
            self.show_message("No instructors found", "red")

    def update_dropdowns(self):
        """Update the dropdowns with the latest student, course, and instructor options.

        Retrieves the latest lists of students, courses, and instructors,
        and populates the corresponding combo boxes in the UI.

        :return: None
        :rtype: None
        :raises ValueError: If the update fails, an appropriate message is shown.
        """
        student_options = self.get_student_options()
        course_options = self.get_course_options()
        instructor_options = self.get_instructor_options()

        self.select_student_combo.clear()
        self.select_student_combo.addItems(student_options)
        self.select_student_remove_combo.clear()
        self.select_student_remove_combo.addItems(student_options)
        self.select_delete_student_combo.clear()
        self.select_delete_student_combo.addItems(student_options)

        self.select_course_combo.clear()
        self.select_course_combo.addItems(course_options)
        self.select_course_remove_combo.clear()
        self.select_course_remove_combo.addItems(course_options)
        self.select_course_instructor_combo.clear()
        self.select_course_instructor_combo.addItems(course_options)
        self.select_course_instructor_remove_combo.clear()
        self.select_course_instructor_remove_combo.addItems(course_options)
        self.select_delete_course_combo.clear()
        self.select_delete_course_combo.addItems(course_options)

        self.select_instructor_combo.clear()
        self.select_instructor_combo.addItems(instructor_options)
        self.select_instructor_remove_combo.clear()
        self.select_instructor_remove_combo.addItems(instructor_options)
        self.select_delete_instructor_combo.clear()
        self.select_delete_instructor_combo.addItems(instructor_options)


    def get_student_options(self):
        """Retrieve a list of student options for the combo boxes.

        This method fetches all registered students and formats their names 
        and IDs for display in combo boxes.

        :return: List of formatted strings representing students.
        :rtype: list
        """
        students, _ = get_students()
        return [f"{student.name}: {student.student_id}" for student in students['students'].values()]

    def get_course_options(self):
        """Retrieve a list of course options for the combo boxes.

        This method fetches all registered courses and formats their names 
        and IDs for display in combo boxes.

        :return: List of formatted strings representing courses.
        :rtype: list
        """
        courses, _ = get_courses()
        return [f"{course.name}: {course.course_id}" for course in courses['courses'].values()]

    def get_instructor_options(self):
        """Retrieve a list of instructor options for the combo boxes.

        This method fetches all registered instructors and formats their names 
        and IDs for display in combo boxes.

        :return: List of formatted strings representing instructors.
        :rtype: list
        """
        instructors, _ = get_instructors()
        return [f"{instructor.name}: {instructor.instructor_id}" for instructor in instructors['instructors'].values()]

    def show_message(self, message, color):
        """Display a message to the user.

        Args:
            message (str): The message to display.
            color (str): The color for the message text (e.g., "green", "red").
        """
        self.message_label.setText(message)
        self.message_label.setStyleSheet(f"color: {color}")
        self.timer.start(4000)

    def clear_message(self):
        """Clear the message label after a timeout."""
        self.message_label.clear()
        self.timer.stop()

    def validate_register_student_fields(self):
        """Validate the fields for registering a student.

        This method checks if all required fields (name, age, email) are 
        filled in and enables the register button accordingly.

        :return: None
        :rtype: None
        """
        if self.student_name_entry.text() and self.student_age_entry.text() and self.student_email_entry.text():
            self.register_student_button.setEnabled(True)
        else:
            self.register_student_button.setEnabled(False)

    def validate_delete_student_fields(self):
        """Validate the fields for deleting a student.

        This method checks if the student ID field is filled in and enables 
        the delete button accordingly.

        :return: None
        :rtype: None
        """
        if self.delete_student_id_entry.text():
            self.delete_student_button.setEnabled(True)
        else:
            self.delete_student_button.setEnabled(False)

    def validate_select_delete_student_fields(self):
        """Validate the selection of a student to delete.

        This method checks if a student is selected in the combo box and 
        enables the delete selected button accordingly.

        :return: None
        :rtype: None
        """
        if self.select_delete_student_combo.currentText():
            self.select_delete_student_button.setEnabled(True)
        else:
            self.select_delete_student_button.setEnabled(False)

    def validate_select_add_student_to_course_fields(self):
        """Validate the selection of a student and course to add.

        This method checks if both a student and a course are selected in the 
        combo boxes and enables the add student to course button accordingly.

        :return: None
        :rtype: None
        """
        if self.select_student_combo.currentText() and self.select_course_combo.currentText():
            self.add_student_to_course_button.setEnabled(True)
        else:
            self.add_student_to_course_button.setEnabled(False)

    def validate_select_remove_student_from_course_fields(self):
        """Validate the selection of a student and course to remove.

        This method checks if both a student and a course are selected in the 
        combo boxes and enables the remove student from course button accordingly.

        :return: None
        :rtype: None
        """
        if self.select_student_remove_combo.currentText() and self.select_course_remove_combo.currentText():
            self.remove_student_from_course_button.setEnabled(True)
        else:
            self.remove_student_from_course_button.setEnabled(False)

    def validate_register_instructor_fields(self):
        """Validate the fields for registering an instructor.

        This method checks if all required fields (name, age, email) are 
        filled in and enables the register button accordingly.

        :return: None
        :rtype: None
        """
        if self.instructor_name_entry.text() and self.instructor_age_entry.text() and self.instructor_email_entry.text():
            self.register_instructor_button.setEnabled(True)
        else:
            self.register_instructor_button.setEnabled(False)

    def validate_delete_instructor_fields(self):
        """Validate the fields for deleting an instructor.

        This method checks if the instructor ID field is filled in and enables 
        the delete button accordingly.

        :return: None
        :rtype: None
        """
        if self.delete_instructor_id_entry.text():
            self.delete_instructor_button.setEnabled(True)
        else:
            self.delete_instructor_button.setEnabled(False)

    def validate_select_delete_instructor_fields(self):
        """Validate the selection of an instructor to delete.

        This method checks if an instructor is selected in the combo box and 
        enables the delete selected button accordingly.

        :return: None
        :rtype: None
        """
        if self.select_delete_instructor_combo.currentText():
            self.select_delete_instructor_button.setEnabled(True)
        else:
            self.select_delete_instructor_button.setEnabled(False)

    def validate_select_add_instructor_to_course_fields(self):
        """Validate the selection of an instructor and course to add.

        This method checks if both an instructor and a course are selected in the 
        combo boxes and enables the add instructor to course button accordingly.

        :return: None
        :rtype: None
        """
        if self.select_instructor_combo.currentText() and self.select_course_instructor_combo.currentText():
            self.add_instructor_to_course_button.setEnabled(True)
        else:
            self.add_instructor_to_course_button.setEnabled(False)

    def validate_select_remove_instructor_from_course_fields(self):
        """Validate the selection of an instructor and course to remove.

        This method checks if both an instructor and a course are selected in the 
        combo boxes and enables the remove instructor from course button accordingly.

        :return: None
        :rtype: None
        """
        if self.select_instructor_remove_combo.currentText() and self.select_course_instructor_remove_combo.currentText():
            self.remove_instructor_from_course_button.setEnabled(True)
        else:
            self.remove_instructor_from_course_button.setEnabled(False)

    def validate_add_course_fields(self):
        """Validate the fields for adding a course.

        This method checks if the course name field is filled in and enables 
        the add course button accordingly.

        :return: None
        :rtype: None
        """
        if self.add_course_name_entry.text():
            self.add_course_button.setEnabled(True)
        else:
            self.add_course_button.setEnabled(False)

    def validate_remove_course_fields(self):
        """Validate the fields for removing a course.

        This method checks if the course ID field is filled in and enables 
        the remove course button accordingly.

        :return: None
        :rtype: None
        """
        if self.remove_course_id_entry.text():
            self.remove_course_button.setEnabled(True)
        else:
            self.remove_course_button.setEnabled(False)

    def validate_select_delete_course_fields(self):
        """Validate the selection of a course to delete.

        This method checks if a course is selected in the combo box and 
        enables the delete selected button accordingly.

        :return: None
        :rtype: None
        """
        if self.select_delete_course_combo.currentText():
            self.select_delete_course_button.setEnabled(True)
        else:
            self.select_delete_course_button.setEnabled(False)

    def validate_student_search_fields(self):
        """Validate the fields for searching students.

        This method checks if any search criteria are provided and enables 
        the search button accordingly.

        :return: None
        :rtype: None
        """
        if self.search_student_name_entry.text() or self.search_student_id_entry.text() or self.search_student_email_entry.text():
            self.search_student_button.setEnabled(True)
        else:
            self.search_student_button.setEnabled(False)

    def validate_instructor_search_fields(self):
        """Validate the fields for searching instructors.

        This method checks if any search criteria are provided and enables 
        the search button accordingly.

        :return: None
        :rtype: None
        """
        if self.search_instructor_name_entry.text() or self.search_instructor_id_entry.text() or self.search_instructor_email_entry.text():
            self.search_instructor_button.setEnabled(True)
        else:
            self.search_instructor_button.setEnabled(False)

class SaveSessionWindow(QDialog):
    """Dialog for saving the current session before exiting the application."""

    def __init__(self, parent=None):
        """Initialize the SaveSessionWindow instance.

        Args:
            parent (QWidget, optional): The parent widget for the dialog.
        """
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        """Set up the UI components for the save session dialog."""
        self.setWindowTitle("Save Session")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()

        label = QLabel("Save session as:")
        layout.addWidget(label)

        self.save_format = QComboBox()
        self.save_format.addItems(["csv", "json", "pickle"])
        self.save_format.setCurrentIndex(-1)  # No default selection
        self.save_format.currentIndexChanged.connect(self.enable_save_button)
        layout.addWidget(self.save_format)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_and_close)
        self.save_button.setEnabled(False)  # Disabled by default
        layout.addWidget(self.save_button)

        info_label1 = QLabel("This session will be restored the next time you start the app.")
        info_label1.setWordWrap(True)
        info_label1.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label1)

        info_label2 = QLabel("Please note that any previous sessions found will be deleted.")
        info_label2.setWordWrap(True)
        info_label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label2)

        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        no_button = QPushButton("No")
        no_button.clicked.connect(self.close_without_saving)
        button_layout.addWidget(no_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def enable_save_button(self, index):
        """Enable or disable the save button based on the selected format.

        This method enables the save button if a valid save format is 
        selected from the dropdown (i.e., the index is not -1). Otherwise, 
        it disables the button.

        :param index: The index of the selected save format in the dropdown.
        :type index: int
        :return: None
        :rtype: None
        """
        self.save_button.setEnabled(index != -1)

    def save_and_close(self):
        """Save the current session in the selected format and close the application.

        This method retrieves the currently selected save format from the 
        dropdown and calls the method to save the session. After saving, 
        it terminates the application.

        :return: None
        :rtype: None
        :raises Exception: Raises an exception if the save format is invalid.
        """
        format = self.save_format.currentText()
        if format:
            self.save_session_as(format)
            QApplication.quit()

    def close_without_saving(self):
        """Close the application without saving the current session.

        This method is called when the user opts to exit the application 
        without saving their current session. It triggers the QApplication 
        to quit, effectively closing the application.

        :return: None
        :rtype: None
        """
        QApplication.quit()

    def save_session_as(self, format):
        """Save the current session data in the specified format.

        This method saves the session data (students, instructors, and courses) 
        in the format specified by the user (pickle, CSV, or JSON). It retrieves 
        the current working directory and creates a DataManager instance for 
        handling the data saving operations. If an invalid format is specified, 
        it displays an error message.

        :param format: The format in which to save the session data. 
        This can be either 'pickle', 'csv', or 'json'.
        :type format: str
        :return: None
        :rtype: None
        :raises Exception: Raises an error message if an invalid format is specified.
        """
        directory = os.getcwd()
        data_manager = DataManager(directory)
        students, instructors, courses = terminate()
        
        if format == "pickle":
            data_manager.pickle_data(students, instructors, courses)
        elif format == "csv":
            data_manager.save_to_csv(students, instructors, courses)
        elif format == "json":
            data_manager.save_to_json(students, instructors, courses)
        else:
            QMessageBox.critical(self, "Error", "Invalid format specified.")
            return
        
        QMessageBox.information(self, "Success", f"Session saved as {format}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())