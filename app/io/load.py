from typing import Any, Callable, Dict, List, Type
import time
import yaml
import logging
from app.brain.brain_component import BrainComponent
from app.creatures.creature import Creature
from app.desire import Grab, MoveTo, StayStill, Wander
from core.component.component import EnergyComponent, MetaDataComponent, MovementComponent

from core.entity import Entity
from app.render_system.graphics import SimpleGraphicComponent
from app.location import Location, Somewhere
from core.primitives import Vector
from app.sensor.sensor import RadialSensor, Sensor
from app.sensor.sensor_component import SensorComponent
from app.desire.desire_abstract import Desire, DesireComponent
from core.world import Frame, World
from core.random_generator import generator as random_gen

from .generator import GeneratorLoader


class ParseException(Exception):
  def __init__(self, msg: str, *args: object) -> None:
    super().__init__(*args)
    self.msg = msg
  
  def __str__(self) -> str:
    return f"Parse exception: {self.msg}"


class Loader(object):
  def __init__(self, filename, random_seed=None) -> None:
    self.log = logging.getLogger(self.__class__.__name__)
    self.filename = filename
    self.loader_methods: Dict[str, Callable] = {f: getattr(Loader, f) for f in dir(Loader) if callable(getattr(Loader, f)) and "_load" in f}
    self.entity_by_id: Dict[str, Entity] = {}
    self.desire_by_entity_id: Dict[str, Desire] = {}
    self.world = None
    self.random_seed = random_seed

  @staticmethod
  def _check_type(obj_dict: Dict | str, *classes: Type | str):
    for cls in classes:
      class_name = cls if isinstance(cls, str) else  cls.__name__
      obj_type = obj_dict if isinstance(obj_dict, str) else obj_dict.get('type', class_name)
      if obj_type.lower() == class_name.lower(): return
      
    raise ParseException(f"Type '{obj_type}' is not compatible with '{class_name}'")

  def _load_frame(self, frame_dict: Dict):   
    number = frame_dict.get('number', 0)
    world_dict = frame_dict.get('world', None)

    world = self._load_world(world_dict)

    frame = Frame(world)
    frame.number = number

    return frame
  
  def _load_world(self, world_dict: Dict[str, Any]) -> World:
    self._check_type(world_dict, World)
    
    width = world_dict.get('width', 100)
    height = world_dict.get('height', 100)
    world_random_seed = world_dict.get('random_seed', int(time.time()))
    generator_dicts_list: List[Dict[str, Any]] = world_dict.get('generators', [])
    entities = world_dict.get('entities', [])

    real_random_seed = self.random_seed if self.random_seed else world_random_seed
    random_gen.seed(real_random_seed)

    world = World(width, height, random_seed=world_random_seed)

    self.world = world

    generator_loader = GeneratorLoader()
    for generator_dict in generator_dicts_list:
      generator = generator_loader.load(generator_dict)
      entities.extend(generator.generate())

    for entity_dict in entities:
      world.add(self._load_entity(entity_dict))
    
    self._attach_entity_desires()
    
    return world

  def _attach_entity_desires(self) -> None:
    for entity_id, desire_dict in self.desire_by_entity_id.items():
      entity = self._lookup_entity(entity_id)
      desire = self._load_desire(desire_dict) if desire_dict else None
      if desire:
        desire.entity = entity
        entity.add_component(DesireComponent(desire))

  def _load_entity(self, entity_dict: Dict) -> Entity:
    self._check_type(entity_dict, Entity, 'Resource', 'Creature')

    entity_type = entity_dict.get('type', Entity.__name__)

    if entity_type.lower() == Creature.__name__.lower():
      return self._load_creature(entity_dict).entity

    entity_id = entity_dict.get("id")
    position_dict = entity_dict.get("position", 'Somewhere')
    size = entity_dict.get("size", 10)
    
    default_desire = {'type': 'Wander'} if entity_type == Entity.__name__ else {'type': 'StayStill'}
    
    desire_dict = entity_dict.get("desire", default_desire)
    properties_dict = entity_dict.get('properties', {})
    sensor_list = entity_dict.get('sensors', [])

    position = Somewhere(self.world.width, self.world.height).get() if position_dict == 'Somewhere' else self._load_vector(position_dict)
    entity = Entity(entity_id) 
    self.entity_by_id[entity_id] = entity
    self.desire_by_entity_id[entity_id] = desire_dict
    entity.size = size
    entity.properties = properties_dict
    entity.add_component(MovementComponent(position))
    entity.add_component(MetaDataComponent(properties_dict.get('name', entity_id), entity_type))
    
    sensors = self._load_sensors(sensor_list)
    if sensors:
      entity.add_component(SensorComponent(sensors))
    
    if not entity.is_resource:
      entity.add_component(EnergyComponent())
    
    entity.desire = self._load_desire(desire_dict)

    entity.add_component(SimpleGraphicComponent(entity))

    return entity

  def _load_sensors(self, sensor_list: List[Dict[str, Any]]) -> List[Sensor]:
    if isinstance(sensor_list, list):
      return [RadialSensor(s['radius']) for s in sensor_list]
    return []

  def _load_creature(self, creature_dict: Dict[str, Any]) -> Creature:
    creature_id        = creature_dict.get('id', f"creature_{id(creature_dict)}")
    properties_dict    = creature_dict.get('properties', {})

    creature_metadata  = MetaDataComponent(properties_dict.get('name', creature_id), Creature.__name__)
    creature_desire    = self._load_desire(creature_dict.get('desire')) if 'desire' in creature_dict else StayStill(None)

    sensors_list       = creature_dict.get('sensors', [])
    sensors            = self._load_sensors(sensors_list)

    position_dict      = creature_dict.get('position', None)
    position           = Somewhere(self.world.width, self.world.height).get() if position_dict == 'Somewhere' else self._load_vector(position_dict)
    movement_component = MovementComponent(position)

    creature           = Creature(
      creature_id,
      metadata=creature_metadata,
      desire=creature_desire,
      properties=properties_dict,
      sensor=sensors[0] if sensors else RadialSensor(50),
      movement=movement_component,
      brain=BrainComponent(None),
      energy=EnergyComponent()
    )

    return creature

  def _load_vector(self, vector_dict: Dict[str, float]) -> Vector:
    if not vector_dict: return None
    self._check_type(vector_dict, Vector)
    x = vector_dict['x']
    y = vector_dict['y']

    return Vector(x, y)
  
  def _load_desire(self, desire: Dict[str, Any] | str) -> Desire:
    desire_type: str = desire if isinstance(desire, str) else desire.get('type', None)

    if not desire_type:
      raise ParseException(msg=f"Type '{desire_type}' is not a subclass of {Desire.__name__}")
    
    loader_name = f"_load_{desire_type.lower()}"

    if loader_name not in self.loader_methods:
      raise ParseException(msg=f"No loader found for {desire_type}. Tried '{loader_name}()'")
    else:
      loader_method = self.loader_methods[loader_name]
      return loader_method(self, desire)
  
  def _load_moveto(self, moveto_dict: Dict[str, Any]) -> MoveTo:
    self._check_type(moveto_dict, MoveTo)

    location_dict   = moveto_dict.get("location", None)
    never_satisfied = moveto_dict.get("never_satisfied", False)

    if not location_dict:
      raise ParseException('MoveTo desire needs a location')
    
    location = None
    if isinstance(location_dict, str):
      entity = self._lookup_entity(location_dict)
      location = Location(lambda: entity.movement.position)
    elif isinstance(location_dict, dict):
      if location_dict.get('type', '') == Entity.__name__:
        target = self._lookup_entity(location_dict.get('location'))
        location = Location(self._make_location_func(target), target.name)
      else:
        location = Location(self._load_vector(location_dict))
    
    return MoveTo(None, location, never_satisfied, world=self.world)

  def _load_follow(self, moveto_dict: Dict[str, Any]) -> MoveTo:
    location_id = moveto_dict.get("entity", None)

    if not location_id or not isinstance(location_id, str):
      raise ParseException('Follow desire needs an entity id')
    
    target = self._lookup_entity(location_id)
    location = Location(self._make_location_func(target), target.name)
    
    return MoveTo(None, location, True, self.world)

  def _load_wander(self, move_dict) -> Wander:
    self._check_type(move_dict, Wander)
    return Wander(None, world=self.world)

  def _load_grab(self, grab_dict) -> Grab:
    self._check_type(grab_dict, Grab)

    resource_id = grab_dict.get("resource", None)
    if not resource_id:
      raise ParseException('Grab desire needs a resource')

    return Grab(None, lambda: self._lookup_entity(resource_id).position, world=self.world)

  def _load_staystill(self, staystill_dict) -> StayStill:
    self._check_type(staystill_dict, StayStill)

    return StayStill(None)

  def _lookup_entity(self, entity_id: str):
    entity = self.entity_by_id.get(entity_id, None)
    if not entity:
      raise ParseException(msg=f"entity with id '{entity_id}' not found.")
    
    return entity

  def load(self) -> Frame:
    self.log.info(self.filename)
    content = self._load_yaml(self.filename)
    return self._load_frame(content['frame'])
  
  def _load_yaml(self, filename: str) -> Dict[Any, Any]:
    with open(filename) as fd:
      return yaml.safe_load(fd)

  def _make_location_func(self, entity: Entity) -> Callable:
    return lambda: entity.movement.position
