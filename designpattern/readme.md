
https://github.com/faif/python-patterns

根据入参的不同，返回不同的结果

all the pattern are to make your code easy to maintain, to achieve the goal 'open for extension but close for modification'

the prinple will always be to identify the aspects that very and separate them from what stays the same.

for exampel, if you have to access three different api to get a value from the rseponse,
as those apis have different address, you better define three different api objects,
 each object is responsible for the
api address and the way to get expected value as them may be different too.
then we can have an interface object, it will be act as a manager,
because the way the call the api address and read the response are the same
among all those apis. so now we have an interface object and an api object A and api objectt B and C,
each time you try to get the value from api A, new the object A
and make the interface call the func to actually
send a request to the server and get a response,
and then can the function defined in object A again to
pick out the expected value from the response.
In this case, api is different, and the way to request for the response are the same.

bridge pattern allows you to split a large class into two separate hierarchies.
The Bridge pattern attempts to solve this problem by switching from inheritance to the object composition. What this means is that you extract one of the dimensions into a separate class hierarchy, so that the original classes will reference an object of the new hierarchy, instead of having all of its state and behaviors within one class.

factory pattern allows you to easy to maintain you code,
In class-based programming, the factory method pattern is a creational pattern that uses factory methods to deal with the problem of creating objects without having to specify the exact class of the object that will be created. This is done by creating objects by calling a factory method—either specified in an interface and implemented by child classes, or implemented in a base class and optionally overridden by derived classes—rather than by calling a constructor.
"Define an interface for creating an object, but let subclasses decide which class to instantiate.
provide an interface to create objects, but without the knowledge of the actual product that will be created,
which is decided by the subclass that is used.


https://realpython.com/factory-method-python/
根据入参的不同，返回不同的结果

dependency inversion principle -

