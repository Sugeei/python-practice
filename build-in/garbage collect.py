Garbage collection algorithms

Standard CPython's garbage collector has two components,' \
                ' the reference counting collector and the generational garbage collector, known as gc module.

The reference counting algorithm is incredibly efficient and straightforward,
but it cannot detect reference cycles.
That is why Python has a supplemental algorithm called generational cyclic GC,
that specifically deals with reference cycles.

The reference counting module is fundamental to Python and can't be disabled, ' \
                                                              'whereas the cyclic GC is optional and can be invoked manually.

Reference counting

Reference counting is a simple technique in which objects are deallocated when there is no reference to them in a program.

Every variable in Python is a reference (a pointer) to an object and not the actual value itself.
For example, the assignment statement just adds a new reference to the right-hand side.

To keep track of references, every object (even integer) has an extra field called reference count
that is increased or decreased when a pointer to the object is created or deleted.
See Objects, Types and Reference Counts section, for a detailed explanation.