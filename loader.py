from dataclasses import Field
import logging
from typing import Any, Dict
import yaml

CASTS = {
  'float': float,
  'int': int,
  'string': str,
  'dict': dict
}

logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s [%(levelname)s] %(filename)s:%(name)s.%(funcName)s(): %(message)s'
)


class Type(object):
  def __init__(self, desc_dict: str | dict) -> None:
    if isinstance(desc_dict, str):
      self.name = desc_dict 
      self.of = None
    else:
      self.name = desc_dict['name']
      self.of = Type(desc_dict['of'])
  
  @property
  def is_list(self):
    return self.name == 'list'

  @property
  def can_cast(self):
    return self.name in CASTS

  def __str__(self) -> str:
    if self.of is None:
      return self.name
    else:
      return f"a {self.name} of {self.of}"


class FieldDescription(object):
  def __init__(self, desct_dict: dict) -> None:
    self.name: str = desct_dict['name']
    self.type: Type = Type(desct_dict['type'])
    self.summary: str = desct_dict['summary']
    self.doc: str = desct_dict['doc']
    self.required: list = desct_dict['required']
    self.default: str | None = desct_dict['default'] if 'default' in desct_dict else None
  
  def __str__(self) -> str:
    return f"{self.name} ({self.type})"


class ClassDescription(object):
  def __init__(self, class_name: str, desct_dict: dict) -> None:
    self.class_name: str = class_name
    self.type = Type(desct_dict['type'])
    self.summary: str = desct_dict['summary']
    self.doc: str = desct_dict['doc']
    self.fields: list = [FieldDescription(f) for f in desct_dict['fields']]
  
  def __str__(self) -> str:
    return f"{self.class_name}({self.type})"


class Loader(object):
  def __init__(self, descriptions: Dict[str, ClassDescription], root_description_name: str) -> None:
    self.log = logging.getLogger(f"{self.__class__.__name__}({root_description_name})")
    self.descriptions = descriptions
    self.description = self.descriptions[root_description_name]
    self.value = {}
  
  def load(self, content: dict):
    self.log.debug(f"Analyzing {content}")
    for field in self.description.fields:
      self.log.debug(f"Analyzing {field}")
      if field.name in content:
        raw_value = content[field.name]
        if field.type.is_list:
            self.value[field.name] = [self.load_field(field, item) for item in raw_value]
        else:
          self.value[field.name] = self.load_field(field, raw_value)

    return self.value

  def load_field(self, field, value):
    field_type = field.type.of if field.type.is_list else field.type
    valid = False
    validated_value = None
    if field_type.name in self.descriptions:
      self.log.debug(f"Found description for {field_type.name}")
      value_loader = Loader(self.descriptions, field_type.name)
      validated_value = value_loader.load(value)
      valid = True
    else:
      if not field_type.can_cast:
        self.log.warning(f"No loader found for {field_type.name}")
      else:
        validated_value = self.validate(value, field)
        valid = validated_value is not None
    
    validation_str = 'Valid.' if valid else f"Not valid, expected {field_type.name}."
    print(f"Found value {field.name} = {value if not isinstance(value, dict) else '{...}'} ({type(validated_value).__name__}). {validation_str}")
    if not valid:
      doc_str = f"{field.name} ({field.type}): {field.summary}"
      print('  ', doc_str)
    
    return validated_value
  
  def validate(self, value: Any, field: Field) -> Any | None:
    if type(value).__name__ == field.type.name:
      return value
    elif field.type.can_cast:
      try:
        return CASTS[field.type.name](value)
      except:
        return None
    else:
      return None


def main():
  with open('schema.yml') as fd:
    descriptions = yaml.safe_load(fd)

  descriptions = {n: ClassDescription(n, d) for n, d in descriptions.items()}

  for c in descriptions.values():
    print(f"{c.class_name}: {c.summary}")
    format_doc = lambda f: f.replace('\n', '\n    ') if f else ''
    fields_str = '\n  '.join([f"{f.name} ({f.type}): {f.summary}\n    {format_doc(f.doc)}" for f in c.fields])
    print(f"  {fields_str}")
    print('---')
  
  loader = Loader(descriptions, 'Frame')

  content = {}
  with open('scenarios/blue.yml') as fd:
    content = yaml.safe_load(fd)
  
  loaded = loader.load(content['frame'])

  print(loaded)


if __name__ == '__main__':
  main()
