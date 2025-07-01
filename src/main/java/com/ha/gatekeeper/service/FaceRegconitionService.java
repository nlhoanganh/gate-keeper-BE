package com.ha.gatekeeper.service;

import org.bytedeco.javacpp.opencv_core;
import org.bytedeco.javacpp.opencv_face;
import org.bytedeco.javacpp.opencv_imgcodecs;
import org.bytedeco.javacpp.opencv_imgproc;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FilenameFilter;
import java.nio.IntBuffer;

import static org.bytedeco.javacpp.opencv_face.createLBPHFaceRecognizer;

@Service
public class FaceRegconitionService {

    public void training()
    {
        String basePath = System.getProperty("user.dir");
        String resourcePath = basePath + "\\src\\main\\resources";
        String photosPath = resourcePath + "\\training\\photos";
        File directory = new File (photosPath);
        FilenameFilter imageFilter = new FilenameFilter() {   // filter image type
            public boolean accept(File dir, String name) {
                return name.endsWith(".jpg") || name.endsWith(".gif") || name.endsWith(".png") ;
            }
        };

        File[] files = directory.listFiles(imageFilter);
        opencv_core.MatVector photos = new opencv_core.MatVector(files.length);
        opencv_core.Mat labels = new opencv_core.Mat(files.length, 1 , opencv_core.CV_32SC1);
        IntBuffer bufferLabels = labels.createBuffer();
        int counter = 0;

        for( File image : files) {   // fill in the data to train classifiers
            opencv_core.Mat photo = opencv_imgcodecs.imread(image.getAbsolutePath(), opencv_imgcodecs.CV_LOAD_IMAGE_GRAYSCALE);   //take the image by name and convert to gray scale
            String name = image.getName().split("\\.")[0].substring(0);
            int personId = Integer.parseInt(image.getName().split("\\.")[1]);  // search person id

            opencv_imgproc.resize(photo, photo, new opencv_core.Size(160,160));
            photos.put(counter, photo);   //search photo
            bufferLabels.put(counter, personId);  //search person id
            counter++;
        }

        //classifiers
        opencv_face.FaceRecognizer lbph = createLBPHFaceRecognizer();

        lbph.train(photos, labels);
        lbph.save(resourcePath + "\\classifierLBPH.yml");
        System.out.println("Training Completed");
    }
}
