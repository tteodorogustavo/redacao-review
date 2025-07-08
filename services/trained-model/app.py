from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "trained-model"})


def gerar_feedback_ollama(text):
    prompt = f"""
Você é um avaliador de redações do ENEM. Sua tarefa é analisar a redação que será fornecida a seguir, atribuir uma nota geral de 0 a 1000 e, para cada uma das cinco competências do ENEM, fornecer uma nota (de 0 a 200), um feedback detalhado sobre os pontos fortes e fracos, e sugestões específicas para melhoria. O feedback deve ser construtivo e claro, explicando o porquê das notas atribuídas.

Competências a serem avaliadas:

1.
Domínio da escrita formal da língua portuguesa: Avalie a adequação às regras de ortografia (acentuação, uso de hífen, maiúsculas/minúsculas, separação silábica), regência verbal e nominal, concordância verbal e nominal, pontuação, paralelismo, emprego de pronomes e crase. Identifique e explique os desvios gramaticais e de convenção da escrita, e seu impacto na clareza e formalidade do texto.

2.
Compreender o tema e não fugir do que é proposto: Verifique se o tema foi abordado de forma completa, sem tangenciamento ou fuga. A redação deve demonstrar compreensão do núcleo das ideias e manter o foco na delimitação proposta. Justifique a nota com base na pertinência e profundidade da abordagem temática.

3.
Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista: Analise a clareza da tese, a relevância e a pertinência dos argumentos, e a solidez da defesa do ponto de vista. Forneça feedback sobre a estrutura argumentativa e a organização das ideias.

4.
Conhecimento dos mecanismos linguísticos necessários para a construção da argumentação: Avalie a estruturação lógica e formal entre as partes da redação. Verifique o uso adequado de elementos coesivos (preposições, conjunções, advérbios, locuções adverbiais) para garantir a sequência coerente do texto e a interdependência entre as ideias. O feedback deve abordar a fluidez e a progressão textual.

5.
Respeito aos direitos humanos: Verifique a presença, a clareza, a exequibilidade e o respeito aos direitos humanos na proposta de intervenção. A proposta deve ser detalhada (agente, ação, meio, finalidade e detalhamento). Forneça feedback sobre a qualidade e a adequação da solução apresentada.

--- Redação a ser avaliada --- 

{text}
"""
    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
        json={"model": "gemma3:1b", "prompt": prompt, "stream": False},
        timeout=120,
    )
    result = response.json()
    return result.get("response", "Não foi possível gerar feedback.")


@app.route("/analyze-competencies", methods=["POST"])
def analyze_competencies():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "Texto não fornecido"}), 400

        # Chama o modelo LLM via Ollama
        llm_feedback = gerar_feedback_ollama(text)

        return jsonify({"llm_feedback": llm_feedback, "service": "trained-model"})

    except Exception as e:
        return (
            jsonify({"success": False, "error": str(e), "service": "trained-model"}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
