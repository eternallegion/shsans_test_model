import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

with open(in_file, "r", encoding="utf-8") as fin, \
     open(out_file, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("|")

        # wav|text  → wav|0|text
        if len(parts) == 2:
            wav, text = parts
            fout.write(f"{wav}|0|{text}\n")

        # 이미 wav|sid|text 인 경우 그대로
        elif len(parts) == 3:
            fout.write(line + "\n")

        else:
            raise ValueError(f"Invalid line format: {line}")
