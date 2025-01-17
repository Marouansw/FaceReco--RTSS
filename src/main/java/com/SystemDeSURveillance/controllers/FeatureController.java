package com.SystemDeSURveillance.controllers;

import com.SystemDeSURveillance.service.FeatureConsumer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class FeatureController {

    @Autowired
    private FeatureConsumer featureConsumer;

    @GetMapping("/matching_result")
    
    public String getResult(Model model) throws InterruptedException {
       
        String lastMessage = featureConsumer.getLastConsumedMessage();
        
        if (lastMessage != null && lastMessage.contains("error")) {
            model.addAttribute("infos", "No matching found");
        } else {
            model.addAttribute("infos", lastMessage);
        }

        return "matching_result";
    }
}