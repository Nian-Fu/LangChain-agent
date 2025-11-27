package com.funian.agent.rag;

// 导入必要的类和接口
import jakarta.annotation.Resource;
import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.pgvector.PgVectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.List;

import static org.springframework.ai.vectorstore.pgvector.PgVectorStore.PgDistanceType.COSINE_DISTANCE;
import static org.springframework.ai.vectorstore.pgvector.PgVectorStore.PgIndexType.HNSW;

/**
 * 配置类：用于创建并配置基于 PgVector 的向量存储（VectorStore）
 *
 * @Auther FuNian
 * @Date 2025/7/2 20:56
 * @ClassName: PgVectorVectorStoreConfig
 * @School Sichuan University
 * @Major Computer Software
 */
//@Configuration // 当前被注释掉，表示该类暂未作为 Spring 配置类启用
public class PgVectorVectorStoreConfig {

    /**
     * 自定义文档加载器，用于从指定路径或资源中加载 Document 数据。
     * 使用 @Resource 注解自动注入 Bean 实例。
     */
    @Resource
    private TravelAppDocumentLoader travelAppDocumentLoader;

    /**
     * 定义一个名为 "pgVectorVectorStore" 的 Bean，返回类型为 VectorStore。
     * 此 Bean 是基于 PostgreSQL 的向量数据库实现的向量存储。
     *
     * @param jdbcTemplate           Spring 提供的 JDBC 模板，用于操作数据库
     * @param dashscopeEmbeddingModel 嵌入模型，用于将文本转换为向量
     * @return 返回构建好的 VectorStore 实例
     */
    @Bean
    public VectorStore pgVectorVectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel dashscopeEmbeddingModel) {

        // 使用 PgVectorStore.builder 构建向量存储实例
        VectorStore vectorStore = PgVectorStore.builder(jdbcTemplate, dashscopeEmbeddingModel)
                .dimensions(1536)                    // 设置向量维度，默认为 1536
                .distanceType(COSINE_DISTANCE)       // 设置距离计算方式为余弦相似度
                .indexType(HNSW)                     // 设置索引类型为 HNSW（高效近似最近邻搜索）
                .initializeSchema(true)              // 是否初始化数据库 schema（true 表示每次启动都重建）
                .schemaName("public")                // 指定数据库 schema 名称
                .vectorTableName("vector_store")     // 指定向量表名称
                .maxDocumentBatchSize(10000)         // 批量处理最大文档数量
                .build();                            // 构建完成

        // 加载文档到向量库（当前被注释，可用于初始化数据）
//        List<Document> documents = travelAppDocumentLoader.loadMarkdowns();
//        vectorStore.add(documents);

        return vectorStore;
    }
}
