
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

function addIngrediente() {
    materia_prima = document.getElementById('ingrediente_input').value;
    cantidad = document.getElementById('cantidad_input').value;
    porcentaje_merma = document.getElementById('porcentaje_merma_input').value;
    unidad_medida = document.getElementById('unidad_medida_input').value;
    if(parseFloat(cantidad)<=0){
        Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Necesita cantidad ser mayor a 0'
        });
    }
    else if(parseFloat(porcentaje_merma)<=0){
        Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Necesita procentaje de merma necesita ser mayor a 0'
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

        ingredientes.push(nueva_materia_prima);
        document.getElementById('ingredientes').value = JSON.stringify(ingredientes);
        console.log(document.getElementById('ingredientes').value);
        loadIngredientes();
    }
}