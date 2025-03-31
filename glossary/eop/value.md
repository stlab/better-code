A [[datum]] and its [[interpretation]]. 

We use values to represent entities. Since values are unchanging, they can represent [[abstract entity|abstract entities]]. Sequences of values can also represent sequences of [[snapshot|snapshots]] of [[concrete entity|concrete entities]]. 

# Examples

- Integers represented in 32-bit two's complement big-endian format
- Rational numbers represented as a concatenation of two 32-bit sequences, interpreted as integer numerator and denominator, represented as two's complement big-endian values.

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.2

> A [[value type]] is a correspondence between a species ([[abstract species|abstract]] or [[concrete species|concrete]]) and a set of [[datum|datums]]. A datum corresponding to a particular entity is called a [[representation]] of the entity; the entity is called the [[interpretation]] of the datum. We refer to datum together with its interpretation as a [[value]].