# Architecture Overview

This document describes the architectural design of the AirBnB Clone project.

## System Architecture

The AirBnB Clone follows a modified Model-View-Controller (MVC) architecture:

```mermaid
graph TD
    User[User] --> Console[Console Controller]
    Console --> Models[Models]
    Models --> Storage[Storage]
    Console --> Views[Static Views]
    
    subgraph "Controller"
        Console
    end
    
    subgraph "Models"
        Models --> BaseModel[BaseModel]
        BaseModel --> User_Model[User]
        BaseModel --> Place[Place]
        BaseModel --> State[State]
        BaseModel --> City[City]
        BaseModel --> Amenity[Amenity]
        BaseModel --> Review[Review]
    end
    
    subgraph "Storage"
        Storage --> FileStorage[FileStorage]
        FileStorage --> JSON_File[JSON File]
    end
    
    subgraph "Views"
        Views --> HTML[HTML Pages]
        Views --> CSS[CSS Styles]
    end
```

### Components

#### Models (`models/`)
- **Purpose**: Define the data structures and business logic
- **Key Components**:
  - `BaseModel`: Parent class for all models with common functionality
  - Domain-specific models (User, Place, State, City, etc.)
  
#### Storage Engine (`models/engine/`)
- **Purpose**: Handle data persistence
- **Current Implementation**: `FileStorage` - JSON file-based storage
- **Future Implementations**: MySQL database storage with SQLAlchemy (v2)

#### Controller (`console.py`)
- **Purpose**: Process user commands and interact with models/storage
- **Implementation**: Command-line interpreter using Python's cmd module
- **Functions**: CRUD operations (Create, Read, Update, Delete)

#### Views (`web_static/`)
- **Purpose**: Present data to users
- **Current Implementation**: Static HTML/CSS pages
- **Future Implementations**: Dynamic web pages with JavaScript (v4)

## Data Flow

1. **Command Input**: User enters command in console
2. **Command Processing**: Console parses command and determines action
3. **Model Interaction**: Console creates/modifies model instances
4. **Storage Interaction**: Models are saved/loaded from storage
5. **Output**: Results displayed to user via console

## Storage Architecture

The current storage system follows this flow:

```mermaid
flowchart LR
    Instance[Python Instance] -->|to_dict| Dictionary[Dictionary]
    Dictionary -->|json.dumps| JSONString[JSON String]
    JSONString -->|file.write| File[File.json]
    File -->|file.read| LoadedJSON[JSON String]
    LoadedJSON -->|json.loads| LoadedDict[Dictionary]
    LoadedDict -->|Class(**dict)| Instance
```
- **Serialization**: Python objects → Dictionary → JSON string → File
- **Deserialization**: File → JSON string → Dictionary → Python objects