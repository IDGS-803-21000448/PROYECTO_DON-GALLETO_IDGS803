function mostrarContrasenia() {
  let password = document.getElementById("txtPassword");
  let showPassword = document.getElementById("mostrarPassword");

  showPassword.addEventListener("change", function () {
    if (showPassword.checked) {
      // Si el checkbox está marcado, cambiar a tipo 'text'
      password.type = "text";
    } else {
      // Si el checkbox no está marcado, volver a tipo 'password'
      password.type = "password";
    }
  });
}

function comprobarCampos() {
  let user = document.getElementById("txtUsername").value;
  let password = document.getElementById("txtPassword").value;
  let labelPassword = document.getElementById("labelPass");
  let labelUser = document.getElementById("labelUser");
  labelUser.style.display = "none";
  labelPassword.style.display = "none";

  if (user === "" && password === "") {
    labelUser.style.display = "block";
    labelPassword.style.display = "block";
    return;
  } else if (user === "") {
    labelUser.style.display = "block";
    return;
  } else if (password === "") {
    labelPassword.style.display = "block";
    return;
  } else {
    iniciarSesion(user, password);
    //window.location.href = "paginaPrincipal.html";
  }
}

function iniciarSesion(user, password){
  // Objeto con usuarios y contraseñas
  const usuarios = {
    "Admin": "1234",
    "david": "1234",
    "carlos": "8765"
  };

  // Verifica si el usuario existe en el objeto y si la contraseña coincide
  if (user in usuarios && password === usuarios[user]) {
    window.location.href = "main.html";
  } else {
    Swal.fire('', 'Usuario o contraseña incorrectos', 'error');
  }
}
