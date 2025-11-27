package com.funian.agent.chatmemory;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;
import org.objenesis.strategy.StdInstantiatorStrategy;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.messages.Message;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * 基于文件持久化的对话记忆实现。
 * 使用 Kryo 序列化框架将对话记录保存到磁盘文件中，支持根据会话 ID 读取、追加和清除消息。
 *
 * @Auther FuNian
 * @Major Computer Software
 */
public class FileBasedChatMemory implements ChatMemory {

    /**
     * 对话记录存储的基础目录路径
     */
    private final String BASE_DIR;

    /**
     * 全局静态 Kryo 实例，用于对象的序列化与反序列化
     */
    private static final Kryo kryo = new Kryo();

    /**
     * 静态初始化块：配置 Kryo 的行为
     */
    static {
        /**
         * 禁用强制类型注册，允许序列化未显式注册的类（可能影响性能）
         */
        kryo.setRegistrationRequired(false);

        /**
         * 设置实例化策略为标准构造器策略，适用于大多数 Java 类型
         */
        kryo.setInstantiatorStrategy(new StdInstantiatorStrategy());
    }

    /**
     * 构造基于文件的对话记忆管理器
     *
     * @param dir 存储对话记录的目录路径
     */
    public FileBasedChatMemory(String dir) {
        this.BASE_DIR = dir;
        File baseDir = new File(dir);
        if (!baseDir.exists()) {
            baseDir.mkdirs(); // 若目录不存在则创建
        }
    }

    /**
     * 向指定会话中追加新的对话消息，并持久化到文件
     *
     * @param conversationId 会话唯一标识符
     * @param messages       要添加的消息列表
     */
    @Override
    public void add(String conversationId, List<Message> messages) {
        List<Message> conversationMessages = getOrCreateConversation(conversationId);
        conversationMessages.addAll(messages);
        saveConversation(conversationId, conversationMessages);
    }

    /**
     * 获取指定会话的最近 N 条消息
     *
     * @param conversationId 会话唯一标识符
     * @param lastN          返回最近的 N 条消息数量
     * @return 最近 N 条消息列表
     */
    @Override
    public List<Message> get(String conversationId, int lastN) {
        List<Message> allMessages = getOrCreateConversation(conversationId);
        return allMessages.stream()
                .skip(Math.max(0, allMessages.size() - lastN)) // 取最后 N 条
                .toList();
    }

    /**
     * 清除指定会话的所有历史记录（删除对应的磁盘文件）
     *
     * @param conversationId 会话唯一标识符
     */
    @Override
    public void clear(String conversationId) {
        File file = getConversationFile(conversationId);
        if (file.exists()) {
            file.delete(); // 删除文件
        }
    }

    /**
     * 获取指定会话的消息列表。如果会话文件不存在，则返回空列表。
     *
     * @param conversationId 会话唯一标识符
     * @return 当前会话的消息列表
     */
    private List<Message> getOrCreateConversation(String conversationId) {
        File file = getConversationFile(conversationId);
        List<Message> messages = new ArrayList<>();
        if (file.exists()) {
            try (Input input = new Input(new FileInputStream(file))) {
                messages = kryo.readObject(input, ArrayList.class);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return messages;
    }

    /**
     * 将指定会话的消息列表写入磁盘文件，覆盖原有内容
     *
     * @param conversationId 会话唯一标识符
     * @param messages       要写入的消息列表
     */
    private void saveConversation(String conversationId, List<Message> messages) {
        File file = getConversationFile(conversationId);
        try (Output output = new Output(new FileOutputStream(file))) {
            kryo.writeObject(output, messages);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 根据会话 ID 构建对应的文件对象
     *
     * @param conversationId 会话唯一标识符
     * @return 对应的 [.kryo](file://F:\FN\Agent\tmp\chat-memory\20b895fe-86b5-4cf1-9233-bd5c9eb53f8c.kryo) 文件对象
     */
    private File getConversationFile(String conversationId) {
        return new File(BASE_DIR, conversationId + ".kryo");
    }
}
