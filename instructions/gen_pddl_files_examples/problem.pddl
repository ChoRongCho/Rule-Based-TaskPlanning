(define (problem packing)
(:domain packing)
(:objects
    item1, item2, item3 - item
    bot - robot
    box - bin
    plate - out_bin
)

(:init
    (is-empty box)
    (hand-empty bot)
    (out_of_bin item1)
    (out_of_bin item2)
    (out_of_bin item3)
)

(:goal
    (and
        (is-clear plate)
        (hand-empty bot)
        (in_bin item1)
        (in_bin item2)
        (in_bin item3)
    )
)
)
