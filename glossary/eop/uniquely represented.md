1. Describes a [[value type]] if and only if at most one [[value]] corresponds to each [[abstract entity]]. 

	If a value type is uniquely represented, we implement equality by testing that both sequences of 0s and 1s are the same. Otherwise we must implement equality in such a way that preserves its consistency with the [[interpretation|interpretations]] of its [[argument|arguments]].

	Nonunique [[representation|representations]] are chosen when testing equality is done less frequently than operations generating new values and when it is possible to make generating new values faster at the cost of making equality slower. 

2. Describes an [[object type]] if and only if its value type is uniquely represented.

# Examples

- A type representing a truth value as a byte that interprets zero as false and nonzero as true is **not** uniquely represented.
- A type representing integer as a sign bit and an unsigned magnitude does **not** provide a unique representation of zero. 
- A type representing an integer in two's complement is uniquely represented.

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapters 1.2 (Defn. 1), 1.3 (Defn. 2)