
let ingredientes = [];

document.addEventListener('DOMContentLoaded', function () {

    if (document.getElementById('ingredientes').value != '') {
        ingredientes = JSON.parse(document.getElementById('ingredientes').value);
    }else{
        ingredientes = [];
    }

    console.log(document.getElementById('ingredientes').value);

    console.log(document.getElementById('ingredientes').value);
    loadIngredientes();
});

function loadIngredientes() {
    const tabla = document.getElementById('tblIngredientes');
    tabla.innerHTML = '';

    ingredientes.forEach(ingrediente => {
        const row = tabla.insertRow();

        row.insertCell(0).textContent = ingrediente.ingrediente_id;
        row.insertCell(1).textContent = ingrediente.ingrediente;
        row.insertCell(2).textContent = ingrediente.cantidad + ' ' + ingrediente.unidad_medida;
        row.insertCell(3).textContent = ingrediente.porcentaje_merma;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Eliminar';
        deleteButton.className = 'btn btn-danger';
        deleteButton.addEventListener('click', () => {
            eliminarIngrediente(ingrediente);
            document.getElementById('ingredientes').value = JSON.stringify(ingredientes);
        });
        row.insertCell(4).appendChild(deleteButton);
    });
}

function eliminarIngrediente(ingrediente) {
    const index = ingredientes.indexOf(ingrediente);
    if (index !== -1) {
        ingredientes.splice(index, 1);
        console.log(ingredientes);
        console.log(document.getElementById('ingredientes').value);
        loadIngredientes();
    }
}

async function addIngrediente() {
    materia_prima = document.getElementById('ingrediente_input').value;
    cantidad = document.getElementById('cantidad_input').value;
    porcentaje_merma = document.getElementById('porcentaje_merma_input').value;
    unidad_medida = document.getElementById('unidad_medida_input').value;

    if (parseFloat(cantidad) <= 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'La cantidad debe ser mayor a 0'
        });
    }
    else if (parseFloat(porcentaje_merma) <= 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El porcentaje de merma debe ser mayor a 0'
        });
    }
    else {
        let valores = materia_prima.slice(1, -1).split(',').map(value => value.trim());
        let id = parseInt(valores[0]);
        let nombre = valores[1].slice(1, -1);
        nueva_materia_prima = {
            'ingrediente_id': id,
            'ingrediente': nombre,
            'cantidad': cantidad,
            'unidad_medida': unidad_medida,
            'porcentaje_merma': parseFloat(porcentaje_merma)
        };
        if ((unidad_medida === 'kg' || unidad_medida === 'l') && parseFloat(cantidad) > 5) {
            const result = await Swal.fire({
                title: 'Alerta de cantidad',
                text: 'Parece demasiada cantidad para una receta, ¿Deseas agregarla a la lista?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, agregar',
                cancelButtonText: 'Cancelar'
            });

            if (result.isConfirmed) {
                ingredientes.push(nueva_materia_prima);
                document.getElementById('ingredientes').value = JSON.stringify(ingredientes);
                console.log(document.getElementById('ingredientes').value);
                loadIngredientes();
            }
        } else if ((unidad_medida === 'g' && cantidad >= 1000) || (unidad_medida === 'ml' && cantidad >= 1000)) {
            Swal.fire({
                icon: 'error',
                title: 'Cantidad incorrecta',
                text: 'Si la cantidad es mayor o igual a 1000, asegúrate de usar la medida KG o L respectivamente.'
            });
        } else if (porcentaje_merma >= 60 && porcentaje_merma < 100) {
            const result = await Swal.fire({
                title: 'Alerta de porcentaje de merma.',
                text: 'Parece demasiado porcentaje de merma para un ingrediente, ¿Deseas agregarla aún así?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, agregar',
                cancelButtonText: 'Cancelar'
            });

            if (result.isConfirmed) {
                ingredientes.push(nueva_materia_prima);
                document.getElementById('ingredientes').value = JSON.stringify(ingredientes);
                console.log(document.getElementById('ingredientes').value);
                loadIngredientes();
            }
        } else if(porcentaje_merma >= 100) {
            Swal.fire({
                icon: 'error',
                title: 'Porcentaje incorrecto.',
                text: 'No puedes poner un porcentaje de merma mayor o igual a 100.'
            });
        }
        else if (parseFloat(cantidad) >= 50 && unidad_medida == "pz") {
            const result = await Swal.fire({
                title: 'Alerta de cantidad de piezas.',
                text: 'Parece demasiada cantidad de piezas, ¿Deseas agregarla aún así?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, agregar',
                cancelButtonText: 'Cancelar'
            });

            if (result.isConfirmed) {
                ingredientes.push(nueva_materia_prima);
                document.getElementById('ingredientes').value = JSON.stringify(ingredientes);
                console.log(document.getElementById('ingredientes').value);
                loadIngredientes();
            }
        } else {
            ingredientes.push(nueva_materia_prima);
            document.getElementById('ingredientes').value = JSON.stringify(ingredientes);
            console.log(document.getElementById('ingredientes').value);
            loadIngredientes();
        }
    }
}
