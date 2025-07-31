import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from gerador_discursos import GeradorDiscursos

app = Flask(__name__)
CORS(app)

# Configurar OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    print("⚠️ AVISO: OPENAI_API_KEY não configurada")

# Inicializar gerador
gerador = GeradorDiscursos(openai_api_key) if openai_api_key else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    """Verificar status da IA"""
    if gerador and gerador.verificar_conexao():
        return jsonify({
            'status': 'online',
            'ia_ativa': True,
            'mensagem': 'Sistema Online: IA configurada'
        })
    else:
        return jsonify({
            'status': 'offline',
            'ia_ativa': False,
            'mensagem': 'IA não configurada - Configure OPENAI_API_KEY'
        })

@app.route('/gerar_discurso', methods=['POST'])
def gerar_discurso():
    """Gerar discurso personalizado"""
    try:
        if not gerador:
            return jsonify({
                'erro': True,
                'mensagem': 'IA não configurada. Configure OPENAI_API_KEY nas variáveis de ambiente.'
            })
        
        dados = request.json
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome_noivo', 'nome_noiva']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return jsonify({
                    'erro': True,
                    'mensagem': f'Campo obrigatório: {campo}'
                })
        
        # Gerar discurso
        discurso = gerador.gerar_discurso(dados)
        
        if discurso:
            # Estatísticas
            caracteres = len(discurso)
            palavras = len(discurso.split())
            
            return jsonify({
                'sucesso': True,
                'discurso': discurso,
                'estatisticas': {
                    'caracteres': caracteres,
                    'palavras': palavras,
                    'qualidade': 'Excelente' if 4200 <= caracteres <= 4800 else 'Boa'
                }
            })
        else:
            return jsonify({
                'erro': True,
                'mensagem': 'Erro ao gerar discurso. Tente novamente.'
            })
            
    except Exception as e:
        print(f"Erro ao gerar discurso: {e}")
        return jsonify({
            'erro': True,
            'mensagem': 'Erro interno do servidor. Tente novamente.'
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

