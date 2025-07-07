from flask import Blueprint, jsonify, request, Flask
from mysql.connector import Error
from conection_mysql import connect_mysql
from flask_login import login_required  # Importa diretamente do Flask-Login
from decorador import roles_required 
import os

app = Flask(__name__)
app.config["BASE_PDF_FOLDER"] = os.path.join('setor')

bp_listar_pdfs_estagiarios = Blueprint('bp_listar_pdfs_estagiarios', __name__)

@bp_listar_pdfs_estagiarios.route("/api/estagiarios/pdfs", methods=["GET"])
# @login_required
# @roles_required('admin','editor')
def listar_pdfs_estagiarios():
    try:
        dados = explorar_pastas(app.config['BASE_PDF_FOLDER'])
        return jsonify({ "estagiarios_pdf": [dados] })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
def explorar_pastas(caminho_base):
    dados = {}
    for item in os.listdir(caminho_base):
        caminho_completo = os.path.join(caminho_base, item)

        
        if os.path.isdir(caminho_completo):
            # Se for uma pasta, explora recursivamente
            subdados = explorar_pastas(caminho_completo)
            if subdados:  # Só adiciona se contiver PDFs
                dados[item] = subdados
        elif item.endswith('.pdf'):
            # Se for um PDF, adiciona ao nível atual
            if 'arquivos' not in dados:
                dados['arquivos'] = []
            dados['arquivos'].append(item)
    return dados
