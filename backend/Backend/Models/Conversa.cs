using System;

namespace Backend.Models
{
    public class Conversa
    {
        public int Id { get; set; }

        public string SessionId { get; set; } = string.Empty;

        public string Pergunta { get; set; } = string.Empty;

        public string Resposta { get; set; } = string.Empty;

        public DateTime DataCriacao { get; set; } = DateTime.UtcNow;
    }
}
