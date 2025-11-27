package com.funian.agent.tools;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

/**
 * @Auther FuNian
 * @ClassName:PDFGenerationToolTest
 */
@SpringBootTest
class PDFGenerationToolTest {

    @Test
    public void testGeneratePDF() {
        PDFGenerationTool tool = new PDFGenerationTool();
        String fileName = "Spring  AI.pdf";
        String content = "Spring  AI项目 https://docs.spring.io/spring-ai/reference/api/chat/comparison.html";
        String result = tool.generatePDF(fileName, content);
        assertNotNull(result);
    }
}
