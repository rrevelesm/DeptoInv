// API Base URL
const API_URL = 'http://localhost:5000/api';

// Estado global
let currentTab = 'investigadores';
let investigadores = [];
let proyectos = [];
let publicaciones = [];
let sniiList = [];

// ============== Funciones de Inicialización ==============

document.addEventListener('DOMContentLoaded', () => {
    loadEstadisticas();
    loadInvestigadores();
    setupSearchFilters();
});

// ============== Gestión de Tabs ==============

function showTab(tabName) {
    // Ocultar todos los tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remover clase active de todos los botones
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostrar el tab seleccionado
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    currentTab = tabName;
    
    // Cargar datos según el tab
    switch(tabName) {
        case 'investigadores':
            loadInvestigadores();
            break;
        case 'proyectos':
            loadProyectos();
            break;
        case 'publicaciones':
            loadPublicaciones();
            break;
        case 'snii':
            loadSNII();
            break;
    }
}

// ============== Gestión de Modales ==============

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('active');
    
    // Limpiar formulario si es nuevo registro
    if (modalId === 'investigadorModal' && !document.getElementById('investigadorId').value) {
        document.getElementById('investigadorForm').reset();
    } else if (modalId === 'proyectoModal' && !document.getElementById('proyectoId').value) {
        document.getElementById('proyectoForm').reset();
    } else if (modalId === 'publicacionModal' && !document.getElementById('publicacionId').value) {
        document.getElementById('publicacionForm').reset();
    } else if (modalId === 'sniiModal') {
        loadInvestigadoresForSelect();
        if (!document.getElementById('sniiId').value) {
            document.getElementById('sniiForm').reset();
        }
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    
    // Limpiar formularios
    const forms = {
        'investigadorModal': 'investigadorForm',
        'proyectoModal': 'proyectoForm',
        'publicacionModal': 'publicacionForm',
        'sniiModal': 'sniiForm'
    };
    
    if (forms[modalId]) {
        document.getElementById(forms[modalId]).reset();
        if (modalId === 'investigadorModal') document.getElementById('investigadorId').value = '';
        if (modalId === 'proyectoModal') document.getElementById('proyectoId').value = '';
        if (modalId === 'publicacionModal') document.getElementById('publicacionId').value = '';
        if (modalId === 'sniiModal') document.getElementById('sniiId').value = '';
    }
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}

// ============== Notificaciones ==============

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ============== Estadísticas ==============

async function loadEstadisticas() {
    try {
        const response = await fetch(`${API_URL}/estadisticas`);
        const stats = await response.json();
        
        document.getElementById('totalInvestigadores').textContent = stats.total_investigadores;
        document.getElementById('totalProyectos').textContent = stats.total_proyectos;
        document.getElementById('totalPublicaciones').textContent = stats.total_publicaciones;
        document.getElementById('sniiVigentes').textContent = stats.snii_vigentes;
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
}

// ============== INVESTIGADORES ==============

async function loadInvestigadores() {
    try {
        const response = await fetch(`${API_URL}/investigadores`);
        investigadores = await response.json();
        displayInvestigadores(investigadores);
    } catch (error) {
        console.error('Error al cargar investigadores:', error);
        showToast('Error al cargar investigadores', 'error');
    }
}

function displayInvestigadores(data) {
    const tbody = document.getElementById('investigadoresTableBody');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><div class="empty-state-icon">📭</div><div class="empty-state-text">No hay investigadores registrados</div></td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(inv => `
        <tr>
            <td>${inv.id}</td>
            <td>${inv.nombre_completo}</td>
            <td>${inv.email}</td>
            <td>${inv.especialidad || '-'}</td>
            <td>${inv.grado_academico || '-'}</td>
            <td><span class="badge badge-${getStatusClass(inv.estatus)}">${inv.estatus}</span></td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-primary btn-sm" onclick="editInvestigador(${inv.id})">✏️</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteInvestigador(${inv.id})">🗑️</button>
                </div>
            </td>
        </tr>
    `).join('');
}

async function submitInvestigador(event) {
    event.preventDefault();
    
    const id = document.getElementById('investigadorId').value;
    const data = {
        nombre: document.getElementById('nombre').value,
        apellido_paterno: document.getElementById('apellidoPaterno').value,
        apellido_materno: document.getElementById('apellidoMaterno').value,
        email: document.getElementById('email').value,
        telefono: document.getElementById('telefono').value,
        especialidad: document.getElementById('especialidad').value,
        grado_academico: document.getElementById('gradoAcademico').value,
        institucion: document.getElementById('institucion').value,
        departamento: document.getElementById('departamento').value,
        fecha_ingreso: document.getElementById('fechaIngreso').value,
        estatus: document.getElementById('estatus').value
    };
    
    try {
        const url = id ? `${API_URL}/investigadores/${id}` : `${API_URL}/investigadores`;
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast(id ? 'Investigador actualizado' : 'Investigador creado', 'success');
            closeModal('investigadorModal');
            loadInvestigadores();
            loadEstadisticas();
        } else {
            throw new Error('Error en la operación');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al guardar investigador', 'error');
    }
}

async function editInvestigador(id) {
    try {
        const response = await fetch(`${API_URL}/investigadores/${id}`);
        const inv = await response.json();
        
        document.getElementById('investigadorId').value = inv.id;
        document.getElementById('nombre').value = inv.nombre;
        document.getElementById('apellidoPaterno').value = inv.apellido_paterno;
        document.getElementById('apellidoMaterno').value = inv.apellido_materno || '';
        document.getElementById('email').value = inv.email;
        document.getElementById('telefono').value = inv.telefono || '';
        document.getElementById('especialidad').value = inv.especialidad || '';
        document.getElementById('gradoAcademico').value = inv.grado_academico || '';
        document.getElementById('institucion').value = inv.institucion || '';
        document.getElementById('departamento').value = inv.departamento || '';
        document.getElementById('fechaIngreso').value = inv.fecha_ingreso || '';
        document.getElementById('estatus').value = inv.estatus || 'Activo';
        
        document.getElementById('investigadorModalTitle').textContent = 'Editar Investigador';
        showModal('investigadorModal');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar datos del investigador', 'error');
    }
}

async function deleteInvestigador(id) {
    if (!confirm('¿Estás seguro de eliminar este investigador?')) return;
    
    try {
        const response = await fetch(`${API_URL}/investigadores/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Investigador eliminado', 'success');
            loadInvestigadores();
            loadEstadisticas();
        } else {
            throw new Error('Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al eliminar investigador', 'error');
    }
}

// ============== PROYECTOS ==============

async function loadProyectos() {
    try {
        const response = await fetch(`${API_URL}/proyectos`);
        proyectos = await response.json();
        displayProyectos(proyectos);
    } catch (error) {
        console.error('Error al cargar proyectos:', error);
        showToast('Error al cargar proyectos', 'error');
    }
}

function displayProyectos(data) {
    const tbody = document.getElementById('proyectosTableBody');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="empty-state"><div class="empty-state-icon">📭</div><div class="empty-state-text">No hay proyectos registrados</div></td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(proy => `
        <tr>
            <td>${proy.id}</td>
            <td>${proy.clave_sip || '-'}</td>
            <td>${proy.titulo}</td>
            <td>${proy.responsable_nombre || '-'}</td>
            <td>${proy.tipo || '-'}</td>
            <td>${proy.fuente_financiamiento || '-'}</td>
            <td>${proy.monto ? '$' + proy.monto.toLocaleString() : '-'}</td>
            <td>${proy.fecha_inicio || '-'}</td>
            <td><span class="badge badge-${getStatusClass(proy.estatus)}">${proy.estatus}</span></td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-primary btn-sm" onclick="editProyecto(${proy.id})">✏️</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteProyecto(${proy.id})">🗑️</button>
                </div>
            </td>
        </tr>
    `).join('');
}

async function submitProyecto(event) {
    event.preventDefault();
    
    const id = document.getElementById('proyectoId').value;
    const data = {
        clave_sip: document.getElementById('proyectoClaveSip').value,
        titulo: document.getElementById('proyectoTitulo').value,
        descripcion: document.getElementById('proyectoDescripcion').value,
        tipo: document.getElementById('proyectoTipo').value,
        fuente_financiamiento: document.getElementById('proyectoFinanciamiento').value,
        monto: parseFloat(document.getElementById('proyectoMonto').value) || null,
        fecha_inicio: document.getElementById('proyectoFechaInicio').value,
        fecha_fin: document.getElementById('proyectoFechaFin').value,
        estatus: document.getElementById('proyectoEstatus').value
    };
    
    try {
        const url = id ? `${API_URL}/proyectos/${id}` : `${API_URL}/proyectos`;
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast(id ? 'Proyecto actualizado' : 'Proyecto creado', 'success');
            closeModal('proyectoModal');
            loadProyectos();
            loadEstadisticas();
        } else {
            throw new Error('Error en la operación');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al guardar proyecto', 'error');
    }
}

async function editProyecto(id) {
    try {
        const response = await fetch(`${API_URL}/proyectos/${id}`);
        const proy = await response.json();
        
        document.getElementById('proyectoId').value = proy.id;
        document.getElementById('proyectoClaveSip').value = proy.clave_sip || '';
        document.getElementById('proyectoTitulo').value = proy.titulo;
        document.getElementById('proyectoDescripcion').value = proy.descripcion || '';
        document.getElementById('proyectoTipo').value = proy.tipo || '';
        document.getElementById('proyectoFinanciamiento').value = proy.fuente_financiamiento || '';
        document.getElementById('proyectoMonto').value = proy.monto || '';
        document.getElementById('proyectoFechaInicio').value = proy.fecha_inicio || '';
        document.getElementById('proyectoFechaFin').value = proy.fecha_fin || '';
        document.getElementById('proyectoEstatus').value = proy.estatus || 'En curso';
        
        document.getElementById('proyectoModalTitle').textContent = 'Editar Proyecto';
        showModal('proyectoModal');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar datos del proyecto', 'error');
    }
}

async function deleteProyecto(id) {
    if (!confirm('¿Estás seguro de eliminar este proyecto?')) return;
    
    try {
        const response = await fetch(`${API_URL}/proyectos/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Proyecto eliminado', 'success');
            loadProyectos();
            loadEstadisticas();
        } else {
            throw new Error('Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al eliminar proyecto', 'error');
    }
}

// ============== PUBLICACIONES ==============

async function loadPublicaciones() {
    try {
        const response = await fetch(`${API_URL}/publicaciones`);
        publicaciones = await response.json();
        displayPublicaciones(publicaciones);
    } catch (error) {
        console.error('Error al cargar publicaciones:', error);
        showToast('Error al cargar publicaciones', 'error');
    }
}

function displayPublicaciones(data) {
    const tbody = document.getElementById('publicacionesTableBody');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><div class="empty-state-icon">📭</div><div class="empty-state-text">No hay publicaciones registradas</div></td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(pub => `
        <tr>
            <td>${pub.id}</td>
            <td>${pub.titulo}</td>
            <td>${pub.tipo || '-'}</td>
            <td>${pub.revista_editorial || '-'}</td>
            <td>${pub.anio || '-'}</td>
            <td>${pub.indexada || '-'}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-primary btn-sm" onclick="editPublicacion(${pub.id})">✏️</button>
                    <button class="btn btn-danger btn-sm" onclick="deletePublicacion(${pub.id})">🗑️</button>
                </div>
            </td>
        </tr>
    `).join('');
}

async function submitPublicacion(event) {
    event.preventDefault();
    
    const id = document.getElementById('publicacionId').value;
    const data = {
        titulo: document.getElementById('publicacionTitulo').value,
        tipo: document.getElementById('publicacionTipo').value,
        revista_editorial: document.getElementById('publicacionRevista').value,
        anio: parseInt(document.getElementById('publicacionAnio').value) || null,
        volumen: document.getElementById('publicacionVolumen').value,
        paginas: document.getElementById('publicacionPaginas').value,
        doi: document.getElementById('publicacionDOI').value,
        issn_isbn: document.getElementById('publicacionISSN').value,
        url: document.getElementById('publicacionURL').value,
        resumen: document.getElementById('publicacionResumen').value,
        palabras_clave: document.getElementById('publicacionPalabras').value,
        indexada: document.getElementById('publicacionIndexada').value,
        factor_impacto: parseFloat(document.getElementById('publicacionFactorImpacto').value) || null
    };
    
    try {
        const url = id ? `${API_URL}/publicaciones/${id}` : `${API_URL}/publicaciones`;
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast(id ? 'Publicación actualizada' : 'Publicación creada', 'success');
            closeModal('publicacionModal');
            loadPublicaciones();
            loadEstadisticas();
        } else {
            throw new Error('Error en la operación');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al guardar publicación', 'error');
    }
}

async function editPublicacion(id) {
    try {
        const response = await fetch(`${API_URL}/publicaciones/${id}`);
        const pub = await response.json();
        
        document.getElementById('publicacionId').value = pub.id;
        document.getElementById('publicacionTitulo').value = pub.titulo;
        document.getElementById('publicacionTipo').value = pub.tipo || '';
        document.getElementById('publicacionRevista').value = pub.revista_editorial || '';
        document.getElementById('publicacionAnio').value = pub.anio || '';
        document.getElementById('publicacionVolumen').value = pub.volumen || '';
        document.getElementById('publicacionPaginas').value = pub.paginas || '';
        document.getElementById('publicacionDOI').value = pub.doi || '';
        document.getElementById('publicacionISSN').value = pub.issn_isbn || '';
        document.getElementById('publicacionURL').value = pub.url || '';
        document.getElementById('publicacionResumen').value = pub.resumen || '';
        document.getElementById('publicacionPalabras').value = pub.palabras_clave || '';
        document.getElementById('publicacionIndexada').value = pub.indexada || '';
        document.getElementById('publicacionFactorImpacto').value = pub.factor_impacto || '';
        
        document.getElementById('publicacionModalTitle').textContent = 'Editar Publicación';
        showModal('publicacionModal');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar datos de la publicación', 'error');
    }
}

async function deletePublicacion(id) {
    if (!confirm('¿Estás seguro de eliminar esta publicación?')) return;
    
    try {
        const response = await fetch(`${API_URL}/publicaciones/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Publicación eliminada', 'success');
            loadPublicaciones();
            loadEstadisticas();
        } else {
            throw new Error('Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al eliminar publicación', 'error');
    }
}

// ============== SNII ==============

async function loadSNII() {
    try {
        const response = await fetch(`${API_URL}/snii`);
        sniiList = await response.json();
        displaySNII(sniiList);
    } catch (error) {
        console.error('Error al cargar SNII:', error);
        showToast('Error al cargar registros SNII', 'error');
    }
}

function displaySNII(data) {
    const tbody = document.getElementById('sniiTableBody');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="empty-state"><div class="empty-state-icon">📭</div><div class="empty-state-text">No hay registros SNII</div></td></tr>';
        return;
    }
    
    tbody.innerHTML = data.map(snii => `
        <tr>
            <td>${snii.id}</td>
            <td>${snii.investigador?.nombre_completo || '-'}</td>
            <td><span class="badge badge-info">${snii.nivel}</span></td>
            <td>${snii.area_conocimiento || '-'}</td>
            <td>${snii.fecha_ingreso || '-'}</td>
            <td>${snii.fecha_vigencia || '-'}</td>
            <td><span class="badge badge-${getStatusClass(snii.estatus)}">${snii.estatus}</span></td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-primary btn-sm" onclick="editSNII(${snii.id})">✏️</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteSNII(${snii.id})">🗑️</button>
                </div>
            </td>
        </tr>
    `).join('');
}

async function loadInvestigadoresForSelect() {
    try {
        const response = await fetch(`${API_URL}/investigadores`);
        const invs = await response.json();
        
        const select = document.getElementById('sniiInvestigador');
        select.innerHTML = '<option value="">Seleccionar investigador...</option>' +
            invs.map(inv => `<option value="${inv.id}">${inv.nombre_completo}</option>`).join('');
    } catch (error) {
        console.error('Error:', error);
    }
}

async function submitSNII(event) {
    event.preventDefault();
    
    const id = document.getElementById('sniiId').value;
    const data = {
        investigador_id: parseInt(document.getElementById('sniiInvestigador').value),
        nivel: document.getElementById('sniiNivel').value,
        fecha_ingreso: document.getElementById('sniiFechaIngreso').value,
        fecha_vigencia: document.getElementById('sniiFechaVigencia').value,
        estatus: document.getElementById('sniiEstatus').value,
        numero_registro: document.getElementById('sniiNumeroRegistro').value,
        area_conocimiento: document.getElementById('sniiArea').value
    };
    
    try {
        const url = id ? `${API_URL}/snii/${id}` : `${API_URL}/snii`;
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast(id ? 'Registro SNII actualizado' : 'Registro SNII creado', 'success');
            closeModal('sniiModal');
            loadSNII();
            loadEstadisticas();
        } else {
            throw new Error('Error en la operación');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al guardar registro SNII', 'error');
    }
}

async function editSNII(id) {
    try {
        const response = await fetch(`${API_URL}/snii/${id}`);
        const snii = await response.json();
        
        await loadInvestigadoresForSelect();
        
        document.getElementById('sniiId').value = snii.id;
        document.getElementById('sniiInvestigador').value = snii.investigador_id;
        document.getElementById('sniiNivel').value = snii.nivel || '';
        document.getElementById('sniiFechaIngreso').value = snii.fecha_ingreso || '';
        document.getElementById('sniiFechaVigencia').value = snii.fecha_vigencia || '';
        document.getElementById('sniiEstatus').value = snii.estatus || 'Vigente';
        document.getElementById('sniiNumeroRegistro').value = snii.numero_registro || '';
        document.getElementById('sniiArea').value = snii.area_conocimiento || '';
        
        document.getElementById('sniiModalTitle').textContent = 'Editar Registro SNII';
        showModal('sniiModal');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar datos del registro SNII', 'error');
    }
}

async function deleteSNII(id) {
    if (!confirm('¿Estás seguro de eliminar este registro SNII?')) return;
    
    try {
        const response = await fetch(`${API_URL}/snii/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Registro SNII eliminado', 'success');
            loadSNII();
            loadEstadisticas();
        } else {
            throw new Error('Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al eliminar registro SNII', 'error');
    }
}

// ============== Utilidades ==============

function getStatusClass(status) {
    const statusMap = {
        'Activo': 'success',
        'En curso': 'success',
        'Vigente': 'success',
        'Finalizado': 'info',
        'Inactivo': 'warning',
        'Vencido': 'warning',
        'Planeado': 'info',
        'Jubilado': 'danger',
        'Cancelado': 'danger',
        'En evaluación': 'warning'
    };
    return statusMap[status] || 'info';
}

// ============== Búsqueda y Filtros ==============

function setupSearchFilters() {
    document.getElementById('searchInvestigadores').addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = investigadores.filter(inv => 
            inv.nombre_completo.toLowerCase().includes(searchTerm) ||
            inv.email.toLowerCase().includes(searchTerm) ||
            (inv.especialidad && inv.especialidad.toLowerCase().includes(searchTerm))
        );
        displayInvestigadores(filtered);
    });
    
    document.getElementById('searchProyectos').addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = proyectos.filter(proy => 
            proy.titulo.toLowerCase().includes(searchTerm) ||
            (proy.descripcion && proy.descripcion.toLowerCase().includes(searchTerm))
        );
        displayProyectos(filtered);
    });
    
    document.getElementById('searchPublicaciones').addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = publicaciones.filter(pub => 
            pub.titulo.toLowerCase().includes(searchTerm) ||
            (pub.revista_editorial && pub.revista_editorial.toLowerCase().includes(searchTerm))
        );
        displayPublicaciones(filtered);
    });
    
    document.getElementById('searchSNII').addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = sniiList.filter(snii => 
            (snii.investigador && snii.investigador.nombre_completo.toLowerCase().includes(searchTerm)) ||
            (snii.nivel && snii.nivel.toLowerCase().includes(searchTerm))
        );
        displaySNII(filtered);
    });
}


