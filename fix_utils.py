with open('utils.py', 'r') as f:
    lines = f.readlines()

# Line 152-153을 찾아서 수정
for i in range(len(lines)):
    if '../drive/MyDrive' in lines[i]:
        # 해당 줄과 다음 줄을 주석 처리
        lines[i] = '  # ' + lines[i]
        if i+1 < len(lines) and 'os.path.join' in lines[i+1]:
            lines[i+1] = '  # ' + lines[i+1]
        # 새로운 줄 추가
        lines.insert(i+2, '  model_dir = args.model\n')
        break

with open('utils.py', 'w') as f:
    f.writelines(lines)

print("✅ utils.py 수정 완료!")
