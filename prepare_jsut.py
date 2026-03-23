#!/usr/bin/env python3
import os
import librosa
import soundfile as sf
from pathlib import Path
from tqdm import tqdm

def prepare_jsut():
    jsut_path = "data/jsut_ver1.1"
    output_dir = "dataset/jsut"
    filelist_dir = "filelists"
    sample_rate = 22050
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(filelist_dir).mkdir(exist_ok=True)
    
    subset = 'basic5000'
    subset_path = Path(jsut_path) / subset
    
    print(f"\n처리 중: {subset}")
    
    # 트랜스크립트 읽기
    transcript_path = subset_path / "transcript_utf8.txt"
    transcripts = {}
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                wav_id, text = line.split(':', 1)
                transcripts[wav_id] = text
    
    filelist = []
    wav_dir = subset_path / "wav"
    
    for wav_file in tqdm(sorted(wav_dir.glob("*.wav"))):
        wav_id = wav_file.stem
        
        if wav_id not in transcripts:
            continue
        
        try:
            # 오디오 로드 및 리샘플링 (48kHz → 22050Hz)
            audio, sr = librosa.load(wav_file, sr=sample_rate, mono=True)
            
            # 길이 체크 (1-10초)
            duration = len(audio) / sample_rate
            if duration < 1.0 or duration > 10.0:
                continue
            
            # 저장
            output_filename = f"{subset}_{wav_id}.wav"
            output_path = Path(output_dir) / output_filename
            sf.write(output_path, audio, sample_rate, subtype='PCM_16')
            
            # Filelist 항목 추가 (speaker_id=0 포함!)
            text = transcripts[wav_id]
            filelist.append(f"{output_path}|0|{text}")
            
        except Exception as e:
            print(f"Error: {wav_id}: {e}")
    
    print(f"총 샘플 수: {len(filelist)}")
    
    # Train/Val 분할 (90:10)
    split_idx = int(len(filelist) * 0.9)
    train_list = filelist[:split_idx]
    val_list = filelist[split_idx:]
    
    # Filelist 저장
    with open(f"{filelist_dir}/jsut_train.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(train_list))
    
    with open(f"{filelist_dir}/jsut_val.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(val_list))
    
    print(f"Train: {len(train_list)}, Val: {len(val_list)}")
    print("✅ 전처리 완료!")

if __name__ == "__main__":
    prepare_jsut()
