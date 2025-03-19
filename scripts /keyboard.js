/**
 * keyboard.js - Gerencia o teclado virtual para entrada de símbolos mágicos
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do teclado
    const keyboardGrid = document.getElementById('keyboardGrid');
    const punctuationGrid = document.getElementById('punctuationGrid');
    const backspaceButton = document.getElementById('keyboardBackspace');
    const spaceButton = document.getElementById('keyboardSpace');
    const inputText = document.getElementById('inputText');
    
    // Configurar eventos do teclado após o PyScript estar pronto
    window.addEventListener('py-ready', function() {
        setupKeyboardEvents();
    });
    
    function setupKeyboardEvents() {
        // Teclas de símbolos
        document.querySelectorAll('.key').forEach(key => {
            key.addEventListener('click', function() {
                insertSymbol(this.getAttribute('data-symbol'));
            });
        });
        
        // Teclas de pontuação
        document.querySelectorAll('.punct-key').forEach(key => {
            key.addEventListener('click', function() {
                insertSymbol(this.getAttribute('data-symbol'));
            });
        });
        
        // Tecla de espaço
        spaceButton.addEventListener('click', function() {
            insertSymbol(' ');
        });
        
        // Tecla de backspace (apagar)
        backspaceButton.addEventListener('click', backspaceSymbol);
        
        // Adicionamos suporte a manter pressionado para apagar contínuo
        let backspaceInterval;
        
        backspaceButton.addEventListener('mousedown', function() {
            backspaceSymbol();
            backspaceInterval = setInterval(backspaceSymbol, 100);
        });
        
        backspaceButton.addEventListener('mouseup', function() {
            clearInterval(backspaceInterval);
        });
        
        backspaceButton.addEventListener('mouseleave', function() {
            clearInterval(backspaceInterval);
        });
        
        // Também suporta eventos de toque (touch) para dispositivos móveis
        backspaceButton.addEventListener('touchstart', function(e) {
            e.preventDefault();
            backspaceSymbol();
            backspaceInterval = setInterval(backspaceSymbol, 100);
        });
        
        backspaceButton.addEventListener('touchend', function() {
            clearInterval(backspaceInterval);
        });
    }
    
    // Inserir símbolo no campo de texto
    function insertSymbol(symbol) {
        if (!inputText) return;
        
        // Obtém a posição atual do cursor
        const cursorPos = inputText.selectionStart;
        
        // Constrói o novo texto com o símbolo inserido na posição do cursor
        const textBefore = inputText.value.substring(0, cursorPos);
        const textAfter = inputText.value.substring(inputText.selectionEnd);
        
        // Atualiza o texto do campo
        inputText.value = textBefore + symbol + textAfter;
        
        // Move o cursor para depois do símbolo inserido
        const newCursorPos = cursorPos + symbol.length;
        inputText.setSelectionRange(newCursorPos, newCursorPos);
        
        // Foca no campo de texto para continuar a digitação
        inputText.focus();
    }
    
    // Apagar um símbolo do campo de texto
    function backspaceSymbol() {
        if (!inputText) return;
        
        // Obtém a posição atual do cursor
        const cursorPos = inputText.selectionStart;
        
        // Se não há seleção e o cursor não está no início
        if (inputText.selectionStart === inputText.selectionEnd && cursorPos > 0) {
            // Remove o caractere antes do cursor
            const textBefore = inputText.value.substring(0, cursorPos - 1);
            const textAfter = inputText.value.substring(cursorPos);
            
            // Atualiza o texto do campo
            inputText.value = textBefore + textAfter;
            
            // Posiciona o cursor
            const newCursorPos = cursorPos - 1;
            inputText.setSelectionRange(newCursorPos, newCursorPos);
        } 
        // Se há texto selecionado
        else if (inputText.selectionStart !== inputText.selectionEnd) {
            // Remove o texto selecionado
            const textBefore = inputText.value.substring(0, inputText.selectionStart);
            const textAfter = inputText.value.substring(inputText.selectionEnd);
            
            // Atualiza o texto do campo
            inputText.value = textBefore + textAfter;
            
            // Posiciona o cursor
            inputText.setSelectionRange(inputText.selectionStart, inputText.selectionStart);
        }
        
        // Foca no campo de texto
        inputText.focus();
    }
});
