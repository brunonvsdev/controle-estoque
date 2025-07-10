/*
Módulo estoque.js - Lógica do controle de estoque (frontend)

Este arquivo contém as funções JavaScript responsáveis pela interação do usuário com a interface de controle de estoque.
Inclui manipulação de eventos, requisições ao backend, atualização dinâmica da interface e validações.

Autor: Bruno Novais Costa Simões
Data: 10/07/2025
Versão: 1.0
*/
        // Funções para alternar entre seções
        function mostrarSecao(secao) {
            document.querySelectorAll('section').forEach(s => {
                s.style.display = 'none';
            });
            document.getElementById(`secao-${secao}`).style.display = 'block';
            
            document.querySelectorAll('nav a').forEach(link => {
                link.classList.remove('active');
            });
            event.target.classList.add('active');
        
            // Salva a seção ativa
            localStorage.setItem('secaoAtiva', secao);
        }
        

        // Verifica se tem seção salva e exibe
        document.addEventListener('DOMContentLoaded', () => {
            const secaoSalva = localStorage.getItem('secaoAtiva') || 'produtos';
            mostrarSecao(secaoSalva);
        });


        // Adicionar produto
        document.getElementById('form-produto').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const produto = {
                nome: document.getElementById('nome').value,
                descricao: document.getElementById('descricao').value,
                quantidade: document.getElementById('quantidade').value,
                preco: document.getElementById('preco').value
            };

            function enviarProduto(forcar = false) {
                const body = { ...produto };
                if (forcar) body.forcar = true;
                fetch('/api/produtos', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(body)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Produto adicionado com sucesso!');
                        window.location.reload();
                    } else if (data.duplicate) {
                        if (confirm('Você já tem um produto cadastrado com esse nome, deseja continuar?')) {
                            enviarProduto(true);
                        }
                    } else {
                        alert('Erro: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Erro ao adicionar produto');
                });
            }

            enviarProduto();
        });

        // Editar produto
        const modalEdicao = new bootstrap.Modal(document.getElementById('modalEdicao'));
        
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-editar') || e.target.closest('.btn-editar')) {
                const btn = e.target.classList.contains('btn-editar') ? e.target : e.target.closest('.btn-editar');
                const row = btn.closest('tr');
                document.getElementById('edit-id').value = row.dataset.id;
                document.getElementById('edit-nome').value = row.cells[0].textContent;
                document.getElementById('edit-descricao').value = row.cells[1].textContent;
                document.getElementById('edit-quantidade').value = row.cells[2].textContent;
                document.getElementById('edit-preco').value = row.cells[3].textContent.replace('R$ ', '');
                
                modalEdicao.show();
            }
        });

        document.getElementById('btn-salvar-edicao').addEventListener('click', function() {
            const produto = {
                nome: document.getElementById('edit-nome').value,
                descricao: document.getElementById('edit-descricao').value,
                quantidade: document.getElementById('edit-quantidade').value,
                preco: document.getElementById('edit-preco').value
            };
            
            const id = document.getElementById('edit-id').value;

            fetch(`/api/produtos/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(produto)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Produto atualizado com sucesso!');
                    modalEdicao.hide();
                    window.location.reload();
                } else {
                    alert('Erro: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao atualizar produto');
            });
        });

        // Excluir produto
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-excluir') || e.target.closest('.btn-excluir')) {
                const btn = e.target.classList.contains('btn-excluir') ? e.target : e.target.closest('.btn-excluir');
                if (confirm('Tem certeza que deseja excluir este produto?')) {
                    const id = btn.closest('tr').dataset.id;
                    
                    fetch(`/api/produtos/${id}`, {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Produto excluído com sucesso!');
                            window.location.reload();
                        } else {
                            alert('Erro: ' + data.error);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Erro ao excluir produto');
                    });
                }
            }
        });

        // Registrar venda
        document.getElementById('form-venda').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const venda = {
                produto_id: document.getElementById('produto-venda').value,
                quantidade: document.getElementById('quantidade-venda').value
            };

            fetch('/api/vendas', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(venda)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    localStorage.setItem('secaoAtiva', 'vendas');
                    window.location.reload();
                } else {
                    alert('Erro: ' + (data.error || data.message));
                }
            })
            
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao registrar venda');
            });
        });

        // Buscar produtos
        document.getElementById('btn-buscar').addEventListener('click', buscarProdutos);
        document.getElementById('termo-busca').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') buscarProdutos();
        });

        function buscarProdutos() {
            const termo = document.getElementById('termo-busca').value;
            
            fetch(`/api/buscar?termo=${encodeURIComponent(termo)}`)
            .then(response => response.json())
            .then(produtos => {
                const tbody = document.getElementById('resultados-busca');
                tbody.innerHTML = '';
                
                if (produtos.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="4" class="text-center">Nenhum produto encontrado</td></tr>';
                    return;
                }
                
                produtos.forEach(produto => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${produto.nome}</td>
                        <td>${produto.descricao}</td>
                        <td>${produto.quantidade}</td>
                        <td>R$ ${produto.preco.toFixed(2)}</td>
                    `;
                    tbody.appendChild(tr);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao buscar produtos');
            });
        }