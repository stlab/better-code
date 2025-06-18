Okay, now let's talk about errors.  So we already talked about bugs as
faulty code, resulting in a failure to satisfy preconditions or
postconditions.  If we detect one of these conditions, in general,
there's no way to know where the bug is or how much damage has been
done to the program's supposed invariants: it could be "in a bad
state."  The bug may have been in the very code that was responsible
for maintaining that state.  That's why diagnosing and fixing bugs is
hard!

An error is not-that.  When there's an error, no code is at fault, but
the postcondition can't be satisfied.

For example, you can't save a document if the disk is full, and you
may not be able to load a document from disk if the data turns out to
be corrupted.  In these cases the program state is still okay, and the
client might have a reasonable way to recover and continue running.
Sometimes this just means reporting the error to the user and waiting
for the next command.

>> So only the neeedless postcondition violations are bugs.Let's
>update our sorting function to deal with a comparison that can report
>errors.  Maybe the comparison needs to allocate space on disk or
>something.

In Swift we'd do that by making the comparison a throwing function.
And then we have to say that sort can throw if the comparison can
throwIn Swift, if something is going to throw, you have to declare
that fact explicitly, If you're stuck with a language like C++,
Python, or Java that doesn't make you put error information in the
signature, you have to find another way to document it for client
coders.

In those cases I normally have a policy that by default, anything can
report an error, and say that operations that will never report errors
must document that fact.

Because we said an error represents a failure to meet postconditions,
the postcondition doesn't tell you anything about the the state of the
program when an error is reported.  But if you really don't know
*anything* about the state of the program, you probably can't recover.

Fortunately, we can assume by default that a failing operation only
mutates the things it would mutate in case of success.

So in the case of `sort`, we know the array was mutated… somehow, but
we don't know much more than that.  Is there anything more we can
reasonably guarantee in case of an error?

You might think, it's _possible_ that our clients could do something
with the array if they know that the array is still a permutation of
the original elements, just rearranged, but I want to caution you
against the line of thinking that goes, “it's *conceivable* that some
unknown client may have a use for this feature or guarantee, so I'm
going to give it to them.”

1. It's very hard to retract once it's given, because you may break
   code.
2. The guarantee complicates your contract: it needs to be described;
   potential clients need to read and understand it.
3. The guarantee is likely to complicate your implementation and your
   tests.
4. Making needless guarantees may constrain the implementation in ways
   that rule out the most efficient implementation, now or in the
   future.

In general, describing a partially mutated state is complex, probably
not useful, and may be impossible. So clients need to assume values
under mutation have arbitrary meaningless values after an error is
reported.

This is not as useless as it sounds at first: there's a good chance
they're on the stack and will be destroyed when the scope exits.  And
if you work on a desktop application with undo, it's effectively
saving a snapshot of the document before every mutation, so your
program is very likely set up to discard partial mutations of
important state.

So this is the theory of error handling I developed back in 1998 for
the C++ standard library.  It says that there are 3 useful kinds of
promises an operation can make with respect to errors.

The minimum guarantee is this basic guarantee that invariants are
always upheld, the idea being that we don't know how to reason about a
program if broken invariants are visible outside a type's
encapsulation boundary.

The next stronger guarantee says that if an error is reported, the
operation has no observable effects; it's transactional

And then the strongest guarantee an operation can make is that it
won't report any errors at all.  You need a no-error guarantee from
any operations used in error recovery, or you end up with some kind of
infinite recovery recursion.  I told you that you can lean on
invariants for reasoning, so you might find the idea of an
interrupted, partial mutation alarming, because that could leave
invariants broken.  That collection of pairs offers a good example, if
appending an element to a vector can fail, as in C++

Now I realize that lots of modern programming languages treat
out-of-memory as something that can't happen, so if you use one of
those languages, imagine that the private arrays in this thing are a
different type, `DiskVector`, that's backed by storage on disk, and we
can run out of disk space trying to grow them.

If an error occurs trying to do the second append, as coded, we're
left with a broken invariant, because the length of `xs` is one
greater than the length of `ys`.

So how could we uphold the invariant? There are a number of
strategies.

Here's one totally legit way.

If anything fails, we just discard all the elements.  This is what we
call the Basic Error Guarantee: it says that all invariants are upheld
and nothing is leaked.

This is a nice place to land because the instance of `PairVector` is
still in a good state, and its operations still function as normal.
On the other hand, even if the invariant is upheld, from the client's
perspective this is still a partially mutated object with a
meaningless value, and we really shouldn't be doing anything with it.
We'll come back to that.

By the way, we need to know something in order for this method to give
the basic guarantee: it only works if `clear()` can't fail—if it gives
the nothrow or nofail guarantee.  Remember I said that whether an
error can occur is part of an operation's contract?  It's crucial
information because error *recovery* needs to use operations that
can't themselves report errors.

In contrast, which specific errors can be reported is comparatively
unimportant except for the very lowest level primitives, because
there's usually just one strategy for error recovery.  And remember,
if you try to spell that information out and your clients don't need
it, you've fallen into the trap of giving premature guarantees.It
turns out that `push_back` can give a stronger guarantee than the
basic one if we recover this way:

>> If the second `push_back` fails, we just undo the first one and the
>`PairVector` is unchanged.  >>

The strong guarantee that an operation either succeeds or has no
effects is actually useful to clients in practice, unlike most
statements describing partial mutations.It's also very simple to
describe, so it doesn't overly complicate the specification.

In fact, we're taking advantage of the strong guarantee from
`vector`'s own `push_back` method hereit's why no recovery is needed
if the first `push_back` failsand it's why the catch block only needs
to adjust `xs`: because we know that if we get there, `ys` is still
unchanged.

So this is nice.  Should all operations give the strong guarantee?
Let's look at sort

Pretty much the only way to get the strong guarantee here is to use
what I call a "copy and swap" strategy.

First we make a copy of the thing under mutation, then we try to do
the mutation on the copy, and only if everything works out, we swap
the original for the copy.

This approach leaves `self` unmodified if `actuallySort` fails.  But
it's super expensive: it allocates memory, and incurs O(N) space and
time overhead.  Since we're not sure every client of `sort` needs the
strong guarantee, we shouldn't force them to accept this expense.
It's a form of giving away the store.

On the other hand, the strong guarantee makes sense for `PairVector`'s
`push_back` because it's achievable without loss of efficiency. It
even falls out of maintaining invariants in the most natural way.

What you've seen so far is basically the theory of error handling that
I developed back in 1998 for the C++ standard library, with every
operation being required to give at least the Basic Guarantee, because
the idea that invariants must always be maintained is sort of
foundational. It's a tried and true way to approach thinking about
errors and correctness.  But I'd be remiss if I didn't describe Sean's
2022 update to the theory which he calls “error handling the other way
around.”

It's based on the insight that an unknown partially-mutated value is
meaningless, so any operations you do on it, other than destruction
and maybe assignment, represent a bug—also known as nonsense.
Remember if the client uses an operation in a buggy way, the ethos of
blame says the operation has no obligations.

So Sean's thesis is that when an operation can't efficiently give the
strong guarantee, maybe upholding invariants is a waste of effort,
because further operations on the value are all bugs.

It's the client's obligation to discard any partially mutated value
via destruction or assignment, so all we really need to do is leave
the partially-mutated object in a destructible and assignable state.

In my 1998 theory of error handling, type invariants are required to
hold after every public operation, whether an error is reported or
not.  If we do error handling “the other way around,” they're only
required to hold if the operation is successful or if it gives the
strong guarantee.  Whichever policy you choose—you got it—write it
down in your policy document.  You own a supercar, a $8M Bugatti Divo.
This thing has extremely tight tolerances, basically to be “in a good
state” you have to care for it properly and maintain its invariants.
Therefore you've got a contract with an ultra-exclusive "car butler"
who takes care of all the maintenance, including refueling.  The
contract, of course, says the butler is only going to use
ultra-premium gas.  One day you get a notice from the state that says
it's time to come in for a smog check. You have your assistant drive
take the car in and you find out the car violates the precondition for
continued operation.  You take the car back to the dealer and they
tell you the engine is shot and now the car is valued at only $2M,
practically worthless.  How did this happen?!  You ask the dealer to
investigate, so they do a whole battery of tests and the only thing
they can find is that the car's tank is full of economy gas like you'd
use in a Prius.  Your butler, clearly, had a bug, and the wrong fuel
has been eating away at the valves and piston heads for months.  You
never really push the car too hard, so you don't notice any difference
in performance, but the damage is done.
