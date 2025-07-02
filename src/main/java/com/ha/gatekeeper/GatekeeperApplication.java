package com.ha.gatekeeper;

import org.bytedeco.javacpp.opencv_face;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.bytedeco.javacpp.opencv_face.createLBPHFaceRecognizer;

@SpringBootApplication
public class GatekeeperApplication {
	public static void main(String[] args) {
		SpringApplication.run(GatekeeperApplication.class, args);
	}

	@Bean
	public WebMvcConfigurer corsConfigurer() {
		return new WebMvcConfigurer() {
			@Override
			public void addCorsMappings(CorsRegistry registry) {
				registry.addMapping("/**") // All endpoints
						.allowedOrigins("*") // All origins
						.allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
						.allowedHeaders("*")
						.allowCredentials(false)
						.maxAge(3600);
			}
		};
	}

	@Bean
	public opencv_face.FaceRecognizer faceRecognizer() {
		String basePath = System.getProperty("user.dir");
		String filePath = basePath+"\\src\\main\\resources\\classifierLBPH.yml"; // Replace with the actual file path
		Path path = Paths.get(filePath);
		opencv_face.FaceRecognizer recognizer = createLBPHFaceRecognizer();

		if (Files.exists(path)) {
			recognizer.load(filePath);
			recognizer.setThreshold(50.0);
		}

		return  recognizer;

	}
}
