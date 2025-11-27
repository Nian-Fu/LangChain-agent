package com.funian.agent.demo.rag;

import jakarta.annotation.Resource;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.ai.rag.Query;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * @Auther FuNian
 * @Date 2025/7/3 18:00
 * @ClassName:MultiQueryExpanderDemoTest
 * @School SiChuan University
 * @Major Computer Software
 */
@SpringBootTest
class MultiQueryExpanderDemoTest {

    @Resource
    private MultiQueryExpanderDemo multiQueryExpanderDemo;


    @Test
    void expand() {
        List<Query> queries = multiQueryExpanderDemo.expand("啥是职业旅游？请回答我哈哈哈哈");
        Assertions.assertNotNull(queries);
    }
}
