A [[procedure]] causing the cessation of an [[object|object's]] existence. After a destructor has been called on object, no procedure can be applied to it, and its former [[memory]] locations and resources may be reused for other purposes.

The destructor is normally invoked implicitly. 

Global objects are destroyed when the application terminates, local objects are destroyed when the block in which they are declared is exited, and elements of a data structure are destroyed when the data structure is destroyed.

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.5