from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import eng_to_ipa as p
from googletrans import Translator

import io

bancoDePalavras = open("1 - banco.txt", 'r', encoding="utf-8")

palavras = []

for line in bancoDePalavras:
    palavra = line.replace('-', '').replace('**', '').strip()
    palavras.append(palavra)

selecionadas = []
não_selecionadas = []

# Limpar dados
for i in range(len(palavras)):
    frase = palavras[i]
    divisao = frase.split()

    phonetic = p.convert(frase)

    if (divisao[0] != divisao[-1] or '*' in phonetic):
        não_selecionadas.append(palavras[i])
    else:
        selecionadas.append(palavras[i])

filename = "Formatados.md"
f = open(filename, "w", encoding="utf-8")

# f = open(filename, "w")

for i in range(len(palavras)):
    if (i < len(selecionadas)):
        f.write("\n<details>")

        f.write(f'\n    <summary>{selecionadas[i].capitalize()}</summary>\n')

        phonetic = p.convert(selecionadas[i])
        f.write(f'\n    /{phonetic}/\n')

        trans = Translator()
        t = trans.translate(
            selecionadas[i], src='en', dest='pt'
        )
        f.write(f'\n    {selecionadas[i].capitalize()}: {t.text}\n')

        req = Request(
            f'https://context.reverso.net/traducao/ingles-portugues/{selecionadas[i]}', headers={'User-Agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        page_soup = soup(page_html, "html.parser")

        # contador de quantas frases tem
        containers = page_soup.findAll("div", {"class": "ltr"})

        limit = 7

        english_container = page_soup.findAll(
            "span", {"lang": "en"}, limit=limit)  # pegando o que eu quero
        portuguese_container = page_soup.findAll(
            "div", class_="trg ltr")  # pegando o que eu quero

        for container in range(2, limit):
            english = english_container[container].text
            f.write(f"\n    " + english.strip() + "\n") # limapando as strings

            portuguese = portuguese_container[container].text
            f.write(f"\n    " + portuguese.strip() + "\n")
        f.write("\n</details>\n")
        f.write(f'\n[mais...](https://context.reverso.net/traducao/ingles-portugues/{selecionadas[i]})\n')
    else:
        break

f.write(f'\n<h2>Não serão Consideradas:</h2>\n')

for index in range(len(não_selecionadas)):
    f.write("\n<details>")

    f.write(f'\n    <summary>{não_selecionadas[index]}</summary>\n')
    
    trans = Translator()
    t = trans.translate(
        não_selecionadas[index], src='en', dest='pt'
    )
    
    f.write(f'\n    {t.text}\n')
    
    f.write("\n</details>\n")

    f.write(f'\n[mais...](https://context.reverso.net/traducao/ingles-portugues/{não_selecionadas[index]})\n')
    f.write(f'\n<hr>\n')
