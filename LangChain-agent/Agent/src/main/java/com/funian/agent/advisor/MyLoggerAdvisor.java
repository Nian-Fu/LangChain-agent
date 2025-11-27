package com.funian.agent.advisor;

import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.client.advisor.AbstractChatMemoryAdvisor;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.client.advisor.QuestionAnswerAdvisor;
import org.springframework.ai.chat.client.advisor.api.*;
import org.springframework.ai.chat.model.MessageAggregator;
import reactor.core.publisher.Flux;

/**
 * @Auther FuNian
 * @Major Computer Software
 */

/**
 * 自定义日志 Advisor
 * 打印 info 级别日志、只输出单次用户提示词和 AI 回复的文本，
 */
@Slf4j
public class MyLoggerAdvisor implements CallAroundAdvisor, StreamAroundAdvisor {

    /**
     * 获取当前 Advisor 的名称，通常用于标识或调试
     * @return 当前类的简单类名
     */
    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    /**
     * 定义此 Advisor 在执行链中的顺序
     * 数值越小，优先级越高
     * @return 返回 0 表示该 Advisor 具有默认优先级
     */
    @Override
    public int getOrder() {
        return 0;
    }

    /**
     * 在处理请求之前调用，用于记录用户的输入内容
     * @param request 用户的请求对象
     * @return 修改后的请求对象（这里直接返回原对象）
     */
    private AdvisedRequest before(AdvisedRequest request) {
        log.info("AI Request: {}", request.userText());
        return request;
    }

    /**
     * 在处理响应之后调用，用于记录 AI 模型的回复内容
     * @param advisedResponse AI 模型的响应对象
     */
    private void observeAfter(AdvisedResponse advisedResponse) {
        log.info("AI Response: {}", advisedResponse.response().getResult().getOutput().getText());
    }

    /**
     * 处理同步请求的方法
     * 调用链中下一个 Advisor 或最终目标
     * @param advisedRequest 用户的请求对象
     * @param chain 请求处理链
     * @return AI 模型的响应对象
     */
    @Override
    public AdvisedResponse aroundCall(AdvisedRequest advisedRequest, CallAroundAdvisorChain chain) {

        // 在请求处理前打印日志
        advisedRequest = before(advisedRequest);

        // 调用链中的下一个 Advisor 或实际处理逻辑
        AdvisedResponse advisedResponse = chain.nextAroundCall(advisedRequest);


//        // 读取多个拦截器的上下文
//        Object value = advisedResponse.adviseContext().get("key");

        // 在响应处理后打印日志
        observeAfter(advisedResponse);

        // 返回响应结果
        return advisedResponse;
    }

    /**
     * 处理流式请求的方法（如 Flux 流）
     * 适用于需要逐步接收响应数据的场景
     * @param advisedRequest 用户的请求对象
     * @param chain 请求处理链
     * @return 包含多个响应片段的 Flux 流
     */
    @Override
    public Flux<AdvisedResponse> aroundStream(AdvisedRequest advisedRequest, StreamAroundAdvisorChain chain) {

        // 在请求处理前打印日志
        advisedRequest = before(advisedRequest);

        // 调用链中的下一个 Advisor 或实际处理逻辑，获取响应流
        Flux<AdvisedResponse> advisedResponses = chain.nextAroundStream(advisedRequest);

        // 使用 MessageAggregator 将流式响应聚合，并在完成时调用 observeAfter 方法
        return new MessageAggregator().aggregateAdvisedResponse(advisedResponses, this::observeAfter);
    }
}
