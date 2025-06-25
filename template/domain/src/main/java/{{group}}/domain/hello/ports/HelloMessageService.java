package {{group}}.domain.hello.ports;

public interface HelloMessageService {
    String getHelloMessage();

    String getHelloMessage(String name);
}
