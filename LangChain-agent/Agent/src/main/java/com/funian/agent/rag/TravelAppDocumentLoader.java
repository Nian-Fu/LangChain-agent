package com.funian.agent.rag;

import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.markdown.MarkdownDocumentReader;
import org.springframework.ai.reader.markdown.config.MarkdownDocumentReaderConfig;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.ResourcePatternResolver;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * @Auther FuNian
 * @Major Computer Software
 */
/**
 * 旅游大师应用文档加载器
 *
 * 负责从 classpath 中加载指定目录下的 Markdown 文档（.md），
 * 并提取元数据信息（如文件名和状态标签），用于后续检索增强生成（RAG）流程。
 */
@Component
@Slf4j
public class TravelAppDocumentLoader {

    /**
     * Spring 的资源模式解析器，用于匹配并获取资源路径下的文件列表
     */
    private final ResourcePatternResolver resourcePatternResolver;

    /**
     * 构造函数注入 ResourcePatternResolver 实例
     *
     * @param resourcePatternResolver Spring 提供的资源解析器
     */
    public TravelAppDocumentLoader(ResourcePatternResolver resourcePatternResolver) {
        this.resourcePatternResolver = resourcePatternResolver;
    }

    /**
     * 加载所有 Markdown 格式的文档，并将其转换为 Document 对象列表
     *
     * 每个文档会附加以下元数据：
     * - filename：原始文件名
     * - status：从文件名倒数第 6 至第 4 个字符提取的状态标签
     *
     * @return 包含所有文档内容与元数据的 Document 列表
     */
    public  List<Document> loadMarkdowns() {
        List<Document> allDocuments = new ArrayList<>();
        try {
            // 获取 classpath 下 document 目录中的所有 .md 文件
            Resource[] resources = resourcePatternResolver.getResources("classpath:document/*.md");

            for (Resource resource : resources) {
                String filename = resource.getFilename();

                // 提取文件名倒数第 6 至第 4 个字符作为状态标签（例如“草稿”或“上线”）
                String status = filename.substring(filename.length() - 6, filename.length() - 4);

                // 配置 Markdown 解析参数
                MarkdownDocumentReaderConfig config = MarkdownDocumentReaderConfig.builder()
                        .withHorizontalRuleCreateDocument(true)  // 将水平线分割的内容也视为独立段落
                        .withIncludeCodeBlock(false)              // 不包含代码块内容
                        .withIncludeBlockquote(false)             // 不包含引用块内容
                        .withAdditionalMetadata("filename", filename) // 添加文件名元数据
                        .withAdditionalMetadata("status", status)     // 添加状态标签元数据
                        .build();

                // 创建 Markdown 文档读取器
                MarkdownDocumentReader markdownDocumentReader = new MarkdownDocumentReader(resource, config);

                // 读取文档内容并添加到总列表中
                allDocuments.addAll(markdownDocumentReader.get());
            }
            log.info("Markdown 文档加载成功");
        } catch (IOException e) {
            log.error("Markdown 文档加载失败", e);
        }
        return allDocuments;
    }
}
