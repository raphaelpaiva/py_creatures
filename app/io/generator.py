import json
import random
import re
import time
import logging
import copy
from typing import List, Dict, Any, Callable


class Generator(object):
  def __init__(self,
               generator_type: str,
               random_seed: Any = time.time_ns(),
               quantity: int = 10,
               id_prefix: str = None,
               template: Dict[str, Any] = None):
    self.type = generator_type
    self.id_prefix = id_prefix
    self.random_seed: Any = random_seed
    self.quantity: int = quantity
    self.template: Dict[str, Any] = template if template else {}

    random.seed(self.random_seed)

  def generate(self) -> List[Dict[str, Any]]:
    result = []
    for i in range(self.quantity):
      object = {
        'id': f"{self.id_prefix}{i}",
        'type': self.type
      }
      object.update(copy.deepcopy(self.template))
      result.append(object)

    return result


class ValidationException(Exception):
  def __init__(self, e):
    super().__init__(e)


class GeneratorLoader(object):
  def __init__(self):
    self.log = logging.getLogger(self.__class__.__name__)
    self.current_dict = None

  def load(self, generator_dict: Dict[str, Any]) -> Generator:
    self.current_dict = generator_dict
    generator_type = self.validate(
      name='type',
      validation_function=lambda x: str(x) if x and re.match(r"\w+", x) else None,
      default_value='entity'
    )
    random_seed = self.validate(
      name='random_seed',
      validation_function=lambda x: x if random.seed(x) is None else None,
      default_value=time.time_ns()
    )
    quantity = self.validate(
      name='quantity',
      validation_function=int,
      default_value='10'
    )
    id_prefix = self.validate(
      name='id_prefix',
      validation_function=lambda x: str(x) if x and re.match(r"\w+", x) else None,
      default_value=f"generated_{generator_type}_"
    )
    template = self.validate(
      name='template',
      validation_function=lambda x: x if isinstance(x, dict) else None,
      default_value={}
    )

    return Generator(
      generator_type=generator_type,
      random_seed=random_seed,
      quantity=quantity,
      id_prefix=id_prefix,
      template=template
    )

  def dump(self, generator: Generator) -> Dict[str, Any]:
    return generator.__dict__

  def validate(self,
               name: str,
               validation_function: Callable,
               default_value: Any = None) -> Any:
    value = '<NOT_PRESENT>'
    try:
      value = self.current_dict[name]
      validation = validation_function(value)
      if validation:
        return validation
      else:
        return default_value
    except KeyError as ke:
      if default_value:
        self.log.warning(f"Field '{name}' not found in dict. Using default value of {default_value}.")
        return default_value
      else:
        self.log.error(f"Field '{name}' not found in dict. Using default value of {default_value}.")
        raise ValidationException(ke)
    except Exception as e:
      if default_value:
        self.log.warning(
          f"Error validating value '{value}' for field '{name}': {e} Using default value of {default_value}.")
        return default_value
      else:
        self.log.warning(f"Error validating value '{value}' for field '{name}': {e}")
        raise ValidationException(e)


class Template(object):
  def __init__(self, type: str, properties: Dict[str, Any], id_prefix: str = None):
    self.type = type
    self.id_prefix = id_prefix if id_prefix else f"{type}_"
    self.properties = properties


def main():
  try:
    logging.basicConfig(
      level=logging.DEBUG,
      format='%(asctime)s [%(levelname)s] %(filename)s.%(name)s.%(funcName)s(): %(message)s'
    )
    generator = GeneratorLoader().load({
      'random_seed': 1234,
      'quantity': 2,
      'type': 'creature',
      'id_prefix': 'creature_',
      'template': {
        'position': 'Somewhere',
        'properties': {
          'color': 'green',
          'speed': 1,
          'grab_radius': 7.0,
          'size': 7,
          'desire': 'Wander'
        },
        'sensors': [
          {'radius': 40}
        ]
      }
    })

    print(GeneratorLoader().dump(generator))
    print(json.dumps(generator.generate(), indent=2))
  except:
    pass


if __name__ == '__main__':
  main()
