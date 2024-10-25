# CITS3005 IFixIt Knowldge Graph for game consoles
### Heidi Leow (23643117) and James Frayne (23372032)

## Overview
This is a Flask application to explore and manipulate the Game Console data from the [MyFixit-Dataset.](https://github.com/rub-ksv/MyFixit-Dataset) This application consists of multiple parts:
- requirements.txt          PIP packages required to run the application
- Game Console.json         Original data for game consoles from the MyFixit Dataset
- ontology.py               Python script to convert the json data into the ontology.owl file
- ontology.owl              XML OWL file storing the IFixit ontology
- swrl.txt                  SWRL rules used to perform logic on the ontology
- query.py                  Test script to run SPARQL queries on the ontology
- shapes.ttl                SHACL shapes to validate the ontology against
- validate.py               Test script to run the SHACL validation against the ontology
- app                       Flask application contents

## User guide
1. Set up your python virtual environment using `python -m venv .venv`.
2. Activate your virtual environment using `source .venv/bin/activate`, or `.venv/Scripts/activate` if you're on Windows.
3. Install the required packages using `pip install -r requirements.txt`.
4. Run the application by using `cd app && python web_app.py`

### Exploring the knowledge graph

### Adding new items to the knowledge graph

### Editing items in the knowledge graph

### Deleting items in the knowledge graph

### Modifying the ontology

## Ontology structure

### Overview

### Building the ontology

### Validating the ontology