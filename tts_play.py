import sys
import re
import json
import ollama
import soundfile as sf
import torch
from torchaudio import transforms as T
from neucodec import NeuCodec

# Output WAV path
OUTPUT_WAV = "output_from_ollama.wav"

# Ollama model and prompt
MODEL_NAME = "hf.co/neuphonic/neutts-air-q8-gguf"
PROMPT = "This is a test of Neutts-Air GGUF running through Ollama. Generating audio now."

# Token settings
MIN_TOKENS = 256       # Minimum token length for NeuCodec
MAX_ID = 1023          # Maximum token ID

def main():
    print(f"🔊 Model: {MODEL_NAME}")
    print(f"🗣️  Prompt: {PROMPT}\n")

    # 1️⃣ Generate tokens via Ollama
    print("1) Requesting speech tokens from Ollama...")
    resp = ollama.generate(model=MODEL_NAME, prompt=PROMPT, stream=False)
    token_str = resp.get("response", "")
    if not token_str:
        print("❌ No token response from Ollama!")
        print(json.dumps(resp, indent=2)[:800])
        sys.exit(1)

    print(f"   > Received {len(token_str)} characters of token data")

    # 2️⃣ Parse <|speech_12345|> → integer IDs
    print("2) Parsing tokens...")
    token_ids = [int(x) for x in re.findall(r"<\|speech_(\d+)\|>", token_str)]
    if not token_ids:
        print("❌ No audio tokens found. First 400 chars:\n", token_str[:400])
        sys.exit(1)

    # Remap tokens to valid range
    token_ids = [x % (MAX_ID + 1) for x in token_ids]

    # Pad short sequences
    if len(token_ids) < MIN_TOKENS:
        print(f"   > Padding tokens from {len(token_ids)} → {MIN_TOKENS}")
        token_ids += [0] * (MIN_TOKENS - len(token_ids))

    print(f"   > Parsed and remapped {len(token_ids)} tokens")
    print(f"   > Token IDs min/max: {min(token_ids)}/{max(token_ids)}")

    # 3️⃣ Decode tokens → waveform using PyTorch NeuCodec
    print("3) Decoding tokens to audio with NeuCodec PyTorch...")
    try:
        codec = NeuCodec.from_pretrained("neuphonic/distill-neucodec")
    except Exception as e:
        print("❌ Failed to load NeuCodec PyTorch decoder!")
        print(e)
        sys.exit(1)

    with torch.no_grad():
        codes = torch.tensor(token_ids, dtype=torch.long).unsqueeze(0)  # [1, T]
        wav = codec.decode_code(codes).squeeze().cpu().numpy()

    # 4️⃣ Save WAV
    sf.write(OUTPUT_WAV, wav, 16000)
    print(f"\n✅ Success! Audio written to {OUTPUT_WAV}")

if __name__ == "__main__":
    import traceback

    try:
        if not hasattr(torch, "tensor"):
            print("Error: torch is broken (missing torch.tensor).")
            print("Use Python 3.10+ and install PyTorch via conda.")
            sys.exit(1)
        main()
    except Exception:
        print("\n❌ Error during execution:\n")
        traceback.print_exc()
        print("\nChecklist:")
        print("- Ollama running on localhost:11434")
        print("- pip install neucodec soundfile torch ollama")
        print("- If using ONNX later, ensure decoder exists and onnxruntime is installed")
        print("- conda install -y -c conda-forge libsndfile (if soundfile DLL error)")
        sys.exit(1)
