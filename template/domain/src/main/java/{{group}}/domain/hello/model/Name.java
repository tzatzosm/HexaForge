package {{group}}.domain.hello.model;

import lombok.Builder;
import lombok.NonNull;

@Builder
public record Name(@NonNull String value) { }
