import os 
import random

JSUT_ROOT = "/mnt/c/Users/eternal/vits-finetuning-main/data/jsut_ver1.1/basic5000/" 
WAV_DIR = os.path.join(JSUT_ROOT, "wav") 
TRANSCRIPT = os.path.join(JSUT_ROOT, "transcript_utf8.txt")

OUT_DIR = "filelists" 
os.makedirs(OUT_DIR, exist_ok=True)

train_out = open(f"{OUT_DIR}/jsut_train.txt", "w", encoding="utf-8") 
val_out = open(f"{OUT_DIR}/jsut_val.txt", "w", encoding="utf-8")

with open(TRANSCRIPT, encoding="utf-8") as f:
    lines = f.readlines()

pairs = []
for line in lines:
    key, text = line.strip().split(":", 1)
    wav_path = os.path.join(WAV_DIR, key + ".wav")
    if os.path.exists(wav_path):
        pairs.append((wav_path, text))

random.shuffle(pairs)

val_size = 100  # JSUT 기준 적절
for i, (wav, text) in enumerate(pairs):
    row = f"{wav}|0|{text}\n"
    if i < val_size:
        val_out.write(row)
    else:
        train_out.write(row)

train_out.close()
val_out.close()
