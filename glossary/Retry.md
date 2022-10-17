A strategy for handling an [[Error]] in which the program attempts the erroneous [[operation]] again. It may use the same, or a different approach. 

Generally, the Retry strategy is rare (the canonical example is a network call with exponential backoff). 

Retry has [[Requirement]]s: to discard any incomplete work. 

Retry is best done near the point of failure. 

# Resources
Sean Parent: [Exceptions the other way around]()