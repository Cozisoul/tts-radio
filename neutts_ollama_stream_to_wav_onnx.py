#!/usr/bin/env python3
# --------------------------------------------------------------------
#  neutts_ollama_stream_to_wav_onnx.py
# ---------------------------------------------------------------
#  Streaming variant: collect tokens chunk‑by‑chunk from Ollama,
#  then decode with the ONNX decoder.
# --------------------------------------------------------------------

import json
import os
import re
import sys

import numpy as np
import ollama
import soundfile as sf
from huggingface_hub import snapshot_download

try:
    import onnxruntime as ort
except Exception as e:
    print("Import error:", e)
    print("Install deps with:\n  pip install onnxruntime huggingface_hub soundfile ollama numpy")
    sys.exit(1)

# --------------------------------- Config ---------------------------------
MODEL_NAME = "hf.co/neuphonic/neutts-air-q8-gguf"
PROMPT     = "Streaming test with Neutts-Air via Ollama (GGUF)."
OUTPUT_WAV = "output_from_ollama_stream.wav"
DECODER_REPO = "neuphonic/neucodec-onnx-decoder"

# --------------------------------‑ Helpers --------------------------------

def load_onnx_decoder() -> ort.InferenceSession:
    cache_dir = snapshot_download(DECODER_REPO, force_download=False)
    onnx_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(cache_dir)
        for f in files
        if f.lower().endswith(".onnx")
    ]

    if not onnx_files:
        raise FileNotFoundError("No .onnx file found in the HF repo snapshot.")
    candidates = [p for p in onnx_files if "decoder" in os.path.basename(p).lower()]
    onnx_path = candidates[0] if candidates else max(onnx_files, key=os.path.getsize)

    print(f"Using ONNX decoder: {onnx_path}")
    return ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])

def tokens_to_wav(token_str: str, sess: ort.InferenceSession) -> np.ndarray:
    speech_ids = [int(x) for x in re.findall(r"<\\|speech_(\\d+)>", token_str)]
    if not speech_ids:
        raise ValueError("No valid speech tokens found in the output.")

    inp = np.array(speech_ids, dtype=np.int32)[np.newaxis, np.newaxis, :]
    inp_name  = sess.get_inputs()[0].name
    out_name = sess.get_outputs()[0].name
    out = sess.run([out_name], {inp_name: inp})[0]

    wav = np.squeeze(out).astype(np.float32)
    return wav

# --------------------------------- Main ---------------------------------

def main() -> None:
    print(f"Model: {MODEL_NAME}\nPrompt: {PROMPT}\n")

    # 1) Stream tokens from Ollama
    print("1) Streaming tokens from Ollama …")
    token_parts = []
    for chunk in ollama.generate(model=MODEL_NAME, prompt=PROMPT, stream=True):
        response = chunk.get("response", "")
        if response:
            token_parts.append(response)

    token_str = "".join(token_parts)
    if not token_str:
        print("No response text returned by Ollama streaming.")
        sys.exit(1)

    print(f"   > Received {len(token_str)} chars of token text.")

    # 2) Load ONNX decoder
    print("2) Loading ONNX decoder …")
    sess = load_onnx_decoder()

    # 3) Decode tokens to audio
    print("3) Decoding tokens to audio …")
    wav = tokens_to_wav(token_str, sess)

    # 4) Write WAV
    print(f"4) Writing: {OUTPUT_WAV}")
    sf.write(OUTPUT_WAV, wav, 16000)
    print("✅ Done.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nError:", e)
        print("\nChecklist:")
        print("- Ollama running locally (port 11434)")
        print("- pip install onnxruntime huggingface_hub soundfile ollama numpy")
        print("- Decoder repo reachable: neuphonic/neucodec-onnx-decoder")
        sys.exit(1)
