# Skills Index

This document maps specific skills demonstrated in the AirBnB clone project to code components and features.

## Programming Fundamentals

### Object-Oriented Programming
- **Class Definition and Inheritance**: [`models/base_model.py`](models/base_model.py) - BaseModel serves as parent class
- **Encapsulation**: Storage engine abstraction in [`models/engine/file_storage.py`](models/engine/file_storage.py)
- **Polymorphism**: Common interface for all models inheriting from BaseModel

### Data Structures
- **Dictionary Manipulation**: Object serialization in BaseModel's `to_dict()` method
- **JSON Handling**: File storage for object persistence

## Software Design

### Architectural Patterns
- **MVC (Model-View-Controller)**: 
  - Models: [`models/`](models/) directory
  - Views: [`web_static/`](web_static/) directory
  - Controller: [`console.py`](console.py) for command processing

### Interface Design
- **Command Line Interface**: Interactive shell with tab completion and help documentation
- **Web Interface**: Progressive HTML/CSS layouts showing accommodation listings

## Technical Implementation

### Serialization/Deserialization
- **JSON Conversion**: [`models/engine/file_storage.py`](models/engine/file_storage.py) - `save()` and `reload()` methods
- **Object Recreation**: Instance reconstruction from stored data

### Testing
- **Unit Testing**: Test cases in [`tests/`](tests/) directory
- **Test Discovery**: Automated test running via unittest

## Web Development

### Frontend Development
- **HTML Structure**: Semantic markup in web_static HTML files
- **CSS Styling**: Responsive design with media queries
- **UI Components**: Accommodation cards, filters, amenity icons

## Specific Domain Knowledge

### Accommodation Systems
- **Property Modeling**: [`models/place.py`](models/place.py) with attributes for location, size, pricing
- **User Management**: [`models/user.py`](models/user.py) for customer and host information
- **Review Systems**: [`models/review.py`](models/review.py) for feedback and ratings
- **Location Hierarchy**: State, city, and address modeling