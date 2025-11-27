package com.funian.agent.tools;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * @Auther FuNian
 * @Date 2025/7/3 19:23
 * @ClassName:FileOperationToolTest
 * @School SiChuan University
 * @Major Computer Software
 */
class FileOperationToolTest {


    @Test
    void readFile() {
        FileOperationTool fileOperationTool = new FileOperationTool();
        String fileName = "Spring AI.txt";
        String result = fileOperationTool.readFile(fileName);
        Assertions.assertNotNull(result);
    }

    @Test
    void writeFile() {
        FileOperationTool fileOperationTool = new FileOperationTool();
        String fileName = "Spring AI.txt";
        String content = "Spring AI交流社区";
        String result = fileOperationTool.writeFile(fileName, content);
        Assertions.assertNotNull(result);
    }
}
