package com.ha.gatekeeper.dto;

import java.util.List;

public class VerifyFaceDTO {
    private List<String> base64Faces;

    public void setBase64Faces(List<String> base64Faces) {
        this.base64Faces = base64Faces;
    }

    public List<String> getBase64Faces() {
        return this.base64Faces;
    }
}
