(define (problem blocksworld_problem)
  (:domain blocksworld)
  (:objects 
    block1 block2 block3 block4 - block
    table1 table2 table3 table4 - table
    robot1 - robot
  )
  (:init 
    (on block1 block2)
    (on block2 block3)
    (on block3 table1)
    (on block4 table2)
    (clear table1)
    (clear table2)
    (clear table3)
    (handempty robot1)
  )
  (:goal 
    (and 
      (on block3 block2)
      (on block2 table1)
      (on block4 block1)
      (on block1 table3)
    )
  )
)