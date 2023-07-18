import logging
import re
import time
import logging
import copy
from typing import List, Dict, Any, Callable
from .random_param import RandomParam
from core.random_generator import generator as random


class Generator(object):
  def __init__(self,
               generator_type: str,
               quantity: int = 10,
               id_prefix: str = None,
               template: Dict[str, Any] = None):
    self.log = logging.getLogger(self.__class__.__name__)
    self.type = generator_type
    self.id_prefix = id_prefix
    self.quantity: int = quantity
    self.template: Dict[str, Any] = template if template else {}

  def generate(self) -> List[Dict[str, Any]]:
    result = []
    for i in range(self.quantity):
      obj = {
        'id': f"{self.id_prefix}{i}",
        'type': self.type
      }
      obj.update(copy.deepcopy(self.template))
      self.resolve_random_params(obj)
      result.append(obj)

    return result

  def resolve_random_params(self, obj: Any):
    if isinstance(obj, dict):
      for key, value in obj.items():
        if isinstance(value, dict):
          self.resolve_random_params(value)
        elif isinstance(value, list):
          for item in value:
            self.resolve_random_params(item)
        elif isinstance(value, str):
          pattern = re.compile(r".*random\((.*)\).*")
          if isinstance(value, str):
            match = pattern.match(value)
            if match:
              params = match.groups()[0] if match.groups() else ''
              random_value = RandomParam(params).get()
              obj[key] = random_value
              self.log.debug(f"Setting random value: {key} = {random_value}")


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


