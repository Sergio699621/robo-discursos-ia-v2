import openai
import re

class GeradorDiscursos:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
    
    def verificar_conexao(self):
        """Verificar se a conexão com OpenAI está funcionando"""
        if not self.api_key:
            return False
        
        try:
            # Teste simples de conexão
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "teste"}],
                max_tokens=5
            )
            return True
        except:
            return False
    
    def analisar_religiosidade(self, dados):
        """Analisar crenças religiosas do casal"""
        religiao_noivo = dados.get('religiao_noivo', '').lower()
        religiao_noiva = dados.get('religiao_noiva', '').lower()
        
        # Palavras-chave para identificar religiosidade
        palavras_catolicas = ['católic', 'cristã', 'cristão', 'igreja', 'deus', 'jesus', 'fé']
        palavras_ateias = ['ateu', 'ateia', 'agnóstic', 'não acredito', 'sem religião']
        
        religioso = False
        ateu = False
        
        for palavra in palavras_catolicas:
            if palavra in religiao_noivo or palavra in religiao_noiva:
                religioso = True
                break
        
        for palavra in palavras_ateias:
            if palavra in religiao_noivo or palavra in religiao_noiva:
                ateu = True
                break
        
        if religioso:
            return 'religioso'
        elif ateu:
            return 'ateu'
        else:
            return 'neutro'
    
    def gerar_discurso(self, dados):
        """Gerar discurso personalizado baseado nos dados do casal"""
        if not self.api_key:
            return None
        
        try:
            # Analisar religiosidade
            tipo_religioso = self.analisar_religiosidade(dados)
            
            # Construir prompt personalizado
            prompt = self.construir_prompt(dados, tipo_religioso)
            
            # Gerar discurso com GPT-4
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um celebrante de casamentos experiente que cria discursos emocionantes e personalizados."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.8
            )
            
            discurso = response.choices[0].message.content.strip()
            
            # Verificar tamanho e ajustar se necessário
            if len(discurso) < 4200:
                discurso = self.expandir_discurso(discurso, dados)
            elif len(discurso) > 4800:
                discurso = self.encurtar_discurso(discurso)
            
            return discurso
            
        except Exception as e:
            print(f"Erro ao gerar discurso: {e}")
            return None
    
    def construir_prompt(self, dados, tipo_religioso):
        """Construir prompt personalizado baseado nos dados"""
        
        # Extrair informações principais
        nome_noivo = dados.get('nome_noivo', 'Noivo')
        nome_noiva = dados.get('nome_noiva', 'Noiva')
        como_conheceram = dados.get('como_conheceram', '')
        primeiro_encontro = dados.get('primeiro_encontro', '')
        momento_paixao = dados.get('momento_paixao', '')
        diferenca_marcante = dados.get('diferenca_marcante', '')
        sonho_futuro = dados.get('sonho_futuro', '')
        
        # Adaptar linguagem religiosa
        if tipo_religioso == 'religioso':
            linguagem_espiritual = """
            Use linguagem religiosa apropriada: "Deus abençoou", "fé divina", "união sagrada", 
            "mãos celestiais", "bênção do Senhor", "amor divino", "promessa diante de Deus".
            """
        elif tipo_religioso == 'ateu':
            linguagem_espiritual = """
            Use linguagem neutra e humanista: "universo conspirou", "forças naturais", 
            "destino entrelaçou", "energia poderosa", "conexão especial", "força da natureza".
            Evite referências religiosas.
            """
        else:
            linguagem_espiritual = """
            Use linguagem neutra: "destino", "forças maiores", "energia especial", 
            "conexão única", "poder do amor". Seja respeitoso a todas as crenças.
            """
        
        prompt = f"""
        Crie um discurso de casamento personalizado para {nome_noivo} e {nome_noiva} com EXATAMENTE 4500 caracteres.

        INFORMAÇÕES DO CASAL:
        - Como se conheceram: {como_conheceram}
        - Primeiro encontro: {primeiro_encontro}
        - Momento da paixão: {momento_paixao}
        - Diferença marcante: {diferenca_marcante}
        - Sonho futuro: {sonho_futuro}

        ESTILO E ESTRUTURA:
        1. INTRODUÇÃO ESPIRITUAL (2-3 parágrafos)
           - Reflexão sobre o amor e união
           {linguagem_espiritual}
        
        2. APRESENTAÇÃO INDIVIDUAL (1 parágrafo cada)
           - Características únicas de cada um
           - Use os dados fornecidos
        
        3. HISTÓRIA DO CASAL (3-4 parágrafos)
           - Como se conheceram (use detalhes fornecidos)
           - Evolução do relacionamento
           - Momentos marcantes
           - Inclua humor sutil se apropriado
        
        4. DEFINIÇÃO DO AMOR (2 parágrafos)
           - O que o amor significa para eles
           - Como se complementam
        
        5. VOTOS E FUTURO (2-3 parágrafos)
           - Desejos para o futuro
           - Bênçãos finais
           {linguagem_espiritual}

        DIRETRIZES:
        - Tom: Formal mas acessível, poético e emotivo
        - Linguagem: Português brasileiro natural
        - Humor: Sutil e apropriado, baseado nas diferenças/situações engraçadas
        - Emoção: Momentos tocantes baseados na história real
        - Tamanho: EXATAMENTE ~4500 caracteres
        - Evite clichês genéricos, use os detalhes específicos fornecidos
        
        Crie um discurso único que conte a história real deste casal de forma emocionante e memorável.
        """
        
        return prompt
    
    def expandir_discurso(self, discurso, dados):
        """Expandir discurso se estiver muito curto"""
        # Adicionar mais detalhes emocionais
        adicional = f"\n\nE assim, {dados.get('nome_noivo', 'ele')} e {dados.get('nome_noiva', 'ela')}, "
        adicional += "vocês nos ensinam que o amor verdadeiro não é apenas um sentimento, mas uma escolha diária "
        adicional += "de cuidar, respeitar e crescer juntos. Que esta união seja fonte de alegria, "
        adicional += "força e inspiração para todos que os cercam."
        
        return discurso + adicional
    
    def encurtar_discurso(self, discurso):
        """Encurtar discurso se estiver muito longo"""
        # Remover frases muito longas ou repetitivas
        frases = discurso.split('. ')
        if len(frases) > 20:
            # Manter as frases mais importantes (início, meio e fim)
            inicio = '. '.join(frases[:8])
            meio = '. '.join(frases[8:15])
            fim = '. '.join(frases[-5:])
            return f"{inicio}. {meio}. {fim}"
        
        return discurso[:4500]

