package {{group}}.api.hello;

import {{group}}.api.hello.model.HelloResponse;
import {{group}}.api.hello.model.HelloRequest;
import {{group}}.domain.hello.HelloMessageHandler;
import {{group}}.domain.hello.model.Name;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@AllArgsConstructor
@RestController
@RequestMapping("/hello")
public class HelloController {

    private final HelloMessageHandler helloMessageHandler;

    @GetMapping
    public ResponseEntity<HelloResponse> hello() {
        var message = helloMessageHandler.getHelloMessage();
        return ResponseEntity.ok(HelloResponse.builder().message(message.value()).build());
    }

    @PostMapping
    public ResponseEntity<HelloResponse> hello(@RequestBody @Valid HelloRequest request) {
        var name = Name.builder().value(request.name()).build();
        var message = helloMessageHandler.getHelloMessage(name);
        return ResponseEntity.ok(HelloResponse.builder().message(message.value()).build());
    }

}
