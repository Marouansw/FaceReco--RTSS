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

    @GetMapping("/Matching_results")
    
    public String getResult(Model model) throws InterruptedException {
       
        String lastMessage = featureConsumer.getLastConsumedMessage();
        
        model.addAttribute("message", lastMessage);
        return "matching_results";
    }
}