document.addEventListener('DOMContentLoaded', () => {
    const PROMETHEUS_API_ADDR = window.location.origin;
    let codeMirrorInstance;

    const toolbar = document.querySelector('.toolbar');
    const editConfigBtn = document.getElementById('editConfigBtn');
    const yamlEditor = document.getElementById('yamlEditor');
    const editorContainer = document.getElementById('editorContainer');
    const saveBtn = document.getElementById('saveBtn');
    const applyBtn = document.getElementById('applyBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const modal = document.getElementById('responseModal');
    const modalText = document.getElementById('modal-text');

    document.getElementById('homeBtn').addEventListener('click', () => {
        window.location.href = `${PROMETHEUS_API_ADDR}`;
    });

    document.getElementById('prometheusBtn').addEventListener('click', () => {
        window.location.href = `${PROMETHEUS_API_ADDR}/graph`;
    });

    codeMirrorInstance = CodeMirror.fromTextArea(yamlEditor, {
        mode: 'yaml',
        lineNumbers: true,
        theme: 'monokai',
        lineWrapping: true,
        viewportMargin: Infinity,
        tabSize: 2,
        indentWithTabs: false
    });

    const showModal = (message) => {
        modalText.textContent = message;
        modal.style.display = 'flex';
    };

    const hideModal = () => {
        modal.style.display = 'none';
    };

    const fetchConfig = async () => {
        try {
            const response = await fetch(`${PROMETHEUS_API_ADDR}/api/v1/configs`, {
                headers: { 'Content-Type': 'application/yaml' },
            });

            if (!response.ok) throw new Error(`Failed to fetch config: ${response.statusText}`);
            const yaml = await response.text();

            toolbar.style.display = 'none';
            editorContainer.style.display = 'block';
            codeMirrorInstance.setValue(yaml);

            setTimeout(() => {
                codeMirrorInstance.refresh();
            }, 50);
        } catch (error) {
            showModal(`Error: ${error.message}`);
        }
    };

    const saveConfig = async () => {
        const yaml = codeMirrorInstance.getValue();
        try {
            const jsonData = jsyaml.load(yaml);

            const response = await fetch(`${PROMETHEUS_API_ADDR}/api/v1/configs`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData),
            });

            const result = await response.json();

            if (!response.ok) throw new Error(result.message || 'Unknown error');

            editorContainer.style.display = 'none';
            codeMirrorInstance.setValue('');
            toolbar.style.display = 'flex';
            showModal(`Configuration saved successfully.`);
        } catch (error) {
            showModal(`Error: ${error.message}`);
        }
    };

    const applyConfig = async () => {
        const yaml = codeMirrorInstance.getValue();
        try {
            const jsonData = jsyaml.load(yaml);

            const response = await fetch(`${PROMETHEUS_API_ADDR}/api/v1/configs`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData),
            });

            const result = await response.json();

            if (!response.ok) throw new Error(result.message || 'Unknown error');

            showModal(`Configuration applied successfully.`);
        } catch (error) {
            showModal(`Error: ${error.message}`);
        }
    };

    editConfigBtn.addEventListener('click', fetchConfig);

    saveBtn.addEventListener('click', saveConfig);

    applyBtn.addEventListener('click', applyConfig);

    cancelBtn.addEventListener('click', () => {
        editorContainer.style.display = 'none';
        codeMirrorInstance.setValue('');
        toolbar.style.display = 'flex';
    });

    modal.addEventListener('click', hideModal);
});
