"""Quick manual test client for the chat endpoint — stand-in for the iOS
client until that's built. Run the server first:

    uvicorn app.main:app --reload

Then in another terminal:

    python test_client.py "¿Cuántos días de vacaciones me corresponden si llevo 2 años trabajando?"
"""

import sys

import httpx

BASE_URL = "http://127.0.0.1:8000"


def main() -> None:
    message = " ".join(sys.argv[1:]) or "¿Qué pasa si me despiden sin previo aviso?"
    resp = httpx.post(f"{BASE_URL}/v1/chat/message", json={"message": message}, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    print("\n--- PREGUNTA ---")
    print(message)
    print("\n--- RESPUESTA NICTÉ BOT ---")
    print(data["answer"])
    print("\n--- CITAS ---")
    for c in data["citations"]:
        print(f"  {c['law_name']} — Artículo {c['article_number']} (score={c['relevance_score']})")
    print(f"\n--- legal_area: {data['legal_area']} | safety_flag: {data['safety_flag']} ---\n")


if __name__ == "__main__":
    main()
