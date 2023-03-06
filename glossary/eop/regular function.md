A [[function]] which respects [[equal|equality]]: substituting an equal [[value]] for an [[argument]] gives an equal [[result]]. 

Regular functions allow _equational reasoning_: substituting equals for equals.

A nonregular function depends on the [[representation]], not just the [[interpretation]], of its [[argument]]. When designing the representation for a value type, two tasks go hand in hand: implementing equality and deciding which functions will be regular.  

# Examples

- Most numeric functions
- A function that returns the numerator of a rational number represented as a pair of integers, since 1/2 = 2/4 but `numerator(1/2) != numerator(2/4)`.  

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.2