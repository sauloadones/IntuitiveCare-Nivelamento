# Flask backend com integração ao MySQL

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados MySQL
DB_CONFIG = {
    'host': 'mysql',           # nome do serviço no docker-compose
    'user': 'usuario',
    'password': 'senha',
    'database': 'meu_banco'
}

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

dataframes = []

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        df = pd.read_csv(filepath, sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')
    except Exception as e:
        return jsonify({'error': f'Erro ao ler o CSV: {str(e)}'}), 500

    if 'VL_SALDO_FINAL' not in df.columns:
        return jsonify({
            'error': 'Coluna VL_SALDO_FINAL não encontrada.',
            'colunas_disponiveis': df.columns.tolist()
        }), 400

    try:
        df['TRIMESTRE'] = file.filename.replace('.csv', '')
        df['VL_SALDO_FINAL'] = df['VL_SALDO_FINAL'].astype(str).str.replace(',', '.').astype(float)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO balanco_trimestral (
                    DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO,
                    VL_SALDO_INICIAL, VL_SALDO_FINAL, TRIMESTRE
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row.get('DATA'),
                row.get('REG_ANS'),
                row.get('CD_CONTA_CONTABIL'),
                row.get('DESCRICAO'),
                row.get('VL_SALDO_INICIAL'),
                row.get('VL_SALDO_FINAL'),
                row.get('TRIMESTRE')
            ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': f'{file.filename} carregado com sucesso no banco de dados.'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao processar os dados: {str(e)}'}), 500

@app.route('/top-despesas', methods=['GET'])
def top_despesas():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = """
            SELECT REG_ANS, TRIMESTRE, SUM(VL_SALDO_FINAL) AS TOTAL
            FROM balanco_trimestral
            WHERE
                UPPER(DESCRICAO) LIKE '%EVENTOS%' AND
                UPPER(DESCRICAO) LIKE '%SINISTRO%' AND
                UPPER(DESCRICAO) LIKE '%ASSISTENCIA%' AND
                UPPER(DESCRICAO) LIKE '%MEDICO%' AND
                UPPER(DESCRICAO) LIKE '%HOSPITALAR%'
            GROUP BY REG_ANS, TRIMESTRE
            ORDER BY TOTAL DESC
            LIMIT 10;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': f'Erro na consulta: {str(e)}'}), 500

@app.route('/top-despesas-trimestre', methods=['GET'])
def top_despesas_trimestre():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = """
            SELECT REG_ANS, TRIMESTRE, SUM(VL_SALDO_FINAL) AS TOTAL
            FROM balanco_trimestral
            WHERE
                UPPER(DESCRICAO) LIKE '%EVENTOS%' AND
                UPPER(DESCRICAO) LIKE '%SINISTRO%' AND
                UPPER(DESCRICAO) LIKE '%ASSISTENCIA%' AND
                UPPER(DESCRICAO) LIKE '%MEDICO%' AND
                UPPER(DESCRICAO) LIKE '%HOSPITALAR%' AND
                TRIMESTRE = (SELECT MAX(TRIMESTRE) FROM balanco_trimestral)
            GROUP BY REG_ANS, TRIMESTRE
            ORDER BY TOTAL DESC
            LIMIT 10;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': f'Erro na consulta do trimestre: {str(e)}'}), 500

@app.route('/top-despesas-ano', methods=['GET'])
def top_despesas_ano():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = """
            SELECT bt.REG_ANS, SUM(bt.VL_SALDO_FINAL) AS TOTAL
            FROM balanco_trimestral bt
            JOIN (
                SELECT DISTINCT TRIMESTRE
                FROM balanco_trimestral
                ORDER BY TRIMESTRE DESC
                LIMIT 4
            ) ultimos
            ON bt.TRIMESTRE = ultimos.TRIMESTRE
            WHERE
                UPPER(bt.DESCRICAO) LIKE '%EVENTOS%' AND
                UPPER(bt.DESCRICAO) LIKE '%SINISTRO%' AND
                UPPER(bt.DESCRICAO) LIKE '%ASSISTENCIA%' AND
                UPPER(bt.DESCRICAO) LIKE '%MEDICO%' AND
                UPPER(bt.DESCRICAO) LIKE '%HOSPITALAR%'
            GROUP BY bt.REG_ANS
            ORDER BY TOTAL DESC
            LIMIT 10;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': f'Erro na consulta do ano: {str(e)}'}), 500

@app.route('/buscar-operadora')
def buscar_operadora():
    termo = request.args.get('q', '').strip().lower()
    if not termo:
        return jsonify({'erro': 'Você precisa fornecer um parâmetro de busca (?q=...)'}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql("SELECT * FROM operadoras_ans", conn)
        conn.close()

        df.columns = df.columns.str.strip().str.lower()
        df['texto_busca'] = (
            df.get('razao_social', '') + ' ' +
            df.get('nome_fantasia', '') + ' ' +
            df.get('cnpj', '')
        ).astype(str).str.lower()

        filtro = df['texto_busca'].str.contains(termo, na=False)
        resultados = df[filtro].head(10)

        return jsonify(resultados.drop(columns=['texto_busca']).to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': f'Erro na busca: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)