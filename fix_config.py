import json

with open('configs/config-single-speaker.json', 'r') as f:
    config = json.load(f)

# Filelist 경로 수정
config['data']['training_files'] = 'filelists/jsut_train.txt.cleaned'
config['data']['validation_files'] = 'filelists/jsut_val.txt.cleaned'

# 22050Hz 확인
config['data']['sampling_rate'] = 22050

with open('configs/config-single-speaker.json', 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("✅ Config 수정 완료!")
