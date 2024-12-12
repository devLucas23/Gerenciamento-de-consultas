#!/bin/bash

PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"

ADDRESS="127.0.0.1"
PORT=8000            

check_dependencies() {
    echo "Verificando dependências..."
    if ! command -v python3 &>/dev/null; then
        echo "Python3 não está instalado. Instale antes de continuar."
        exit 1
    fi
    if ! command -v pip &>/dev/null; then
        echo "pip não está instalado. Instale antes de continuar."
        exit 1
    fi
}

activate_venv() {
    echo "Ativando o ambiente virtual..."
    if [ ! -d "$VENV_DIR" ]; then
        echo "Ambiente virtual não encontrado. Criando um novo..."
        python3 -m venv "$VENV_DIR"
    fi
    source "$VENV_DIR/bin/activate"
}

install_dependencies() {
    echo "Instalando dependências..."
    pip install --upgrade pip
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        pip install -r "$PROJECT_DIR/requirements.txt"
    else
        echo "Arquivo requirements.txt não encontrado. Certifique-se de que as dependências estão corretas."
    fi
}

run_server() {
    echo "Aplicando migrações..."
    python3 manage.py makemigrations
    python3 manage.py migrate

    echo "Iniciando o servidor Django em $ADDRESS:$PORT..."
    python3 manage.py runserver "$ADDRESS:$PORT"
}

echo "Iniciando o script de execução do projeto Django..."
check_dependencies
cd "$PROJECT_DIR"
activate_venv
install_dependencies
run_server
