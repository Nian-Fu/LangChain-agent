package com.funian.agent.demo.invoke;

import jakarta.annotation.Resource;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

/**
 * @Auther FuNian
 * @Date 2025/7/2 13:10
 * @ClassName: OllamaAiInvoke
 * @School SiChuan University
 * @Major Computer Software
 */

/**
 * Spring AI 框架调用 AI 大模型（Ollama）
 */
// 取消注释后，项目启动时会执行
//@Component
public class OllamaAiInvoke implements CommandLineRunner {

    @Resource
    private ChatModel ollamaChatModel;


    @Override
    public void run(String... args) throws Exception {
        AssistantMessage assistantMessage = ollamaChatModel.call(new Prompt("你好，我是爱健身的大学生，叫周杰伦"))
                .getResult()
                .getOutput();
        System.out.println(assistantMessage.getText());
    }
}
