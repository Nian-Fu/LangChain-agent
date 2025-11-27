package com.funian.agent.advisor;

import org.springframework.ai.chat.client.advisor.api.*;
import reactor.core.publisher.Flux;

import java.util.HashMap;
import java.util.Map;

/**
 * 自定义 Re2 Advisor
 * 可提高大型语言模型的推理能力
 */
public class ReReadingAdvisor implements CallAroundAdvisor, StreamAroundAdvisor {

    /**
     * 在处理请求之前调用，用于改写用户输入的 Prompt。
     * 通过将原始查询插入两次，让 AI 模型重新审视问题，以提升推理准确性。
     *
     * @param advisedRequest 用户的原始请求对象
     * @return 改写后的请求对象
     */
    private AdvisedRequest before(AdvisedRequest advisedRequest) {

        // 复制原有的用户参数，并新增一个 re2_input_query 参数保存原始查询
        Map<String, Object> advisedUserParams = new HashMap<>(advisedRequest.userParams());
        advisedUserParams.put("re2_input_query", advisedRequest.userText());

		// 更新上下文，多个拦截器全局可使用
//	advisedRequest = advisedRequest.updateContext(context -> {
//		context.put("key", "value");
//		return context;
//	});

        // 修改用户输入文本，在原始内容后添加“Read the question again: ...”
        return AdvisedRequest.from(advisedRequest)
            .userText("""
                {re2_input_query}
                Read the question again: {re2_input_query}
                """)
            .userParams(advisedUserParams)
            .build();
    }

    /**
     * 处理同步请求的方法
     * 调用链中下一个 Advisor 或最终目标
     *
     * @param advisedRequest 用户的请求对象
     * @param chain 请求处理链
     * @return AI 模型的响应对象
     */
    @Override
    public AdvisedResponse aroundCall(AdvisedRequest advisedRequest, CallAroundAdvisorChain chain) {
        // 在发送请求前对请求进行改写，然后继续执行调用链
        return chain.nextAroundCall(this.before(advisedRequest));
    }

    /**
     * 处理流式请求的方法（如 Flux 流）
     * 适用于需要逐步接收响应数据的场景
     *
     * @param advisedRequest 用户的请求对象
     * @param chain 请求处理链
     * @return 包含多个响应片段的 Flux 流
     */
    @Override
    public Flux<AdvisedResponse> aroundStream(AdvisedRequest advisedRequest, StreamAroundAdvisorChain chain) {
        // 在发送请求前对请求进行改写，然后继续执行调用链
        return chain.nextAroundStream(this.before(advisedRequest));
    }

    /**
     * 定义此 Advisor 在执行链中的顺序
     * 数值越小，优先级越高
     *
     * @return 返回 0 表示该 Advisor 具有默认优先级
     */
    @Override
    public int getOrder() {
        return 0;
    }

    /**
     * 获取当前 Advisor 的名称，通常用于标识或调试
     *
     * @return 当前类的简单类名
     */
    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }
}
