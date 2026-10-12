package dev.dfip;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.client.RestClient;
@RestController @RequestMapping("/api/v1")
public class IncidentController {
 private final RestClient analyzer; private final JdbcTemplate jdbc; private final ObjectMapper mapper;
 public IncidentController(@Value("${dfip.analyzer-url:http://localhost:8001}") String analyzerUrl, JdbcTemplate jdbc, ObjectMapper mapper) { this.analyzer=RestClient.builder().baseUrl(analyzerUrl).build(); this.jdbc=jdbc; this.mapper=mapper; }
 @GetMapping("/health") public Map<String,Object> health() { return Map.of("status","ok","service","dfip-api","timestamp",Instant.now().toString()); }
 @PostMapping("/analyze") public Map<?,?> analyze(@RequestBody AnalyzeRequest request) {
  if(request.repository()==null||request.repository().isBlank()||request.runId()==null||request.runId().isBlank()||request.logText()==null||request.logText().isBlank()) throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"repository, runId and logText are required");
  try {
   Map<?,?> diagnosis=analyzer.post().uri("/analyze").body(Map.of("repository",request.repository(),"run_id",request.runId(),"log_text",request.logText())).retrieve().body(Map.class);
   if(diagnosis==null) throw new ResponseStatusException(HttpStatus.BAD_GATEWAY,"Analyzer returned an empty response");
   long id=jdbc.queryForObject("INSERT INTO incidents(repository,run_id,category,summary,confidence,evidence,recommended_actions,needs_human_review) VALUES(?,?,?,?,?,?::jsonb,?::jsonb,?) ON CONFLICT(repository,run_id) DO UPDATE SET category=EXCLUDED.category,summary=EXCLUDED.summary,confidence=EXCLUDED.confidence,evidence=EXCLUDED.evidence,recommended_actions=EXCLUDED.recommended_actions,needs_human_review=EXCLUDED.needs_human_review RETURNING id",Long.class,request.repository(),request.runId(),diagnosis.get("category"),diagnosis.get("summary"),diagnosis.get("confidence"),json(diagnosis.get("evidence")),json(diagnosis.get("recommended_actions")),diagnosis.get("needs_human_review"));
   Map<String,Object> result=new HashMap<>(); diagnosis.forEach((k,v)->result.put(String.valueOf(k),v)); result.put("incident_id",id); return result;
  } catch(ResponseStatusException ex) { throw ex; } catch(Exception ex) { throw new ResponseStatusException(HttpStatus.BAD_GATEWAY,"Analysis or incident persistence failed",ex); }
 }
 @GetMapping("/incidents") public List<Map<String,Object>> incidents(@RequestParam(defaultValue="50") int limit) { int safeLimit=Math.max(1,Math.min(limit,200)); return jdbc.queryForList("SELECT id,repository,run_id,category,summary,confidence,evidence,recommended_actions,needs_human_review,created_at FROM incidents ORDER BY created_at DESC LIMIT ?",safeLimit); }
 @GetMapping("/analytics") public Map<String,Object> analytics() {
  Map<String,Object> summary=jdbc.queryForMap("SELECT COUNT(*) AS total_incidents,COUNT(*) FILTER (WHERE needs_human_review) AS needs_review,COUNT(*) FILTER (WHERE NOT needs_human_review) AS classified,ROUND(COALESCE(AVG(confidence),0)::numeric,3) AS average_confidence FROM incidents");
  List<Map<String,Object>> categories=jdbc.queryForList("SELECT category,COUNT(*) AS count FROM incidents GROUP BY category ORDER BY count DESC");
  List<Map<String,Object>> daily=jdbc.queryForList("SELECT date_trunc('day',created_at)::date AS day,COUNT(*) AS count FROM incidents WHERE created_at >= NOW() - INTERVAL '30 days' GROUP BY day ORDER BY day");
  return Map.of("summary",summary,"by_category",categories,"last_30_days",daily);
 }
 private String json(Object value) { try { return mapper.writeValueAsString(value==null?java.util.List.of():value); } catch(JsonProcessingException ex) { throw new IllegalArgumentException("Could not serialize diagnosis evidence",ex); } }
 public record AnalyzeRequest(String repository,String runId,String logText) {}
}