# Introduction

This book is the product of the Authors' shared career-long mission to
empower programmers and elevate the practice of programming. The title
comes from Sean's influential *Better Code* series of talks, which
came out of Herb Sutter's suggestion that he focus on practical tips a
developer could apply immediately to improve their code.


Taken
together, these enormously influential talks reveal a surprising
truth: the most impactful practical advice is also deeply principled.
Correctness, quality, and yes, even velocity and satisfaction go hand
in hand with


That talk was
sub-titled "Three Goals for Better Code." That talk was given over a decade ago,
and what follows is a reflection of my and my coauthor's distillation of our
career-long pursuit to write, and assist others in writing, better code.


It is not a how-to guide, or a book on software engineering practices


. Euclid famously said "there is no royal road to
geometry." Likewise, there is no royal road to better code. To get the most out
of this book you're going to have to engage deeply with the material. The
included exercises are necessary to hone your skills.

This book is also not a book on software engineering practices. We will not
cover topics like Agile, Scrum, team dynamics, meeting customer's expectations,
or other such concerns. There is much involved in building great software but
this book is focused on the qualify of the code you write when in front of your
keyboard.

Each chapter will start with a _rubric_, often [always?] stated as what _not_ to
do. The chapter will then explain why such constructions work against one or
more of our measures and what some better alternatives might be. Ultimately, the
choice of what _to do_ is going to depend on the specific constraints of the
problem you're solving.


- Confidence in your results
- Velocity
- Less code to maintain
- Easier debugging
- Less debugging

and their work more rewarding.

+## Who we are
+
+## Why we wrote this book
+
+## Why and how you will benefit
+
 ## What to expect

This book is about how to write _better code_. The idea for this book came from
Herb Sutter who suggested I (Sean) give a talk focused on practical tips a
developer could apply immediately to improve their code. That talk was
sub-titled "Three Goals for Better Code." That talk was given over a decade ago,
and what follows is a reflection of my and my coauthor's distillation of our
career-long pursuit to write, and assist others in writing, better code.

This book presents and advocates for a principled and rigorous approach to
software development. Instead of focusing on finding _a_ solution to a problem,
we'll be searching for the _best_ solution. This kind of endeavor necessarily
requires a certain amount of discipline and effort, but our goal is that the
book is approachable and immediately applicable while having enough depth that
you'll keep coming back to it as you gain experience.

The name of the book
implies that we have some way to measure the _quality_ of code, and that we can
objectively improve it. 

We start by defining, _good code_:

> _good code_: code that is _correct_ , _efficient_ , and _abstract_.

A _correct_ program is without contradictions to any relavent specification,
documentation, tests, or examples. Correctness defined in this way is either
satified or not, and is not something that can be incrementally improved. 

This definition is unsatisfying because in practice, we rely on incorrect
software all the time. As a practical approach, we define a _semi-correct_
program as one for which there exists a valid initial state and inputs, such
that the program will generate a valid output. As an analogy, a broken clock is
semi-correct, it is correct twice a day. This definition provides a partial
ordering of correctness, where a program is _more correct_ than another if the
initial states under which it is correct are a superset of the other.

An _efficient_ program uses minimal resources (time, space, energy, etc.) to
generate a valid output. A program is _more efficient_ than another if it uses
less resources to generate the same output.

An _abstract_ program relies on a minimal set of assumptions, _axioms_, that if
true, will allow the program to generate valid output. A program expressed in an
abstract form can be reused anyplace the underlying axioms hold.

As we will see, these three measures are sometimes at odds with each other and
we are limited by the programming language and tools we have available. We do
not see a way to achieve a perfect program but we strive to be more correct,
more efficient, and more abstract. We strive for _better code_.

## What to expect

This book is not a how-to guide. Euclid famously said "there is no royal road to
geometry." Likewise, there is no royal road to better code. To get the most out
of this book you're going to have to engage deeply with the material. The
included exercises are necessary to hone your skills.

This book is also not a book on software engineering practices. We will not
cover topics like Agile, Scrum, team dynamics, meeting customer's expectations,
or other such concerns. There is much involved in building great software but
this book is focused on the qualify of the code you write when in front of your
keyboard.

Each chapter will start with a _rubric_, often [always?] stated as what _not_ to
do. The chapter will then explain why such constructions work against one or
more of our measures and what some better alternatives might be. Ultimately, the
choice of what _to do_ is going to depend on the specific constraints of the
problem you're solving.

## Programming Language

The examples in this book are written in Swift. We chose Swift because it
provides capabilities that balance the three measures so we can illustrate the
concepts in a way that is easy to understand and easy to implement without
getting bogged down by language limitations.

The ideas in this book are not specific to Swift. We have included in Appendix A
a short language summary to help you understand the examples if you are not
familiar with Swift. The ideas are applicable to any language although every
language has trade-offs that will make the expression of the ideas more or less
awkward.

## Forewarning

It is important to forwarn you that we're going to take some strong stances
against some of today's commonly accepted practices. We want to emphasize that
these are exclusively criticisms of practices, not practitioners. We urge you to
keep an open mind as you reflect upon our suggested alternatives. You can expect
that it may take some time reviewing code in practice before you reach the same
conclusions we have. Of course, you might never agree with our conclusions. We
encourage you to rigorously develop your criticisms of our work, and invite you
into the uniquely cooperative pursuit of programming truth.

## Exercises

[ Say something here about the importance and structure of exercises ]
