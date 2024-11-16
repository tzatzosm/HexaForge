package {{group}}.domain.hello.model;


import lombok.Builder;
import lombok.NonNull;

@Builder
public record Message(@NonNull String value) { }
