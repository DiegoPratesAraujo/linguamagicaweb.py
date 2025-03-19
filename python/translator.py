"""
translator.py - Contém a lógica de tradução entre Latim e Língua Mágica
Adaptado do código original para funcionar com PyScript no navegador
"""

import re
from python.hyphenator import Hyphenator

# Criação de um divisor silábico para português
hyphenator = Hyphenator("pt_BR")

# -------------------------------------------------------------------------------
# Dicionário com os símbolos e fonemas (Língua Mágica)
# -------------------------------------------------------------------------------
MAGIC_ALPHABET = {
    'A': ('𐐅', 'to'),
    'B': ('𐐆', 'ta'),
    'C': ('𐐇', 'nes'),
    'D': ('𐐈', 'nas'),
    'E': ('𐐉', 'nos'),
    'F': ('𐐊', 'tes'),
    'G': ('𐐋', 'la'),
    'H': ('𐐌', 'me'),
    'I': ('𐐍', 'mo'),
    'K': ('𐐏', 'le'),
    'L': ('𐐐', 'lo'),
    'M': ('𐐑', 'sa'),
    'N': ('£', 'se'),
    'O': ('𐐓', 'so'),
    'P': ('𐐔', 'ba'),
    'Q': ('€', 'be'),
    'R': ('𐐖', 'bo'),
    'S': ('𐐗', 'sko'),
    'T': ('𐐘', 'ska'),
    'V': ('𐐙', 'po'),
    'X': ('𐐜', 'chi'),
    'Y': ('𐐝', 'cho'),
    'Z': ('𐐞', 'cha'),
}

# -------------------------------------------------------------------------------
# Funções de conversão
# -------------------------------------------------------------------------------
def dividir_silabas(palavra):
    """Divide uma palavra em sílabas usando o hyphenator"""
    silabas = hyphenator.hyphenate_word(palavra)
    return silabas if silabas else [palavra]

def inverter_silaba(silaba):
    """Inverte os caracteres de uma sílaba"""
    return silaba[::-1]

def latim_para_magico(frase_latim):
    """
    Converte uma frase do latim para a língua mágica
    
    Args:
        frase_latim (str): A frase em latim a ser convertida
        
    Returns:
        tuple: (frase_magica, frase_fonemas, process_description)
            - frase_magica: A frase convertida para símbolos mágicos
            - frase_fonemas: A pronúncia fonética da frase mágica
            - process_description: Descrição detalhada do processo de conversão
    """
    palavras = frase_latim.split()
    palavras_invertidas = []
    process_description = ""
    
    for palavra in palavras:
        silabas = dividir_silabas(palavra)
        process_description += f"\nDivisão de sílabas de '{palavra}': {silabas}\n"
        
        silabas_invertidas = [inverter_silaba(silaba) for silaba in silabas]
        process_description += f"Sílabas invertidas: {silabas_invertidas}\n"
        
        palavra_invertida = ".".join(silabas_invertidas)
        palavras_invertidas.append(palavra_invertida)
    
    frase_invertida = " ".join(palavras_invertidas[::-1])
    process_description += f"\nFrase invertida: {frase_invertida}\n"
    
    frase_magica = ""
    frase_fonemas = ""
    palavra_fonemas = ""
    
    for idx, char in enumerate(frase_invertida.upper()):
        if char == " ":
            frase_magica += char
            frase_fonemas += palavra_fonemas.strip() + " "
            palavra_fonemas = ""
        elif char in MAGIC_ALPHABET:
            frase_magica += MAGIC_ALPHABET[char][0]
            palavra_fonemas += MAGIC_ALPHABET[char][1]
        else:
            frase_magica += char
    
    frase_fonemas += palavra_fonemas.strip()
    return frase_magica, frase_fonemas.strip(), process_description

def magico_para_latim(frase_magica):
    """
    Converte uma frase da língua mágica para o latim
    
    Args:
        frase_magica (str): A frase em símbolos mágicos a ser convertida
        
    Returns:
        tuple: (frase_latim, process_description)
            - frase_latim: A frase convertida para latim
            - process_description: Descrição detalhada do processo de conversão
    """
    # Preserva pontuação final
    trailing = ""
    m = re.search(r'([.!?…]+)$', frase_magica)
    if m:
        trailing = m.group(1)
        frase_magica = frase_magica[:-len(trailing)].rstrip()
    
    # Cria dicionário reverso para tradução de símbolos para letras
    REVERSE_MAGIC_ALPHABET = {v[0]: k for k, v in MAGIC_ALPHABET.items()}
    
    frase_invertida = ""
    process_description = "Processo de conversão:\n"
    
    for idx, char in enumerate(frase_magica):
        if char in REVERSE_MAGIC_ALPHABET:
            frase_invertida += REVERSE_MAGIC_ALPHABET[char]
        else:
            frase_invertida += char
    
    process_description += f"Frase invertida: {frase_invertida}\n"
    
    palavras_invertidas = frase_invertida.split()
    palavras = []
    
    for palavra_invertida in palavras_invertidas:
        silabas_invertidas = palavra_invertida.split(".")
        silabas = [inverter_silaba(silaba) for silaba in silabas_invertidas]
        palavra = "".join(silabas)
        palavras.append(palavra)
    
    frase_latim = " ".join(palavras[::-1])
    frase_latim = frase_latim.rstrip() + trailing
    
    process_description += f"Frase em latim: {frase_latim}\n"
    
    return frase_latim, process_description
