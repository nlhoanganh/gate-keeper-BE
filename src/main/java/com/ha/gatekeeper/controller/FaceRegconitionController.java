package com.ha.gatekeeper.controller;

import com.ha.gatekeeper.dto.TrainFaceDTO;
import com.ha.gatekeeper.dto.VerifyFaceDTO;
import com.ha.gatekeeper.service.FaceRegconitionService;
import lombok.AllArgsConstructor;
import org.apache.logging.log4j.util.Strings;
import org.bytedeco.javacpp.*;
import org.bytedeco.javacpp.opencv_core.Mat;
import org.bytedeco.javacpp.opencv_core.RectVector;
import org.bytedeco.javacpp.opencv_objdetect.CascadeClassifier;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.List;

@Controller
@RequestMapping("/face-regconition")
public class FaceRegconitionController {

    private final FaceRegconitionService faceRegconitionService;

    private final opencv_face.FaceRecognizer recognizer;

    public FaceRegconitionController(FaceRegconitionService faceRegconitionService, opencv_face.FaceRecognizer faceRecognizer) {
        this.faceRegconitionService = faceRegconitionService;
        this.recognizer = faceRecognizer;
    }

    @RequestMapping(value = "train", method = RequestMethod.POST)
    @ResponseBody
    public ResponseEntity<?> train(@RequestBody TrainFaceDTO trainFaceDTO) throws Exception {
        String basePath = System.getProperty("user.dir");

        // Edit and save images for training
        CascadeClassifier faceDetector = new CascadeClassifier(basePath+"\\src\\main\\resources\\haarcascade_frontalface_alt.xml");
        for (int i = 0; i < trainFaceDTO.getBase64Images().size(); i++) {
            byte[] bytes = Base64.getDecoder().decode(trainFaceDTO.getBase64Images().get(i));
            Mat buf = new Mat(new BytePointer(bytes));
            Mat gray = opencv_imgcodecs.imdecode(buf, opencv_imgcodecs.IMREAD_GRAYSCALE);

            RectVector detecFace = new RectVector(); // store detected faces
            faceDetector.detectMultiScale(gray, detecFace, 1.1, 1, 0, new opencv_core.Size(150, 150), new opencv_core.Size(500, 500));
            opencv_core.Rect faceD = detecFace.get(0);

            if (faceD == null) { // when face can't be detected
                continue;
            }

            Mat captface = new Mat(gray, faceD);
            opencv_imgproc.resize(captface, captface, new opencv_core.Size(160, 160));
            opencv_imgcodecs.imwrite(basePath+"\\src\\main\\resources\\training\\photos\\" + trainFaceDTO.getName() + "." + trainFaceDTO.getId() +       "." + i + ".jpg",captface);
        }

        // Write data to namedata file
        File namedataFile = new File(basePath+"\\src\\main\\resources\\namedata.csv");
        FileWriter writer = new FileWriter(namedataFile, true);
        BufferedWriter bufferedWriter = new BufferedWriter(writer);
        bufferedWriter.newLine();
        bufferedWriter.write(trainFaceDTO.getId() + "," + trainFaceDTO.getName());
        bufferedWriter.close();
        writer.close();

        faceRegconitionService.training();
        return ResponseEntity.status(HttpStatus.OK)
                .body("Training Completed");
    }

    @RequestMapping(value = "verify", method = RequestMethod.POST)
    @ResponseBody
    public String verify(@RequestBody VerifyFaceDTO verifyFaceDTO) throws Exception {
        String basePath = System.getProperty("user.dir");
        HashMap<String,String> data = new HashMap<>();
        Path path= Paths.get(basePath+"\\src\\main\\resources\\namedata.csv");
        try {
            List<String> list= Files.readAllLines(path, StandardCharsets.UTF_8);
            for(String lis:list) {
                data.put(lis.split(",")[0].toString(), lis.split(",")[1].toString());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        CascadeClassifier faceDetector = new CascadeClassifier(basePath+"\\src\\main\\resources\\haarcascade_frontalface_alt.xml");
        String name = "";
        opencv_face.FaceRecognizer recognizer = opencv_face.createLBPHFaceRecognizer();
        recognizer.load(basePath+"\\src\\main\\resources\\classifierLBPH.yml");
        recognizer.setThreshold(65.0);
        for (int i = 0; i < verifyFaceDTO.getBase64Faces().size(); i++) {
            byte[] bytes = Base64.getDecoder().decode(verifyFaceDTO.getBase64Faces().get(0));
            BytePointer bytePointer = new BytePointer(bytes);
            Mat buf = new Mat(bytePointer);
            Mat grayImage = opencv_imgcodecs.imdecode(buf, opencv_imgcodecs.IMREAD_GRAYSCALE);

            RectVector detectedFaces = new RectVector(); // store detected faces
            faceDetector.detectMultiScale(grayImage, detectedFaces, 1.1, 1, 0, new opencv_core.Size(150, 150), new opencv_core.Size(500, 500));

            for (int j = 0; j < detectedFaces.size(); j++) // cycle detected faces vector
            {
                opencv_core.Rect faceData = detectedFaces.get(j);
                Mat capturedface = new Mat(grayImage, faceData);
                opencv_imgproc.resize(capturedface, capturedface, new opencv_core.Size(160, 160));

                IntPointer label = new IntPointer(1); // identify the image label
                DoublePointer confidence = new DoublePointer(1);
                recognizer.predict(capturedface, label, confidence); // will classify the new image according to the training
                int selection = label.get(0); // choice made by the classifier
                if (selection == -1)
                {
                    name = "Unknown";
                } else
                {
                    name= data.get(Integer.toString(selection)) + " - " + confidence.get(0);
                    break;
                }
            }

            if (!Strings.isBlank(name)) {
                break;
            }
        }

        return name;
    }
}
