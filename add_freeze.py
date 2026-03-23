with open('train_ms.py', 'r') as f:
    lines = f.readlines()

# net_d 생성 줄 찾기
freeze_code = '''
  # Fine-tuning: Freeze text encoder, flow, duration predictor
  for name, param in net_g.named_parameters():
      if "enc_p" in name or "flow" in name or "dp" in name:
          param.requires_grad = False
  
  for name, p in net_g.named_parameters():
      if not p.requires_grad:
          print("[FREEZE]", name)

'''

inserted = False
for i, line in enumerate(lines):
    if "net_d = MultiPeriodDiscriminator" in line and not inserted:
        # 다음 줄에 freeze 코드 삽입
        lines.insert(i+1, freeze_code)
        inserted = True
        break

if inserted:
    with open('train_ms.py', 'w') as f:
        f.writelines(lines)
    print("✅ Freeze 코드 추가 완료!")
else:
    print("❌ 삽입 위치를 찾을 수 없습니다.")
