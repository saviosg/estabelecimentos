# Estabelecimentos

Aplicação em Flask para uma vaga de emprego.

Permite cadastrar e visualizar dados de
estabelecimentos, além de ter uma página
com uma lista de tarefas em JavaScript puro.

Os dados são armazenados em Elasticsearch e MongoDB.

## Instalação

Para executar a aplicação, use o Docker Compose
na pasta raiz do projeto:

    docker compose up -d

Para importar os dados, baixe o arquivo
[Estabelecimentos9.zip](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-jurdica---cnpj).

Extraia e renomeie o arquivo `K3241.K03200Y9.D30211.ESTABELE` para `estabelecimentos.csv`.

Importe os dados iniciais com
o comando `docker compose exec`:

    sudo docker compose exec -it web python3 load_data.py

## Desenvolvimento

Instale o plugin [EditorConfig](https://editorconfig.org/)
no seu editor para padronizar indentação em HTML.

Recomendo o Pyright para edição em Python.

Recomendo [Nix](https://nixos.org) e
[venv](https://docs.python.org/3/library/venv.html)
para um ambiente de desenvolvimento isolado.

Use os comandos a seguir parar gerar
um ambiente de desenvolvimento Nix
com Python e bibliotecas instaladas:

    nix develop
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt


