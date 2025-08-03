"""
target_text = "Нужная подпись"

# Найти все div с классами bItm и oItm
blocks = soup.select('div.bItm.oItm')

for block in blocks:
    link = block.select_one('div > a')  # или просто 'a', если уверены, что структура простая
    if link and link.text.strip() == target_text:
        print(link['href'])
        break  # если нужен только первый подходящий

img_url = None
for block in blocks:
    img = block.find('img', class_='artM')
    if img:
        img_url = img.get('data-src') or img.get('src')
        break
    link = block.select()
----------------------------------------------------"""


