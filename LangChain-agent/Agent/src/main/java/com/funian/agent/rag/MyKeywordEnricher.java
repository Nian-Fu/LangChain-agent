package com.funian.agent.rag;

import jakarta.annotation.Resource;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.document.Document;
import org.springframework.ai.transformer.KeywordMetadataEnricher;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * @Auther FuNian
 * @Date 2025/7/3 17:44
 * @ClassName: MyKeywordEnricher
 * @School SiChuan University
 * @Major Computer Software
 */

/**
 * 基于 AI 的文档元信息增强器
 *
 * 该组件使用大语言模型（LLM）为文档自动提取关键词，并将这些关键词作为元数据添加到文档中，
 * 以提升后续检索时的匹配准确率和语义相关性。
 */
@Component
public class MyKeywordEnricher {

    /**
     * 注入 ChatModel 实例，用于调用大语言模型执行关键词提取任务
     */
    @Resource
    private ChatModel dashscopeChatModel;

    /**
     * 对传入的文档列表进行关键词提取并丰富其元数据
     *
     * 每个文档将通过 LLM 提取最多 5 个关键词，并将这些关键词加入到文档的 metadata 中，
     * 可用于后续基于关键词的检索或过滤操作。
     *
     * @param documents 待增强的文档列表
     * @return 已添加关键词元数据的文档列表
     */
    public List<Document> enrichDocuments(List<Document> documents) {
        // 创建 KeywordMetadataEnricher 实例，指定使用的 ChatModel 和关键词数量
        KeywordMetadataEnricher keywordMetadataEnricher = new KeywordMetadataEnricher(dashscopeChatModel, 5);

        // 应用增强器处理文档，返回已添加关键词元数据的新文档列表
        return keywordMetadataEnricher.apply(documents);
    }
}
