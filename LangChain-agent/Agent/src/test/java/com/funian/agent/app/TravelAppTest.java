package com.funian.agent.app;

import jakarta.annotation.Resource;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.UUID;

/**
 * @Auther FuNian
 * @Date 2025/7/2 16:39
 * @ClassName:TravelAppTest
 * @School SiChuan University
 * @Major Computer Software
 */
@SpringBootTest
class TravelAppTest {


    @Resource
    private TravelApp TravelApp;

    @Test
    void testChat() {
        String chatId = UUID.randomUUID().toString();
        // 第一轮
        String message = "你好，我是爱健身的大学，给出夏天6月份9天8晚的印度尼西亚的旅游计划";
        String answer = TravelApp.doChat(message, chatId);
        // 第二轮
        message = "我想让去美国旅游";
        answer = TravelApp.doChat(message, chatId);
        Assertions.assertNotNull(answer);
        // 第三轮
        message = "我想去哪里旅游？刚跟你说过，帮我回忆一下";
        answer = TravelApp.doChat(message, chatId);
        Assertions.assertNotNull(answer);
    }

    @Test
    void doChatWithReport() {
        String chatId = UUID.randomUUID().toString();
        String message = "你好，我是爱健身的大学生，给出一份想去日本旅游的报告";
        TravelApp.TravelReport TravelReport = TravelApp.doChatWithReport(message, chatId);
        Assertions.assertNotNull(TravelReport);
    }

    @Test
    void doChatWithRag() {
        String chatId = UUID.randomUUID().toString();
        String message = "中国热门目的地的最佳旅游季节有哪些";
        String answer = TravelApp.doChatWithRag(message, chatId);
        Assertions.assertNotNull(answer);
    }

    @Test
    void doChatWithMcp() {
        String chatId = UUID.randomUUID().toString();
        // 测试地图 MCP
//        String message = "帮我搜索成都武侯区的景点图片";
//        String answer = TravelApp.doChatWithMcp(message, chatId);
//        Assertions.assertNotNull(answer);
        // 测试图片搜索 MCP
        String message = "帮我搜索成都武侯区的景点图片";
        String answer =  TravelApp.doChatWithMcp(message, chatId);
        Assertions.assertNotNull(answer);
    }

    @Test
    void doChatWithTools() {
        // 测试联网搜索问题的答案
        testMessage("周末想去成都，推荐几个适合的小众打卡地？");

        // 测试网页抓取：旅游案例分析
        testMessage("如何制定旅游攻略");

        // 测试资源下载：图片下载
        testMessage("下载一张成都SKP的照片");

        // 测试文件操作：保存用户档案
        testMessage("保存我的旅游攻略为文件");

        // 测试 PDF 生成
        testMessage("生成一份‘成都旅游计划’PDF，包括具体路线、消费");
    }

    private void testMessage(String message) {
        String chatId = UUID.randomUUID().toString();
        String answer = TravelApp.doChatWithTools(message, chatId);
        Assertions.assertNotNull(answer);
    }
}
