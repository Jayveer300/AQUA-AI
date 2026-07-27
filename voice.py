print("VOICE.PY LOADED")

import edge_tts
import asyncio
import tempfile

def detect_language(text):
    # Hindi Unicode
    if any('\u0900' <= c <= '\u097F' for c in text):
        return "hi"

    # Gujarati Unicode
    if any('\u0A80' <= c <= '\u0AFF' for c in text):
        return "gu"

    return "en"


async def generate(text):
    lang = detect_language(text)

    if lang == "hi":
        voice = "hi-IN-SwaraNeural"

    elif lang == "gu":
        # Gujarati TTS voice
        voice = "gu-IN-DhwaniNeural"

    else:
        voice = "en-US-AriaNeural"

    filename = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="+30%",
        pitch="+0Hz"
    )

    await communicate.save(filename.name)

    return filename.name


def text_to_audio(text):
    return asyncio.run(generate(text))