(define (domain hanoi)
    (:requirements :strips)
    (:predicates
        ; general predicates
        (clear ?x)
        (on ?x ?y)
        (smaller ?x ?y)

        ; robot predicates
        (move ?disc ?to)

        ; object property predicates

        ; add other predicates if you need
    )
    (:action move
        :parameters (?disc ?from ?to)
        :precondition (and (smaller ?to ?disc) (on ?disc ?from)
                      (clear ?disc) (clear ?to))
        :effect  (and (clear ?from) (on ?disc ?to) (not (on ?disc ?from))
                 (not (clear ?to)))
    )
)
