A [[representation]] of a [[concrete entity]] as a [[value]] in [[memory]]. 

An object has a [[state]] that is a value of some [[value type]]. The state of an object is changeable. Given an object corresponding to a concrete entity, its state corresponds to a [[snapshot]] of that entity. An object owns a set of _resources_, such as memory words or records in a file, to hold its state.

While the value of an object is a contiguous sequence of 0s and 1s, the resources in which those 0s and 1s are stored are not necessarily contiguous. It is the [[interpretation]] that gives unity to an object.

Values and objects play complementary roles. Values are unchanging and are independent of any particular implementation in the computer. Objects are changeable and have computer-specific implementations. 

Objects hold values representing entities. Since objects are changeable, they can represent concrete entities by taking on a new value to represent a change in the entity. Objects can also represent abstract entities: staying constant or taking on different approximations to the abstract. 

# Source

[Elements of Programming](http://elementsofprogramming.com/eop.pdf), Chapter 1.3