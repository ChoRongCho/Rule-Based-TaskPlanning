(define (domain blocksworld)
    (:requirements :strips :typing)
    (:types block table robot)
    (:predicates 
        (on ?x - block ?y - block)
        (clear ?x - block)
        (handempty ?x - robot)
        (handfull ?x - robot)
        (holding ?x - block)
    )
    (:action pick-up
        :parameters (?x - block ?robot - robot)
        :precondition (and
            (clear ?x) 
            (on ?x ?y)  ; 추가된 부분
            (handempty ?robot)
        )
        :effect (and
            (not (on ?x ?y))  ; 추가된 부분
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
            (on ?x ?y)  ; 추가된 부분
        )
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