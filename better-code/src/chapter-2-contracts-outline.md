Better Code: Contracts
What's holding our software together?  Can we do better than duct tape and good intentions?
The connective tissue of correct software  |  Agenda
Correctness
Local reasoning
Design by Contract
Contract style
Error Handling
Contract checking and Offensive programming
What to do in existing codebases

Correctness
Pursuing Correctness  |  Reasons
It's more practical than you might think
Simplicity
Fulfillment
Strong Contracts Simplify Code
Pursuing Correctness
Ordinary stuff:

var names = [ "Sean", "Laura", "Dave", "Crusty" ]
names.sort()
print(names[3])
Pursuing Correctness
Ordinary stuff:

var names = [ "Sean", "Laura", "Dave", "Crusty" ]
names.sort()
print(names[3])
Pursuing Correctness
Ordinary stuff:

var names = [ "Sean", "Laura", "Dave", "Crusty" ]
names.sort()
print(names[3])
Local reasoning



Local reasoning is the idea that the reader can make sense of the code directly in front of them, without going on a journey discovering how the code works.
—Nathan Gitter
(https://medium.com/@nathangitter/local-reasoning-in-swift-6782e459d)

Best practices that exist to support local reasoning
Using private data members
Keeping functions small
Creating components
Avoiding global variables
Avoiding (smart) pointers
Building/using libraries
Following the single-responsibility principle
(ahem) Using contracts
What is DbC?
Hoare Logic  |  Preconditions and Postconditions
{P}C{Q}
If precondition P is met, executing C establishes postcondition Q

{x < INT_MAX}  x+=1  {x > INT_MIN}

Hoare Logic  |  Loop Invariants
A condition that holds before and after each iteration

var i = 0
while (i != a.length && a[i] != x) {
  i += 1
}

In this case: all elements preceding a[i] ≠ x

Conclusion: the loop finds the first x, if there is one.

Design by Contract  |  Bertrand Meyer
“…a software system is viewed as a set of communicating components whose interaction is based on precisely defined specifications of the mutual obligations — contracts.”

—Building bug-free O-O software: An Introduction to Design by Contract™
https://www.eiffel.com/values/design-by-contract/introduction/

Design by Contract  |  The basics

Contract: specifies the relationship between an operation and the clients that invoke it.

Preconditions: what a correct client must ensure in order to use the operation

Postconditions: the return value and effects of the successful operation

Invariant: condition preserved by the operation
Meyer innovation #1  |  An ethos of blame
If preconditions don't hold, that's a bug.  The client is at fault, and the operation makes no promises.

If preconditions hold but postconditions are not fulfilled* that's a bug, and the operation is at fault.

If software malfunctions and you can't clearly assign blame, a contract is missing somewhere.

The technical term for such software is footgun.
* stay tuned
Meyer innovation #2  |  Type invariants
Condition that holds whenever a type interacts with clients.

“It's in a good state” ≅ the invariant is upheld
Meyer innovation #2  |  Type invariants
Condition that holds whenever a type interacts with clients.

“It's in a good state” ≅ the invariant is upheld
Meyer innovation #2  |  Type invariants
Condition that holds whenever a type interacts with clients.

“It's in a good state” ≅ the invariant is upheld
Spoiler Alert: It's Documentation
“…a software system is viewed as a set of communicating components whose interaction is based on precisely defined specifications of the mutual obligations — contracts.”

—Building bug-free O-O software: An Introduction to Design by Contract™
https://www.eiffel.com/values/design-by-contract/introduction/

Local reasoning  |  The tower of abstraction



All undocumented software is waste. It's a liability for a company.
—Alexander Stepanov (https://youtu.be/COuHLky7E2Q?t=1773)


The tower of invariants  |  Formalizing “good program state”










var employees = SQLDatabase("/var/db/employees")

The tower of invariants  |  Formalizing “good program state”
class EmployeeDatabase {
  private var SQLDatabase;

  // operations that uphold the invariant
  public foo()
  public bar()
  ...
}


var employees
   = EmployeeDatabase("/var/db/employees")

Put the documentation in comments in your code
The correspondence is important
Bouncing between editing code and docs is a drag.
Language and Library Support
class Array<T> {
  ...

  // Returns the `i`th element.
  @requires(i >= 0 && i < self.length)
  fun getNth(i: Integer): T

  ...
}

Examples
Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  /// - Postcondition: The length is one less than before
  ///   the call. Returns the original last element.
 public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  /// - Postcondition: The length is one less than before
  ///   the call. Returns the original last element.
  /// - Invariant: the values of the remaining elements.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  /// - Postcondition: The length is one less than before
  ///   the call. Returns the original last element.
  /// - Invariant: the values of the remaining elements.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  /// - Invariant: the values of the remaining elements.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example  |  Design by Contract
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
 public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}

Example #2  |  Sorting
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

var a = [7, 9, 2, 7]
a.sort(areInIncreasingOrder: <)
print(a)     // prints [2, 7, 7, 9]
Example #2  |  Sorting
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

var a = [7, 9, 2, 7]
a.sort(areInIncreasingOrder: <)
print(a)     // prints [2, 7, 7, 9]
Example #2  |  Sorting
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

var a = [7, 9, 2, 7]
a.sort(areInIncreasingOrder: <)
print(a)     // prints [2, 7, 7, 9]
Example #2  |  Sorting
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

Example #2  |  Sorting
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

Example #2  |  Sorting
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

Document project-wide policies  |  e.g., Policies.md
- Every declaration outside a function body must have a documentation comment that describes
  its contract.
  - Start with a summary sentence fragment.
    - Describe what a function or method does and what it returns.
    - Describe what a property or type is.
    - Separate the fragment from any additional documentation with a blank line and end it
      with a period.
  - Preconditions, postconditions and invariants obviously implied by the summary need not
    be explicitly documented.

- End every file with a newline.
- Do not strip trailing whitespace from lines you're not editing; it creates spurious VC diffs.
- Document the performance of every operation that doesn't execute in constant time and space.
- Unless otherwise specified, every function can throw arbitrary exceptions.

Example #2  |  Sorting
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

Errors
Bugs vs. errors
Bug: faulty code
Example:
Precondition is violated
Postcondition is violated
Program may be in a bad state; recovery not possible in general.
Error: code is fine but can't satisfy postcondition
Example:
Resource exhaustion (e.g. memory/disk needed for the operation but unavailable)
Reading document but file on disk is corrupted
Program state is intact
Example #2  |  Adding errors
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

Example #2  |  Adding errors
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T) throws->Bool) { ... }
}

Example #2  |  Adding errors
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T) throws->Bool) rethrows { ... }
}

Postcondition wasn't met  |  What do we know?
Details of mutation are not specified by postcondition.
Can assume mutation doesn't extend beyond the objects the operation modifies in case of success.
What can we say about sort in case of error?
Don't give away the store: premature/speculative features and guarantees are costly, and you're stuck with them.
Clients should assume values under mutation were partially mutated and have meaningless values.
Operating on a meaningless value is a bug.
Three useful possible guarantees regarding errors / exceptions
The basic error / exception guarantee: all invariants are preserved (and nothing is leaked), even in case of error.

The strong error / exception guarantee: if an error is reported, the operation had no effects.

The nothrow / no-error guarantee: the operation will not report errors; if precondition is met, postcondition is fulfilled unconditionally.



Partial mutation breaks invariants!
/// A dynamic random-access collection of `pair<X, Y>`.
class PairVector<X, Y> {
  vector<X> xs;
  vector<Y> ys;
 public:
  /// Adds `p` to the end.
  void push_back(std::pair<X, Y> p) {
    xs.push_back(p.first);
    ys.push_back(p.second);
  }
  ...
}

Upholding invariants  |  The basic guarantee
/// A dynamic random-access collection of `pair<X, Y>`.
class PairVector<X, Y> {
  vector<X> xs;
  vector<Y> ys;
 public:
  /// Adds `p` to the end.
  void push_back(std::pair<X, Y> p) {
    try {
	  xs.push_back(p.first);
	  ys.push_back(p.second);
	}
	catch(...) { xs.clear(); ys.clear(); throw; }
  }
  ...
}

Upholding invariants  |  The basic guarantee
/// A dynamic random-access collection of `pair<X, Y>`.
class PairVector<X, Y> {
  vector<X> xs;
  vector<Y> ys;
 public:
  /// Adds `p` to the end.
  void push_back(std::pair<X, Y> p) {
    try {
	  xs.push_back(p.first);
	  ys.push_back(p.second);
	}
	catch(...) { xs.clear(); ys.clear(); throw; }
  }
  ...
}

Upholding invariants  |  The strong guarantee
/// A dynamic random-access collection of `pair<X, Y>`.
class PairVector<X, Y> {
  vector<X> xs;
  vector<Y> ys;
 public:
  /// Adds `p` to the end.
  ///
  /// - If an exception is thrown, there are no effects.
  void push_back(std::pair<X, Y> p) {
    xs.push_back(p.first);
    try { ys.push_back(p.second); }
	catch(...) { xs.pop_back(); throw; }
  }
  ...
}

Upholding invariants  |  The strong guarantee
/// A dynamic random-access collection of `pair<X, Y>`.
class PairVector<X, Y> {
  vector<X> xs;
  vector<Y> ys;
 public:
  /// Adds `p` to the end.
  ///
  /// - If an exception is thrown, there are no effects.
  void push_back(std::pair<X, Y> p) {
    xs.push_back(p.first);
    try { ys.push_back(p.second); }
	catch(...) { xs.pop_back(); throw; }
  }
  ...
}

Upholding invariants  |  The strong guarantee
/// A dynamic random-access collection of `pair<X, Y>`.
class PairVector<X, Y> {
  vector<X> xs;
  vector<Y> ys;
 public:
  /// Adds `p` to the end.
  ///
  /// - If an exception is thrown, there are no effects.
  void push_back(std::pair<X, Y> p) {
    xs.push_back(p.first);
    try { ys.push_back(p.second); }
	catch(...) { xs.pop_back(); throw; }
  }
  ...
}

Upholding invariants  |  The strong guarantee
/// A dynamic random-access collection of `pair<X, Y>`.
class PairVector<X, Y> {
  vector<X> xs;
  vector<Y> ys;
 public:
  /// Adds `p` to the end.
  ///
  /// - If an exception is thrown, there are no effects.
  void push_back(std::pair<X, Y> p) {
    xs.push_back(p.first);
    try { ys.push_back(p.second); }
	catch(...) { xs.pop_back(); throw; }
  }
  ...
}

Which guarantee?
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1], self[i])` is false for each `i` in
  /// 0 ..< length - 1.
  ///   ...
  /// If an error is thrown, there are no effects.
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T) throws->Bool) rethrows
  {
      var tentative = self                             // copy self
      try tentative.actuallySort(areInIncreasingOrder) // sort the copy
      swap(&self, &tentative)                          // swap if no failure
  }
