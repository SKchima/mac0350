async function login() {
    const nome = document.getElementById('nome').value;
    const senha = document.getElementById('senha').value;

    if (!nome || !senha) {
        alert("Preencha todos os campos");
        return;
    }

    const dados = {
        nome: nome,
        senha: senha
    };

    const resposta = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });

    if (resposta.ok) {
        alert("Login realizado com sucesso");
        window.location.href = "/";
    } else {
        const erro = await resposta.json();
        alert("Erro no login: " + (erro.detail || "Verifique suas credenciais"));
    }
}
