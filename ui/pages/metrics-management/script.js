// Load metrics when document is ready
document.addEventListener('DOMContentLoaded', function() {
    loadMetrics();
});

async function loadMetrics() {
    showLoading();
    try {
        const response = await fetch('/api/v1/metrics');
        if (!response.ok) throw new Error('Failed to load metrics');
        const data = await response.json();
        displayMetrics(data);
    } catch (error) {
        showError('Error loading metrics: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayMetrics(metrics) {
    const container = document.querySelector('.metrics-container');
    const table = document.createElement('table');
    table.className = 'metrics-table';
    
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Metric Name</th>
            <th>Type</th>
            <th>Labels</th>
            <th>Actions</th>
        </tr>
    `;
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    metrics.forEach(metric => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${metric.name}</td>
            <td>${metric.type}</td>
            <td>${metric.labels.join(', ')}</td>
            <td>
                <button onclick="deleteMetric('${metric.name}')">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    
    container.innerHTML = '';
    container.appendChild(table);
}

async function deleteMetric(name) {
    if (!confirm(`Are you sure you want to delete metric "${name}"?`)) return;

    showLoading();
    try {
        const response = await fetch(`/api/v1/metrics/${name}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete metric');
        await loadMetrics();
    } catch (error) {
        showError('Error deleting metric: ' + error.message);
    } finally {
        hideLoading();
    }
}
