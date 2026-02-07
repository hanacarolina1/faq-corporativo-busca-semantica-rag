from fastapi import APIRouter
from sentence_transformers import SentenceTransformer, util
import os

router = APIRouter(prefix="/faq")

model = SentenceTransformer('all-MiniLM-L6-v2')

def carregar_base():
    #para carregar arquivos
    caminho_base="base_conhecimento.txt" #fala onde armazena as perguntas e respostas
    if not os.path.exists(caminho_base): #perguntando pro sistema se o arquivo existe dentro da pasta mesmo e faz o programa nao quebrar
        return[] #se n tiver nada ele retorna uma lista vazia
    with open(caminho_base, "r", encoding="utf-8") as f:#abre a base de conhecimento pra leitura e o with serve pra fechar o arquivo assim que ler e nao gastar memoria atoa
        return[linha.strip() for linha in f.readlines() if linha.strip()]#linha.strip remove os espaços em branco desnecessarios f.readlines le todas as linhas e deixa em lista  if.linha.strip ignora as linhas vazias pra nao virar vetor vzaio
    
    @router.post("/perguntar")
    def buscar_resposta(pergunta_usuario: str):
        base = carregar_base()
        if not base:
            return {"erro": "A Base de Conhecimento está vazia ou não foi encontrada."}
        
        embeddings_base = model.encode(base, convert_to_tensor=True)#transforma o texto na base em vetores
    embedding_pergunta = model.encode(pergunta_usuario, convert_to_tensor=True)#transforma o texto da pergunta do usuario em vetores
    
    scores = until.cos_sim(embedding_pergunta, embeddings_base)[0] #scores é igual à similaridade dos cossenos dos embeddings da pergunta e da base
    
    melhor_match_idx = scores.arg.max().item() #quem ganhou a comparação é dada por score(lista dos vetores) arg.max(uma funcao que percorre a lista e fala que o maior valor ta na posição tal) e .item(transforma o resultado de arg.max em número inteiro) 
    return {
        "pergunta_recebida": pergunta_usuario,#pega a pergunta do usuario
        "resposta": base[melhor_match_idx],#pega o texto que recebeu melhor_match_idx
        "confianca": round(float(scores[melhor_match_idx]), 4)#confianca(mostra o quao certeira é a resposta) scores[melhor_match_idx](pega o valor da similaridade) float(faz o numero ser decimal) round[4](faz com que tenha no maximo 4 casas decimais)
    }
    