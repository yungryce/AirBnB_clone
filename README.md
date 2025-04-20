# AirBnB Clone

![AirBnB Logo](https://i.imgur.com/QiU1LdE.png)

A command-line clone of AirBnB with a console interface and file storage.

## Technology Signature

| Category | Technologies |
|----------|-------------|
| **Languages** | Python 3.x |
| **Frontend** | HTML5, CSS3 |
| **Storage** | JSON File Storage |
| **Interface** | Command-line (cmd module) |
| **Testing** | unittest framework |

## Demonstrated Competencies

### Technical Skills
- **Object-Oriented Programming**: Class inheritance, encapsulation, polymorphism
- **Serialization/Deserialization**: JSON conversion, data persistence
- **Command-line Interface Development**: Interactive shell using cmd module
- **Web Frontend Development**: Responsive HTML/CSS layouts
- **Software Architecture**: MVC pattern implementation
- **Testing**: Unit testing with Python's unittest framework

### Domain Knowledge
- **Property Management Systems**: Modeling of places, users, reviews
- **Accommodation Services**: Representation of amenities, locations
- **Data Modeling**: Entity relationships between users, places, and reviews

## System Context

This project implements a command-line interpreter to manage AirBnB objects with file-based storage and static web pages.

## Getting Started

### Installation
```bash
git clone https://github.com/username/AirBnB_clone.git
cd AirBnB_clone
```

## Usage

### Interactive Mode
```bash
./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) create BaseModel
49faff9a-6318-451f-87b6-910505c55907
(hbnb) all
["[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'id': '49faff9a-6318-451f-87b6-910505c55907', 'created_at': datetime.datetime(2023, 2, 18, 10, 21, 12, 96959), 'updated_at': datetime.datetime(2023, 2, 18, 10, 21, 12, 96971)}"]
```

### Non-Interactive Mode
```bash
echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update
```

## Running Tests
```bash
python3 -m unittest discover tests
```

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.

## Authors
See the list of [contributors](./AUTHORS) who participated in this project.