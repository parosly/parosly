// Initialize form event listeners when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add form submit event listener
    document.querySelector('form').addEventListener('submit', handleExport);
});

async function handleExport(event) {
    event.preventDefault();
    showLoading();

    const formData = new FormData(event.target);
    const format = document.getElementById('format').value;
    const expr = formData.get('expr');
    const start = formData.get('start');
    const end = formData.get('end');
    const step = formData.get('step');
    const timestamp_format = formData.get('timestamp_format');
    const replaceFields = formData.get('replace_fields') === 'on';

    const data = {
        expr,
        start,
        end,
        step,
        timestamp_format,
        replace_fields: replaceFields
    };

    try {
        const response = await fetch('/api/v1/export?format=' + format, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `data.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}
