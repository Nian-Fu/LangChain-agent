package com.funian.agent.rag;

import jakarta.annotation.Resource;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

/**
 * @Auther FuNian
 * @Date 2025/7/2 18:38
 * @ClassName:TravelAppDocumentLoaderTest
 * @School SiChuan University
 * @Major Computer Software
 */
@SpringBootTest
class TravelAppDocumentLoaderTest {

    @Resource
    private TravelAppDocumentLoader TravelAppDocumentLoader;

    @Test
    void loadMarkdowns() {
        TravelAppDocumentLoader.loadMarkdowns();
    }
}
