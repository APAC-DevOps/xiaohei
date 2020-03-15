# File person.py (final)
"""
Record and process information about people. Run this file directly to test its classes. 
"""

class AttrDisplay:
    """
    Provides an inheritable display overload method that shows instances with their class names and a name=value pair for each attribute stored on the instance itself (but not attrs inherited from its classes). Can be mixed into any class, and will work on any instance.
    """
    #def _gatherAttrs(self): sudoprivate method in class. just like python module's global variable

    def __gatherAttrs(self):    # Python automatically expands Dunder names to include the enclosing class’s name
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('%s=%s' % (key, getattr(self, key)))
        return ', '.join(attrs)

    def __repr__(self):
        return '[%s: %s]' % (self.__class__.__name__, self.__gatherAttrs())

class Person(AttrDisplay):
  def __init__(self, name, job=None, pay=0):
    self.name = name
    self.job = job
    self.pay = pay

  def lastName(self):
    return self.name.split()[-1]

  def giveRaise(self, percent):
    self.pay = int(self.pay * (1 + percent))

  # def __str__(self):
  #   return '[Person Detail: %s, %s]' % (self.name, self.pay)

  # def __repr__(self):
  #   return '[Person: %s, %s]' % (self.name, self.pay)

class Manager(Person): # Inherit Person attrs 
  def __init__(self, name, pay): 
    Person.__init__(self, name, 'mgr', pay)
  def giveRaise(self, percent, bonus=.10):
    #self.pay = int(self.pay * (1 + percent + bonus))   # Bad: cut and paste
    Person.giveRaise(self, percent + bonus)             # Good: augment original

class Delegation_Manager:
  def __init__(self, name, pay):
    self.person = Person(name, 'mgr', pay)      # Embed a Person object
  def giveRaise(self, percent, bonus=.10):
    self.person.giveRaise(percent + bonus)      # Intercept and delegate
  def __getattr__(self, attr):
    return getattr(self.person, attr)           # Delegate all other attrs
  def __repr__(self):                           # Must overload again (in 3.X)
    return str(self.person)                     # overload is not intercept and deleate in 3.x

class Department:
  def __init__(self, *args):
    self.members = list(args) 
  def addMember(self, person):
    self.members.append(person) 
  def giveRaises(self, percent):
    for person in self.members: 
      person.giveRaise(percent)
  def showAll(self):
    for person in self.members:
      print(person)


if __name__ == '__main__':
  person_a = Person('Jianhua Wu')
  person_b = Person('Sue Jones', job='dev', pay=100000)
  person_c = Manager('Tom Landy',  50000) 
  # print('{0} {1}'.format(person_a.name, person_a.pay))
  # print(person_b.name, person_b.pay)
  for employee in (person_a, person_b, person_c):
    employee.giveRaise(.10)
    print(employee.lastName())
    print(employee)
  engineer_dept = Department(person_a, person_b)
  engineer_dept.addMember(person_c)
  engineer_dept.giveRaises(.10)
  engineer_dept.showAll()
