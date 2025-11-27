package com.funian.agent.rag;

import jakarta.annotation.Resource;
import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

/**
 * @Auther FuNian
 * @Major Computer Software
 * 基于内存的向量数据库，调用embedding模型 ,自动的模型注入
 */
@Configuration
public class TravelAppVectorStoreConfig {

    @Resource
    private TravelAppDocumentLoader travelAppDocumentLoader;

//    @Resource
//    private PgVectorVectorStoreConfig pgVectorVectorStoreConfig;

    @Resource
    private MyKeywordEnricher myKeywordEnricher;
    private EmbeddingModel dashscopeEmbeddingModel;
    @Resource
    private MyTokenTextSplitter myTokenTextSplitter;

    @Bean
    VectorStore travelAppVectorStore(EmbeddingModel dashscopeEmbeddingModel) {
        this.dashscopeEmbeddingModel = dashscopeEmbeddingModel;
        SimpleVectorStore simpleVectorStore = SimpleVectorStore.builder(dashscopeEmbeddingModel).build();
        // 加载文档
        List<Document> documentList = travelAppDocumentLoader.loadMarkdowns();
        // 自主切分文档
       List<Document> splitDocuments = myTokenTextSplitter.splitCustomized(documentList);
        // 自动补充关键词元信息、增强器
        List<Document> enrichedDocuments = myKeywordEnricher.enrichDocuments(documentList);
        simpleVectorStore.add(documentList);
//        pgVectorVectorStoreConfig.pgVectorVectorStore(documentList);
        return simpleVectorStore;
    }
}
