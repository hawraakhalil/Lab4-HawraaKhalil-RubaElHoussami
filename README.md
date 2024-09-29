# Lab4-HawraaKhalil-RubaElHoussami

The school management system combining Tkinter and PyQt documented implementations of Hawraa and Ruba. This School Management System is a Python-based project designed to manage students, instructors, and courses efficiently. The system is implemented using three different graphical user interfaces (GUIs) with varied data storage methods, providing flexibility in managing and storing data.

## Division of Work
- **Tkinter Documentation**: Hawraa Khalil
- **PYQT Documentation**: Ruba El Houssami

## Features

Both versions of the system include the following features:
- **Student Management**: Add, edit, delete student records.
- **Instructor Management**: Add, edit, delete instructor records.
- **Course Management**: Add, edit, delete course records.
- **Instructor Assignment**: Assign instructors to specific courses.
- **Course Registration**: Register students for courses.
- **Search Functionality**: Search for students, instructors, and courses.
  
### Available GUIs

1. **Tkinter JSON-Based GUI (`tkinter_gui`)**
   - Implements the user interface using Tkinter.
   - Data is stored in and loaded from JSON files.

2. **PyQt File-Based GUI (`pyqt_gui`)**
   - Implements the user interface using PyQt.
   - Data is stored in and loaded from JSON, CSV, Pickle files.

## Installation

### Prerequisites
- Python 3.x
- Required Python libraries: 
  - Tkinter (for `tkinter_gui`)
  - PyQt5 (for `pyqt_gui`)

### Installation Instructions
1. Clone this repository:
   ```bash
   git clone https://github.com/hawraakhalil/Lab4-HarwaaKhalil-RubaElHoussami.git
   cd Lab4-HarwaaKhalil-RubaElHoussami
   ```
2. Install the required Python packages:
   ```bash
   pip install pyqt5
   ```

## Usage

### Running the Tkinter GUI (`tkinter_gui`)
To run the Tkinter version:
   ```bash
   python tkinter_gui.py
 ```
### Running the PyQt GUI (`pyqt_gui`)
To run the PyQt version that uses files for data storage:
   ```bash
   python pyqt_gui.py
```
## Data Storage
- **File-Based GUIs**: Data is stored locally in JSON/CSV/Pickle files. Ensure that you have read and write access to the working directory.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
