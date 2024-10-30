package {{group}}.api.hello.model;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

public record HelloRequest(
    @NotNull @NotEmpty String name
) { }
