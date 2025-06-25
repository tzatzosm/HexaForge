package {{group}}.domain.hello.adapters;

import org.springframework.stereotype.Service;
import {{group}}.domain.hello.ports.HelloMessageService;

@Service
public class HelloMessageServiceImpl extends HelloMessageService {

    @Override
    public String getHelloMessage() {
        return "Hello, World!";
    }

    @Override
    public String getHelloMessage(String name) {
        return "Hello, " + name + "!";
    }

}
