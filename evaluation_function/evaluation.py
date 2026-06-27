import re
from typing import Any

from lf_toolkit.evaluation import Result, Params

# Rubric for: "Which of the above sources has the same type of sugar? Why?"
# Correct claim: honey and apple share the same sugar, evidenced by matching
# density (~1.69-1.70 g/cm3) and melting point (103 oC), reasoned through the
# fact that density and melting point are characteristic properties used to
# identify a substance.

_CLAIM_NAMES = ("honey", "apple")

_NEGATION_PATTERN = re.compile(
    r"\bnone\b.{0,40}same sugar|\bno(ne)? of (them|the).{0,30}same sugar",
    re.IGNORECASE,
)

_REASONING_KEYWORDS = (
    "characteristic propert",
    "identify the substance",
    "identifies substances",
    "identify substances",
    "unique substance",
    "same substance",
    "used to identify",
    "determine whether",
)


def _check_claim(text: str) -> bool:
    if _NEGATION_PATTERN.search(text):
        return False
    return all(name in text for name in _CLAIM_NAMES)


def _check_evidence(text: str) -> bool:
    has_density = "density" in text
    has_melting_point = "melting point" in text or "melt" in text
    return has_density and has_melting_point


def _check_reasoning(text: str) -> bool:
    return any(keyword in text for keyword in _REASONING_KEYWORDS)


def evaluation_function(
    response: Any,
    answer: Any,
    params: Params,
) -> Result:
    """
    Grades open-ended responses to the "Comparing Types of Natural Sugars"
    question using a claim/evidence/reasoning (CER) rubric.
    ---
    A response is marked correct only if it:
    - Claims honey and apple have the same sugar (the claim).
    - Cites density and melting point as supporting data (the evidence).
    - Explains that matching characteristic properties identify the same
      substance (the reasoning).
    """

    text = str(response).lower()

    claim_ok = _check_claim(text)
    evidence_ok = _check_evidence(text)
    reasoning_ok = _check_reasoning(text)

    if claim_ok and evidence_ok and reasoning_ok:
        feedback = "Well done! Your claim, evidence, and reasoning are all correct."
    else:
        feedback_parts = []
        if not claim_ok:
            feedback_parts.append(
                "Your claim should state that honey and apple contain the same type of sugar."
            )
        if not evidence_ok:
            feedback_parts.append(
                "Support your claim with evidence: the density and melting point values from the table."
            )
        if not reasoning_ok:
            feedback_parts.append(
                "Explain your reasoning: density and melting point are characteristic properties, "
                "so matching values mean the sugar is the same substance."
            )
        feedback = " ".join(feedback_parts)

    return Result(
        is_correct=claim_ok and evidence_ok and reasoning_ok,
        feedback=feedback,
    )
