import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()


# Read API configuration
api_key = os.getenv("GOOGLE_API_KEY")

model_name = os.getenv(
    "GOOGLE_MODEL",
    "gemini-3.8-flash"
)


# Check API key
if not api_key:

    print("ERROR: GOOGLE_API_KEY not found.")

    raise SystemExit(1)


print("API KEY FOUND")
print("Selected Model:", model_name)

print("\nTesting Gemini connection...")


try:

    model = ChatGoogleGenerativeAI(

        model=model_name,

        google_api_key=api_key,

        temperature=0,

        max_retries=3,

        timeout=120,
    )

    response = model.invoke(
        """
        Generate a short hospital operations summary.

        Mention:
        1. Resource monitoring
        2. Patient queue management
        3. Hospital workflow coordination

        Do not invent statistics.
        """
    )

    # Extract readable text
    content = response.content

    if isinstance(content, list):

        text_parts = []

        for block in content:

            if isinstance(block, dict):

                text_value = block.get("text", "")

            elif isinstance(block, str):

                text_value = block

            else:

                text_value = getattr(
                    block,
                    "text",
                    ""
                )

            if text_value:
                text_parts.append(str(text_value))

        content = "\n".join(text_parts)

    print("\n" + "=" * 50)

    print("GEMINI CONNECTION SUCCESSFUL")

    print("=" * 50)

    print("\nGENERATED RESPONSE:\n")

    print(content)

    print("\n" + "=" * 50)


except Exception as error:

    print("\n" + "=" * 50)

    print("GEMINI CONNECTION FAILED")

    print("=" * 50)

    print("\nERROR DETAILS:")

    print(error)