;Header and description

(define (domain bin_packing_gt)

;remove requirements that are not needed
(:requirements :strips :typing :conditional-effects)

(:types 
    object
    robot
    box
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    ; general predicates
    (in_bin ?x - object ?b - box)

    ; robot predicates
    (handempty ?r - robot) ; robot_hand is empty.
    (handfull ?r - robot) ; robot hand is full, that means, robot is now holding something.
    (holding ?x - object)

    ; object property predicates
    (is_soft ?x - object) ; object x is soft
    (is_foldable ?x - object) ; object x is foldable
    (is_elastic ?x - object) ; object x is elastic
    (is_fragile ?x - object) ; object x is fragile

    ; on the object
    (on ?x -object ?y - object)
    (folded ?x - object)
    (pushed ?x - object)
)


;define actions here
(:action pick
    :parameters (?x - object, ?r - robot, ?b - box)
    :precondition (and 
        (handempty ?r)
    )
    :effect (and 
        (not (handempty ?r))
        (handfull ?r)
        (in_bin ?x ?b)
        (holding ?x)
    )
)

(:action place
    :parameters (?x - object, ?y - object, ?r - robot, ?b - box)
    :precondition (and 
        (handfull ?r) 
        (holding ?x)
    )
    :effect (and 
        (when (and (is_fragile ?x) (is_soft ?y) (in_bin ?y ?b)) (on ?x ?y))
        (handempty ?r)
        (not (handfull ?r))
        (not (holding ?x))
        (in_bin ?x ?b)
    )
    
)

(:action fold
    :parameters (?x - object, ?r - robot)
    :precondition (and 
        (is_foldable ?x)
        (handempty ?r)
    )
    :effect (and 
        (handempty ?r)
        (folded ?x)
        (not (is_foldable ?x))
    )
)

(:action push
    :parameters (?x - object ?r - robot ?b - box)
    :precondition (and 
        (handempty ?r)
        (in_bin ?x ?b)
        (is_soft ?x)
    )
    :effect (and 
        (pushed ?x)
    )
)
)