package com.funian.agent.tools;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

/**
 * @Auther FuNian
 * @ClassName:WebSearchToolTest
 */

@SpringBootTest
public class WebSearchToolTest {

    @Test
    public void testSearchWeb() {
        WebSearchTool tool = new WebSearchTool("oJQtz4cpK4QgbfjyGV7Vsw6g");
        String query = "Spring AI官网";
        String result = tool.searchWeb(query);
        assertNotNull(result);
    }
}
