from sentence_transformers import SentenceTransformer, util

# 1. Carrega o modelo (na primeira vez vai fazer o download)
print("A carregar o modelo...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. A sua base de conhecimento (simulando a leitura do ficheiro)
base = [
    "O horário de trabalho na empresa é das 09:00 às 18:00, de segunda a sexta.",
    "Para pedir reembolso de viagens, deve anexar os recibos no portal do RH até ao dia 5.",
    "A password do Wi-Fi para convidados é 'CafeComLeite2024'."
]

# 3. Gerar os embeddings (RF01)
embeddings_base = model.encode(base, convert_to_tensor=True)

# 4. Simular uma pergunta do utilizador
pergunta = "Qual o horário de trabalho na empresa?" 
# Note que não usei a palavra "horário", mas a IA vai entender o significado.

embedding_pergunta = model.encode(pergunta, convert_to_tensor=True)

# 5. Calcular a similaridade (RF02)
scores = util.cos_sim(embedding_pergunta, embeddings_base)[0]
melhor_indice = scores.argmax().item()

# 6. Mostrar o resultado
print(f"\nPergunta: {pergunta}")
print(f"Resposta sugerida: {base[melhor_indice]}")
print(f"Confiança: {scores[melhor_indice].item():.4f}")