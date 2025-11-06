from lark import Lark, Transformer
import json

class Lamb:
  names = {}

  @classmethod
  def load_names(cls, filepath="names.json"):
    with open(filepath,"r") as f:
        names = json.load(f)
        for k,v in names.items():
            cls.names[k] = parse(v)
    
  def church(self, n):
    return parse("zero"+ n * ".succ")

  def __mul__(self, other):
    return Application(self,other)

  def __matmul__(self, other):
    y = self.pattern()
    match y:
      case ("abs", w):
        return w.beta(other)
    return self * other

  def beta(self, other, v=1):
    y = self.pattern()
    match y:
      case ("var", value):
        return other if value == v else self
      case ("abs", w):
        return Abstraction(w.beta(other, v+1))
      case ("app", w1, w2):
        return Application(w1.beta(other,v), w2.beta(other,v))

      case ("church", value):
        return self
      case ("name", name):
        return self

  def neg(self):
    y = self.pattern()
    match y:
      case ("var", value):
        return -value
      case ("abs", w):
        return w.neg() + 1
      case ("app", w1, w2):
        return min(w1.neg(), w2.neg())

      case ("church", value):
        return 0
      case ("name", name):
        if name in self.names.keys():
          return self.names[name].neg()
        return 0

  def dfs_derive(self):
    flag = True
    res = self
    while flag:
      print(f"= {res}")
      flag, res = res.dfs_reduce()

  def eval(self):
    flag = True
    res = self
    while flag:
      flag, res = res.dfs_reduce()
    return res

  def dfs_reduce(self, node = None):
    if node is None:
      node = self
    y = node.pattern()
    match y:
      case ("church", value):
        return True, self.church(value)

      case ("name", name):
        if name in self.names.keys():
          return True, self.names[name]
        else:
          return False, node

      case ("var", value):
        return False, node

      case ("abs", w):
        flag, res = self.dfs_reduce(w)
        if flag:
          return True, Abstraction(res)
        else:
          return False, Abstraction(w)

      case ("app", w1, w2):
        if isinstance(w1, Abstraction) and w1.neg()>=0:
            return True, w1 @ w2
        else:
          flag, res = self.dfs_reduce(w1)
          if flag:
            return True, Application(res, w2)
          flag, res = self.dfs_reduce(w2)
          if flag:
            return True, Application(w1, res)
          return False, node

class Variable(Lamb):
  def __init__(self, index):
    self.index = index

  def pattern(self):
    return ("var", self.index)

  def __repr__(self):
    return f"v{self.index}"

class Abstraction(Lamb):
  def __init__(self, lamb):
    self.lamb = lamb

  def pattern(self):
    return ("abs", self.lamb)

  def __repr__(self):
    x = self
    k = 0
    while(isinstance(x,Abstraction)):
      x = x.lamb
      k = k + 1
    expo = f"^{k}"
    expr = "{"+x.__repr__()+"}"
    return f"λ{'' if k==1 else expo}({x})"


class Application(Lamb):
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def pattern(self):
    return ("app", self.left, self.right)

  def __repr__(self):
    return f"({self.left} {self.right})"

class Name(Lamb):
  def __init__(self, name):
    self.name = name

  def pattern(self):
    return ("name", self.name)

  def __repr__(self):
    return f"{self.name}"

class Church(Lamb):
  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return f"{self.value}"

  def pattern(self):
    return ("church", self.value)
  


class LambdaTransformer(Lamb):
    def variable(self, items):
        return Variable(int(items[0][1:]))

    def abstraction(self, items):
        return Abstraction(items[1])

    def abstractions(self, items):
        func_token, expr = items
        exp_str = str(func_token).split("^")[1]
        k = int(exp_str)
        res = expr
        for _ in range(k):
            res = Abstraction(res)
        return res

    def application0(self, items):
        left, right = items
        return Application(left, right)

    def application1(self, items):
        left, right = items
        return Application(right, left)

    def church(self, items):
        return Church(int(items[0]))

    def name(self, items):
        return Name(str(items[0]))

grammar = open("grammar.txt").read()

def parse(src):
  #src = " ".joint([f"({line})" for line in src.split("\n")])
  return Lark(grammar, parser="lalr", transformer=LambdaTransformer()).parse(src)
