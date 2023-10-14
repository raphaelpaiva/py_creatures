# Py Creatures

This documentation is a work in progress. Please look at reference in the nav bar to the left.

## Application Docs

This is a simulation application with optional (but very fun!) real time rendering.

The goal is to create a fairly generic engine so users can also build and add their own systems into the program.

### Dependencies

I heavily recommend the use of virtual environments, but it is up to the user.

To install dependencies, simply run `pip install -r requirements.txt`.
To run the application itself, run `python main.py`.
The default scenario loaded is [blue_creatures.yml](../scenarios/blue_creatures.yml).

There are several examples in the [scenarios](../scenarios) folder.

### YAML Loading

The application uses scenarios that can be defined in YAML files. You can write json into a yaml file just fine if you
prefer.

You can pass a custom scenario to the program as a command line argument, such
as `python main.py scenarios/generator_random.yml`.

Scenarios are defined specifying simulation parameters, such as world size, population and systems.

Population can be anything you want. The built-in simulation is about creatures looking for food and trying to survive.

You can check parameters for the yaml scenarios in the [scenarios](../scenarios) folder. A quick reference for the syntax follows:

```yaml
---
frame: # Required.
  world: # Simulation world definition. Required.
    width:  100 # World width. Required.
    height: 100 # World height. Required.
    random_seed: 12345 # Seed for random number generation consistency. A seed will generate the same numbers, thus the simulation will be the same. 
    systems: # Systems definition. Optional, defaults to the values listed below.
      - BrainSystem # Enables creatures brains
      - SensorSystem # Enables creatures sensors, to detect other entities.
      - DesireSystem # Enables entity desires (or objectives).
      - ActionSystem # Enables atomic actions for entities.
      - MovementSystem # Enables movement for entities.
      - EnergySystem # Enables energy management for entities. If not present creatures can roam forever.
    generators: # Entity generators. Used to generate many entities with one definition. Optional.
      - type: creature # Type of entity to be generated. Required.
        quantity: 5 # How Many entities will be created. Required. 
        id_prefix: 'creature_' # prefix of creature id's. Optional.
        template: # Template for entity definition. The fields under this are the same required to create individual entities
          position: Somewhere # Position within World. Required. Can be 'Somewhere', a random location or a Vector, defined as '{x: <x_value>, y: <y_value>}'
          properties: # Entity properties. All properties are optional and should have internal default values. There is no restriction to properties. Their processing will be system-specific.
            name: random(ze,maria,ablinio,apolo,matraca,max,astolfo,rubens,alan,jessica,ana,mariana,astrogilda,joana,edmarta) # Display name for entity. Optional, defaults to entity id. Can be a string or 'random(values)' where values is a list of names to be chosen randomly.
            color: random(pink,magenta,grey,brown,blue,chocolate,darkslategrey) # Display color for the entity. Optional, defaults to 'blue'. Can be a string with a color name like 'blue', a hex code for color like '#AABBCC' or a random statement like this example.
            speed: random(0.5,1.8) # Entity max speed (velocity magnitude). Optional, defaults to 5. Can be a floating point number or a random statement such as 'random(<min_value>,<max_value>)' meaning a random number will be generated between <min_value> and <max_value>.
            size: random(2,5) # Size of the creature. Optional. Values are the same as speed.
            grab_radius: random(3.0,7) # Grab radius. Optional. Enables an interaction range for an entity.
            diet: random(carnivore,herbivore) # Determines whether creatures feed of resources (Herbivores) or other creatures (Carnivore). Optional. 
          desire: Wander # Creature's default desire (or objective). Optional.
          brain: # Defines if a creature have a brain or not. Optional.
          sensors: # A list of creature sensors. Optional. Only Radial sensors are currently available, thus, the only property of sensors is a radius.  
            - radius: random(10,20)
      - type: Resource
        quantity: 10
        template:
          properties:
            size: random(1,3)
            color: random(green,yellow,gold)
```

### Command Line Options

pass

### Sprite Loading

pass

### UI

pass

## Development Docs

pass

### Overall architecture

pass

#### Entity-Component-System

pass

#### Core Package

pass

#### World and Time

pass

### App package (Add-ons)

pass

