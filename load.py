import json
import sys
import traceback
from typing import Any, Callable, Dict
import yaml
from world import Entity, Action, Frame, Grab, Location, MoveAround, MoveTo, Resource, StayStill, Vector, World, frame_generator
from plot import generate_frames, live_plot, static_plot

DEFAULT_FILENAME = 'world.yaml'
DEFAULT_FRAME_NUMBER = 'infinite'

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
    self.action_by_entity_id: Dict[str, Action] = {}

  @staticmethod
  def _check_type(obj_dict: Dict, cls):
    type = obj_dict.get('type', cls.__name__)
    if type != cls.__name__:
      raise ParseException(f"Type '{type}' is not compatible with '{cls.__name__}'")

  def _load_frame(self, frame_dict: Dict):   
    number     = frame_dict.get('number', 0)
    world_dict = frame_dict.get('world', None)

    world = self._load_world(world_dict)

    frame = Frame(world)
    frame.number = number

    return frame
  
  def _load_world(self, world_dict: Dict[str, Any]) -> World:
    self._check_type(world_dict, World.__class__)
    
    width  = world_dict.get('width', 100)
    height = world_dict.get('height', 100)
    entities = world_dict.get('entities', [])

    world = World(width, height)

    self.world = world

    for entity_dict in entities:
      world.add(self._load_entity(entity_dict))
    
    self._attach_entity_actions()
    
    return world

  def _attach_entity_actions(self) -> None:
    for entity_id, action_dict in self.action_by_entity_id.items():
      entity = self._lookup_entity(entity_id)
      action = self._load_action(action_dict) if action_dict else None
      if action:
        action.entity = entity
        entity.action = action

  def _load_entity(self, entity_dict: Dict) -> Entity:
    if entity_dict.get('type', None) == Resource.__name__:
      return self._load_resource(entity_dict)
    self._check_type(entity_dict, Entity.__class__)

    id = entity_dict.get("id")
    position_dict = entity_dict.get("position")
    size = entity_dict.get("size", 10)
    action_dict = entity_dict.get("action", None)
    properties_dict = entity_dict.get('properties', {})
    inventory = entity_dict.get("inventory", [])

    position = self._load_vector(position_dict)
    entity = Entity(id, position)
    self.entity_by_id[id] = entity
    self.action_by_entity_id[id] = action_dict
    entity.size = size
    entity.properties = properties_dict
    # entity.inventory = Inventory.from_dict(inventory)
    return entity

  def _load_resource(self, resource_dict: Dict) -> Resource:
    self._check_type(resource_dict, Resource)

    id = resource_dict.get("id")
    position_dict = resource_dict.get("position")
    size = resource_dict.get("size", 10)
    action_dict = resource_dict.get("action", None)
    inventory = resource_dict.get("inventory", [])

    resource = Resource(id, self._load_vector(position_dict))
    self.entity_by_id[id] = resource
    resource.size = size
    return resource

  def _load_vector(self, vector_dict: Dict[str, float]):
    if not vector_dict: return None
    self._check_type(vector_dict, Vector.__class__)
    x = vector_dict['x']
    y = vector_dict['y']

    return Vector(x, y)

  def _load_action(self, action_dict: Dict[str, Any]) -> Action:
    type: str = action_dict.get('type', None)

    if not type:
      raise ParseException(msg=f"Type '{type}' is not a subclass of {Action.__name__}")
    
    loader_name = f"_load_{type.lower()}"

    if loader_name not in self.loader_methods:
      raise ParseException(msg=f"No loader found for {type}. Tried '{loader_name}()'")
    else:
      loader_method = self.loader_methods[loader_name]
      return loader_method(self, action_dict)
  
  def _load_moveto(self, moveto_dict: Dict[str, Any]) -> MoveTo:
    self._check_type(moveto_dict, MoveTo)

    location_dict   = moveto_dict.get("location", None)
    never_satisfied = moveto_dict.get("never_satisfied", False)

    if not location_dict:
      raise ParseException(f"MoveTo action needs a location")
    
    location = None
    if isinstance(location_dict, str):
      location = Location(self._lookup_entity(location_dict))
    elif isinstance(location_dict, dict):
      location = Location(self._load_vector(location_dict))
    
    return MoveTo(None, location, never_satisfied)

  def _load_follow(self, moveto_dict: Dict[str, Any]) -> MoveTo:
    location_id = moveto_dict.get("entity", None)

    if not location_id or not isinstance(location_id, str):
      raise ParseException(f"Follow action needs an entity id")
    
    location = Location(self._lookup_entity(location_id))
    
    return MoveTo(None, location, True)

  def _load_movearound(self, move_dict) -> MoveAround:
    self._check_type(move_dict, MoveAround)
    return MoveAround(None)

  def _load_grab(self, grab_dict) -> Grab:
    self._check_type(grab_dict, Grab)

    resource_id = grab_dict.get("resource", None)
    if not resource_id:
      raise ParseException(f"Grab action needs a resource")

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

def main():
  filename = DEFAULT_FILENAME
  frame_number = DEFAULT_FRAME_NUMBER
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  if len(sys.argv) > 2:
    frame_number = int(sys.argv[2])
  
  try:
    frame = Loader(filename).load()
    if frame_number == DEFAULT_FRAME_NUMBER:
      live_plot(frame_generator(frame))
    else:
      frames = generate_frames(frame_number, world=frame.world)
      live_plot(frames)
  except ParseException as e:
    print(e)
    exit(1)
  except Exception as e:
    traceback.print_exc() #sys.exc_info()[2]
    exit(255)

if __name__ == '__main__':
  main()