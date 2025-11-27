package com.funian.agent.rag;

import com.alibaba.cloud.ai.dashscope.api.DashScopeApi;
import com.alibaba.cloud.ai.dashscope.rag.DashScopeDocumentRetriever;
import com.alibaba.cloud.ai.dashscope.rag.DashScopeDocumentRetrieverOptions;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.client.advisor.RetrievalAugmentationAdvisor;
import org.springframework.ai.chat.client.advisor.api.Advisor;
import org.springframework.ai.rag.retrieval.search.DocumentRetriever;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @Auther FuNian
 * @Date 2025/7/2 13:10
 * @ClassName: TravelAppRagCloudAdvisorConfig
 * @School SiChuan University
 * @Major Computer Software
 */

/**
 * 自定义基于阿里云 DashScope 知识库服务的 RAG（Retrieval-Augmented Generation）增强顾问配置类。
 *
 * 该类用于构建一个基于云端知识库检索的 Advisor 组件，供 ChatClient 使用，
 * 在用户提问时自动从指定的知识索引中检索相关信息，并将其注入到提示词中以增强模型输出。
 */
@Configuration
@Slf4j
public class TravelAppRagCloudAdvisorConfig {

    /**
     * 注入 DashScope API 的访问密钥，来源于 application.properties 或 application.yml 配置文件
     */
    @Value("${spring.ai.dashscope.api-key}")
    private String dashScopeApiKey;

    /**
     * 定义并注册一个自定义的 Advisor Bean，用于支持基于阿里云 DashScope 知识库的 RAG 增强功能。
     *
     * 此 Advisor 将在每次对话请求中触发文档检索流程，
     * 检索结果将作为上下文附加到 prompt 中，提升大模型回答的准确性与专业性。
     *
     * @return 返回配置好的 Advisor 实例
     */
    @Bean
    public Advisor TravelAppRagCloudAdvisor() {
        // 创建 DashScope API 客户端实例
        DashScopeApi dashScopeApi = new DashScopeApi(dashScopeApiKey);

        // 设置知识库索引名称，应与 DashScope 控制台中创建的索引一致
        final String KNOWLEDGE_INDEX = "旅游知识问答";

        // 创建文档检索器，用于从 DashScope 知识库中根据查询语句检索相关文档
        DocumentRetriever dashScopeDocumentRetriever = new DashScopeDocumentRetriever(
                dashScopeApi,
                DashScopeDocumentRetrieverOptions.builder()
                        .withIndexName(KNOWLEDGE_INDEX) // 指定使用的知识库索引
                        .build());

        // 构建并返回 RetrievalAugmentationAdvisor，集成文档检索能力到对话流程中
        return RetrievalAugmentationAdvisor.builder()
                .documentRetriever(dashScopeDocumentRetriever) // 设置检索器
                .build();
    }
}
