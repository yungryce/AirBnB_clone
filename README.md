# AirBnB Clone Project

## Description

The AirBnB clone project involves building a command-line interpreter to manage AirBnB objects. The primary steps include:

1. **BaseModel Class:**
   - Implement a parent class named `BaseModel` responsible for the initialization, serialization, and deserialization of future instances.

2. **Serialization/Deserialization Flow:**
   - Create a simple flow of serialization/deserialization: `Instance <-> Dictionary <-> JSON string <-> File`.

3. **AirBnB Classes:**
   - Create classes for AirBnB objects (e.g., User, State, City, Place, etc.) that inherit from the `BaseModel` class.

4. **Storage Engine:**
   - Develop the first abstracted storage engine for the project: File storage.

5. **Unit Tests:**
   - Implement unittests to validate all classes and the storage engine.

## Command Interpreter

### Features:

- **Create a New Object:**
  - Create a new instance of an object, such as a new User or a new Place.

- **Retrieve an Object:**
  - Retrieve an object from a file, database, etc.

- **Operations on Objects:**
  - Perform operations on objects, such as counting, computing stats, etc.

- **Update Object Attributes:**
  - Update attributes of an object.

- **Destroy an Object:**
  - Delete an object.

### Usage:

**Interactive Mode:**
```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$

**Non-Interactive Mode:**
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$

**Running Tests:**
$ echo "python3 -m unittest discover tests" | bash
