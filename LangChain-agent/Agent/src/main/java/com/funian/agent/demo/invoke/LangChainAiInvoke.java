package com.funian.agent.demo.invoke;

import dev.langchain4j.community.model.dashscope.QwenChatModel;
import dev.langchain4j.model.chat.ChatLanguageModel;

/**
 * @Auther FuNian
 * @Major Computer Software
 */
public class LangChainAiInvoke {

    public static void main(String[] args) {
        ChatLanguageModel qwenChatModel = QwenChatModel.builder()
                .apiKey(TestApiKey.API_KEY)
                .modelName("qwen-turbo")
                .build();
        String answer = qwenChatModel.chat("我是爱健身的大学生");
        System.out.println(answer);
    }
}
