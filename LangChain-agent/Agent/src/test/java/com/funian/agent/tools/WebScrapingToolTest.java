package com.funian.agent.tools;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

/**
 * @Auther FuNian
 * @Major Computer Software
 */
@SpringBootTest
class WebScrapingToolTest {

    @Test
    void scrapeWebPage() {
        WebScrapingTool webScrapingTool = new WebScrapingTool();
        String url = "https://www.aliyun.com/resources?spm=5176.29677750.J_4VYgf18xNlTAyFFbOuOQe.d_menu_3.275b154aRdMaua";
        String result = webScrapingTool.scrapeWebPage(url);
        Assertions.assertNotNull(result);
    }
}

