import requests
from argparse import ArgumentParser
import subprocess
import base64

def get_access_token():
    result = subprocess.run(["gcloud", "auth", "print-access-token"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()

def ask_gemini(
            prompt: str,
            project_id: str = "bliss-hack24ber-6526",
            model_id: str = "gemini-1.5-pro-preview-0409",
            image_url: str = ""
    ):
    print("Prompt:", prompt)
    parts = [
                {
                "text": prompt
                }
            ]
    if image_url != "":
        parts.append({
                    "fileData": {
                        "mimeType": "image/webp",
                        "fileUri": image_url
                    }
                })
    response = requests.request("POST", f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/{model_id}:streamGenerateContent",
        headers={
            "Authorization": f"Bearer {get_access_token()}",
            "Content-Type": "application/json; charset=utf-8"
        },
        json={
            "contents": {
            "role": "user",
            "parts": parts
            }
        }
    ).json()
    print(response)
    answer = "".join(part["candidates"][0]["content"]["parts"][0]["text"] for part in response)
    print("Answer:", answer)
    return answer


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("prompt", type=str, help="Prompt, use quotes")
    args = parser.parse_args()
    gen_img(args.prompt)