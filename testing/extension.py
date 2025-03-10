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

``````````````````

const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

function activate(context) {
  let disposable = vscode.commands.registerCommand('extension.createStructure', () => {
    const panel = vscode.window.createWebviewPanel(
      'createStructure',
      'Create Project Structure',
      vscode.ViewColumn.One,
      { enableScripts: true }
    );

    panel.webview.html = getWebviewContent();

    let businessFilePath = null;
    let dataFilePath = null;

    panel.webview.onDidReceiveMessage(async (message) => {
      switch (message.command) {
        case 'selectBusiness':
          const businessFile = await vscode.window.showOpenDialog({
            canSelectMany: false,
            canSelectFiles: true,
            openLabel: 'Select Business Requirements'
          });
          if (businessFile && businessFile[0]) {
            businessFilePath = businessFile[0].fsPath;
            panel.webview.postMessage({
              command: 'updateBusiness',
              path: businessFilePath
            });
          }
          break;

        case 'selectData':
          const dataFile = await vscode.window.showOpenDialog({
            canSelectMany: false,
            canSelectFiles: true,
            openLabel: 'Select Data Upload (Optional)'
          });
          if (dataFile && dataFile[0]) {
            dataFilePath = dataFile[0].fsPath;
            panel.webview.postMessage({
              command: 'updateData',
              path: dataFilePath
            });
          }
          break;

        case 'submit':
          if (!businessFilePath) {
            vscode.window.showErrorMessage('Business file is required.');
            return;
          }

          const workspaceFolders = vscode.workspace.workspaceFolders;
          if (!workspaceFolders) {
            vscode.window.showErrorMessage('Open a workspace first.');
            return;
          }

          const workspaceRoot = workspaceFolders[0].uri.fsPath;
          createDirectoryStructure(workspaceRoot);
          panel.dispose();
          break;
      }
    });
  });

  context.subscriptions.push(disposable);
}

function createDirectoryStructure(workspaceRoot) {
  const directories = [
    'src/core',
    'src/models',
    'src/services',
    'src/utils',
    'src/config',
    'src/api',
    'tests',
    'docs',
    'scripts'
  ];

  directories.forEach(dir => {
    const dirPath = path.join(workspaceRoot, dir);
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
  });

  vscode.window.showInformationMessage('Directory structure created!');
}

function getWebviewContent() {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        .container { padding: 20px; }
        .input-group { margin: 10px 0; }
        button { margin: 5px; }
        #submitBtn { background: #007acc; color: white; border: none; padding: 10px; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="input-group">
          <strong>Business File (Required):</strong><br/>
          <button onclick="selectBusiness()">Choose File</button>
          <span id="businessPath"></span>
        </div>

        <div class="input-group">
          <strong>Data File (Optional):</strong><br/>
          <button onclick="selectData()">Choose File</button>
          <span id="dataPath"></span>
        </div>

        <button id="submitBtn" onclick="submit()">Create Structure</button>
      </div>

      <script>
        function selectBusiness() {
          vscode.postMessage({ command: 'selectBusiness' });
        }

        function selectData() {
          vscode.postMessage({ command: 'selectData' });
        }

        function submit() {
          vscode.postMessage({ command: 'submit' });
        }

        window.addEventListener('message', event => {
          if (event.data.command === 'updateBusiness') {
            document.getElementById('businessPath').textContent = event.data.path;
          } else if (event.data.command === 'updateData') {
            document.getElementById('dataPath').textContent = event.data.path;
          }
        });
      </script>
    </body>
    </html>
  `;
}

exports.activate = activate;

function deactivate() {}
module.exports = { activate, deactivate };

`````````````


const vscode = require("vscode");
const fs = require("fs");
const path = require("path");

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  let disposable = vscode.commands.registerCommand(
    "extension.createProject",
    async function () {
      // Ask for Business Requirements file (Mandatory)
      const businessFileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        openLabel: "Select Business Requirements File",
        filters: { "Text Files": ["txt", "md", "docx"], "All Files": ["*"] },
      });

      if (!businessFileUri || businessFileUri.length === 0) {
        vscode.window.showErrorMessage("Business Requirements file is required.");
        return;
      }

      // Ask for Data Upload file (Optional)
      const dataFileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        openLabel: "Select Data Upload File (Optional)",
        filters: { "CSV Files": ["csv"], "Excel Files": ["xlsx", "xls"], "All Files": ["*"] },
      });

      // Ask user where to create the project
      const projectUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        canSelectFiles: false,
        canSelectFolders: true,
        openLabel: "Select Project Directory",
      });

      if (!projectUri || projectUri.length === 0) {
        vscode.window.showErrorMessage("You must select a project directory.");
        return;
      }

      const projectRoot = projectUri[0].fsPath;

      // Define the folder structure
      const folders = [
        "src/core",
        "src/models",
        "src/services",
        "src/utils",
        "src/config",
        "src/api",
        "tests",
        "docs",
        "scripts",
      ];

      try {
        // Create directories
        folders.forEach((folder) => {
          const dirPath = path.join(projectRoot, folder);
          if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
          }
        });

        vscode.window.showInformationMessage("Project structure created successfully!");
      } catch (error) {
        vscode.window.showErrorMessage(`Error creating directories: ${error.message}`);
      }
    }
  );

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};

````````````

const vscode = require("vscode");
const fs = require("fs");
const path = require("path");

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  let disposable = vscode.commands.registerCommand(
    "extension.createProject",
    async function () {
      // Ask for Business Requirements file (Mandatory)
      const businessFileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        openLabel: "Select Business Requirements File",
        filters: { "Text Files": ["txt"], "All Files": ["*"] },
      });

      if (!businessFileUri || businessFileUri.length === 0) {
        vscode.window.showErrorMessage("Business Requirements file is required.");
        return;
      }

      // Ask for Data Upload file (Optional)
      const dataFileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        openLabel: "Select Data Upload File (Optional)",
        filters: { "CSV Files": ["csv"], "All Files": ["*"] },
      });

      // Ask user where to create the project
      const projectUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        canSelectFiles: false,
        canSelectFolders: true,
        openLabel: "Select Project Directory",
      });

      if (!projectUri || projectUri.length === 0) {
        vscode.window.showErrorMessage("You must select a project directory.");
        return;
      }

      const projectRoot = projectUri[0].fsPath;

      // Define the folder structure
      const folders = [
        ".vscode",
        "images",
        "static",
        "pages",
        "src/core",
        "src/utils",
        "src/config",
        "tests",
        "docs",
        "data",
      ];

      // Create directories
      try {
        folders.forEach((folder) => {
          const dirPath = path.join(projectRoot, folder);
          if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
          }
        });

        // Copy uploaded Business Requirement file to 'data/' directory
        const businessFilePath = path.join(projectRoot, "data", "business_requirement.txt");
        fs.copyFileSync(businessFileUri[0].fsPath, businessFilePath);

        // If Data file is uploaded, copy it too
        if (dataFileUri && dataFileUri.length > 0) {
          const dataFilePath = path.join(projectRoot, "data", "data.csv");
          fs.copyFileSync(dataFileUri[0].fsPath, dataFilePath);
        }

        // Predefined files stored in extension's storage (Assume they exist in extension's media folder)
        const extensionMediaPath = context.extensionPath;

        // Copy predefined files from extension storage
        const predefinedFiles = [
          { src: "media/streamlit_instructions.md", dest: "streamlit_instructions.md" },
          { src: "media/.vscode/settings.json", dest: ".vscode/settings.json" },
          { src: "media/static/style.css", dest: "static/style.css" },
        ];

        predefinedFiles.forEach(({ src, dest }) => {
          const srcPath = path.join(extensionMediaPath, src);
          const destPath = path.join(projectRoot, dest);

          if (fs.existsSync(srcPath)) {
            fs.copyFileSync(srcPath, destPath);
          }
        });

        // Create empty files
        ["app.py", "requirements.txt", ".env"].forEach((file) => {
          const filePath = path.join(projectRoot, file);
          if (!fs.existsSync(filePath)) {
            fs.writeFileSync(filePath, "");
          }
        });

        vscode.window.showInformationMessage("Project structure created successfully!");
      } catch (error) {
        vscode.window.showErrorMessage(`Error creating directories: ${error.message}`);
      }
    }
  );

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};

````````````` typescript

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

/**
 * @param {vscode.ExtensionContext} context
 */
export function activate(context: vscode.ExtensionContext): void {
  const disposable = vscode.commands.registerCommand(
    'extension.createProject',
    async function () {
      // Ask for Business Requirements file (Mandatory)
      const businessFileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        openLabel: 'Select Business Requirements File',
        filters: { 'Text Files': ['txt'], 'All Files': ['*'] },
      });

      if (!businessFileUri || businessFileUri.length === 0) {
        vscode.window.showErrorMessage('Business Requirements file is required.');
        return;
      }

      // Ask for Data Upload file (Optional)
      const dataFileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        openLabel: 'Select Data Upload File (Optional)',
        filters: { 'CSV Files': ['csv'], 'All Files': ['*'] },
      });

      // Ask user where to create the project
      const projectUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        canSelectFiles: false,
        canSelectFolders: true,
        openLabel: 'Select Project Directory',
      });

      if (!projectUri || projectUri.length === 0) {
        vscode.window.showErrorMessage('You must select a project directory.');
        return;
      }

      const projectRoot = projectUri[0].fsPath;

      // Define the folder structure
      const folders: string[] = [
        '.vscode',
        'images',
        'static',
        'pages',
        'src/core',
        'src/utils',
        'src/config',
        'tests',
        'docs',
        'data',
      ];

      // Create directories
      try {
        folders.forEach((folder: string) => {
          const dirPath = path.join(projectRoot, folder);
          if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
          }
        });

        // Copy uploaded Business Requirement file to 'data/' directory
        const businessFilePath = path.join(projectRoot, 'data', 'business_requirement.txt');
        fs.copyFileSync(businessFileUri[0].fsPath, businessFilePath);

        // If Data file is uploaded, copy it too
        if (dataFileUri && dataFileUri.length > 0) {
          const dataFilePath = path.join(projectRoot, 'data', 'data.csv');
          fs.copyFileSync(dataFileUri[0].fsPath, dataFilePath);
        }

        // Predefined files stored in extension's storage (Assume they exist in extension's media folder)
        const extensionMediaPath = context.extensionPath;

        // Copy predefined files from extension storage
        const predefinedFiles: { src: string; dest: string }[] = [
          { src: 'media/streamlit_instructions.md', dest: 'streamlit_instructions.md' },
          { src: 'media/.vscode/settings.json', dest: '.vscode/settings.json' },
          { src: 'media/static/style.css', dest: 'static/style.css' },
        ];

        predefinedFiles.forEach(({ src, dest }: { src: string; dest: string }) => {
          const srcPath = path.join(extensionMediaPath, src);
          const destPath = path.join(projectRoot, dest);

          if (fs.existsSync(srcPath)) {
            fs.copyFileSync(srcPath, destPath);
          }
        });

        // Create empty files
        const emptyFiles: string[] = ['app.py', 'requirements.txt', '.env'];
        emptyFiles.forEach((file: string) => {
          const filePath = path.join(projectRoot, file);
          if (!fs.existsSync(filePath)) {
            fs.writeFileSync(filePath, '');
          }
        });

        vscode.window.showInformationMessage('Project structure created successfully!');
      } catch (error) {
        vscode.window.showErrorMessage(`Error creating directories: ${(error as Error).message}`);
      }
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate(): void {}

`````````````````````````````````````````````````````


import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios'; // Make sure to install axios

interface ThreadResponse {
    thread_id: string;
    thread: {
        id: string;
        name: string;
        repoID: number;
        repoOwnerID: number;
        createdAt: string;
        updatedAt: string;
    };
}

interface MessageResponse {
    message: {
        id: string;
        threadID: string;
        turnID: string;
        role: string;
        content: string;
        createdAt: string;
        intent: 'cli-explain' | 'cli-suggest';
        references: any[];
    };
}

class CopilotAPI {
    private static readonly BASE_URL = 'https://api.githubcopilot.com/github/chat';

    static async createThread(): Promise<ThreadResponse> {
        try {
            const response = await axios.post(`${this.BASE_URL}/threads`, {});
            return response.data;
        } catch (error) {
            throw new Error(`Failed to create thread: ${error}`);
        }
    }

    static async sendMessage(
        threadUuid: string,
        content: string,
        intent: 'cli-explain' | 'cli-suggest',
        program: string
    ): Promise<MessageResponse> {
        try {
            const response = await axios.post(
                `${this.BASE_URL}/threads/${threadUuid}/messages`,
                {
                    content,
                    intent,
                    references: [
                        {
                            type: 'cli-command',
                            program
                        }
                    ]
                }
            );
            return response.data;
        } catch (error) {
            throw new Error(`Failed to send message: ${error}`);
        }
    }
}

export function activate(context: vscode.ExtensionContext): void {
    const disposable = vscode.commands.registerCommand(
        'extension.createProject',
        async function () {
            try {
                // Initialize Copilot thread
                const thread = await CopilotAPI.createThread();
                
                // Ask for Business Requirements file (Mandatory)
                const businessFileUri = await vscode.window.showOpenDialog({
                    canSelectMany: false,
                    openLabel: 'Select Business Requirements File',
                    filters: { 'Text Files': ['txt'], 'All Files': [''] },
                });

                if (!businessFileUri || businessFileUri.length === 0) {
                    vscode.window.showErrorMessage('Business Requirements file is required.');
                    return;
                }

                // Read business requirements file content
                const businessReqContent = fs.readFileSync(businessFileUri[0].fsPath, 'utf8');
                
                // Send business requirements to Copilot for suggestions
                const suggestResponse = await CopilotAPI.sendMessage(
                    thread.thread_id,
                    businessReqContent,
                    'cli-suggest',
                    'project-structure'
                );

                // Ask for Data Upload file (Optional)
                const dataFileUri = await vscode.window.showOpenDialog({
                    canSelectMany: false,
                    openLabel: 'Select Data Upload File (Optional)',
                    filters: { 'CSV Files': ['csv'], 'All Files': ['*'] },
                });

                // Ask user where to create the project
                const projectUri = await vscode.window.showOpenDialog({
                    canSelectMany: false,
                    canSelectFiles: false,
                    canSelectFolders: true,
                    openLabel: 'Select Project Directory',
                });

                if (!projectUri || projectUri.length === 0) {
                    vscode.window.showErrorMessage('You must select a project directory.');
                    return;
                }

                const projectRoot = projectUri[0].fsPath;

                // Define the folder structure
                const folders: string[] = [
                    '.vscode',
                    'images',
                    'static',
                    'pages',
                    'src/core',
                    'src/utils',
                    'src/config',
                    'tests',
                    'docs',
                    'data',
                ];

                // Create directories
                folders.forEach((folder: string) => {
                    const dirPath = path.join(projectRoot, folder);
                    if (!fs.existsSync(dirPath)) {
                        fs.mkdirSync(dirPath, { recursive: true });
                    }
                });

                // Copy uploaded Business Requirement file to 'data/' directory
                const businessFilePath = path.join(projectRoot, 'data', 'business_requirement.txt');
                fs.copyFileSync(businessFileUri[0].fsPath, businessFilePath);

                // If Data file is uploaded, copy it too
                if (dataFileUri && dataFileUri.length > 0) {
                    const dataFilePath = path.join(projectRoot, 'data', 'data.csv');
                    fs.copyFileSync(dataFileUri[0].fsPath, dataFilePath);

                    // Send data file analysis request to Copilot
                    await CopilotAPI.sendMessage(
                        thread.thread_id,
                        'Analyze data structure and suggest schema',
                        'cli-explain',
                        'data-analysis'
                    );
                }

                // Predefined files stored in extension's storage
                const extensionMediaPath = context.extensionPath;

                // Copy predefined files from extension storage
                const predefinedFiles: { src: string; dest: string }[] = [
                    { src: 'media/streamlit_instructions.md', dest: 'streamlit_instructions.md' },
                    { src: 'media/.vscode/settings.json', dest: '.vscode/settings.json' },
                    { src: 'media/static/style.css', dest: 'static/style.css' },
                ];

                predefinedFiles.forEach(({ src, dest }: { src: string; dest: string }) => {
                    const srcPath = path.join(extensionMediaPath, src);
                    const destPath = path.join(projectRoot, dest);

                    if (fs.existsSync(srcPath)) {
                        fs.copyFileSync(srcPath, destPath);
                    }
                });

                // Create empty files
                const emptyFiles: string[] = ['app.py', 'requirements.txt', '.env'];
                emptyFiles.forEach((file: string) => {
                    const filePath = path.join(projectRoot, file);
                    if (!fs.existsSync(filePath)) {
                        fs.writeFileSync(filePath, '');
                    }
                });

                vscode.window.showInformationMessage('Project structure created successfully!');
            } catch (error) {
                vscode.window.showErrorMessage(`Error: ${(error as Error).message}`);
            }
        }
    );

    context.subscriptions.push(disposable);
}

export function deactivate(): void {}


```````````````````````````

import * as vscode from 'vscode';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
  // Register chat participant
  const chatParticipant = vscode.chat.createChatParticipant('vscode-snowflake-accelerator', async (request, context, response, token) => {
    try {
      const userQuery = request.prompt;
      
      // Get uploaded files from the chat context
      const uploadedFiles = context.files || [];
      
      // Process uploaded files
      const fileContents: { [key: string]: string } = {};
      for (const file of uploadedFiles) {
        try {
          // Read file contents using the VS Code API
          const document = await vscode.workspace.openTextDocument(file.uri);
          fileContents[file.name] = document.getText();
        } catch (error) {
          response.markdown(`Error reading file ${file.name}: ${error.message}`);
          return;
        }
      }

      // Read the default markdown instructions
      const markdownFilePath = '/Users/a854236/Music/extension/vscode-snowflake-accelerator/src/streamlit_instructions.md';
      let markdownContent = '';
      try {
        markdownContent = fs.readFileSync(markdownFilePath, 'utf8');
      } catch (error) {
        response.markdown(`Error reading instructions file: ${error.message}`);
        return;
      }

      // Select chat model
      const chatModels = await vscode.chat.selectChatModels({ 'vendor': 'copilot', 'family': 'gpt-4' });
      if (!chatModels || chatModels.length === 0) {
        response.markdown('Sorry, no compatible chat models found.');
        return;
      }

      // Prepare messages array with uploaded file contents
      const messages = [
        vscode.chat.createChatMessage('system', 
          "You are an expert in generating boilerplate code for Streamlit Applications based on business requirements uploaded in a text file! " +
          "Think carefully and step by step like a streamlit expert would. Your job is to generate the directory structure along with the " +
          "boilerplate code. Always start your response by stating what concept you are explaining. Always include code samples."
        ),
        vscode.chat.createChatMessage('system', 
          "Go through the contents of the markdown file so that you can get a gist of how we are building streamlit applications and " +
          "what coding practices we are adopting for our projects."
        ),
        vscode.chat.createChatMessage('system', `The markdown file is as follows: ${markdownContent}`),
      ];

      // Add uploaded file contents to the messages
      for (const [fileName, content] of Object.entries(fileContents)) {
        messages.push(
          vscode.chat.createChatMessage('user', 
            `Contents of uploaded file ${fileName}:\n\n${content}`
          )
        );
      }

      // Add the user's query
      messages.push(vscode.chat.createChatMessage('user', userQuery));

      // Send request to chat model
      const chatRequest = await chatModels[0].sendRequest(messages, undefined, token);
      
      // Stream the response
      for await (const chunk of chatRequest.text) {
        response.markdown(chunk);
      }

    } catch (error) {
      response.markdown(`An error occurred: ${error.message}`);
    }
  });

  // Register the chat participant with the extension's subscriptions
  context.subscriptions.push(chatParticipant);
}

export function deactivate() {}
