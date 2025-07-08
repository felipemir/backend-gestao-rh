# tests/test_app.py

import pytest
from main import app  # Importa a sua aplicação Flask do ficheiro main.py

# Cria um "cliente de teste" para a nossa aplicação.
# Isso permite simular requisições (GET, POST, etc.) sem precisar de um servidor real.
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Nosso primeiro teste! Funções de teste também devem começar com "test_".
def test_home_route(client):
    """
    Testa se a rota principal ('/') responde com sucesso (código 200 OK).
    """
    # Simula uma requisição GET para a rota "/"
    response = client.get('/')
    
    # Verifica se o código de status da resposta é 200
    assert response.status_code == 200