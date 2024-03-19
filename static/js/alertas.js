// Alertas para el módulo de usuarios
function confirmarBorradoUsuario(usuarioId) {
    // Utiliza SweetAlert para mostrar la alerta de confirmación
    Swal.fire({
        title: '¿Estás seguro?',
        text: 'Esta acción eliminará el usuario de forma permanente.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario confirma la acción, redirige a la ruta para eliminar el usuario
            window.location.href = '/eliminarUsuario?id=' + usuarioId;
        }
    });
}