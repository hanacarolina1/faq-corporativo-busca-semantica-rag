import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");

  async function sendQuestion() {
    if (!question.trim()) return;

    // adiciona mensagem do usuário
    setMessages(prev => [...prev, { from: "user", text: question }]);

    try {
      const res = await fetch("http://localhost:5223/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question,
          sessionId: "user1"
        })
      });

      const data = await res.json();

      // adiciona resposta do bot
      setMessages(prev => [...prev, { from: "bot", text: data.answer }]); 
    } catch (err) {
      setMessages(prev => [...prev, { from: "bot", text: "Erro ao conectar com backend" }]);
    }

    setQuestion("");
  }

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", background: "white", padding: 20, borderRadius: 8 }}>
      <h2>FAQ Corporativo</h2>

      <div
        style={{
          height: 350,
          border: "1px solid #ccc",
          padding: 10,
          display: "flex",
          flexDirection: "column",
          gap: 8,
          overflowY: "auto"
        }}
      >
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              alignSelf: m.from === "user" ? "flex-end" : "flex-start",
              background: m.from === "user" ? "#cce5ff" : "#eee",
              padding: 8,
              borderRadius: 6,
              maxWidth: "80%"
            }}
          >
            {m.text}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
        <input
          style={{ flex: 1, padding: 8 }}
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Digite sua pergunta"
          onKeyDown={e => e.key === "Enter" && sendQuestion()}
        />

        <button onClick={sendQuestion}>Enviar</button>
      </div>
    </div>
  );
}

export default App;


