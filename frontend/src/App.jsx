import React, { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";
import "./index.css"; // Importar o CSS global

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5004";

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setText(""); // Limpa o texto se um arquivo for carregado
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "image/jpeg": [],
      "image/png": [],
      "application/pdf": [],
    },
    multiple: false,
  });

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    const formData = new FormData();

    if (file) {
      formData.append("image", file);
    } else if (text) {
      formData.append("text", text);
    } else {
      setError("Por favor, insira um texto ou faça upload de um arquivo.");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post(
        `${API_URL}/process-redaction`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Resposta da API:", response.data);
      setAnalysisResult(response.data);
    } catch (err) {
      console.error("Erro ao processar redação:", err);
      setError(
        err.response?.data?.error ||
          "Erro ao processar redação. Tente novamente."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Sistema de Correção de Redações ENEM</h1>

      <div className="upload-section">
        <h2>Upload</h2>
        <textarea
          placeholder="Cole sua redação aqui ou digite..."
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            setFile(null); // Limpa o arquivo se o texto for digitado
          }}
        ></textarea>
        <div {...getRootProps()} className="dropzone">
          <input {...getInputProps()} />
          <p>
            Arraste e solte um arquivo aqui, ou clique para selecionar (JPG,
            PNG, PDF)
          </p>
          {file && <p>Arquivo selecionado: {file.name}</p>}
        </div>
        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Processando..." : "Analisar Redação"}
        </button>
        {error && <p className="error-message">{error}</p>}
      </div>

      {analysisResult && (
        <div className="analysis-section">
          <h2>Resultado da Análise</h2>
          <h3>Texto Extraído:</h3>
          <div className="result-box">
            <p>{analysisResult.extracted_text}</p>
          </div>

          {/* <h3>Análise de Competências:</h3>
          <div className="result-box">
            {analysisResult.analysis &&
              Object.keys(analysisResult.analysis).map((key) => (
                <div key={key}>
                  <strong>
                    {analysisResult.analysis[key].description || key}:
                  </strong>{" "}
                  {analysisResult.analysis[key].score} pontos
                  {analysisResult.analysis[key].errors &&
                    analysisResult.analysis[key].errors.length > 0 && (
                      <p>
                        Erros: {analysisResult.analysis[key].errors.join(", ")}
                      </p>
                    )}
                  {analysisResult.analysis[key].feedback &&
                    analysisResult.analysis[key].feedback.length > 0 && (
                      <p>
                        Feedback:{" "}
                        {analysisResult.analysis[key].feedback.join(", ")}
                      </p>
                    )}
                </div>
              ))}
            {analysisResult.analysis &&
              analysisResult.analysis.overall_score && (
                <p>
                  <strong>Pontuação Geral:</strong>{" "}
                  {analysisResult.analysis.overall_score.toFixed(2)}/1000
                </p>
              )}
          </div> */}

          <h3>Feedback Personalizado:</h3>
          <div className="result-box">
            {analysisResult.feedback &&
              analysisResult.feedback.personalized_feedback && (
                <>
                  <p>
                    {analysisResult.analysis.llm_feedback}
                  </p>
                </>
              )}
            {analysisResult.feedback &&
              analysisResult.feedback.content_recommendations &&
              analysisResult.feedback.content_recommendations.length > 0 && (
                <>
                  <h4>Recomendações de Conteúdo:</h4>
                  <ul>
                    {analysisResult.feedback.content_recommendations.map(
                      (rec, index) => (
                        <li key={index}>{rec}</li>
                      )
                    )}
                  </ul>
                </>
              )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
