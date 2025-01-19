let codeMirrorInstance;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize CodeMirror editor
    codeMirrorInstance = CodeMirror(document.querySelector('.editor-container'), {
        mode: 'yaml',
        theme: 'monokai',
        lineNumbers: true,
        indentUnit: 2,
        tabSize: 2,
        lineWrapping: true,
        extraKeys: {
            'Ctrl-S': saveRule,
            'Cmd-S': saveRule
        }
    });

    loadRules();
});

async function loadRules() {
    showLoading();
    try {
        const response = await fetch('/api/v1/rules');
        if (!response.ok) throw new Error('Failed to load rules');
        const data = await response.json();
        displayRules(data);
    } catch (error) {
        showError('Error loading rules: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayRules(rules) {
    const container = document.querySelector('.rules-list');
    container.innerHTML = '';
    
    rules.forEach(rule => {
        const div = document.createElement('div');
        div.className = 'rule-item';
        div.textContent = rule.name;
        div.onclick = () => loadRule(rule.name);
        container.appendChild(div);
    });
}

async function loadRule(name) {
    showLoading();
    try {
        const response = await fetch(`/api/v1/rules/${name}`);
        if (!response.ok) throw new Error('Failed to load rule');
        const data = await response.text();
        
        document.querySelector('.editor-container').style.display = 'block';
        codeMirrorInstance.setValue(data);
    } catch (error) {
        showError('Error loading rule: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function saveRule() {
    showLoading();
    try {
        const rule = codeMirrorInstance.getValue();
        const response = await fetch('/api/v1/rules', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-yaml' },
            body: rule
        });

        if (!response.ok) throw new Error('Failed to save rule');
        showSuccess('Rule saved successfully');
        await loadRules();
    } catch (error) {
        showError('Error saving rule: ' + error.message);
    } finally {
        hideLoading();
    }
}

function createNewRule() {
    document.querySelector('.editor-container').style.display = 'block';
    codeMirrorInstance.setValue('');
}