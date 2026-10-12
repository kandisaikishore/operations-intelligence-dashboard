package dev.dfip;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.client.RestClient;

@RestController
@RequestMapping("/api/v1")
public class IncidentController {
    private final RestClient analyzer;
    public IncidentController(@Value("${dfip.analyzer-url:http://localhost:8001}") String analyzerUrl) {
        this.analyzer = RestClient.builder().baseUrl(analyzerUrl).build();
    }

    @GetMapping("/health")
    public Map<String, Object> health() {
        return Map.of("status", "ok", "service", "dfip-api", "timestamp", Instant.now().toString());
    }

    @PostMapping("/analyze")
    public Map<?, ?> analyze(@RequestBody AnalyzeRequest request) {
        if (request.repository() == null || request.repository().isBlank()
                || request.runId() == null || request.runId().isBlank()
                || request.logText() == null || request.logText().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "repository, runId and logText are required");
        }
        try {
            return analyzer.post().uri("/analyze")
                .body(Map.of("repository", request.repository(), "run_id", request.runId(), "log_text", request.logText()))
                .retrieve().body(Map.class);
        } catch (Exception ex) {
            throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "Analyzer service is unavailable", ex);
        }
    }

    public record AnalyzeRequest(String repository, String runId, String logText) {}
}
