document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('searchInput1');
    const userTable = document.getElementById('solicitudesTable');
    const rows = userTable.getElementsByTagName('tr');

    searchInput.addEventListener('input', function() {
      const searchText = this.value.toLowerCase();
      for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;
        for (let j = 0; j < cells.length; j++) {
          const cell = cells[j];
          if (cell.textContent.toLowerCase().indexOf(searchText) > -1) {
            found = true;
            break;
          }
        }
        if (found) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      }
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('searchInput2');
    const userTable = document.getElementById('procesoTable');
    const rows = userTable.getElementsByTagName('tr');

    searchInput.addEventListener('input', function() {
      const searchText = this.value.toLowerCase();
      for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;
        for (let j = 0; j < cells.length; j++) {
          const cell = cells[j];
          if (cell.textContent.toLowerCase().indexOf(searchText) > -1) {
            found = true;
            break;
          }
        }
        if (found) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      }
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('searchInput3');
    const userTable = document.getElementById('postergadasTable');
    const rows = userTable.getElementsByTagName('tr');

    searchInput.addEventListener('input', function() {
      const searchText = this.value.toLowerCase();
      for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;
        for (let j = 0; j < cells.length; j++) {
          const cell = cells[j];
          if (cell.textContent.toLowerCase().indexOf(searchText) > -1) {
            found = true;
            break;
          }
        }
        if (found) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      }
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('searchInput4');
    const userTable = document.getElementById('canceladasTable');
    const rows = userTable.getElementsByTagName('tr');

    searchInput.addEventListener('input', function() {
      const searchText = this.value.toLowerCase();
      for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;
        for (let j = 0; j < cells.length; j++) {
          const cell = cells[j];
          if (cell.textContent.toLowerCase().indexOf(searchText) > -1) {
            found = true;
            break;
          }
        }
        if (found) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      }
    });
  });


  function gestionarProcesar() {
    let modalProcesar = document.getElementById("modalProcesar");
    let btnProcesar = document.getElementById("procesarBtn");
    let confirmarProcesarBtn = document.getElementById("confirmarBtnProcesar");
    let cancelarProcesarBtn = document.getElementById("cancelarBtnProcesar");
    let spanProcesar = document.getElementsByClassName("closeProcesar")[0];

    function mostrarModalProcesar() {
        modalProcesar.style.display = "block";
    }

    function cerrarModalProcesar() {
        modalProcesar.style.display = "none";
    }

    btnProcesar.onclick = function () {
        mostrarModalProcesar();
    }

    spanProcesar.onclick = function () {
        cerrarModalProcesar();
    }

    cancelarProcesarBtn.onclick = function () {
        cerrarModalProcesar();
    }

    function confirmarProcesamiento() {
        let form = document.getElementById("formProcesar");
        form.submit();
        cerrarModalProcesar();
    }

    confirmarProcesarBtn.onclick = function () {
        confirmarProcesamiento();
    }
}



//fin de seccion de procesar --------------------------------------------------

function gestionarCancelarSolicitud() {
    let modalCancelarSolicitud = document.getElementById("modalCancelarSolicitud");
    let btnCancelarSolicitud = document.getElementById("cancelarSolicitudBtn");
    let confirmarCancelarSolicitudBtn = document.getElementById("confirmarBtnCancelarSolicitud");
    let cancelarCancelarSolicitudBtn = document.getElementById("cancelarBtnCancelarSolicitud");
    let spanCancelarSolicitud = document.getElementsByClassName("closeCancelarSolicitud")[0];

    function mostrarModalCancelarSolicitud() {
        modalCancelarSolicitud.style.display = "block";
    }

    function cerrarModalCancelarSolicitud() {
        modalCancelarSolicitud.style.display = "none";
    }

    btnCancelarSolicitud.onclick = function () {
        mostrarModalCancelarSolicitud();
    }

    spanCancelarSolicitud.onclick = function () {
        cerrarModalCancelarSolicitud();
    }

    cancelarCancelarSolicitudBtn.onclick = function () {
        cerrarModalCancelarSolicitud();
    }

    function confirmarCancelacionSolicitud() {
        let form = document.getElementById("formCancelarSolicitud");
        form.submit();
        cerrarModalCancelarSolicitud();
    }

    confirmarCancelarSolicitudBtn.onclick = function () {
        confirmarCancelacionSolicitud();
    }
}




//fin de seccion Cancelar solicitud------------------------------------------------
function gestionarPostergarSolicitud() {
    let modalPostergarSolicitud = document.getElementById("modalPostergarSolicitud");
    let btnPostergarSolicitud = document.getElementById("postergarSolicitudBtn");
    let confirmarPostergarSolicitudBtn = document.getElementById("confirmarBtnPostergarSolicitud");
    let cancelarPostergarSolicitudBtn = document.getElementById("cancelarBtnPostergarSolicitud");
    let spanPostergarSolicitud = document.getElementsByClassName("closePostergarSolicitud")[0];

    function mostrarModalPostergar() {
        modalPostergarSolicitud.style.display = "block";
    }

    function cerrarModalPostergar() {
        modalPostergarSolicitud.style.display = "none";
    }

    btnPostergarSolicitud.onclick = function () {
        mostrarModalPostergar();
    }

    spanPostergarSolicitud.onclick = function () {
        cerrarModalPostergar();
    }

    cancelarPostergarSolicitudBtn.onclick = function () {
        cerrarModalPostergar();
    }

    function confirmarPostergacion() {
        let form = document.getElementById("formPostergarSolicitud");
        form.submit();
        cerrarModalPostergar();
    }

    confirmarPostergarSolicitudBtn.onclick = function () {
        confirmarPostergacion();
    }
}



//fin de seccion postergar solicitud------------------------------------------------

function gestionarTerminarProduccion() {
    let modalTerminarProduccion = document.getElementById("modalTerminarProduccion");
    let btnTerminarProduccion = document.getElementById("terminarProduccionBtn");
    let confirmarTerminarProduccionBtn = document.getElementById("confirmarBtnTerminarProduccion");
    let cancelarTerminarProduccionBtn = document.getElementById("cancelarBtnTerminarProduccion");
    let spanTerminarProduccion = document.getElementsByClassName("closeTerminarProduccion")[0];

    function mostrarModalTerminarProduccion() {
        modalTerminarProduccion.style.display = "block";
    }

    function cerrarModalTerminarProduccion() {
        modalTerminarProduccion.style.display = "none";
    }

    btnTerminarProduccion.onclick = function () {
        mostrarModalTerminarProduccion();
    }

    spanTerminarProduccion.onclick = function () {
        cerrarModalTerminarProduccion();
    }

    cancelarTerminarProduccionBtn.onclick = function () {
        cerrarModalTerminarProduccion();
    }

    function confirmarTerminar() {
        let form = document.getElementById("formTerminarProduccion");
        form.submit();
        cerrarModalTerminarProduccion();
    }

    confirmarTerminarProduccionBtn.onclick = function () {
        confirmarTerminar();
    }
}



//fin de seccion Terminar produccion------------------------------------------------

function gestionarCancelarProduccion() {
    let modalCancelarProduccion = document.getElementById("modalCancelarProduccion");
    let btnCancelarProduccion = document.getElementById("cancelarProduccionBtn");
    let confirmarCancelarProduccionBtn = document.getElementById("confirmarBtnCancelarProduccion");
    let cancelarCancelarProduccionBtn = document.getElementById("cancelarBtnCancelarProduccion");
    let spanCancelarProduccion = document.getElementsByClassName("closeCancelarProduccion")[0];

    function mostrarModalCancelarProduccion() {
        modalCancelarProduccion.style.display = "block";
    }

    function cerrarModalCancelarProduccion() {
        modalCancelarProduccion.style.display = "none";
    }

    btnCancelarProduccion.onclick = function () {
        mostrarModalCancelarProduccion();
    }

    spanCancelarProduccion.onclick = function () {
        cerrarModalCancelarProduccion();
    }

    cancelarCancelarProduccionBtn.onclick = function () {
        cerrarModalCancelarProduccion();
    }

    function confirmarCancelacionProduccion() {
        let form = document.getElementById("formCancelarProduccion");
        form.submit();
        cerrarModalCancelarProduccion();
    }

    confirmarCancelarProduccionBtn.onclick = function () {
        confirmarCancelacionProduccion();
    }
}




//fin de seccion cancelar produccion------------------------------------------------  

function gestionarProduccionPostergada() {
    let modalProdPostergar = document.getElementById("modalProcesarProduccionPostergada");
    let btnProdPostergar = document.getElementById("prodPostergarBtn");
    let confirmarProdPostergarBtn = document.getElementById("confirmarBtnProducirPostergada");
    let cancelarProdPostergarBtn = document.getElementById("cancelarBtnProducirPostergada");
    let spanProdPostergar = document.getElementsByClassName("closeProcesarPostergada")[0];

    function mostrarModalProdPostergar() {
        modalProdPostergar.style.display = "block";
    }

    function cerrarModalProdPostergar() {
        modalProdPostergar.style.display = "none";
    }

    btnProdPostergar.onclick = function () {
        mostrarModalProdPostergar();
    }

    spanProdPostergar.onclick = function () {
        cerrarModalProdPostergar();
    }

    cancelarProdPostergarBtn.onclick = function () {
        cerrarModalProdPostergar();
    }

    confirmarProdPostergarBtn.onclick = function () {
        let form = document.getElementById("formProdPostergar");
        form.submit();
        cerrarModalProdPostergar();
    }
}

function gestionarCancelarProduccionPostergada() {
    let modalCancelarPostergar = document.getElementById("modalCancelarProduccionPostergada");
    let btnCancelarPostergar = document.getElementById("cancelarPostergarBtn");
    let confirmarCancelarPostergarBtn = document.getElementById("confirmarBtnCancelarPostergada");
    let cancelarCancelarPostergarBtn = document.getElementById("cancelarBtnCancelarPostergada");
    let spanCancelarPostergar = document.getElementsByClassName("closeCancelarPostergada")[0];

    function mostrarModalCancelarPostergar() {
        modalCancelarPostergar.style.display = "block";
    }

    function cerrarModalCancelarPostergar() {
        modalCancelarPostergar.style.display = "none";
    }

    btnCancelarPostergar.onclick = function () {
        mostrarModalCancelarPostergar();
    }

    spanCancelarPostergar.onclick = function () {
        cerrarModalCancelarPostergar();
    }

    cancelarCancelarPostergarBtn.onclick = function () {
        cerrarModalCancelarPostergar();
    }

    confirmarCancelarPostergarBtn.onclick = function () {
        let form = document.getElementById("formCancelarPostergar");
        form.submit();
        cerrarModalCancelarPostergar();
    }
}