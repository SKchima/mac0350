async function enviarUsuario() {
    const dados = {
        nome: document.getElementById('nome').value,
        senha: document.getElementById('senha').value,
        bio: document.getElementById('bio').value
    };

    const resposta = await fetch('/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });

    if (resposta.ok) {
        const resultado = await resposta.json();
        alert("Usuário " + resultado.usuario + " criado!");
    } else {
        alert("Erro ao criar usuário!");
    }
}

async function login() {
    const dados = {
        nome: document.getElementById('nome').value,
        senha: document.getElementById('senha').value
    }

    const resposta = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });

    if (resposta.ok) {
        const resultado = await resposta.json();
        alert("Logado com sucesso!");
        window.location.href = "/home";
    } else {
        alert("Erro ao logar!");
    }
}