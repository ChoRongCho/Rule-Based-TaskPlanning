(define (domain blocksworld)
    (:requirements :strips :typing)
    (:types block table robot)
    (:predicates
        ; general predicates
        (on ?x - block ?y - block) ; x is on the y
        (ontable ?x - block)
        (clear ?x - block)

        ; robot predicates
        (handempty ?x - robot)
        (handfull ?x - robot)
        (holding ?x - block)

        ; object property predicates

        ; add other predicates if you need
        ; I'll leave it to your imagination
    )
    (:action pick-up
        :parameters (?x - block ?robot - robot)
        :precondition (and
            (clear ?x) 
            (ontable ?x) 
            (handempty ?robot)
        )
        :effect (and
            (not (ontable ?x))
            (not (clear ?x))
            (not (handempty ?robot))
            (handfull ?robot)
            (holding ?x)
        )
    )
    (:action put-down
        :parameters (?x - block ?robot - robot)
        :precondition (and 
            (holding ?x)
            (handfull ?robot)
        )
        :effect (and 
            (not (holding ?x))
            (clear ?x)
            (handempty ?robot)
            (not (handfull ?robot))
            (ontable ?x))
        )
    (:action stack
        :parameters (?x - block ?y - block ?robot - robot)
        :precondition (and
            (holding ?x) 
            (clear ?y)
            (handfull ?robot)
        )
        :effect (and 
            (not (holding ?x))
            (not (clear ?y))
            (clear ?x)
            (handempty ?robot)
            (not (handfull ?robot))
            (on ?x ?y)
        )
    )
    (:action unstack
        :parameters (?x - block ?y - block ?robot - robot)
        :precondition (and
            (on ?x ?y)
            (clear ?x)
            (handempty ?robot)
        )
        :effect (and 
            (holding ?x)
            (clear ?y)
            (not (clear ?x))
            (not (handempty ?robot))
            (handfull ?robot)
            (not (on ?x ?y))
        )
    )
)