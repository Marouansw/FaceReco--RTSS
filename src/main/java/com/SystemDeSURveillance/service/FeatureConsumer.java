package com.SystemDeSURveillance.service;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;

@Service
public class FeatureConsumer {

    private final AtomicReference<String> lastConsumedMessage = new AtomicReference<>();
    private CountDownLatch latch = new CountDownLatch(1);

    @KafkaListener(topics = "test-topic", groupId = "group_id")
    public void consumeFromTopic2(String message) {
        lastConsumedMessage.set(message);
        latch.countDown();  // Release the latch when a message is consumed
        // System.out.println("Consumed message from topic2: " + message);
    }

    public String getLastConsumedMessage() {
        return lastConsumedMessage.get();
    }

    public void setLatch(CountDownLatch latch) {
        this.latch = latch;
    }
}
