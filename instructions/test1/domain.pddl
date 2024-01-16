;Header and description

(define (domain packing)

;remove requirements that are not needed
(:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    out_bin, bin - place
    robot
    item - object
    soft - property
)

(:predicates ;todo: define predicates here

    ; General place predicates
    (is-clear ?out_bin)
    (is-empty ?bin)

    ; Robot predicates
    (hand-empty ?robot)

    ; Object property predicates
    (is_soft ?soft ?item)

    ; Object place predicates
    (out_of_bin ?item)
    (in_bin ?item)
)


(:functions ;todo: define numeric functions here
)

;define actions here
(:action pick
    :parameters ()
    :precondition (and )
    :effect (and )
)

(:action place
    :parameters ()
    :precondition (and )
    :effect (and )
)

(:action fold
    :parameters ()
    :precondition (and )
    :effect (and )
)

(:action press
    :parameters ()
    :precondition (and )
    :effect (and )
)
)