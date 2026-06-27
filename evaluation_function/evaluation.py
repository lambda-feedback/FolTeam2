from typing import Any

from lf_toolkit.evaluation import Result, Params

# Generic grader for "which two sources share the same substance?"
# short-answer questions, where the correct pair is identified by matching
# characteristic properties (e.g. density, melting point) given in a
# comparison table. `params.sources` lists every source name in the
# question's table, so a wrongly named source can be told apart from a
# missing one.

_DEFAULT_SOURCES = ("honey", "milk", "sugarcane", "sugar cane", "apple")


def _mentioned_sources(text: str, sources) -> set:
    text = text.lower()
    return {source for source in sources if source in text}


def evaluation_function(
    response: Any,
    answer: Any,
    params: Params,
) -> Result:
    """
    Grades short-answer responses naming the two sources that share the
    same substance.
    ---
    - `answer` holds the correct pair of source names, e.g. "Honey and Apple".
    - `response` is the student's short answer naming the pair they picked.
    - `params.sources` (optional) lists every source name in the question's
      table. Defaults to the sugar-comparison sources.
    """

    sources = [s.lower() for s in params.get("sources", _DEFAULT_SOURCES)]

    expected = _mentioned_sources(str(answer), sources)
    given = _mentioned_sources(str(response), sources)

    is_correct = bool(expected) and given == expected

    if is_correct:
        feedback = "Correct! These two sources share the same substance."
    elif not given:
        feedback = "Name the two sources you think share the same substance."
    elif given - expected:
        feedback = "One or more of the sources you named don't match. Check the table values again."
    else:
        feedback = "You're missing one of the two matching sources."

    return Result(
        is_correct=is_correct,
        feedback_items=[("general", feedback)],
    )
