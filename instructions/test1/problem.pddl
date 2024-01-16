(define (problem packing)

(:domain packing)

(:objects
    item1, item2, item3, item4 - item
    bot - robot
    box - bin
    plate - out_bin
)

(:init
    ; additional initial state
    (is_soft item1)
    (is_rigid item2)
    (is_flexible item1)
    (is_flexible item3)
    (is_fragile item4)

    ; basic initial state
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
        (in_bin item4)
        (is_full box)
    )
)
)
