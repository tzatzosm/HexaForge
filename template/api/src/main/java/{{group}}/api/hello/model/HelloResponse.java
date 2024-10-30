package {{group}}.api.hello.model;

import lombok.Builder;

@Builder
public record HelloResponse(String message) { }
