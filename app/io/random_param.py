import re
from typing import List
from core.random_generator import generator as random


def get_type(param: str) -> str:
  test_str = param.strip()
  if re.match(r"\d*\.{0,1}\d+", test_str):
    return 'float' if '.' in test_str else 'int'
  else:
    return 'str'


class RandomParamException(Exception):
  def __init__(self, e):
    super().__init__(e)


class RandomParam(object):
  def __init__(self, arguments_str: str, seed = None):
    self.arguments_str = arguments_str
    self.seed = seed
    self.params: List[str | int | float] = []

    raw_argument_list: List[str] = self.arguments_str.split(',')
    if raw_argument_list:
      number_of_arguments: int = len(raw_argument_list)
      match number_of_arguments:
        case 0:
          raise RandomParamException('Random parameters require at least 2 params')
        case 1:
          raise RandomParamException('Random parameters require at least 2 params')
        case 2:
          param1_str = raw_argument_list[0].strip()
          param2_str = raw_argument_list[1].strip()
          types = [get_type(param1_str), get_type(param2_str)]
          if 'str' in types:
            self.type = 'choice'
            self.params = [param1_str, param2_str]
          elif 'float' in types:
            self.type = 'float'
            self.params = [float(param1_str), float(param2_str)]
          else:
            self.type = 'int'
            self.params = [int(param1_str), int(param2_str)]
        case _:
          self.type = 'choice'
          self.params = [p.strip() for p in raw_argument_list]

  def get(self):
    match self.type:
      case 'choice':
        return random.choice(self.params)
      case 'float':
        return self.params[0] + random.random() * self.params[1]
      case 'int':
        return random.randint(*self.params)
