document.addEventListener("DOMContentLoaded", function () {

    function applyFilter(input, table) {
        const value = input.value.toLowerCase();

        const rows = table.getElementsByTagName("tr");

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const text = row.innerText.toLowerCase();

            row.style.display = text.includes(value) ? "" : "none";
        }
    }

    function initFilters() {
        const inputs = document.querySelectorAll(".js-filter");

        inputs.forEach(input => {
            const targetName = input.dataset.target;
            const table = document.querySelector(`.js-table[data-name="${targetName}"]`);

            if (!table) return;

            input.addEventListener("keyup", function () {
                applyFilter(input, table);
            });
        });
    }

    initFilters();

    // Limpa formulários quando o modal fecha
    const modais = document.querySelectorAll('.modal');

    modais.forEach(modal => {
        modal.addEventListener('hidden.bs.modal', function () {

            const form = modal.querySelector('form');

            if (!form) return;

            // Não limpar formulários de edição
            if (
                modal.id.startsWith('editar') ||
                modal.id.startsWith('editarUsuario') ||
                modal.id.startsWith('editarFabricante') ||
                modal.id.startsWith('editarTipo') ||
                modal.id.startsWith('editarLocal')
            ) {
                form.reset();
                return;
            }

            form.reset();
        });
    });

    // Validação da tela de alteração de senha
    const senha = document.getElementById('senha');
    const confirmar = document.getElementById('confirmar_senha');
    const btn = document.getElementById('btnSalvar');
    const erro = document.getElementById('erroSenha');

    if (senha && confirmar && btn && erro) {

        function validarSenha() {
            const s1 = senha.value;
            const s2 = confirmar.value;

            if (s1.length > 0 && s1 === s2) {
                btn.disabled = false;
                erro.classList.add('d-none');
            } else {
                btn.disabled = true;
                erro.classList.toggle('d-none', s2.length === 0);
            }
        }

        senha.addEventListener('input', validarSenha);
        confirmar.addEventListener('input', validarSenha);
}
});