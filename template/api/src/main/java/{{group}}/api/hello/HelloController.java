package {{group}}.api.hello;

import {{group}}.api.hello.model.HelloRequest;
import {{group}}.api.hello.model.HelloResponse;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/hello")
public class HelloController {

    @GetMapping
    public ResponseEntity<HelloResponse> hello() {
        return ResponseEntity.ok(HelloResponse.builder().message("Hello, World!").build());
    }

    @PostMapping
    public ResponseEntity<HelloResponse> hello(@RequestBody @Valid HelloRequest request) {
        return ResponseEntity.ok(HelloResponse.builder().message(String.format("Hello, %s!", request.name())).build());
    }

}
