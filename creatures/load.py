from typing import Any, Callable, Dict
import yaml
from .behavior import Grab, Wander, MoveTo, StayStill, WanderFollow
from .world import Entity, Behavior, Frame, Location, Resource, Somewhere, Vector, World

class ParseException(Exception):
  def __init__(self, msg: str, *args: object) -> None:
    super().__init__(*args)
    self.msg = msg
  
  def __str__(self) -> str:
    return f"Parse exception: {self.msg}"

class Loader(object):
  def __init__(self, filename) -> None:
    self.filename = filename
    self.loader_methods: Dict[str, Callable] = {f: getattr(Loader, f) for f in dir(Loader) if callable(getattr(Loader, f)) and "_load" in f}
    self.entity_by_id: Dict[str, Entity] = {}
    self.behavior_by_entity_id: Dict[str, Behavior] = {}

  @staticmethod
  def _check_type(obj_dict: Dict | str, cls):
    obj_type = obj_dict if isinstance(obj_dict, str) else obj_dict.get('type', cls.__name__)
    if obj_type != cls.__name__:
      raise ParseException(f"Type '{obj_type}' is not compatible with '{cls.__name__}'")

  def _load_frame(self, frame_dict: Dict):   
    number     = frame_dict.get('number', 0)
    world_dict = frame_dict.get('world', None)

    world = self._load_world(world_dict)

    frame = Frame(world)
    frame.number = number

    return frame
  
  def _load_world(self, world_dict: Dict[str, Any]) -> World:
    self._check_type(world_dict, World)
    
    width  = world_dict.get('width', 100)
    height = world_dict.get('height', 100)
    entities = world_dict.get('entities', [])

    world = World(width, height)

    self.world = world

    for entity_dict in entities:
      world.add(self._load_entity(entity_dict))
    
    self._attach_entity_behaviors()
    
    return world

  def _attach_entity_behaviors(self) -> None:
    for entity_id, behavior_dict in self.behavior_by_entity_id.items():
      entity = self._lookup_entity(entity_id)
      behavior = self._load_behavior(behavior_dict) if behavior_dict else None
      if behavior:
        behavior.entity = entity
        entity.behavior = behavior

  def _load_entity(self, entity_dict: Dict) -> Entity:
    if entity_dict.get('type', None) == Resource.__name__:
      return self._load_resource(entity_dict)
    self._check_type(entity_dict, Entity)

    entity_id = entity_dict.get("id")
    position_dict = entity_dict.get("position")
    size = entity_dict.get("size", 10)
    behavior_dict = entity_dict.get("behavior", {'type': 'Wander'})
    properties_dict = entity_dict.get('properties', {})

    position = Somewhere().get() if position_dict == 'Somewhere' else self._load_vector(position_dict)
    entity = Entity(entity_id, position)
    entity.behavior = self._load_behavior(behavior_dict)
    self.entity_by_id[entity_id] = entity
    self.behavior_by_entity_id[entity_id] = behavior_dict
    entity.size = size
    entity.properties = properties_dict
    return entity

  def _load_resource(self, resource_dict: Dict) -> Resource:
    self._check_type(resource_dict, Resource)

    resouce_id = resource_dict.get("id")
    position_dict = resource_dict.get("position")
    size = resource_dict.get("size", 10)

    resource = Resource(resouce_id, self._load_vector(position_dict))
    self.entity_by_id[resouce_id] = resource
    resource.size = size
    return resource

  def _load_vector(self, vector_dict: Dict[str, float]):
    if not vector_dict: return None
    self._check_type(vector_dict, Vector)
    x = vector_dict['x']
    y = vector_dict['y']

    return Vector(x, y)
  
  def _load_behavior(self, behavior: Dict[str, Any] | str) -> Behavior:
    behavior_type: str = behavior if isinstance(behavior, str) else behavior.get('type', None)

    if not behavior_type:
      raise ParseException(msg=f"Type '{behavior_type}' is not a subclass of {Behavior.__name__}")
    
    loader_name = f"_load_{behavior_type.lower()}"

    if loader_name not in self.loader_methods:
      raise ParseException(msg=f"No loader found for {behavior_type}. Tried '{loader_name}()'")
    else:
      loader_method = self.loader_methods[loader_name]
      return loader_method(self, behavior)
  
  def _load_moveto(self, moveto_dict: Dict[str, Any]) -> MoveTo:
    self._check_type(moveto_dict, MoveTo)

    location_dict   = moveto_dict.get("location", None)
    never_satisfied = moveto_dict.get("never_satisfied", False)

    if not location_dict:
      raise ParseException(f"MoveTo behavior needs a location")
    
    location = None
    if isinstance(location_dict, str):
      location = Location(self._lookup_entity(location_dict))
    elif isinstance(location_dict, dict):
      if location_dict.get('type', '') == Entity.__name__:
        location = Location(self._lookup_entity(location_dict.get('location')))
      else:
        location = Location(self._load_vector(location_dict))
    
    return MoveTo(None, location, never_satisfied)

  def _load_follow(self, moveto_dict: Dict[str, Any]) -> MoveTo:
    location_id = moveto_dict.get("entity", None)

    if not location_id or not isinstance(location_id, str):
      raise ParseException(f"Follow behavior needs an entity id")
    
    location = Location(self._lookup_entity(location_id))
    
    return MoveTo(None, location, True)

  def _load_wander(self, move_dict) -> Wander:
    self._check_type(move_dict, Wander)
    return Wander(None)

  def _load_wanderfollow(self, wanderfollow_dict):
    self._check_type(wanderfollow_dict, WanderFollow)
    return WanderFollow(None)

  def _load_grab(self, grab_dict) -> Grab:
    self._check_type(grab_dict, Grab)

    resource_id = grab_dict.get("resource", None)
    if not resource_id:
      raise ParseException(f"Grab behavior needs a resource")

    return Grab(None, self._lookup_entity(resource_id))

  def _load_staystill(self, staystill_dict) -> StayStill:
    self._check_type(staystill_dict, StayStill)

    return StayStill(None)

  def _lookup_entity(self, entity_id: str):
    entity = self.entity_by_id.get(entity_id, None)
    if not entity:
      raise ParseException(msg=f"entity with id '{entity_id}' not found.")
    
    return entity

  def load(self) -> Frame:
    content = self._load_yaml(self.filename)
    return self._load_frame(content['frame'])
  
  def _load_yaml(self, filename: str) -> Dict[Any, Any]:
    with open(filename) as fd:
      return yaml.safe_load(fd)
