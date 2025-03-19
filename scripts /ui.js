/**
 * ui.js - Gerencia a interatividade da interface do Tradutor Mágico
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos da interface
    const inputLabel = document.getElementById('inputLabel');
    const inputText = document.getElementById('inputText');
    const outputMagicLabel = document.getElementById('outputMagicLabel');
    const outputMagic = document.getElementById('outputMagic');
    const outputMethodLabel = document.getElementById('outputMethodLabel');
    const outputMethod = document.getElementById('outputMethod');
    const outputPronunciationLabel = document.getElementById('outputPronunciationLabel');
    const outputPronunciation = document.getElementById('outputPronunciation');
    const modeSelector = document.getElementById('modeSelector');
    const fontSizeSlider = document.getElementById('fontSizeSlider');
    const randomSentence = document.getElementById('randomSentence');
    const feedbackPopup = document.getElementById('feedbackPopup');
    const virtualKeyboard = document.getElementById('virtualKeyboard');
    const keyboardButton = document.getElementById('keyboardButton');
    
    // Botões e ações
    const infoButton = document.getElementById('infoButton');
    const pasteButton = document.getElementById('pasteButton');
    const clearButton = document.getElementById('clearButton');
    const copyButtons = document.querySelectorAll('.copy-button');
    
    // Fechar teclado
    const closeKeyboard = document.getElementById('closeKeyboard');
    
    // Adicionar indicador de carregamento
    const body = document.body;
    const loading = document.createElement('div');
    loading.id = 'loading';
    loading.innerHTML = '<div class="loading-spinner"></div>';
    body.appendChild(loading);
    
    // Remover indicador de carregamento quando o PyScript estiver pronto
    window.addEventListener('py-ready', function() {
        loading.classList.add('loaded');
    });
    
    // Configuração do modo de tradução
    modeSelector.addEventListener('change', updateUIForMode);
    
    function updateUIForMode() {
        const mode = modeSelector.value;
        
        if (mode === 'latin-to-magic') {
            inputLabel.textContent = 'Digite a frase em Latim:';
            outputMagicLabel.textContent = 'Língua Mágica:';
            outputPronunciationLabel.textContent = 'Pronúncia Fonética:';
            keyboardButton.classList.add('hidden');
            inputText.readOnly = false;
        } else {
            inputLabel.textContent = 'Digite a frase em Mágico:';
            outputMagicLabel.textContent = 'Latim:';
            outputPronunciationLabel.textContent = 'Pronúncia Fonética (N/A):';
            keyboardButton.classList.remove('hidden');
            // Não definimos readonly aqui para permitir entrada direta
        }
        
        // Limpar campos de saída quando mudar o modo
        outputMagic.value = '';
        outputMethod.value = '';
        outputPronunciation.value = '';
    }
    
    // Configuração do slider de tamanho de fonte
    fontSizeSlider.addEventListener('input', updateFontSize);
    
    function updateFontSize() {
        const fontSize = fontSizeSlider.value + 'px';
        
        // Atualizar campos de texto
        inputText.style.fontSize = fontSize;
        outputMagic.style.fontSize = fontSize;
        outputMethod.style.fontSize = fontSize;
        outputPronunciation.style.fontSize = fontSize;
        
        // Atualizar texto de exemplo
        randomSentence.style.fontSize = parseInt(fontSizeSlider.value) * 1.2 + 'px';
    }
    
    // Botão de informações
    infoButton.addEventListener('click', function() {
        window.location.href = 'info.html';
    });
    
    // Botão de colar
    pasteButton.addEventListener('click', async function() {
        try {
            const text = await navigator.clipboard.readText();
            inputText.value = text;
        } catch (err) {
            console.error('Falha ao colar texto: ', err);
            alert('Não foi possível acessar a área de transferência.');
        }
    });
    
    // Botão de limpar
    clearButton.addEventListener('click', function() {
        inputText.value = '';
        outputMagic.value = '';
        outputMethod.value = '';
        outputPronunciation.value = '';
    });
    
    // Botões de copiar
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement && targetElement.value) {
                navigator.clipboard.writeText(targetElement.value)
                    .then(() => showFeedback())
                    .catch(err => {
                        console.error('Falha ao copiar texto: ', err);
                        alert('Não foi possível copiar para a área de transferência.');
                    });
            }
        });
    });
    
    // Teclado virtual
    keyboardButton.addEventListener('click', function() {
        virtualKeyboard.classList.remove('hidden');
    });
    
    closeKeyboard.addEventListener('click', function() {
        virtualKeyboard.classList.add('hidden');
    });
    
    // Mostrar popup de feedback
    function showFeedback() {
        feedbackPopup.classList.remove('hidden');
        setTimeout(() => {
            feedbackPopup.classList.add('hidden');
        }, 1500);
    }
    
    // Inicializar interface
    updateUIForMode();
    updateFontSize();
});
