const API_BASE = 'http://127.0.0.1:5000/api';

const app = {
    currentSection: 'alumnos',
    data: [],

    // Configuration for each section (Table columns and Form fields)
    config: {
        alumnos: {
            title: 'Alumnos',
            idField: 'id_alumno',
            columns: [
                { key: 'id_alumno', label: 'ID' },
                { key: 'matricula', label: 'Matrícula' },
                { key: 'nombres', label: 'Nombres' },
                { key: 'apellido_paterno', label: 'Ap. Paterno' },
                { key: 'id_grupo', label: 'ID Grupo' }
            ],
            fields: [
                { name: 'matricula', label: 'Matrícula', type: 'text', required: true, createOnly: true },
                { name: 'nombres', label: 'Nombres', type: 'text', required: true },
                { name: 'apellido_paterno', label: 'Ap. Paterno', type: 'text', required: true },
                { name: 'apellido_materno', label: 'Ap. Materno', type: 'text' },
                { name: 'curp', label: 'CURP', type: 'text', createOnly: true, minLength: 18, maxLength: 18 },
                { name: 'id_grupo', label: 'Grupo', type: 'select', source: 'grupos', required: true }
            ]
        },
        actividades: {
            title: 'Actividades Académicas',
            idField: 'id_actividad',
            columns: [
                { key: 'id_actividad', label: 'ID' },
                { key: 'titulo', label: 'Título' },
                { key: 'tipo_actividad', label: 'Tipo' },
                { key: 'porcentaje_valor', label: 'Valor (%)' },
                { key: 'id_materia', label: 'ID Materia' }
            ],
            fields: [
                { name: 'titulo', label: 'Título', type: 'text', required: true },
                { name: 'descripcion', label: 'Descripción', type: 'text' },
                { name: 'tipo_actividad', label: 'Tipo Actividad', type: 'text', required: true, createOnly: true },
                { name: 'porcentaje_valor', label: 'Valor (%)', type: 'number', required: true, min: 0, max: 100 },
                { name: 'id_periodo', label: 'ID Periodo', type: 'number', required: true, createOnly: true },
                { name: 'id_materia', label: 'ID Materia', type: 'number', required: true, createOnly: true },
                { name: 'id_grupo', label: 'Grupo', type: 'select', source: 'grupos', required: true, createOnly: true },
                { name: 'id_maestro', label: 'Maestro', type: 'select', source: 'maestros', required: true, createOnly: true }
            ]
        },
        calificaciones: {
            title: 'Calificaciones',
            idField: 'id_calificacion',
            columns: [
                { key: 'id_calificacion', label: 'ID' },
                { key: 'id_actividad', label: 'ID Actividad' },
                { key: 'id_alumno', label: 'ID Alumno' },
                { key: 'calificacion', label: 'Calificación' }
            ],
            fields: [
                { name: 'id_actividad', label: 'Actividad', type: 'select', source: 'actividades', required: true, createOnly: true },
                { name: 'id_alumno', label: 'Alumno', type: 'select', source: 'alumnos', required: true, createOnly: true },
                { name: 'calificacion', label: 'Calificación', type: 'number', step: '0.1', required: true, min: 0, max: 10 },
                { name: 'retroalimentacion', label: 'Retroalimentación', type: 'text' }
            ]
        },
        maestros: {
            title: 'Maestros',
            idField: 'id_maestro',
            columns: [
                { key: 'id_maestro', label: 'ID' },
                { key: 'nombre_completo', label: 'Nombre Completo' },
                { key: 'correo', label: 'Correo' }
            ],
            fields: [
                { name: 'nombre_completo', label: 'Nombre Completo', type: 'text', required: true },
                { name: 'correo', label: 'Correo', type: 'email', required: true },
                { name: 'password_hash', label: 'Contraseña', type: 'password', required: true, createOnly: true, minLength: 6 }
            ]
        },
        grupos: {
            title: 'Grupos',
            idField: 'id_grupo',
            columns: [
                { key: 'id_grupo', label: 'ID' },
                { key: 'grado', label: 'Grado' },
                { key: 'grupo', label: 'Grupo' },
                { key: 'ciclo_escolar', label: 'Ciclo' },
                { key: 'id_maestro_titular', label: 'Titular' }
            ],
            fields: [
                { name: 'grado', label: 'Grado', type: 'number', required: true, createOnly: true, min: 1, max: 6 },
                { name: 'grupo', label: 'Grupo', type: 'text', required: true, createOnly: true, maxLength: 2 },
                { name: 'ciclo_escolar', label: 'Ciclo Escolar', type: 'text', required: true, createOnly: true, placeholder: 'YYYY-YYYY', pattern: "\\d{4}-\\d{4}" },
                { name: 'id_maestro_titular', label: 'Maestro Titular', type: 'select', source: 'maestros', required: true }
            ]
        }
    },

    init: function() {
        this.navigate('alumnos');
        this.createModal();
    },

    navigate: function(section) {
        this.currentSection = section;
        document.getElementById('page-title').innerText = this.config[section].title;
        
        // Update active nav state
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('bg-slate-700');
            if(btn.innerText.toLowerCase().includes(section)) {
                btn.classList.add('bg-slate-700');
            }
        });

        this.fetchData();
    },

    fetchData: async function() {
        const content = document.getElementById('content-area');
        content.innerHTML = '<div class="text-center text-gray-500"><i class="fa-solid fa-spinner fa-spin text-2xl"></i><p>Cargando...</p></div>';
        
        try {
            const res = await fetch(`${API_BASE}/${this.currentSection}`);
            if (!res.ok) throw new Error('Error fetching data');
            this.data = await res.json();
            this.renderTable();
        } catch (err) {
            content.innerHTML = `<div class="text-red-500">Error: ${err.message}</div>`;
        }
    },

    renderTable: function() {
        const conf = this.config[this.currentSection];
        const content = document.getElementById('content-area');
        
        if (this.data.length === 0) {
            content.innerHTML = '<div class="text-center text-gray-500 p-10">No hay registros encontrados.</div>';
            return;
        }

        let html = `
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-slate-50">
                        <tr>
                            ${conf.columns.map(col => `<th class="p-4 border-b font-semibold text-gray-600">${col.label}</th>`).join('')}
                            <th class="p-4 border-b font-semibold text-gray-600 text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        this.data.forEach(item => {
            html += `<tr class="hover:bg-slate-50 transition">`;
            conf.columns.forEach(col => {
                html += `<td class="p-4 border-b text-gray-700">${item[col.key] !== undefined ? item[col.key] : '-'}</td>`;
            });
            html += `
                <td class="p-4 border-b text-right space-x-2">
                    <button onclick="app.editItem(${item[conf.idField]})" class="text-blue-600 hover:text-blue-800" title="Editar">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </button>
                    <button onclick="app.deleteItem(${item[conf.idField]})" class="text-red-600 hover:text-red-800" title="Eliminar">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>
            </tr>`;
        });

        html += `</tbody></table></div>`;
        content.innerHTML = html;
    },

    // --- CRUD Operations ---

    deleteItem: async function(id) {
        if(!confirm('¿Estás seguro de eliminar este registro?')) return;
        
        try {
            const res = await fetch(`${API_BASE}/${this.currentSection}/${id}`, { method: 'DELETE' });
            if(res.ok) {
                this.fetchData();
            } else {
                alert('Error al eliminar');
            }
        } catch(e) {
            console.error(e);
            alert('Error de conexión');
        }
    },

    saveItem: async function(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const payload = {};
        
        // Convert FormData to JSON object, handling numbers
        formData.forEach((value, key) => {
            // Simple heuristic: if it looks like a number, parse it. 
            // In a real app, check the config type.
            if (!isNaN(value) && value !== '') {
                payload[key] = Number(value);
            } else {
                payload[key] = value;
            }
        });

        const id = form.dataset.id;
        const method = id ? 'PUT' : 'POST';
        const url = id ? `${API_BASE}/${this.currentSection}/${id}` : `${API_BASE}/${this.currentSection}`;

        try {
            const res = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if(res.ok) {
                this.closeModal();
                this.fetchData();
            } else {
                const err = await res.json();
                alert('Error: ' + (err.error || 'No se pudo guardar'));
            }
        } catch(e) {
            console.error(e);
            alert('Error de conexión');
        }
    },

    // --- Modal & Form Handling ---

    createModal: function() {
        const modalHtml = `
            <div id="modal-overlay" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center backdrop-blur-sm">
                <div class="bg-white rounded-lg shadow-xl w-full max-w-lg transform transition-all scale-95 opacity-0" id="modal-content">
                    <div class="flex justify-between items-center p-5 border-b">
                        <h3 class="text-xl font-bold text-gray-800" id="modal-title">Nuevo Registro</h3>
                        <button onclick="app.closeModal()" class="text-gray-400 hover:text-gray-600">
                            <i class="fa-solid fa-times text-xl"></i>
                        </button>
                    </div>
                    <form id="crud-form" class="p-6 space-y-4">
                        <div id="form-fields" class="grid grid-cols-1 gap-4"></div>
                        <div class="flex justify-end gap-3 pt-4">
                            <button type="button" onclick="app.closeModal()" class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition">Cancelar</button>
                            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition shadow">Guardar</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        document.getElementById('crud-form').addEventListener('submit', (e) => this.saveItem(e));
    },

    openModal: async function(data = null) {
        const conf = this.config[this.currentSection];
        const overlay = document.getElementById('modal-overlay');
        const content = document.getElementById('modal-content');
        const form = document.getElementById('crud-form');
        const fieldsContainer = document.getElementById('form-fields');
        const title = document.getElementById('modal-title');

        // Reset form
        form.reset();
        fieldsContainer.innerHTML = '';
        delete form.dataset.id;

        title.innerText = data ? `Editar ${conf.title.slice(0, -1)}` : `Nuevo ${conf.title.slice(0, -1)}`;
        if (data) form.dataset.id = data[conf.idField];

        // Generate fields
        for (const field of conf.fields) {
            if (data && field.createOnly) continue;

            const div = document.createElement('div');
            div.className = 'flex flex-col';
            
            const label = document.createElement('label');
            label.className = 'text-sm font-medium text-gray-700 mb-1';
            label.innerText = field.label;
            
            let input;

            if (field.type === 'select') {
                input = document.createElement('select');
                input.className = 'border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white';
                input.name = field.name;
                if (field.required) input.required = true;

                try {
                    const res = await fetch(`${API_BASE}/${field.source}`);
                    if (res.ok) {
                        const options = await res.json();
                        const defaultOpt = document.createElement('option');
                        defaultOpt.value = '';
                        defaultOpt.innerText = 'Seleccione...';
                        input.appendChild(defaultOpt);

                        options.forEach(opt => {
                            const option = document.createElement('option');
                            if (field.source === 'grupos') {
                                option.value = opt.id_grupo;
                                option.innerText = `${opt.grado}° ${opt.grupo} (${opt.ciclo_escolar})`;
                            } else if (field.source === 'maestros') {
                                option.value = opt.id_maestro;
                                option.innerText = opt.nombre_completo;
                            } else if (field.source === 'alumnos') {
                                option.value = opt.id_alumno;
                                option.innerText = `${opt.matricula} - ${opt.nombres} ${opt.apellido_paterno}`;
                            } else if (field.source === 'actividades') {
                                option.value = opt.id_actividad;
                                option.innerText = opt.titulo;
                            } else {
                                option.value = opt.id;
                                option.innerText = opt.nombre || 'Opción';
                            }
                            input.appendChild(option);
                        });
                    }
                } catch (e) {
                    console.error('Error fetching options', e);
                }
            } else {
                input = document.createElement('input');
                input.className = 'border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent';
                input.name = field.name;
                input.type = field.type;
                if (field.required) input.required = true;
                if (field.step) input.step = field.step;
                if (field.min !== undefined) input.min = field.min;
                if (field.max !== undefined) input.max = field.max;
                if (field.minLength) input.minLength = field.minLength;
                if (field.maxLength) input.maxLength = field.maxLength;
                if (field.pattern) input.pattern = field.pattern;
                if (field.placeholder) input.placeholder = field.placeholder;
            }

            if (data && data[field.name] !== undefined) {
                input.value = data[field.name];
            }

            div.appendChild(label);
            div.appendChild(input);
            fieldsContainer.appendChild(div);
        }

        // Show modal with animation
        overlay.classList.remove('hidden');
        // Small delay to allow display:block to apply before opacity transition
        setTimeout(() => {
            content.classList.remove('scale-95', 'opacity-0');
            content.classList.add('scale-100', 'opacity-100');
        }, 10);
    },

    closeModal: function() {
        const overlay = document.getElementById('modal-overlay');
        const content = document.getElementById('modal-content');
        
        content.classList.remove('scale-100', 'opacity-100');
        content.classList.add('scale-95', 'opacity-0');
        
        setTimeout(() => {
            overlay.classList.add('hidden');
        }, 200);
    },

    editItem: function(id) {
        const conf = this.config[this.currentSection];
        const item = this.data.find(d => d[conf.idField] === id);
        if(item) {
            this.openModal(item);
        }
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
