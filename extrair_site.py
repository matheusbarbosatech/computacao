import requests
import re

html = requests.get('https://150mapasdeprogramacao.netlify.app').text
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f"Total imagens encontradas: {len(imgs)}")
for img in imgs:
    print(img)
