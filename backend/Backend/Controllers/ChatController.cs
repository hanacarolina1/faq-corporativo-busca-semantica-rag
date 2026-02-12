using Microsoft.AspNetCore.Mvc;
using Backend.Data;
using Backend.DTOs;
using Backend.Models;
using System.Net.Http.Json;

namespace Backend.Controllers;

[ApiController]
[Route("api/chat")]
public class ChatController : ControllerBase
{
    private readonly AppDbContext _context;
    private readonly HttpClient _http;

    public ChatController(AppDbContext context, IHttpClientFactory factory)
    {
        _context = context;
        _http = factory.CreateClient();
    }

    [HttpPost]
    public async Task<IActionResult> Chat([FromBody] ChatRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.Question))
            return BadRequest("Pergunta é obrigatória");

        // 🔹 1. CACHE
        var cached = _context.Conversas
            .FirstOrDefault(c => c.Pergunta == req.Question);

        if (cached != null)
        {
            return Ok(new
            {
                answer = cached.Resposta,
                cached = true
            });
        }

        // 🔹 2. CHAMADA AO FASTAPI (POST + QUERY STRING)
        var url =
            $"http://localhost:8000/perguntar?pergunta_usuario={Uri.EscapeDataString(req.Question)}";

        HttpResponseMessage response;

        try
        {
            response = await _http.PostAsync(url, null); // ⚠️ POST SEM BODY
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Erro ao conectar no agente Python: {ex.Message}");
        }

        if (!response.IsSuccessStatusCode)
        {
            var erro = await response.Content.ReadAsStringAsync();
            return StatusCode(500, $"Erro do agente Python: {erro}");
        }

        // 🔹 3. LEITURA DA RESPOSTA
        var result = await response.Content.ReadFromJsonAsync<PythonResponse>();

        if (result == null || string.IsNullOrWhiteSpace(result.resposta))
            return StatusCode(500, "Resposta inválida do agente Python");

        // 🔹 4. SALVAR NO BANCO
        var conversa = new Conversa
        {
            Pergunta = req.Question,
            Resposta = result.resposta,
            SessionId = req.SessionId,
            DataCriacao = DateTime.UtcNow
        };

        _context.Conversas.Add(conversa);
        await _context.SaveChangesAsync();

        // 🔹 5. RETORNO FINAL
        return Ok(new
        {
            answer = result.resposta,
            confidence = result.confianca,
            cached = false
        });
    }
}
