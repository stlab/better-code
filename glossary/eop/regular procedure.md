Describes a [[procedure]] if and only if replacing its inputs with [[equal]] [[object|objects]] results in equal output objects.

As with [[value type|value types]], when defining an [[object type]], we must make consistent choices in how to implement [[equality]] and which procedures on the type will be regular.

While regularity is the default, there are reasons for nonregular behavior of procedures:
- A procedure returns the address of an object; for example, the built-in [[function]] `addressof`.
- A procedure returns a [[value]] determined by the state of the real world, such as the value of a clock or other device.
- A procedure returns a value depending on own state; for example, a pseudorandom number generator.
- A procedure returns a representation-dependent [[attribute]] of an object, such as the amount of reserved memory for a data structure.

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.6