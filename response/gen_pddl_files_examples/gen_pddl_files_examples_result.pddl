(define (domain packing)
  (:requirements :strips :typing :conditional-effects :negative-preconditions :equality)
  (:types 
    item - object
    robot
    bin out_bin - place
    soft fragile flexible rigid - property
  )

  (:predicates
    (is-clear ?out_bin - out_bin)
    (is-empty ?bin - bin)
    (hand-empty ?robot - robot)
    (is-soft ?item - item)
    (is-fragile ?item - item)
    (is-flexible ?item - item)
    (is-rigid ?item - item)
    (out_of_bin ?item - item)
    (in_bin ?item - item)
    (on_top ?item1 ?item2 - item)
  )

  (:action pick
    :parameters (?item - item ?robot - robot ?out_bin - out_bin)
    :precondition (and (hand-empty ?robot) (out_of_bin ?item) (is-clear ?out_bin))
    :effect (and (not (hand-empty ?robot)) (not (out_of_bin ?item)))
  )

  (:action place
    :parameters (?item - item ?robot - robot ?bin - bin)
    :precondition (and (not (hand-empty ?robot)) (is-empty ?bin))
    :effect (and (hand-empty ?robot) (in_bin ?item) (is-empty ?bin))
  )

