document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('[data-collapse-toggle="mobile-menu"]');
    const menu = document.querySelector('#mobile-menu');
    menu.style.display = 'none';

    toggleButton.addEventListener('click', () => {
        menu.style.display = (menu.style.display === 'none') ? 'block' : 'none';
    });

    const taskId = document.querySelector('script').innerHTML.match(/taskId = "([^"]+)"/)[1];

    if (taskId) {
        const statusElement = document.getElementById('status');
        const downloadLink = document.getElementById('download-link');
        const interval = setInterval(async () => {
            const response = await fetch(`/task-status/${taskId}`);
            const data = await response.text();
            if (data.status === 'SUCCESS') {
                clearInterval(interval);
                statusElement.textContent = 'Processing complete!';
                downloadLink.href = data.result;
                downloadLink.classList.remove('hidden');
            }
        }, 5000);
    }
});
