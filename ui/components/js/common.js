// Function to load sidebar
function loadSidebar() {
    fetch('/components/templates/sidebar.html')
        .then(response => response.text())
        .then(html => {
            document.getElementById('sidebarContainer').innerHTML = html;
        })
        .catch(error => console.error('Error loading sidebar:', error));
}

// Loading indicator operations
function showLoading() {
    document.querySelector('.loading-indicator').style.display = 'block';
}

function hideLoading() {
    document.querySelector('.loading-indicator').style.display = 'none';
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 3000);
}

// Load sidebar when page is loaded
document.addEventListener('DOMContentLoaded', loadSidebar); 