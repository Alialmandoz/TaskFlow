// dashboard/static/dashboard/js/dashboard_logic.js

// Esperar a que el DOM esté completamente cargado para asegurar que window.AI_COMMAND_HANDLER_URL esté disponible
// y que los elementos del formulario existan.
document.addEventListener('DOMContentLoaded', function() {

    // Elementos del DOM
    const aiCommandForm = document.getElementById('aiCommandForm');
    const instructionTextarea = document.getElementById('instruction');
    const responseArea = document.getElementById('responseArea');
    
    // El input del token CSRF se espera que esté en el <form> dentro del HTML.
    // Lo obtendremos directamente cuando lo necesitemos.

    // Obtener la URL del handler de la variable global 'window' definida en el HTML
    const aiCommandHandlerUrl = window.AI_COMMAND_HANDLER_URL;

    // Verificar si los elementos cruciales y la URL están disponibles
    if (!aiCommandForm || !instructionTextarea || !responseArea || !aiCommandHandlerUrl) {
        console.error('Error crítico: Faltan elementos esenciales del DOM (formulario, textarea, área de respuesta) o la URL del AI Handler no está definida en window.AI_COMMAND_HANDLER_URL.');
        if (responseArea) { // Intentar mostrar error en el área de respuesta si existe
             responseArea.innerHTML = '<p class="error">Error de inicialización del interfaz de IA. Verifique la consola.</p>';
        }
        return; // Detener la ejecución del script si falta algo crucial
    }

    // Listener para el formulario principal de la consola de IA
    aiCommandForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevenir el envío tradicional del formulario
        const instruction = instructionTextarea.value.trim();
        if (!instruction) return; // No hacer nada si la instrucción está vacía

        responseArea.innerHTML = '<p class="loading">Procesando tu instrucción...</p>';
        instructionTextarea.value = ''; // Limpiar el textarea

        // Obtener el token CSRF del input oculto en el formulario
        const csrfTokenInput = aiCommandForm.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenInput) {
            console.error("Error crítico: Input de token CSRF no encontrado en el formulario.");
            responseArea.innerHTML = '<p class="error">Error de configuración: Falta token CSRF.</p>';
            return;
        }
        const currentCsrfToken = csrfTokenInput.value;

        try {
            const response = await fetch(aiCommandHandlerUrl, { // Usar la variable obtenida de window
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': currentCsrfToken
                },
                body: JSON.stringify({ instruction: instruction })
            });

            const data = await response.json(); // Asumimos que la respuesta siempre será JSON o fallará el parseo

            if (response.ok || data.error) { // data.error para errores controlados por el backend con status 200 o 400
                if (data.action_needed === 'confirm_expense') {
                    displayConfirmationUI(data);
                } else if (data.action_needed === 'confirm_project_with_tasks') {
                    displayProjectConfirmationUI(data);
                } else if (data.error) {
                     responseArea.innerHTML = `<p class="error"><strong>Error:</strong> ${data.error}</p>`;
                } else { // Cualquier otra respuesta exitosa sin acción específica o error
                    handleSuccessfulResponse(data);
                }
            } else { // Errores de red o HTTP no OK que no devolvieron JSON con 'error'
                responseArea.innerHTML = `<p class="error"><strong>Error ${response.status}:</strong> ${data.error || 'Ocurrió un error inesperado en el servidor.'}</p>`;
            }
        } catch (error) { // Captura errores del fetch en sí o del response.json()
            console.error('Error en la solicitud inicial AI:', error);
            responseArea.innerHTML = `<p class="error"><strong>Error de conexión o script:</strong> ${error.message}</p>`;
        }
    });

    // Función para mostrar la UI de confirmación de gastos
    function displayConfirmationUI(data) {
        responseArea.innerHTML = ''; // Limpiar área de respuesta

        const messageP = document.createElement('p');
        messageP.textContent = data.message || 'Por favor, confirma los detalles:';
        responseArea.appendChild(messageP);

        const detailsContainer = document.createElement('div');
        detailsContainer.style.padding = '10px';
        detailsContainer.style.border = '1px solid #ccc';
        detailsContainer.style.borderRadius = '4px';
        detailsContainer.style.backgroundColor = '#f8f9fa';
        detailsContainer.style.marginBottom = '15px';

        // Mostrar datos extraídos (descripción, monto, fecha, instrucción original)
        for (const [key, value] of Object.entries(data.extracted_data)) {
            if (key !== 'category_name_guess' && value !== null && value !== undefined) {
                const detailP = document.createElement('p');
                detailP.style.margin = '5px 0';
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                detailP.innerHTML = `<strong>${label}:</strong> ${value}`;
                detailsContainer.appendChild(detailP);
            }
        }

        // Sección para Categorías
        const categorySection = document.createElement('div');
        categorySection.classList.add('mb-3');

        const categoryLabel = document.createElement('label');
        categoryLabel.htmlFor = 'category_select_dropdown';
        categoryLabel.textContent = 'Categoría del Gasto:';
        categoryLabel.classList.add('form-label');
        categorySection.appendChild(categoryLabel);

        const categorySelect = document.createElement('select');
        categorySelect.id = 'category_select_dropdown';
        // console.log("Elemento categorySelect creado con ID:", categorySelect.id, categorySelect);
        categorySelect.classList.add('form-select', 'form-select-sm', 'mb-2');

        const defaultOption = document.createElement('option');
        defaultOption.value = ""; // Valor vacío para "ninguna seleccionada"
        defaultOption.textContent = "--- Seleccionar Categoría Existente ---";
        categorySelect.appendChild(defaultOption);

        let geminiGuessExistsInUserCategories = false;
        if (data.user_categories && data.user_categories.length > 0) {
            data.user_categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.name;
                if (data.extracted_data.category_name_guess &&
                    cat.name.toLowerCase() === data.extracted_data.category_name_guess.toLowerCase()) {
                    option.selected = true;
                    geminiGuessExistsInUserCategories = true;
                }
                categorySelect.appendChild(option);
            });
        } else {
            const noCatOption = document.createElement('option');
            noCatOption.value = "";
            noCatOption.textContent = "No hay categorías creadas";
            noCatOption.disabled = true;
            categorySelect.appendChild(noCatOption);
        }
        categorySection.appendChild(categorySelect);

        const newCategoryLabel = document.createElement('label');
        newCategoryLabel.htmlFor = 'new_category_name_input';
        newCategoryLabel.textContent = 'O crear nueva categoría:';
        newCategoryLabel.classList.add('form-label', 'mt-2');
        categorySection.appendChild(newCategoryLabel);

        const newCategoryInput = document.createElement('input');
        newCategoryInput.type = 'text';
        newCategoryInput.id = 'new_category_name_input';
        // console.log("Elemento newCategoryInput creado con ID:", newCategoryInput.id, newCategoryInput);
        newCategoryInput.placeholder = 'Nombre para la nueva categoría';
        newCategoryInput.classList.add('form-control', 'form-control-sm');

        // Autocompletar newCategoryInput si Gemini hizo una suposición que NO existe
        if (data.extracted_data.category_name_guess && !geminiGuessExistsInUserCategories) {
            newCategoryInput.value = data.extracted_data.category_name_guess;
            const suggestionMessage = document.createElement('small');
            suggestionMessage.classList.add('form-text', 'text-muted', 'd-block', 'mb-2');
            suggestionMessage.textContent = `La IA sugiere "${data.extracted_data.category_name_guess}" como nueva categoría. Puedes editarla.`;
            categorySection.insertBefore(suggestionMessage, newCategoryInput);
        }
        categorySection.appendChild(newCategoryInput);

        detailsContainer.appendChild(categorySection);
        responseArea.appendChild(detailsContainer);

        // Botones de Acción
        const actionButtonsDiv = document.createElement('div');
        const confirmButton = document.createElement('button');
        confirmButton.textContent = 'Confirmar Gasto';
        confirmButton.classList.add('btn', 'btn-success', 'me-2');
        confirmButton.dataset.extractedRaw = JSON.stringify(data.extracted_data); // Contiene _original_user_instruction
        confirmButton.addEventListener('click', handleExpenseConfirmation);
        actionButtonsDiv.appendChild(confirmButton);

        const cancelButton = document.createElement('button');
        cancelButton.textContent = 'Cancelar';
        cancelButton.classList.add('btn', 'btn-secondary');
        cancelButton.addEventListener('click', cancelConfirmation);
        actionButtonsDiv.appendChild(cancelButton);
        responseArea.appendChild(actionButtonsDiv);
    }

    // Función para manejar el clic en "Confirmar Gasto"
    async function handleExpenseConfirmation(event) {
        const button = event.target;
        const originalExtractedData = JSON.parse(button.dataset.extractedRaw);

        // Leer valores ANTES de modificar responseArea
        const categorySelectElement = document.getElementById('category_select_dropdown');
        const newCategoryInputElement = document.getElementById('new_category_name_input');

        // console.log("Inicio handleExpenseConfirmation - categorySelectElement:", categorySelectElement);
        // console.log("Inicio handleExpenseConfirmation - newCategoryInputElement:", newCategoryInputElement);

        if (!categorySelectElement) {
            console.error("FATAL: Elemento 'category_select_dropdown' NO ENCONTRADO al inicio de handleExpenseConfirmation.");
            responseArea.innerHTML = '<p class="error">Error interno (CSD init): No se pudo procesar la categoría.</p>';
            return;
        }
        if (!newCategoryInputElement) {
            console.error("FATAL: Elemento 'new_category_name_input' NO ENCONTRADO al inicio de handleExpenseConfirmation.");
            responseArea.innerHTML = '<p class="error">Error interno (NCI init): No se pudo procesar la categoría.</p>';
            return;
        }

        const selectedCategoryIdValue = categorySelectElement.value;
        const newCategoryName = newCategoryInputElement.value.trim();
        
        responseArea.innerHTML = '<p class="loading">Registrando el gasto...</p>'; // Mostrar estado de carga

        let finalSelectedCategoryId = null;
        if (selectedCategoryIdValue && selectedCategoryIdValue !== "") { // Si hay un valor y no es la opción por defecto vacía
            const parsedId = parseInt(selectedCategoryIdValue, 10);
            if (!isNaN(parsedId)) { // Asegurar que el parseo a número fue exitoso
                finalSelectedCategoryId = parsedId;
            } else {
                console.warn("Advertencia: El valor seleccionado de categoría no es un número válido:", selectedCategoryIdValue);
            }
        }

        const confirmedPayload = {
            description: originalExtractedData.description,
            amount: originalExtractedData.amount,
            transaction_date: originalExtractedData.transaction_date,
            project_name: originalExtractedData.project_name_guess, // Puede ser null
            _original_user_instruction: originalExtractedData._original_user_instruction,
            selected_category_id: finalSelectedCategoryId,
            create_category_with_name: newCategoryName || null // Si newCategoryName es vacío, enviar null
        };
        
        // console.log("Payload para confirmación:", JSON.stringify(confirmedPayload, null, 2));

        // Obtener el token CSRF directamente del DOM aquí, ya que el input original podría no estar en el mismo scope
        const csrfTokenForConfirmation = document.querySelector('form#aiCommandForm [name=csrfmiddlewaretoken]');
        if (!csrfTokenForConfirmation) {
             console.error("Error: Falta token CSRF (input) para confirmación.");
             responseArea.innerHTML = '<p class="error">Error de configuración: No se pudo enviar (falta token CSRF).</p>';
             return;
        }
        const currentCsrfTokenValue = csrfTokenForConfirmation.value;


        try {
            const response = await fetch(window.AI_COMMAND_HANDLER_URL, { // Usar la variable global para la URL
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': currentCsrfTokenValue},
                body: JSON.stringify({
                    action: "confirm_creation",
                    confirmed_data: confirmedPayload
                })
            });

            // console.log("Respuesta del servidor (confirmación):", response.status, response.statusText);
            const responseDataText = await response.text();
            // console.log("Cuerpo de la respuesta (texto):", responseDataText);

            let dataFromServer;
            if (responseDataText) {
                try {
                    dataFromServer = JSON.parse(responseDataText);
                } catch (e) {
                    console.error("Error parseando JSON de respuesta:", e, "Respuesta recibida:", responseDataText);
                    responseArea.innerHTML = `<p class="error">Error: Respuesta inválida del servidor. Contenido: ${responseDataText.substring(0, 200)}...</p>`;
                    return;
                }
            } else {
                console.error("Respuesta del servidor vacía.");
                responseArea.innerHTML = `<p class="error">Error: Respuesta vacía del servidor.</p>`;
                return;
            }

            if (response.ok) {
                if (dataFromServer.type === 'transaction_created') {
                    handleSuccessfulResponse(dataFromServer, true);
                } else if (dataFromServer.error) { // Error controlado devuelto por el backend con status OK
                    responseArea.innerHTML = `<p class="error"><strong>Error al registrar:</strong> ${dataFromServer.error}</p>`;
                } else { // Otro tipo de respuesta OK
                     handleSuccessfulResponse(dataFromServer);
                }
            } else { // Errores HTTP (4xx, 5xx)
                 responseArea.innerHTML = `<p class="error"><strong>Error ${response.status} al registrar:</strong> ${dataFromServer.error || response.statusText || 'Ocurrió un error.'}</p>`;
            }

        } catch (error) { // Errores de red o del propio fetch
            console.error('Error en solicitud de confirmación (catch):', error);
            responseArea.innerHTML = `<p class="error"><strong>Error de conexión o script en confirmación:</strong> ${error.message}</p>`;
        }
    }

    // Función para manejar el clic en "Cancelar"
    function cancelConfirmation() {
        responseArea.innerHTML = 'Operación cancelada. Esperando instrucción...';
    }

    // Función para manejar la confirmación de creación de proyecto
    async function handleProjectCreationConfirmation(event) {
        event.preventDefault();
        const button = event.target;
        const projectData = JSON.parse(button.dataset.projectData);

        const selectedTasks = [];
        const checkedCheckboxes = document.querySelectorAll('input[name="suggested_task"]:checked');
        checkedCheckboxes.forEach(checkbox => {
            selectedTasks.push(checkbox.value);
        });

        responseArea.innerHTML = '<p class="loading">Creating project and tasks...</p>';
        // Deshabilitar botones para evitar doble submission
        button.disabled = true;
        const cancelButton = document.getElementById('cancelProjectCreationBtn');
        if (cancelButton) cancelButton.disabled = true;


        // Obtener el token CSRF del input oculto en el formulario principal
        const csrfTokenInput = aiCommandForm.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenInput) {
            console.error("Error crítico: Input de token CSRF no encontrado para la confirmación del proyecto.");
            responseArea.innerHTML = '<p class="error">Error de configuración: Falta token CSRF.</p>';
            // Re-habilitar botones
            button.disabled = false;
            if (cancelButton) cancelButton.disabled = false;
            return;
        }
        const currentCsrfToken = csrfTokenInput.value;

        try {
            const response = await fetch(window.AI_COMMAND_HANDLER_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': currentCsrfToken
                },
                body: JSON.stringify({
                    action: "confirm_project_creation_with_tasks",
                    project_data: projectData, // Contiene name, description, original_instruction
                    selected_tasks: selectedTasks
                })
            });

            const result = await response.json();

            if (response.ok && result.type === 'project_created_with_tasks') {
                responseArea.innerHTML = `<p class="success"><strong>${result.message || 'Project and tasks created successfully!'}</strong></p>`;
                responseArea.innerHTML += '<p class="loading">Reloading page...</p>';
                setTimeout(() => { window.location.reload(); }, 1500);
            } else {
                responseArea.innerHTML = `<p class="error"><strong>Error:</strong> ${result.error || 'An unknown error occurred during project creation.'}</p>`;
                // Re-habilitar botones en caso de error para permitir reintentar o cancelar
                button.disabled = false;
                if (cancelButton) cancelButton.disabled = false;
            }
        } catch (error) {
            console.error('Error during project creation confirmation:', error);
            responseArea.innerHTML = `<p class="error"><strong>Connection or script error:</strong> ${error.message}</p>`;
            // Re-habilitar botones
            button.disabled = false;
            if (cancelButton) cancelButton.disabled = false;
        }
    }


    // Nueva función para mostrar UI de confirmación de proyecto con tareas
    function displayProjectConfirmationUI(data) {
        responseArea.innerHTML = ''; // Limpiar área de respuesta

        // Mostrar nombre del proyecto
        const projectNameH3 = document.createElement('h3');
        projectNameH3.innerHTML = `<strong>Project Name:</strong> ${data.project_data.name}`;
        responseArea.appendChild(projectNameH3);

        // Mostrar descripción del proyecto
        const projectDescriptionP = document.createElement('p');
        let descriptionText = data.project_data.description || ''; // Usar cadena vacía si es null/undefined
        if (descriptionText.trim() === '') {
            descriptionText = '<em>No description provided.</em>';
        }
        projectDescriptionP.innerHTML = `<strong>Description:</strong> ${descriptionText}`;
        responseArea.appendChild(projectDescriptionP);

        // Encabezado para tareas sugeridas
        const tasksHeading = document.createElement('h4');
        tasksHeading.textContent = 'Suggested Initial Tasks:';
        responseArea.appendChild(tasksHeading);

        // Formulario/Contenedor para las tareas
        const tasksFormContainer = document.createElement('div'); // Usar un div como contenedor
        tasksFormContainer.id = 'suggestedTasksForm';
        tasksFormContainer.style.marginBottom = '15px';

        data.suggested_tasks.forEach((taskDesc, index) => {
            const taskDiv = document.createElement('div');
            taskDiv.classList.add('form-check', 'mb-2');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.classList.add('form-check-input');
            checkbox.value = taskDesc;
            checkbox.id = `suggested_task_${index}`;
            checkbox.name = 'suggested_task';
            checkbox.checked = true; // Marcado por defecto
            taskDiv.appendChild(checkbox);

            const label = document.createElement('label');
            label.classList.add('form-check-label');
            label.htmlFor = checkbox.id;
            label.textContent = taskDesc;
            taskDiv.appendChild(label);

            tasksFormContainer.appendChild(taskDiv);
        });
        responseArea.appendChild(tasksFormContainer);

        // Botones de Acción
        const actionButtonsDiv = document.createElement('div');

        const confirmButton = document.createElement('button');
        confirmButton.id = 'confirmProjectCreationBtn';
        confirmButton.textContent = 'Confirm and Create Project';
        confirmButton.classList.add('btn', 'btn-primary', 'me-2'); // Cambiado a btn-primary
        confirmButton.dataset.projectData = JSON.stringify(data.project_data); // Incluye name, description, original_instruction
        confirmButton.addEventListener('click', handleProjectCreationConfirmation); // Attach event listener
        actionButtonsDiv.appendChild(confirmButton);

        const cancelButton = document.createElement('button');
        cancelButton.id = 'cancelProjectCreationBtn';
        cancelButton.textContent = 'Cancel';
        cancelButton.classList.add('btn', 'btn-secondary');
        cancelButton.addEventListener('click', () => {
            responseArea.innerHTML = '<p>Project creation cancelled. Waiting for new instruction...</p>';
            // Opcionalmente, re-habilitar el formulario de IA si se deshabilita durante la carga
            // instructionTextarea.disabled = false;
            // aiCommandForm.querySelector('button[type="submit"]').disabled = false;
        });
        actionButtonsDiv.appendChild(cancelButton);
        responseArea.appendChild(actionButtonsDiv);

        // donde handleProjectCreationConfirmation será una nueva función similar a handleExpenseConfirmation.
    }


    // Función para manejar respuestas exitosas generales
    function handleSuccessfulResponse(data, forceReload = false) {
        let htmlResponse = '';
        const isCreation = data.type === 'project_created' || data.type === 'task_created' || data.type === 'transaction_created';
        if (isCreation) {
            htmlResponse = `<p class="success"><strong>${data.message || 'Operación completada.'}</strong></p>`;
            if (data.project_id) htmlResponse += `<p>ID Proyecto: ${data.project_id}</p>`;
            if (data.task_id) htmlResponse += `<p>ID Tarea: ${data.task_id}</p>`;
            if (data.transaction_id) htmlResponse += `<p>ID Transacción: ${data.transaction_id}</p>`;
        } else { // Mensaje de texto simple de la IA u otra respuesta no-creación
            htmlResponse = `<p>${data.message || 'Respuesta recibida.'}</p>`;
        }
        responseArea.innerHTML = htmlResponse;
        if (isCreation || forceReload) { // Recargar siempre si es una creación o se fuerza
            responseArea.innerHTML += '<p class="loading">Actualizando página...</p>';
            setTimeout(() => { window.location.reload(); }, 1500);
        }
    }

}); // Fin del DOMContentLoaded listener