package com.SystemDeSURveillance;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.kafka.annotation.EnableKafka;


@SpringBootApplication
@EnableKafka
public class SystemDeSurveillanceApplication {

	public static void main(String[] args) {
		SpringApplication.run(SystemDeSurveillanceApplication.class, args);
	}

}
