document.addEventListener('DOMContentLoaded', () => {
    const userInfo = document.querySelector("#user-info");
    const btnSair = document.querySelector("#btn-sair");

    const usp = localStorage.getItem("usp_logado");

    if (usp) {
        userInfo.innerHTML = usp;
    } else {
        userInfo.innerHTML = "Não logado";
    }

    btnSair.onclick = () => {
        localStorage.removeItem("usp_logado");
        localStorage.removeItem("senha_logada");
    };

    const botoesReserva = document.querySelectorAll(".btn-reservar");
    const listaUsuariosAtivos = document.querySelector("#lista-usuarios-ativos");

    const atualizarListaGeral = () => {
        listaUsuariosAtivos.innerHTML = "";
        const usuariosVistos = new Set();

        for (let i = 1; i <= 4; i++) {
            const user = localStorage.getItem(`user_estacao_${i}`);
            if (user && !usuariosVistos.has(user)) {
                const li = document.createElement("li");
                li.innerHTML = `N°USP: ${user}`;
                listaUsuariosAtivos.appendChild(li);
                usuariosVistos.add(user);
            }
        }
    };

    botoesReserva.forEach((botao) => {
        const estacaoContainer = botao.closest(".estacao-container");
        const square = estacaoContainer.querySelector(".estacao-square");
        const idEstacao = estacaoContainer.dataset.id;

        const userReservado = localStorage.getItem(`user_estacao_${idEstacao}`);
        if (userReservado) {
            botao.classList.add("reservado");
            botao.innerHTML = "Reservado";
            square.innerHTML = userReservado;
        }

        botao.addEventListener("click", () => {
            const usuarioAtual = localStorage.getItem("usp_logado");

            if (!usuarioAtual) {
                alert("Você precisa estar logado para reservar!");
                return;
            }

            if (!botao.classList.contains("reservado")) {
                botao.classList.add("reservado");
                botao.innerHTML = "Reservado";
                square.innerHTML = usuarioAtual;
                localStorage.setItem(`user_estacao_${idEstacao}`, usuarioAtual);
            } else {
                const donoDaReserva = localStorage.getItem(`user_estacao_${idEstacao}`);

                if (usuarioAtual === donoDaReserva) {
                    botao.classList.remove("reservado");
                    botao.innerHTML = "Reservar";
                    square.innerHTML = "";
                    localStorage.removeItem(`user_estacao_${idEstacao}`);
                } else {
                    alert(`Esta estação já está reservada pelo usuário ${donoDaReserva}!`);
                }
            }
            atualizarListaGeral();
        });
    });

    atualizarListaGeral();
});
