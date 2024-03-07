(define (problem bin_packing1) (:domain bin_packing_gt)
(:objects 
    item1, item2, item3, item4 - object
    bot - robot
    bin - box
)

(:init
    (handempty bot)

    (not (in_bin item1 bin))
    (not (in_bin item2 bin))
    (not (in_bin item3 bin))
    (not (in_bin item4 bin))

    (is_fragile item1)
    (is_soft item2)
    (is_soft item3)
    (is_foldable item4)
)

(:goal (and
    (in_bin item1 bin)
    (in_bin item2 bin)
    (in_bin item3 bin)
    (in_bin item4 bin)
    (on item1 item2)
    (pushed item3)
    (folded item4)
))
)
