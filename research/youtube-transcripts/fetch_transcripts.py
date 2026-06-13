import os
import re
import requests

API_KEY = "sd_1c2139d8bf6b2b38201f752a9b9950da"

def get_video_id(url):
    pattern = r"(?:v=|\/shorts\/|\/embed\/|\/v\/|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_transcript(url, filename):
    video_id = get_video_id(url)
    if not video_id:
        print(f"Could not extract video ID from {url}")
        return

    try:
        response = requests.get(
            "https://api.supadata.ai/v1/youtube/transcript",
            params={"videoId": video_id, "format": "text"},
            headers={"x-api-key": API_KEY}
        )

        if response.status_code != 200:
            print(f"❌ Error fetching {url}: {response.status_code} {response.text}")
            return

        data = response.json()
        content = data.get("content", "")
        if isinstance(content, list):
            transcript_text = " ".join([c.get("text", "") for c in content])
        else:
            transcript_text = content

        output_path = f"research/youtube-transcripts/{filename}.md"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Transcript: {filename}\n\n")
            f.write(f"**Source:** {url}\n\n")
            f.write(f"---\n\n")
            f.write(transcript_text)

        print(f"✅ Saved: {output_path}")

    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")

videos = [
    ("https://www.youtube.com/watch?v=Wzyq2u2-M3E", "armand-farrokh-cold-email-30mpc"),
    ("https://www.youtube.com/watch?v=JX1UNIJwcCY", "jason-bay-cold-email-masterclass-2026"),
    ("https://www.youtube.com/watch?v=XJ4-PiouLA8", "jason-bay-high-converting-cold-emails-2026"),
    ("https://www.youtube.com/watch?v=ILK_opONAUg", "nick-abraham-cold-email-tactics"),
    ("https://www.youtube.com/watch?v=f1FdxGD_aY4", "nick-cegelski-cold-email-sequence-2025"),
    ("https://www.youtube.com/shorts/mO4s-9s--RY", "morgan-ingram-outbound-2025"),
]

if __name__ == "__main__":
    for url, filename in videos:
        fetch_transcript(url, filename)