from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Simulação do modelo Llama (pode ser substituído por implementação real)
class LlamaService:
    def __init__(self):
        self.model_loaded = False
    
    def generate_feedback(self, text, analysis_data):
        """Gera feedback personalizado baseado na análise"""
        feedback = {
            "personalized_feedback": self._generate_personalized_feedback(text, analysis_data),
            "content_recommendations": self._generate_content_recommendations(analysis_data),
            "improvement_suggestions": self._generate_improvement_suggestions(analysis_data),
            "service": "llama"
        }
        return feedback
    
    def _generate_personalized_feedback(self, text, analysis_data):
        """Gera feedback personalizado"""
        overall_score = analysis_data.get('overall_score', 0)
        
        if overall_score >= 160:
            tone = "Excelente trabalho! Sua redação demonstra domínio das competências avaliadas."
        elif overall_score >= 120:
            tone = "Boa redação! Há alguns pontos que podem ser aprimorados."
        elif overall_score >= 80:
            tone = "Sua redação precisa de melhorias em algumas competências."
        else:
            tone = "Há muito espaço para melhoramento. Vamos trabalhar juntos!"
        
        return {
            "opening": tone,
            "detailed_analysis": self._analyze_each_competency(analysis_data),
            "overall_impression": f"Pontuação geral: {overall_score:.0f}/1000"
        }
    
    def _analyze_each_competency(self, analysis_data):
        """Analisa cada competência individualmente"""
        competencies_feedback = []
        
        for i in range(1, 6):
            comp_key = f"competencia_{i}"
            if comp_key in analysis_data:
                comp_data = analysis_data[comp_key]
                score = comp_data.get('score', 0)
                description = comp_data.get('description', '')
                
                if score >= 160:
                    level = "Excelente"
                elif score >= 120:
                    level = "Bom"
                elif score >= 80:
                    level = "Regular"
                else:
                    level = "Insuficiente"
                
                competencies_feedback.append({
                    "competency": i,
                    "score": score,
                    "level": level,
                    "description": description
                })
        
        return competencies_feedback
    
    def _generate_content_recommendations(self, analysis_data):
        """Gera recomendações de conteúdo"""
        recommendations = []
        
        # Baseado nas competências com menor pontuação
        for i in range(1, 6):
            comp_key = f"competencia_{i}"
            if comp_key in analysis_data:
                score = analysis_data[comp_key].get('score', 0)
                if score < 120:  # Competência que precisa de melhoria
                    recommendations.extend(self._get_recommendations_for_competency(i))
        
        return recommendations[:5]  # Limitar a 5 recomendações
    
    def _get_recommendations_for_competency(self, competency_num):
        """Retorna recomendações específicas para cada competência"""
        recommendations_map = {
            1: [
                "Estude regras de concordância verbal e nominal",
                "Pratique o uso correto da crase",
                "Revise regras de pontuação"
            ],
            2: [
                "Leia mais sobre temas contemporâneos",
                "Pratique a interpretação de textos",
                "Estude repertório sociocultural"
            ],
            3: [
                "Aprenda a estruturar argumentos",
                "Pratique o uso de dados e estatísticas",
                "Estude técnicas de argumentação"
            ],
            4: [
                "Estude conectivos e elementos coesivos",
                "Pratique a organização textual",
                "Aprenda sobre progressão temática"
            ],
            5: [
                "Estude modelos de propostas de intervenção",
                "Pratique a elaboração de soluções viáveis",
                "Aprenda sobre agentes sociais"
            ]
        }
        return recommendations_map.get(competency_num, [])
    
    def _generate_improvement_suggestions(self, analysis_data):
        """Gera sugestões específicas de melhoria"""
        suggestions = []
        
        overall_score = analysis_data.get('overall_score', 0)
        
        if overall_score < 100:
            suggestions.extend([
                "Foque em escrever textos mais longos e desenvolvidos",
                "Pratique a escrita diária por pelo menos 30 minutos",
                "Leia redações nota 1000 para se inspirar"
            ])
        elif overall_score < 150:
            suggestions.extend([
                "Trabalhe na organização das ideias",
                "Melhore a conexão entre os parágrafos",
                "Desenvolva melhor sua proposta de intervenção"
            ])
        else:
            suggestions.extend([
                "Refine seu repertório cultural",
                "Aperfeiçoe o uso de conectivos",
                "Trabalhe na originalidade da proposta"
            ])
        
        return suggestions

llama_service = LlamaService()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "llama"})

@app.route('/generate-feedback', methods=['POST'])
def generate_feedback():
    try:
        data = request.get_json()
        text = data.get('text', '')
        analysis_data = data.get('analysis_data', {})
        
        if not text or not analysis_data:
            return jsonify({"error": "Texto e dados de análise são obrigatórios"}), 400
        
        feedback = llama_service.generate_feedback(text, analysis_data)
        
        return jsonify({
            "success": True,
            "feedback": feedback
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "llama"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

