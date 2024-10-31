package {{group}}.api.swagger.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfiguration {

    @Bean
    public OpenAPI openApiDefinition() {
        return new OpenAPI()
            .info(new Info()
                .title("{{project}}")
                .description("Swagger for {{project}}")
                .version("0.0.1"));
    }

}
