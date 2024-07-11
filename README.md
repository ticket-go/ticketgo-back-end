# TicketGo

TicketGo é marketplace de ingressos on-line.

## Instalação

Siga os passos abaixo para configurar e executar o projeto localmente.

### Clonar o Repositório

```
git clone https://github.com/seu-usuario/ticketgo.git
cd ticketgo
```

### Criar e Ativar um Ambiente Virtual

```
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

### Instalar as Dependências

```
pip install -r requirements.txt
```

### Copiar .env-EXAMPLE to .env

### Alterar .env conforme necessário

### Criar e conectar um banco de dados PostgreSQL

```
pip install -r requirements.txt
```

## Aplicar migrações

```
python manage.py migrate
```

## Após realizar as migrações, Carregue os dados fictícios

```
python manage.py loaddata initial_data.json
```

### Criar superusuário

```
python manage.py createsuperuser
```

### Rodar o Servidor de Desenvolvimento

```
python manage.py runserver
```
