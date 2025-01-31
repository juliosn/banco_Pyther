# 🚀 Desafio: Conectando Microserviços: Banco Pyther 🚀  

Bem-vindo ao repositório do desafio de programação! Este projeto consiste na criação de dois microsserviços utilizando Spring Boot, com foco em explorar o ecossistema RESTful e a interconexão entre aplicações com Feign Client. O objetivo é construir um sistema para **Cadastro de Clientes do Banco PYTHER**!

## 🛠️ Objetivo  

Criar duas aplicações Flask:  
1. **Aplicação Cliente**:  
   - Expor endpoints CRUD (Create, Read, Update, Delete) para gerenciamento de clientes.  
   - Realizar requisições REST para a **Aplicação Servidora**.  
   - Implementar um endpoint adicional para calcular o **Score de Crédito** baseado no saldo da conta corrente (`saldo_cc`).  

2. **Aplicação Servidora**:  
   - Implementar operações CRUD para gerenciamento de clientes em uma base de dados H2 local.  

Ambas as aplicações devem ser **totalmente testadas**, garantindo robustez e confiabilidade. Neste contexto, foi utilizado testes ponta a ponta com o Pytest...  

---

## 📝 Informações do Cliente  

Cada cliente será representado pelas seguintes propriedades:  
- **nome**: Nome completo do cliente.  
- **telefone**: Número de telefone do cliente.  
- **correntista**: Indica se o cliente é correntista (booleano).  
- **score_credito**: Pontuação de crédito do cliente (calculado).  
- **saldo_cc**: Saldo da conta corrente do cliente.  

---

## 📂 Estrutura do Repositório  

O repositório contém as pastas para cada aplicação:  

- `api_crud`: Código e testes para a **Aplicação Cliente**.  
- `api_requisicao`: Código e testes para a **Aplicação Servidora**.  

---

## ⚙️ Endpoints  

### 1. Aplicação Cliente  
**Base URL**: `/api/v1/conta/clientes`  

| Método  | Rota                | Descrição                                  |  
|---------|---------------------|--------------------------------------------|  
| POST    | `/`                 | Criar um novo cliente.                     |  
| GET     | `/`                 | Listar todos os clientes.                  |  
| GET     | `/{id}`             | Buscar cliente por ID.                     |  
| PUT     | `/{id}`             | Atualizar informações do cliente por ID.   |  
| DELETE  | `/{id}`             | Remover cliente por ID.                    |  
| GET     | `/score/{id}`       | Calcular o Score de Crédito do cliente.    |  

### 2. Aplicação Servidora  
**Base URL**: `/api/v1/conta/clientes`  

| Método  | Rota                | Descrição                                  |  
|---------|---------------------|--------------------------------------------|  
| POST    | `/`                 | Criar um novo cliente no banco.            |  
| GET     | `/`                 | Listar todos os clientes do banco.         |  
| GET     | `/{id}`             | Buscar cliente no banco por ID.            |  
| PUT     | `/{id}`             | Atualizar informações do cliente no banco. |  
| DELETE  | `/{id}`             | Remover cliente do banco por ID.           |  

---
