namespace Backend.DTOs;

public class PythonResponse
{
    public string pergunta_recebida { get; set; } = string.Empty;
    public string resposta { get; set; } = string.Empty;
    public double confianca { get; set; }
}
