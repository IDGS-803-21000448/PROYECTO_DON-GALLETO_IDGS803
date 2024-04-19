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


  function gestionarProcesar(solicitud_id) {
    let modalProcesar = document.getElementById("modalProcesar");
    let btnProcesar = document.getElementById("procesarBtn" + solicitud_id);
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
        let form = document.getElementById("formProcesar" + solicitud_id);
        form.submit();
        cerrarModalProcesar();
    }

    confirmarProcesarBtn.onclick = function () {
        confirmarProcesamiento();
    }
}



//fin de seccion de procesar --------------------------------------------------

function gestionarCancelarSolicitud(solicitud_id) {
    console.log(solicitud_id);
    let modalCancelarSolicitud = document.getElementById("modalCancelarSolicitud");
    let btnCancelarSolicitud = document.getElementById("cancelarSolicitudBtn" + solicitud_id);
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
        let form = document.getElementById("formCancelarSolicitud"+ solicitud_id);
        form.submit();
        cerrarModalCancelarSolicitud();
    }

    confirmarCancelarSolicitudBtn.onclick = function () {
        confirmarCancelacionSolicitud();
    }
}




//fin de seccion Cancelar solicitud------------------------------------------------
function gestionarPostergarSolicitud(solicitud_id) {
    let modalPostergarSolicitud = document.getElementById("modalPostergarSolicitud");
    let btnPostergarSolicitud = document.getElementById("postergarSolicitudBtn" + solicitud_id);
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
        let form = document.getElementById("formPostergarSolicitud" + solicitud_id);
        form.submit();
        cerrarModalPostergar();
    }

    confirmarPostergarSolicitudBtn.onclick = function () {
        confirmarPostergacion();
    }
}



//fin de seccion postergar solicitud------------------------------------------------

function gestionarTerminarProduccion(solicitud_id) {
    let modalTerminarProduccion = document.getElementById("modalTerminarProduccion");
    let btnTerminarProduccion = document.getElementById("terminarProduccionBtn" + solicitud_id);
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
        let form = document.getElementById("formTerminarProduccion" + solicitud_id);
        form.submit();
        cerrarModalTerminarProduccion();
    }

    confirmarTerminarProduccionBtn.onclick = function () {
        confirmarTerminar();
    }
}



//fin de seccion Terminar produccion------------------------------------------------

function gestionarCancelarProduccion(solicitud_id) {
    let modalCancelarProduccion = document.getElementById("modalCancelarProduccion");
    let btnCancelarProduccion = document.getElementById("cancelarProduccionBtn" + solicitud_id);
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
        let form = document.getElementById("formCancelarProduccion" + solicitud_id);
        form.submit();
        cerrarModalCancelarProduccion();
    }

    confirmarCancelarProduccionBtn.onclick = function () {
        confirmarCancelacionProduccion();
    }
}




//fin de seccion cancelar produccion------------------------------------------------  

function gestionarProduccionPostergada(solicitud_id) {
    let modalProdPostergar = document.getElementById("modalProcesarProduccionPostergada");
    let btnProdPostergar = document.getElementById("prodPostergarBtn" + solicitud_id);
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
        let form = document.getElementById("formProdPostergar" + solicitud_id);
        form.submit();
        cerrarModalProdPostergar();
    }
}

function gestionarCancelarProduccionPostergada(solicitud_id) {
    let modalCancelarPostergar = document.getElementById("modalCancelarProduccionPostergada");
    let btnCancelarPostergar = document.getElementById("cancelarPostergarBtn" + solicitud_id);
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
        let form = document.getElementById("formCancelarPostergar" + solicitud_id);
        form.submit();
        cerrarModalCancelarPostergar();
    }
}

function gestionarAgregarMerma(solicitud_id) {
  let modalAgregarMerma = document.getElementById("modalAgregarMerma");
  let btnAgregarMerma = document.getElementById("mandarAMermaBtn" + solicitud_id);
  let confirmarAgregarMermaBtn = document.getElementById("confirmarBtnAgregarMerma");
  let cancelarAgregarMerma = document.getElementById("cancelarBtnAgregarMerma");
  let spanAgregarMerma = document.getElementsByClassName("closeAgregarMerma")[0];

  function mostrarModalAgregarMerma() {
      modalAgregarMerma.style.display = "block";
  }

  function cerrarModalAgregarMerma() {
      modalAgregarMerma.style.display = "none";
  }

  btnAgregarMerma.onclick = function () {
      mostrarModalAgregarMerma();
  }

  spanAgregarMerma.onclick = function () {
      cerrarModalAgregarMerma();
  }

  cancelarAgregarMerma.onclick = function () {
      cerrarModalAgregarMerma();
  }

  function confirmarAgregarMerma() {
      let form = document.getElementById("formMandarAMerma" + solicitud_id);
      form.submit();
      cerrarModalAgregarMerma();
  }

  confirmarAgregarMermaBtn.onclick = function () {
      confirmarAgregarMerma();
  }
}