let codeMirrorInstance;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize CodeMirror editor
    codeMirrorInstance = CodeMirror(document.querySelector('.config-editor'), {
        mode: 'yaml',
        theme: 'monokai',
        lineNumbers: true,
        indentUnit: 2,
        tabSize: 2,
        lineWrapping: true,
        extraKeys: {
            'Ctrl-S': saveConfig,
            'Cmd-S': saveConfig
        }
    });

    // Load existing configuration
    loadConfig();
});

async function loadConfig() {
    showLoading();
    try {
        const response = await fetch('/api/v1/configs');
        if (!response.ok) throw new Error('Failed to load configuration');
        const data = await response.text();
        codeMirrorInstance.setValue(data);
    } catch (error) {
        showError('Error loading configuration: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function saveConfig() {
    showLoading();
    try {
        const config = codeMirrorInstance.getValue();
        const response = await fetch('/api/v1/configs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-yaml' },
            body: config
        });

        if (!response.ok) throw new Error('Failed to save configuration');
        showSuccess('Configuration saved successfully');
    } catch (error) {
        showError('Error saving configuration: ' + error.message);
    } finally {
        hideLoading();
    }
}
