const vscode = require('vscode');

function activate(context) {
    // Register command to show input panel
    let disposable = vscode.commands.registerCommand('copilot-poc.showInput', () => {
        // Create and show WebView panel
        const panel = vscode.window.createWebviewPanel(
            'copilotPoc',
            'Copilot POC',
            vscode.ViewColumn.One,
            {
                enableScripts: true
            }
        );

        // Set initial HTML content
        panel.webview.html = getWebviewContent();

        // Handle messages from webview
        panel.webview.onDidReceiveMessage(async message => {
            if (message.command === 'getCompletion') {
                try {
                    const response = await getCopilotCompletion(message.text);
                    // Send response back to webview
                    panel.webview.postMessage({ 
                        command: 'showResponse', 
                        response: response 
                    });
                } catch (error) {
                    panel.webview.postMessage({ 
                        command: 'showError', 
                        error: error.message 
                    });
                }
            }
        });
    });

    context.subscriptions.push(disposable);
}

async function getCopilotCompletion(prompt) {
    // Get Copilot extension
    const copilot = vscode.extensions.getExtension('GitHub.copilot');
    
    if (!copilot) {
        throw new Error('GitHub Copilot is not installed');
    }

    if (!copilot.isActive) {
        await copilot.activate();
    }

    // Create a temporary file for Copilot
    const document = await vscode.workspace.openTextDocument({
        content: prompt,
        language: 'plaintext'
    });

    // Get Copilot's API
    const copilotApi = copilot.exports;
    
    // Request completion
    const position = new vscode.Position(document.lineCount, 0);
    const completions = await copilotApi.getCompletions(document, position);

    // Close the temporary document
    await vscode.commands.executeCommand('workbench.action.closeActiveEditor');

    return completions[0]?.text || 'No completion available';
}

function getWebviewContent() {
    return `<!DOCTYPE html>
    <html>
        <head>
            <style>
                body {
                    padding: 20px;
                    font-family: sans-serif;
                }
                #input-container {
                    margin-bottom: 20px;
                }
                #prompt-input {
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 10px;
                }
                #submit-button {
                    padding: 8px 16px;
                    background-color: #007acc;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                #submit-button:hover {
                    background-color: #005999;
                }
                #response-container {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #f0f0f0;
                    border-radius: 4px;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <div id="input-container">
                <textarea id="prompt-input" rows="4" placeholder="Enter your prompt here..."></textarea>
                <button id="submit-button">Get Copilot Response</button>
            </div>
            <div id="response-container"></div>

            <script>
                const vscode = acquireVsCodeApi();
                const promptInput = document.getElementById('prompt-input');
                const submitButton = document.getElementById('submit-button');
                const responseContainer = document.getElementById('response-container');

                submitButton.addEventListener('click', () => {
                    const text = promptInput.value;
                    if (text) {
                        responseContainer.textContent = 'Getting response from Copilot...';
                        vscode.postMessage({
                            command: 'getCompletion',
                            text: text
                        });
                    }
                });

                window.addEventListener('message', event => {
                    const message = event.data;
                    switch (message.command) {
                        case 'showResponse':
                            responseContainer.textContent = message.response;
                            break;
                        case 'showError':
                            responseContainer.textContent = 'Error: ' + message.error;
                            break;
                    }
                });
            </script>
        </body>
    </html>`;
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};


```````````````````````````````

const vscode = require('vscode');

function activate(context) {
    // Register command to show input panel
    let disposable = vscode.commands.registerCommand('copilot-poc.showInput', () => {
        // Create and show WebView panel
        const panel = vscode.window.createWebviewPanel(
            'copilotPoc',
            'Copilot POC',
            vscode.ViewColumn.One,
            {
                enableScripts: true
            }
        );

        // Set initial HTML content
        panel.webview.html = getWebviewContent();

        // Handle messages from webview
        panel.webview.onDidReceiveMessage(async message => {
            if (message.command === 'getCompletion') {
                try {
                    const response = await getCopilotResponse(message.text);
                    // Send response back to webview
                    panel.webview.postMessage({ 
                        command: 'showResponse', 
                        response: response 
                    });
                } catch (error) {
                    panel.webview.postMessage({ 
                        command: 'showError', 
                        error: error.message 
                    });
                }
            }
        });
    });

    context.subscriptions.push(disposable);
}

async function getCopilotResponse(prompt) {
    // Get Copilot Chat extension
    const copilotChat = vscode.extensions.getExtension('GitHub.copilot-chat');
    
    if (!copilotChat) {
        throw new Error('GitHub Copilot Chat is not installed');
    }

    if (!copilotChat.isActive) {
        await copilotChat.activate();
    }

    try {
        // Get the chat API
        const api = copilotChat.exports;
        
        // Create a new chat session
        const response = await vscode.commands.executeCommand('github.copilot.chat.explain', prompt);
        
        return response || 'No response from Copilot';
    } catch (error) {
        console.error('Copilot Chat error:', error);
        throw new Error('Failed to get response from Copilot Chat');
    }
}

function getWebviewContent() {
    return `<!DOCTYPE html>
    <html>
        <head>
            <style>
                body {
                    padding: 20px;
                    font-family: sans-serif;
                }
                #input-container {
                    margin-bottom: 20px;
                }
                #prompt-input {
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 10px;
                }
                #submit-button {
                    padding: 8px 16px;
                    background-color: #007acc;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                #submit-button:hover {
                    background-color: #005999;
                }
                #response-container {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #f0f0f0;
                    border-radius: 4px;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <div id="input-container">
                <textarea id="prompt-input" rows="4" placeholder="Enter your prompt here..."></textarea>
                <button id="submit-button">Get Copilot Response</button>
            </div>
            <div id="response-container"></div>

            <script>
                const vscode = acquireVsCodeApi();
                const promptInput = document.getElementById('prompt-input');
                const submitButton = document.getElementById('submit-button');
                const responseContainer = document.getElementById('response-container');

                submitButton.addEventListener('click', () => {
                    const text = promptInput.value;
                    if (text) {
                        responseContainer.textContent = 'Getting response from Copilot...';
                        vscode.postMessage({
                            command: 'getCompletion',
                            text: text
                        });
                    }
                });

                window.addEventListener('message', event => {
                    const message = event.data;
                    switch (message.command) {
                        case 'showResponse':
                            responseContainer.textContent = message.response;
                            break;
                        case 'showError':
                            responseContainer.textContent = 'Error: ' + message.error;
                            break;
                    }
                });
            </script>
        </body>
    </html>`;
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};


``````````````````````
const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('copilot-poc.showInput', () => {
        const panel = vscode.window.createWebviewPanel(
            'copilotPoc',
            'Copilot POC',
            vscode.ViewColumn.One,
            {
                enableScripts: true
            }
        );

        panel.webview.html = getWebviewContent();

        panel.webview.onDidReceiveMessage(async message => {
            if (message.command === 'getCompletion') {
                try {
                    const response = await getCopilotResponse(message.text);
                    panel.webview.postMessage({ 
                        command: 'showResponse', 
                        response: response 
                    });
                } catch (error) {
                    panel.webview.postMessage({ 
                        command: 'showError', 
                        error: error.message 
                    });
                }
            }
        });
    });

    context.subscriptions.push(disposable);
}

async function getCopilotResponse(prompt) {
    // Get the Copilot extension
    const copilot = vscode.extensions.getExtension('GitHub.copilot');
    
    if (!copilot) {
        throw new Error('GitHub Copilot is not installed');
    }

    if (!copilot.isActive) {
        await copilot.activate();
    }

    try {
        // Create a temporary file to get Copilot suggestions
        const document = await vscode.workspace.openTextDocument({
            content: `// ${prompt}\n`,
            language: 'javascript'
        });

        // Show the document
        await vscode.window.showTextDocument(document);

        // Get Copilot's API
        const api = copilot.exports;
        
        // Request inline suggestions
        const position = new vscode.Position(1, 0);
        const suggestions = await vscode.commands.executeCommand(
            'vscode.executeInlineCompletionProvider',
            document.uri,
            position
        );

        // Close the temporary document
        await vscode.commands.executeCommand('workbench.action.closeActiveEditor');

        if (suggestions && suggestions.length > 0) {
            return suggestions[0].items[0].insertText;
        }
        
        return 'No suggestions available from Copilot';
    } catch (error) {
        console.error('Copilot error:', error);
        throw new Error('Failed to get response from Copilot');
    }
}

function getWebviewContent() {
    return `<!DOCTYPE html>
    <html>
        <head>
            <style>
                body {
                    padding: 20px;
                    font-family: sans-serif;
                }
                #input-container {
                    margin-bottom: 20px;
                }
                #prompt-input {
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 10px;
                }
                #submit-button {
                    padding: 8px 16px;
                    background-color: #007acc;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                #submit-button:hover {
                    background-color: #005999;
                }
                #response-container {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #f0f0f0;
                    border-radius: 4px;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <div id="input-container">
                <textarea id="prompt-input" rows="4" placeholder="Enter your prompt here..."></textarea>
                <button id="submit-button">Get Copilot Response</button>
            </div>
            <div id="response-container"></div>

            <script>
                const vscode = acquireVsCodeApi();
                const promptInput = document.getElementById('prompt-input');
                const submitButton = document.getElementById('submit-button');
                const responseContainer = document.getElementById('response-container');

                submitButton.addEventListener('click', () => {
                    const text = promptInput.value;
                    if (text) {
                        responseContainer.textContent = 'Getting response from Copilot...';
                        vscode.postMessage({
                            command: 'getCompletion',
                            text: text
                        });
                    }
                });

                window.addEventListener('message', event => {
                    const message = event.data;
                    switch (message.command) {
                        case 'showResponse':
                            responseContainer.textContent = message.response;
                            break;
                        case 'showError':
                            responseContainer.textContent = 'Error: ' + message.error;
                            break;
                    }
                });
            </script>
        </body>
    </html>`;
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};


````````````````````

// extension.js
const vscode = require('vscode');

async function getCopilotResponse(prompt) {
    const copilotChat = vscode.extensions.getExtension('GitHub.copilot-chat');
    
    if (!copilotChat) throw new Error('GitHub Copilot Chat is not installed');
    
    try {
        // Activate the extension if needed
        if (!copilotChat.isActive) {
            await copilotChat.activate();
        }

        // Get the chat API instance
        const chatApi = copilotChat.exports.chat;
        
        // Create a new chat session
        const session = await chatApi.startSession();
        
        // Send message and wait for response
        const response = await session.sendMessage(prompt);
        
        return response?.response ?? 'No response from Copilot';
    } catch (error) {
        console.error('Copilot error:', error);
        throw new Error('Failed to get response: ' + error.message);
    }
}

````````````````

const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('copilot-poc.showInput', () => {
        const panel = vscode.window.createWebviewPanel(
            'copilotPoc',
            'Copilot POC',
            vscode.ViewColumn.One,
            {
                enableScripts: true
            }
        );

        panel.webview.html = getWebviewContent();

        panel.webview.onDidReceiveMessage(async (message) => {
            if (message.command === 'getCompletion') {
                try {
                    const response = await getCopilotResponse(message.text);
                    panel.webview.postMessage({
                        command: 'showResponse',
                        response: response
                    });
                } catch (error) {
                    panel.webview.postMessage({
                        command: 'showError',
                        error: error.message
                    });
                }
            }
        });
    });

    context.subscriptions.push(disposable);
}

async function getCopilotResponse(prompt) {
    const copilotChat = vscode.extensions.getExtension('GitHub.copilot-chat');

    if (!copilotChat) {
        throw new Error('GitHub Copilot Chat is not installed.');
    }

    if (!copilotChat.isActive) {
        await copilotChat.activate();
    }

    try {
        const api = copilotChat.exports;
        if (!api || typeof api.ask !== 'function') {
            throw new Error('Copilot Chat API is not available.');
        }

        const response = await api.ask(prompt, { source: 'extension' });
        return response ? response.text : 'No response from Copilot.';
    } catch (error) {
        console.error('Error communicating with Copilot Chat:', error);
        throw new Error('Failed to get response from Copilot Chat.');
    }
}

function getWebviewContent() {
    return `<!DOCTYPE html>
    <html>
        <head>
            <style>
                body {
                    font-family: sans-serif;
                    padding: 20px;
                }
                textarea {
                    width: 100%;
                    height: 80px;
                    margin-bottom: 10px;
                }
                button {
                    background-color: #007acc;
                    color: white;
                    padding: 10px;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #005999;
                }
                #response {
                    margin-top: 20px;
                    white-space: pre-wrap;
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <textarea id="prompt" placeholder="Enter your prompt..."></textarea>
            <button id="submit">Get Copilot Response</button>
            <div id="response"></div>

            <script>
                const vscode = acquireVsCodeApi();
                document.getElementById('submit').addEventListener('click', () => {
                    const text = document.getElementById('prompt').value;
                    if (text) {
                        document.getElementById('response').textContent = 'Fetching response...';
                        vscode.postMessage({ command: 'getCompletion', text: text });
                    }
                });

                window.addEventListener('message', event => {
                    const message = event.data;
                    if (message.command === 'showResponse') {
                        document.getElementById('response').textContent = message.response;
                    } else if (message.command === 'showError') {
                        document.getElementById('response').textContent = 'Error: ' + message.error;
                    }
                });
            </script>
        </body>
    </html>`;
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};

