import re

with open('utils.py', 'r') as f:
    content = f.read()

# plot_alignment_to_numpy 함수 전체를 올바르게 수정
old_function = r'def plot_alignment_to_numpy\(alignment, info=None\):.*?(?=\ndef |\Z)'

new_function = '''def plot_alignment_to_numpy(alignment, info=None):
  import matplotlib
  matplotlib.use("Agg")
  import matplotlib.pylab as plt
  import numpy as np

  fig, ax = plt.subplots(figsize=(6, 4))
  im = ax.imshow(alignment.transpose(), aspect='auto', origin='lower',
                  interpolation='none')
  fig.colorbar(im, ax=ax)
  xlabel = 'Decoder timestep'
  if info is not None:
      xlabel += '\\n\\n' + info
  plt.xlabel(xlabel)
  plt.ylabel('Encoder timestep')
  plt.tight_layout()

  fig.canvas.draw()
  data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
  data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
  plt.close()
  return data
'''

content = re.sub(old_function, new_function, content, flags=re.DOTALL)

with open('utils.py', 'w') as f:
    f.write(content)

print("✅ utils.py 수정 완료!")
