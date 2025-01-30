{
    "name": "copilot-poc",
    "displayName": "Copilot POC",
    "description": "Simple POC for Copilot integration",
    "version": "0.0.1",
    "engines": {
        "vscode": "^1.85.0"
    },
    "categories": [
        "Other"
    ],
    "activationEvents": [],
    "main": "./extension.js",
    "contributes": {
        "commands": [
            {
                "command": "copilot-poc.showInput",
                "title": "Show Copilot POC Input"
            }
        ]
    },
    "scripts": {
        "lint": "eslint .",
        "package": "vsce package"
    },
    "devDependencies": {
        "@types/vscode": "^1.85.0",
        "@types/node": "^16.18.34",
        "eslint": "^8.26.0",
        "vsce": "^2.15.0"
    }
}
