function loadInterface(interfaceType) {
    // Update active button state
    const navButtons = document.querySelectorAll('.nav-buttons button');
    navButtons.forEach(btn => btn.classList.remove('active'));
    document.getElementById(`${interfaceType}-btn`).classList.add('active');

    // Update header color
    const header = document.querySelector('.header');
    header.classList.remove('management-active', 'business-active', 'private-active');
    header.classList.add(`${interfaceType}-active`);

    // Hide all dropdowns
    const dropdowns = document.querySelectorAll('.dropdown-content');
    dropdowns.forEach(dropdown => dropdown.style.display = 'none');

    // Show active dropdown
    const activeDropdown = document.getElementById(`${interfaceType}-dropdown`);
    activeDropdown.style.display = 'flex';

    // Show module navigation
    const moduleNav = document.getElementById('module-nav');
    moduleNav.style.display = 'block';

    // Update module container with loading state
    const moduleContainer = document.getElementById('module-container');
    moduleContainer.innerHTML = '<div class="loading">Loading modules...</div>';

    fetch(`/api/${interfaceType}/modules`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(modules => {
            // Clear and populate dropdown
            activeDropdown.innerHTML = '';
            if (modules.length === 0) {
                activeDropdown.innerHTML = '<p class="no-modules">No modules available for this interface.</p>';
                moduleContainer.innerHTML = `
                    <div class="welcome-message">
                        <i class="fas fa-info-circle fa-2x"></i>
                        <p>No modules are currently available for the ${interfaceType} interface.</p>
                    </div>`;
                return;
            }

            modules.forEach(module => {
                const button = document.createElement('button');
                button.innerHTML = `<i class="fas fa-plug"></i> ${module.name}`;
                button.onclick = () => loadSubModule(interfaceType, module.name, module.content);
                activeDropdown.appendChild(button);
            });

            // Load first module by default
            loadSubModule(interfaceType, modules[0].name, modules[0].content);
        })
        .catch(error => {
            console.error(`Error loading ${interfaceType} modules:`, error);
            moduleContainer.innerHTML = `
                <div class="welcome-message">
                    <i class="fas fa-exclamation-triangle fa-2x"></i>
                    <p>Error loading modules. Please try again later.</p>
                    <small>${error.message}</small>
                </div>`;
        });
}

function loadSubModule(interfaceType, moduleName, preloadedContent) {
    // Update active button state in dropdown
    const buttons = document.querySelectorAll(`#${interfaceType}-dropdown button`);
    buttons.forEach(btn => btn.classList.remove('active'));
    const activeButton = Array.from(buttons).find(btn => btn.textContent.includes(moduleName));
    if (activeButton) activeButton.classList.add('active');

    // Show loading state
    const moduleContainer = document.getElementById('module-container');
    moduleContainer.innerHTML = '<div class="loading">Loading module content...</div>';

    if (preloadedContent) {
        moduleContainer.innerHTML = preloadedContent;
        return;
    }

    fetch(`/api/${interfaceType}/${moduleName.toLowerCase().replace(/\s+/g, '_')}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            moduleContainer.innerHTML = data.content;
        })
        .catch(error => {
            console.error(`Error loading module ${moduleName}:`, error);
            moduleContainer.innerHTML = `
                <div class="welcome-message">
                    <i class="fas fa-exclamation-triangle fa-2x"></i>
                    <p>Error loading ${moduleName}</p>
                    <small>${error.message}</small>
                </div>`;
        });
}
