# 🏋️‍♂️ API Academia

API REST desenvolvida com **Flask** para gerenciamento de alunos de academia, utilizando **Firebase Firestore** como banco de dados e autenticação via **JWT (JSON Web Token)**.

---

## 🚀 Funcionalidades

### 🔐 Autenticação

* Login administrativo com geração de token JWT
* Proteção de rotas sensíveis com middleware

### 👨‍🎓 Gestão de Alunos

* Cadastro de alunos com **ID incremental automático**
* Listagem de todos os alunos
* Consulta por:

  * ID
  * CPF
* Atualização parcial (**PATCH**)
* Exclusão de alunos

### 📄 Documentação

* Interface interativa com **Swagger (Flasgger)**
* Teste das rotas diretamente pelo navegador

### ☁️ Deploy

* Estrutura pronta para deploy na **Vercel**

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia         | Descrição                         |
| ------------------ | --------------------------------- |
| Python             | Linguagem principal               |
| Flask              | Framework web                     |
| Firebase Firestore | Banco NoSQL                       |
| Firebase Admin SDK | Integração com Firestore          |
| PyJWT              | Autenticação JWT                  |
| Flask-CORS         | Liberação de acesso entre origens |
| Flasgger           | Documentação OpenAPI              |

---

## 📁 Estrutura do Projeto

```
📦 projeto
 ┣ 📜 app.py
 ┣ 📜 auth.py
 ┣ 📜 openapi.yaml
 ┣ 📜 requirements.txt
 ┣ 📜 firebase.json
 ┗ 📜 .env
```

---

## ⚙️ Configuração do Ambiente

### 1️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta
ADM_USUARIO=senai
ADM_SENHA=sua_senha_aqui
```

---

### 3️⃣ Firebase

* Crie um projeto no Firebase
* Ative o **Firestore Database (modo Native)**
* Baixe as credenciais e salve como:

```bash
firebase.json
```

---

## ▶️ Executando o Projeto

```bash
python app.py
```

A API estará disponível em:

```
http://127.0.0.1:5000
```

---

## 📚 Documentação Swagger

Acesse:

```
http://127.0.0.1:5000/apidocs
```

---

## 🔑 Autenticação

1. Faça login em:

```
POST /login
```

2. Copie o token retornado

3. Use nas rotas protegidas:

```
Authorization: Bearer SEU_TOKEN
```

---

## 📌 Principais Endpoints

### 🔐 Login

```
POST /login
```

### 👨‍🎓 Alunos

| Método | Rota              | Descrição       |
| ------ | ----------------- | --------------- |
| POST   | /cadastro         | Cadastrar aluno |
| GET    | /alunos           | Listar alunos   |
| GET    | /alunos/{id}      | Buscar por ID   |
| GET    | /alunos/cpf/{cpf} | Buscar por CPF  |
| PATCH  | /alunos/{id}      | Editar aluno    |
| DELETE | /alunos/{id}      | Excluir aluno   |

---

## ☁️ Deploy na Vercel

### Variáveis necessárias:

* `SECRET_KEY`
* `ADM_USUARIO`
* `ADM_SENHA`
* `FIREBASE_CREDENTIALS`

> ⚠️ O `FIREBASE_CREDENTIALS` deve conter o JSON do Firebase em formato string.




## 👩‍💻 Autoras

* Ana Beatriz
* Lívia

---

## 📄 Licença

Este projeto é apenas para fins educacionais.
