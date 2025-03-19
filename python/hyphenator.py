"""
hyphenator.py - Implementação simplificada de divisão silábica para português
Adaptado para funcionar com PyScript no navegador sem dependências externas
"""

class Hyphenator:
    """
    Classe para dividir palavras em sílabas
    Esta é uma implementação simplificada para português brasileiro,
    usada quando o pyphen não está disponível no ambiente PyScript
    """
    
    def __init__(self, language="pt_BR"):
        self.language = language
        
        # Vogais em português
        self.vowels = "aeiouáàâãéèêíìóòôõúùûy"
        
        # Ditongos em português
        self.diphthongs = [
            "ai", "ão", "au", "ãe", "ei", "eu", "éi", "éu", "iu", "oi", "ôi", "ói",
            "ou", "ua", "ue", "ui", "uo", "õe"
        ]
        
        # Encontros consonantais que não devem ser separados
        self.consonant_clusters = [
            "bl", "br", "cl", "cr", "dr", "fl", "fr", "gl", "gr", "pl", "pr", "tl", "tr", "vl", "vr"
        ]
    
    def is_vowel(self, char):
        """Verifica se um caractere é uma vogal"""
        return char.lower() in self.vowels
    
    def is_consonant(self, char):
        """Verifica se um caractere é uma consoante"""
        return char.isalpha() and not self.is_vowel(char)
    
    def is_diphthong(self, pair):
        """Verifica se um par de caracteres forma um ditongo"""
        return pair.lower() in self.diphthongs
    
    def is_consonant_cluster(self, pair):
        """Verifica se um par de caracteres forma um encontro consonantal"""
        return pair.lower() in self.consonant_clusters
    
    def hyphenate_word(self, word):
        """
        Divide uma palavra em sílabas.
        
        Args:
            word (str): A palavra a ser dividida
            
        Returns:
            list: Lista de sílabas da palavra
        """
        # Verificação de palavra vazia ou muito curta
        if not word or len(word) <= 1:
            return [word] if word else []
        
        # Normaliza a palavra
        word = word.lower()
        
        # Resultado
        syllables = []
        
        # Índice atual
        i = 0
        
        # Início da sílaba atual
        start = 0
        
        while i < len(word) - 1:
            # Verifica ditongos - não devem ser separados
            if i + 1 < len(word) and self.is_vowel(word[i]) and self.is_vowel(word[i+1]):
                if self.is_diphthong(word[i:i+2]):
                    i += 1
                    continue
            
            # Consoante seguida de vogal - separa antes da consoante que precede a vogal
            if i > 0 and self.is_consonant(word[i]) and self.is_vowel(word[i+1]):
                # Verifica se forma um encontro consonantal com a letra anterior
                if i > 0 and self.is_consonant(word[i-1]):
                    if self.is_consonant_cluster(word[i-1:i+1]):
                        # Não separa encontros consonantais
                        i += 1
                        continue
                    else:
                        # Separa entre as consoantes
                        syllables.append(word[start:i])
                        start = i
                        i += 1
                        continue
                
                # Consoante simples seguida de vogal
                if i > start:
                    syllables.append(word[start:i])
                    start = i
            
            # Vogal seguida de consoante
            if self.is_vowel(word[i]) and i + 1 < len(word) and self.is_consonant(word[i+1]):
                # Verifica o próximo caractere
                if i + 2 < len(word):
                    if self.is_vowel(word[i+2]):
                        # VCV -> V-CV
                        syllables.append(word[start:i+1])
                        start = i + 1
                    elif self.is_consonant(word[i+2]):
                        # VCC
                        if self.is_consonant_cluster(word[i+1:i+3]):
                            # Encontro consonantal começa a próxima sílaba
                            syllables.append(word[start:i+1])
                            start = i + 1
                        else:
                            # CC não é encontro - separar entre as consoantes
                            i += 1
                            syllables.append(word[start:i])
                            start = i
                            continue
            
            i += 1
        
        # Adiciona a última sílaba
        if start < len(word):
            syllables.append(word[start:])
        
        return syllables
    
    def inserted(self, word):
        """
        Retorna a palavra com hífens marcando as posições de separação silábica
        Mantém compatibilidade com a API do pyphen
        
        Args:
            word (str): A palavra a ser dividida
            
        Returns:
            str: Palavra com hífens nas posições de separação silábica
        """
        syllables = self.hyphenate_word(word)
        return "-".join(syllables)
