To install in ubuntu:
sudo apt-get install libopencv-dev

Steps:
    1. Localize the object in the photo --> opencv_annotation --annotations=object_detected.txt --images=positives
    With left and right click select the object. With 'c' key set the object. With 'n' hey go to the next image.

    2. Create more positives images --> opencv_createsamples -info object_detected.txt -num 502 -w 48 -h 24 -vec object_detected.vec
    num==502 because object_detected.txt has 502 rows.
    
    3. Generate negatives.txt file --> run generare_negativesTXT.py script.
    3.1 HAAR:  opencv_traincascade -data classifiers/own/ -vec object_detected.vec -bg negatives.txt -numPos 400 -numNeg 217 -numStages 17 -w 48 -h 24 -featureTypes HAAR -minHitRate 0.99 -maxFalseAlarmRate 0.25 -accepttanceRatioBreakValue 10e-5
    3.2 LBP : opencv_traincascade -data classifiers/ -vec object_detected.vec -bg negatives.txt -numPos 490 -numNeg 217 -numStages 9 -w 200 -h 50 -featureType LBP

    4. Test classifier --> run cascade.py script. Then see if the classifier are drawing rectangle on plate.
    
References: 
    https://www.youtube.com/watch?v=WEzm7L5zoZE
    https://answers.opencv.org/question/75083/documentation-for-opencv_annotation/
    https://docs.opencv.org/2.4/doc/user_guide/ug_traincascade.html