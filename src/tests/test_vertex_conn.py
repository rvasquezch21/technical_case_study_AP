import os
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()


def test_connection():
    print("--- Starting Vertex AI Connectivity Test (Cloud Shell) ---")

    try:
        # On Cloud Shell, initialization is cleanest when we let
        # the SDK pull from the environment automatically.
        client = genai.Client(vertexai=True)

        print(f"Project:  {os.getenv('GOOGLE_CLOUD_PROJECT')}")
        print(f"Location: {os.getenv('GOOGLE_CLOUD_LOCATION')}")

        # Testing with a stable model version
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Are we connected?"
        )

        print(f"\nResponse: {response.text.strip()}")
        print("\n--- Success: Cloud Shell Identity Verified ---")

    except Exception as e:
        print(f"\n--- Test Failed ---")
        print(f"Error: {e}")


if __name__ == "__main__":
    test_connection()