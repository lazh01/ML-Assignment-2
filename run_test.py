import json
import time
from evaluation.test_prompts import EVALUATION_PROMPTS

from agents.planner import planner
from agents.research_agent import research_agent
from workflow.pipeline import run_pipeline


OUTPUT_FILE = "evaluation_results.json"


def evaluate_prompt(prompt: str):
    """
    Runs one evaluation query through the pipeline.
    """

    print(f"\n=== Running Prompt ===")
    print(prompt)

    try:
        result = run_pipeline(prompt, planner, research_agent)

        # Extract full response text properly
        response_text = ""

        if isinstance(result, dict):

            # Try common AutoGen patterns
            if "content" in result:
                response_text = result["content"]

            elif "messages" in result:
                messages = result["messages"]

                if messages and isinstance(messages, list):
                    response_text = messages[-1].get("content", str(messages[-1]))

            else:
                response_text = json.dumps(result, indent=2)

        else:
            response_text = str(result)

        return {
            "prompt": prompt,
            "response": response_text,
            "success": True
        }

    except Exception as e:
        return {
            "prompt": prompt,
            "response": None,
            "success": False,
            "error": str(e)
        }


def main():

    all_results = []

    for idx, prompt in enumerate(EVALUATION_PROMPTS, start=1):

        print(f"\n[{idx}/{len(EVALUATION_PROMPTS)}] Evaluating...")

        result = evaluate_prompt(prompt)

        all_results.append(result)

        # Avoid API rate limits
        time.sleep(2)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\nSaved evaluation results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()