package com.funian.agent.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @Auther FuNian
 * @Date 2025/7/2 12:52
 * @ClassName:hetalth
 * @School SiChuan University
 * @Major Computer Software
 */
@RestController
@RequestMapping("/health")
public class HealthController {

    @GetMapping
    public String healthCheck() {
        return "我是付念，测试成功";
    }
}
