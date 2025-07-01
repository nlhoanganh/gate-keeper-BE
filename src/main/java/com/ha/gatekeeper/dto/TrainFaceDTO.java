package com.ha.gatekeeper.dto;

import lombok.Data;

import java.util.List;

@Data
public class TrainFaceDTO {
    private Integer id;
    private String name;
    private List<String> base64Images;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<String> getBase64Images() {
        return base64Images;
    }

    public void setBase64Images(List<String> base64Images) {
        this.base64Images = base64Images;
    }
}
