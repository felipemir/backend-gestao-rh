from flask import jsonify, request, Blueprint
from conection_mysql import connect_mysql
from mysql.connector import Error
from flask_login import login_required  # Importa diretamente do Flask-Login
from decorador import roles_required  # Importa o decorador personalizado


bp_atualizar_servidor = Blueprint("bp_atualizar_servidor", __name__)


@bp_atualizar_servidor.route("/api/servidores/<int:id>", methods=["PUT"])
# @login_required
# @roles_required('admin','editor')
def atualizar_servidor(id):
    try:
        conexao = connect_mysql()
        cursor = conexao.cursor(dictionary=True)
        body = request.json

        busca_se_existe_servidor = "SELECT * FROM funcionarios WHERE id = %s"
        cursor.execute(busca_se_existe_servidor, (id,))
        servidor = cursor.fetchone()

        if not servidor:
            return jsonify({"erro": "Servidor não encontrado"}), 404

        # Lista de campos que podem ser atualizados
        campos_permitidos = [
            "setor",
            "nome",
            "matricula",
            "cargo",
            "funcao",
            "horario",
            "horarioentrada",
            "horariosaida",
            "feriasinicio",
            "feriasfinal",
            "dataNascimento",
            "sexo",
            "estadoCivil",
            "naturalidade",
            "nacionalidade",
            "identidade",
            "tituloEleitor",
            "cpf",
            "pis",
            "dataAdmissao",
        ]

        # Dicionário para armazenar os campos e valores que serão atualizados
        campos_para_atualizar = {}

        # Verifica quais campos foram enviados no corpo da requisição
        for campo in campos_permitidos:
            if campo in body:
                campos_para_atualizar[campo] = body[campo]

        # Se não houver campos para atualizar, retorna um erro
        if not campos_para_atualizar:
            return (
                jsonify({"erro": "Nenhum campo válido para atualizar foi fornecido"}),
                400,
            )

        # Constrói a query SQL dinamicamente
        set_clause = ", ".join(
            [f"{campo} = %s" for campo in campos_para_atualizar.keys()]
        )
        valores = list(campos_para_atualizar.values())
        valores.append(id)  # Adiciona o ID no final para a cláusula WHERE

        atualizar_dados_servidor = f"""
            UPDATE funcionarios
            SET {set_clause}
            WHERE id = %s
        """

        cursor.execute(atualizar_dados_servidor, valores)
        conexao.commit()
        conexao.close()

        # Retorna os campos atualizados
        return jsonify({"servidor": campos_para_atualizar}), 200

    except Exception as exception:
        return (
            jsonify({"erro": f"Erro ao conectar ao banco de dados: {str(exception)}"}),
            500,
        )
