package {{group}}.domain.hello;

import {{group}}.domain.hello.model.Message;
import {{group}}.domain.hello.model.Name;
import {{group}}.domain.hello.ports.HelloMessageService;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@RequiredArgsConstructor
@Component
public class HelloMessageHandler {

    private final HelloMessageService helloMessageService;

    public Message getHelloMessage() {
        return Message.builder().value(helloMessageService.getHelloMessage()).build();
    }

    public Message getHelloMessage(Name name) {
        var message = helloMessageService.getHelloMessage(name.value());
        return Message.builder().value(message).build();
    }

}