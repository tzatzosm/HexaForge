package {{group}}.domain.hello;

import {{group}}.domain.hello.model.Message;
import {{group}}.domain.hello.model.Name;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

@AllArgsConstructor
@Component
public class HelloMessageHandler {

    public Message getHelloMessage() {
        return Message.builder().value("Hello, World!").build();
    }

    public Message getHelloMessage(Name name) {
        var message = String.format("Hello, %s!", name.value());
        return Message.builder().value(message).build();
    }

}