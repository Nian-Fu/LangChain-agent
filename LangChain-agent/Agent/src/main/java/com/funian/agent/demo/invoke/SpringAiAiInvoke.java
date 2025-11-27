package com.funian.agent.demo.invoke;

import jakarta.annotation.Resource;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

/**
 * @Auther FuNian
 * @Major Computer Software
 */

/**
 * Spring AI 框架调用 AI 大模型（阿里）
 */
// 取消注释后，项目启动时会执行
//@Component
public class SpringAiAiInvoke implements CommandLineRunner {

    // 实现单次执行的run方法
    @Resource
    // 一定要是阿里云积的chatmodel
    private ChatModel dashscopeChatModel;

    @Override
    public void run(String... args) throws Exception {
        AssistantMessage assistantMessage = dashscopeChatModel.call(new Prompt("你好，我是爱健身的大学生"))
                .getResult()
                .getOutput();
        System.out.println(assistantMessage.getText());
    }
}
