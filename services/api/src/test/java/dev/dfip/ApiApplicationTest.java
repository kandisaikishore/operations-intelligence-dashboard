package dev.dfip;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class ApiApplicationTest {
    @Autowired
    private MockMvc mvc;

    @Test
    void dashboardIsServedFromApplicationRoot() throws Exception {
        mvc.perform(get("/"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("Operations Intelligence")));
    }

    @Test
    void apiHealthEndpointResponds() throws Exception {
        mvc.perform(get("/api/v1/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("ok"))
                .andExpect(jsonPath("$.service").value("dfip-api"));
    }

    @Test
    void analyticsEndpointReturnsExpectedSections() throws Exception {
        mvc.perform(get("/api/v1/analytics"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.summary.total_incidents").exists())
                .andExpect(jsonPath("$.by_category").isArray())
                .andExpect(jsonPath("$.last_30_days").isArray());
    }

    @Test
    void incidentHistoryEndpointReturnsArray() throws Exception {
        mvc.perform(get("/api/v1/incidents").param("limit", "500"))
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$").isArray());
    }
}
