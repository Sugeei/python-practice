https://realpython.com/factory-method-python/

https://github.com/faif/python-patterns

根据入参的不同，返回不同的结果

all the pattern are to make your code easy to maintain, to achieve the goal 'open for extension but close for modification'

the prinple will always be to identify the aspects that very and separate them from what stays the same.

for exampel, if you have to access three different api to get a value from the rseponse,
as those apis have different address, you better define three different api objects, each object is responsible for the
api address and the way to get expected value as them may be different too.
then we can have an interface object, it will be act as a manager, because the way the call the api address and read the response are the same
among all those apis. so now we have an interface object and an api object A and api objectt B and C,
each time you try to get the value from api A, new the object A  and make the interface call the func to actually
send a request to the server and get a response, and then can the function defined in object A again to
pick out the expected value from the response.
In this case, api is different, and the way to request for the response are the same.


