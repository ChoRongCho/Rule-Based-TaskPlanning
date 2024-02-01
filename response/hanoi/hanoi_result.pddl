```pddl
(define (domain hanoi)
(:requirements :strips :equality :typing)
(:types 
    disk peg)

(:predicates 
    (on ?x - disk ?y - (either disk peg)) 
    (smaller ?x - disk ?y - disk) 
    (clear ?x - (either disk peg)))

(:action move
    :parameters (?disk - disk ?from - (either disk peg) ?to - (either disk peg))
    :precondition (and (on ?disk ?from) (clear ?disk) (clear ?to) (smaller ?disk ?to))
    :effect (and 
        (not (on ?disk ?from)) 
        (not (clear ?to)) 
        (on ?disk ?to) 
        (clear ?from))))
```