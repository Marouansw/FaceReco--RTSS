package com.SystemDeSURveillance.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class HomeController {
    @RequestMapping(value = "/", method = RequestMethod.GET)
    public String home() {
        return "index";
    }
    @GetMapping("/display")
    public String display() {
        return "image"; // Renvoie vers la page d'affichage
    }

    

}


