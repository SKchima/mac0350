document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector("#form-login");
    const nusp = document.querySelector("#nusp");
    const senha = document.querySelector("#senha");

    form.onsubmit = () => {
        if (nusp.value.trim() === "") {
            alert("O campo N°USP está vazio!");
            return false;
        }
        if (senha.value.trim() === "") {
            alert("O campo Senha está vazio!");
            return false;
        }

        localStorage.setItem("usp_logado", nusp.value);
        localStorage.setItem("senha_logada", senha.value);

        return true;
    };
});
