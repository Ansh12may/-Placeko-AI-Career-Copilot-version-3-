# from groq import Groq

# client = Groq()
# completion = client.chat.completions.create(
#     model="openai/gpt-oss-120b",
#     messages=[
#       {
#         "role": "user",
#         "content": ""
#       }
#     ],
#     temperature=1,
#     max_completion_tokens=2048,
#     top_p=1,
#     reasoning_effort="medium",
#     stream=True,
#     stop=None
# )

# for chunk in completion:
#     print(chunk.choices[0].delta.content or "", end="")

# from backend.tools.resume_parser import parse_resume

# text = parse_resume("/Users/ashutoshkushwaha/Desktop/Ashutosh_resume.pdf")
# print(text)

from pathlib import Path
from backend.graphs.workflow import graph
from backend.graphs.state import GraphState
def main():
    state: GraphState = {
        "messages": [],
        "resume_path": Path("/Users/ashutoshkushwaha/Desktop/Ashutosh_resume.pdf"),
        "resume_text": "",
        "candidate_profile": None,
        "next_node": None,
        "error": None,

    }
    try:
        result = graph.invoke(state)
        print("=" * 80)
        print("RESUME TEXT")
        print("=" * 80)
        print(result["resume_text"])
        print()
        print("=" * 80)
        print("CANDIDATE PROFILE")
        print("=" * 80)
        if result["candidate_profile"] is not None:
            print(result["candidate_profile"].model_dump_json(indent=4))
        else:
            print("No candidate profile returned.")
    except Exception as e:
        print(f"\nError: {e}")
if __name__ == "__main__":
    main()