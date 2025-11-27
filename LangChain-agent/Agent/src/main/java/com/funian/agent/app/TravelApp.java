package com.funian.agent.app;

import com.funian.agent.advisor.MyLoggerAdvisor;
import com.funian.agent.advisor.ReReadingAdvisor;
import com.funian.agent.chatmemory.FileBasedChatMemory;
import com.funian.agent.rag.PgVectorVectorStoreConfig;
import com.funian.agent.rag.QueryRewriter;
import com.funian.agent.rag.TravelAppRagCustomAdvisorFactory;
import jakarta.annotation.Resource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.client.advisor.QuestionAnswerAdvisor;
import org.springframework.ai.chat.client.advisor.SimpleLoggerAdvisor;
import org.springframework.ai.chat.client.advisor.api.Advisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.InMemoryChatMemory;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;

import java.util.List;

import static org.springframework.ai.chat.client.advisor.AbstractChatMemoryAdvisor.CHAT_MEMORY_CONVERSATION_ID_KEY;
import static org.springframework.ai.chat.client.advisor.AbstractChatMemoryAdvisor.CHAT_MEMORY_RETRIEVE_SIZE_KEY;
/**
 * @Auther FuNian
 * @Major Computer Software
 */

@Component
@Slf4j
public class TravelApp {

    private final ChatClient chatClient;

    private static final String SYSTEM_PROMPT = "你是一位专注于中国、日本、美国三地的资深旅游规划专家，"
            + "需具备扎实的目的地知识储备与灵活的行程设计能力。" +
            "你的核心任务是根据用户需求，提供精准、实用、个性化的旅游规划方案，涵盖行程设计、信息查询、避坑建议等全流程服务";

    /**
     * 初始化 ChatClient 根据名称注入大模型
     *
     * @param dashscopeChatModel
     */
    public TravelApp(ChatModel dashscopeChatModel) {
//        // 初始化基于文件的对话记忆
        String fileDir = System.getProperty("user.dir") + "/tmp/chat-memory";
        ChatMemory chatMemory = new FileBasedChatMemory(fileDir);
         // 初始化基于内存的对话记忆
//        ChatMemory chatMemory = new InMemoryChatMemory();
        chatClient = ChatClient.builder(dashscopeChatModel)
                .defaultSystem(SYSTEM_PROMPT)
                .defaultAdvisors(
                        new MessageChatMemoryAdvisor(chatMemory)
//                        , new SimpleLoggerAdvisor()
                        // 自定义日志 Advisor，可按需开启
                         ,new MyLoggerAdvisor()
//                      自定义推理增强 Advisor，可按需开启
//                        ,new ReReadingAdvisor()
                )
                .build();
    }


    /**
     * AI 基础对话（支持多轮对话记忆）
     *
     * @param message
     * @param chatId
     * @return
     */
    public String doChat(String message, String chatId) {
        ChatResponse chatResponse = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
                // 制定历史消息的条数，默认为 10
                .call()
                .chatResponse();
        String content = chatResponse.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }


    record TravelReport(String title, List<String> suggestions) {
    }

        /**
     * AI 旅游报告功能（实战结构化输出）
     *
     * @param message
     * @param chatId
     * @return
     */
    public TravelReport doChatWithReport(String message, String chatId) {
        TravelReport TravelReport = chatClient
                .prompt()
                .system(SYSTEM_PROMPT + "每次对话后都要生成旅游结果，标题为{用户名}的旅游报告，内容为建议列表")
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
                .call()
                // 结构化输出
                .entity(TravelReport.class);
        log.info("TravelReport: {}", TravelReport);
        return TravelReport;
    }


    // AI 旅游知识库问答功能
    @Resource
    private VectorStore travelAppVectorStore;

    @Resource
    private Advisor travelAppRagCloudAdvisor;

    @Resource
    private VectorStore pgVectorVectorStore;

    @Resource
    private QueryRewriter queryRewriter;

    /**
     * 和 RAG 知识库进行对话
     *
     * @param message
     * @param chatId
     * @return
     */
    public String doChatWithRag(String message, String chatId) {
        // 查询重写器
        String rewrittenMessage = queryRewriter.doQueryRewrite(message);
        log.info("rewrittenMessage: {}", rewrittenMessage);
        ChatResponse chatResponse = chatClient
                .prompt()
                // 使用改写后的查询
                .user(rewrittenMessage)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
                // 开启日志，便于观察效果
                .advisors(new MyLoggerAdvisor())
                // 应用内存 RAG 知识库问答
                .advisors(new QuestionAnswerAdvisor(travelAppVectorStore))
                // 应用 RAG 检索增强服务（基于云知识库服务）
//                .advisors(travelAppRagCloudAdvisor)
                // 应用 RAG 检索增强服务（基于 PgVector 向量存储）
//                .advisors(new QuestionAnswerAdvisor(pgVectorVectorStore))
                // 应用自定义的 RAG 检索增强服务（文档查询器 + 上下文增强器）
                .advisors(
                        TravelAppRagCustomAdvisorFactory.createTravelAppRagCustomAdvisor(
                                travelAppVectorStore, "中国"
                        )
                )
                .call()
                .chatResponse();
        String content = chatResponse.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }
//
//    /**
//     * AI 基础对话（支持多轮对话记忆，SSE 流式传输）
//     *
//     * @param message
//     * @param chatId
//     * @return
//     */
//    public Flux<String> doChatByStream(String message, String chatId) {
//        // 查询重写器
//        String rewrittenMessage = queryRewriter.doQueryRewrite(message);
//        return chatClient
//                .prompt()
//                // 使用改写后的查询
//                .user(rewrittenMessage)
//                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
//                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
//                // 开启日志，便于观察效果
//                .advisors(new MyLoggerAdvisor())
//                // 应用内存 RAG 知识库问答
////                .advisors(new QuestionAnswerAdvisor(travelAppVectorStore))
//                // 应用 RAG 检索增强服务（基于云知识库服务）
////                .advisors(travelAppRagCloudAdvisor)
//                // 应用 RAG 检索增强服务（基于 PgVector 向量存储）
//                .advisors(new QuestionAnswerAdvisor(pgVectorVectorStore))
//                // 应用自定义的 RAG 检索增强服务（文档查询器 + 上下文增强器）
//                .advisors(
//                        TravelAppRagCustomAdvisorFactory.createTravelAppRagCustomAdvisor(
//                                pgVectorVectorStore, "中国"
//                        )
//                )
//                .stream()
//                .content();
//    }


    /**
     * AI 基础对话（支持多轮对话记忆，SSE 流式传输）
     *
     * @param message
     * @param chatId
     * @return
     */
    public Flux<String> doChatByStream(String message, String chatId) {
        // 查询重写器
        String rewrittenMessage = queryRewriter.doQueryRewrite(message);
        return chatClient
                .prompt()
                // 使用改写后的查询
                .user(rewrittenMessage)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))

//                .advisors(
//                        TravelAppRagCustomAdvisorFactory.createTravelAppRagCustomAdvisor(
//                                travelAppVectorStore, "中国日本美国"
//                        )
//                )
//                .advisors(new QuestionAnswerAdvisor(travelAppVectorStore))
                .advisors(new QuestionAnswerAdvisor(travelAppVectorStore))
                .stream()
                .content();
    }

    // AI 调用 MCP 服务

    @Resource
    private ToolCallbackProvider toolCallbackProvider;

    /**
     * AI 旅游报告功能（调用 MCP 服务）
     *
     * @param message
     * @param chatId
     * @return
     */
    public String doChatWithMcp(String message, String chatId) {
        ChatResponse chatResponse = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
                // 开启日志，便于观察效果
                .advisors(new MyLoggerAdvisor())
                .tools(toolCallbackProvider)
                .call()
                .chatResponse();
        String content = chatResponse.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }


    // AI 调用工具能力
    @Resource
    private ToolCallback[] allTools;

    /**
     * AI 旅游报告功能（支持调用工具）
     *
     * @param message
     * @param chatId
     * @return
     */
    public String doChatWithTools(String message, String chatId) {
        ChatResponse chatResponse = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
                // 开启日志，便于观察效果
                .advisors(new MyLoggerAdvisor())
                .tools(allTools)
                .call()
                .chatResponse();
        String content = chatResponse.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }

}
