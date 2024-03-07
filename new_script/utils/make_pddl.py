from pddl.action import Action
# from pddl.logic.base import And
from pddl.core import Domain  # , Problem
from pddl.formatter import domain_to_string  # , problem_to_string
from pddl.logic import Predicate, variables
from pddl.requirements import Requirements


def make_domain(domain_name):
    x, y = variables("x y", types=["block"])
    r = variables("r", types=["robot"])[0]

    # r = variables("r", types=["robot"])

    requirements = [Requirements.STRIPS, Requirements.TYPING]

    p_on = Predicate("on", x, y)
    p_ontable = Predicate("ontable", x)
    p_clear = Predicate("clear", x)

    p_handempty = Predicate("handempty", r)
    p_handfull = Predicate("handfull", r)
    p_holding = Predicate("holding", x)

    predicates = [p_on,
                  p_ontable,
                  p_clear,
                  p_handempty,
                  p_handfull,
                  p_holding]

    pickup = Action(
        "pick-up",
        parameters=[x, r],
        precondition=p_clear(x) & p_ontable(x) & p_handempty(r),
        effect=~p_ontable(x) & ~p_clear(x) & ~p_handempty(r) & p_handfull(r) & p_holding(x),
    )

    putdown = Action(
        "put-down",
        parameters=[x, r],
        precondition=p_handfull(r) & p_holding(x),
        effect=p_ontable(x) & p_clear(x) & p_handempty(r) & ~p_handfull(r) & ~p_holding(x),
    )

    stack = Action(
        "stack",
        parameters=[x, y, r],
        precondition=p_holding(x) & p_clear(y) & p_handfull(r),
        effect=p_on(x, y) & p_clear(x) & ~p_clear(y) & p_handempty(r) & ~p_handfull(r) & ~p_holding(x),
    )

    unstack = Action(
        "unstack",
        parameters=[x, y, r],
        precondition=p_on(x, y) & p_clear(x) & p_handempty(r),
        effect=~p_on(x, y) & ~p_clear(x) & p_clear(y) & ~p_handempty(r) & p_handfull(r) & p_holding(x),
    )

    actions = [pickup,
               putdown,
               stack,
               unstack]

    domain = Domain(domain_name,
                    requirements=requirements,
                    types={"block": None, "robot": None},
                    predicates=predicates,
                    actions=actions)

    return domain


def main():
    domain = make_domain("blocksworld")
    result = domain_to_string(domain)
    print("\n\n\n\n\n\n")
    print(result)


if __name__ == '__main__':
    main()
