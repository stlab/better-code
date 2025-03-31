A finite set of [[procedure|procedures]] for a type that enable the construction of any other procedure on the type. 

A basis is _efficient_ if and only if any procedure implemented using it is as efficient as an equivalent procedure written in terms of an alternative basis. 

- A basis for unsigned k-bit integers providing only zero, equality, and the successor function is not efficient, since the complexity of addition in terms of successor is exponential in k.

A basis is _expressive_ if and only if it allows compact and convenient definitions of procedures on the type. In particular, all the common mathematical operations need to be provided when they are appropriate.

- Subtraction could be implemented using negation and addition, but should be included in an expressive basis. 

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.4
