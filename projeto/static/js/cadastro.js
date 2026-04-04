async function enviarUsuario() {
    const nome = document.getElementById('nome').value;
    const senha = document.getElementById('senha').value;

    if (!nome || !senha) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    const dados = {
        nome: nome,
        senha: senha
    };

    const existeUsuario = await fetch('/usuarios', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nome)
    });

    if (existeUsuario.ok) {
        alert("Usuário já existe!");
        return;
    }

    const resposta = await fetch('/usuarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });

    if (resposta.ok) {
        alert("Usuário criado com sucesso!");
        window.location.href = "/login";
    } else {
        const erro = await resposta.json();
        alert("Erro ao criar usuário: " + (erro.detail || "Tente novamente"));
    }
}
