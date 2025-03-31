A sequence of instructions that creates, destroys, or modifies the [[state]] of some [[object|objects]]. 

The objects with which a procedure interacts can be divided into four kinds, corresponding to the intentions of the programmer:

- _Input-Output_ consists of objects passed to/from a procedure directly or indirectly through its arguments or returned state. 
- _Local state_ consists of objects created, destroyed, and usually modified during a single invocation of the procedure.
- _Global State_ consists of objects accessible to this and other procedures across multiple invocations.
- _Own State_ consists of objects accessible only to this procedure (and its affiliated procedures) but shared across multiple invocations.

An object is passed _directly_ if it is passed as an argument or returned as the result and is passed _indirectly_ if it is passed via a pointer or pointer-like object. 

- An object is an _input_ to a procedure if it is read, but not modified, by the procedure. 
- An object is an _output_ from a procedure if it is written, created, or destroyed by the procedure, but its initial state is not read y the procedure.

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.4