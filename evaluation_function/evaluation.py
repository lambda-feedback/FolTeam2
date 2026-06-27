import json
import os
from typing import Any
from openai import OpenAI
from dotenv import load_dotenv
from lf_toolkit.evaluation import Result, Params

load_dotenv()

DEFAULT_MODEL = "openai/gpt-4o-mini"



def evaluation_function(
    response: Any,
    answer: Any,
    params: Params,
) -> Result:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """

    client = OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        max_retries=3,
    )

    FEEDBACK_DIMENSION_PROMPT="""
    Provide the feedback on these dimseions: 1) Claim 2) Evidence 3) Reasoning. Provide the feedback in one sentence for each..
    """

    question = params.get("question")
    model = params.get('model', DEFAULT_MODEL)

    system_prompt = (
        f"{FEEDBACK_DIMENSION_PROMPT} You are a science teacher grading a student's short-answer response. "
        'Output your response as a JSON object with exactly two fields: '
        '"is_correct" (boolean, true if the student response is correct, false otherwise) '
        f'and "feedback" (string, feedback for the student). The question is: {question} '
        f'The correct answer is: {answer}.'
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": response},
        ],
    )

    raw = completion.choices[0].message.content.strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON: {e}") from e

    result = Result(is_correct=bool(data["is_correct"]))
    result.add_feedback("feedback", str(data.get("feedback", "")))
    return result
