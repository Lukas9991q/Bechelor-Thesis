# importowanie niezbędnych bibliotek
import numpy as np
import cv2
import serial,time
import pytesseract


# zainicjalizowanie HOG descriptor/detektor osób
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# Otwarcie kamery głównej 
cap = cv2.VideoCapture(0)

#obiekt Serial z portem 'com10' i szybkością transmisji 9600 bps.
ArduinoSerial=serial.Serial('com12',9600,timeout=0.1)

#zapis wideo do pliku o nazwie 'face detection4.avi' z kodekiem fourcc,
#liczbą klatek na sekundę 20 oraz rozdzielczością 640x480."
#out= cv2.VideoWriter('face detection4.avi',fourcc,20.0,(640,480))
time.sleep(1)


# dane wyjściowe zostaną zapisane w output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))


 # Wybór trybu wykrywania
mode = input("Wybierz tryb wykrywania (wpisz cyfrę):\n1. Wykrywanie ludzi\n2. Wykrywanie twarzy\n3. Wykrywanie zwierząt\n4. Wykrywanie rejestracji samochodów\n")

while(True):
    




    if mode == "1":

        # Przechwytywanie klatka po klatce
        ret, frame = cap.read()
        #odwróć klatkę w poziomie
        frame=cv2.flip(frame,1)

        # resizing for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        #śledzenie ludzi na obrazie
        #zwraca ramki dla wykrytych obiektów
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
        #przetwarzanie ramki za pomocą numpy array
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        # Jeśli liczba ramkowych wykrytych przez algorytm HOG jest większa niż 0
        if len(boxes)>0: 

         # Rysowanie ramki wokół wykrytych obiektów
         for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            
            cv2.rectangle(frame, (xA, yA), (xB , yB),
                            (0, 255, 0), 2)

            # Obliczanie środka ramki wykrytego obiektu           
            X= int((xA + xB)/2)
            Y= int((yA + yB)/2)
            # Przypisanie środka ramki do zmiennej center_pt 
            center_pt=(X ,Y)

            # Rysowanie kółka o średnicy 5px wokół środka ramki wykrytego obiektu
            cv2.circle(frame, center_pt, 5, (0,0,255), -1)
            # Obliczanie środka wszystkich ramkowych wykrytych przez algorytm HOG
            centroid_X = int((np.mean(boxes, axis=0)[0] + np.mean(boxes, axis=0)[2])/2) 
            centroid_Y = int((np.mean(boxes, axis=0)[1] + np.mean(boxes, axis=0)[3])/2) 
            
            # Przypisanie środka wszystkich ramkowych do zmiennej centroid_pt
            centroid_pt=(centroid_X,centroid_Y) 
            # Rysowanie kółka o średnicy 10px wokół środka wszystkich ramkowych wykrytych przez algorytm HOG 
            cv2.circle(frame, centroid_pt, 10, (130,0,75), -1)
            
            #tworzenie zmiennej string
            string='X{0:d}Y{1:d}'.format(centroid_X, centroid_Y)
            #wyświetlenie zawartości string
            print(string)
            #wysłanie zawartości do Arduino
            ArduinoSerial.write(string.encode('utf-8'))

         else:
          # przypisz wartości centroid_X = 320 i centroid_Y = 240
          centroid_X = 320
          centroid_Y = 240

        # Write the output video 
        out.write(frame.astype('uint8'))
        # Display the resulting frame
        cv2.imshow('frame',frame)
    






    elif mode == "2":

       # Capture frame-by-frame
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)

         # resizing for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        if len(boxes)>0: 

         for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            
            cv2.rectangle(frame, (xA, yA), (xB , yB),
                            (0, 255, 0), 2)
                        
            X= int((xA + xB)/2)
            Y= int((yA + yB)/2)
                   
            center_pt=(X ,Y)

            cv2.circle(frame, center_pt, 5, (0,0,255), -1)
            centroid_X = int((np.mean(boxes, axis=0)[0] + np.mean(boxes, axis=0)[2])/2) 
            centroid_Y = int((np.mean(boxes, axis=0)[1] + np.mean(boxes, axis=0)[3])/2) 
            centroid_pt=(centroid_X,centroid_Y)   
            cv2.circle(frame, centroid_pt, 10, (130,0,75), -1)

            string='X{0:d}Y{1:d}'.format(centroid_X, centroid_Y)
            print(string)
            ArduinoSerial.write(string.encode('utf-8'))

         else:
          centroid_X = 320
          centroid_Y = 240

        # Write the output video 
        out.write(frame.astype('uint8'))
        # Display the resulting frame
        cv2.imshow('frame',frame)







    elif mode == "3":

            # Capture frame-by-frame
        image, frame = cap.read()
        image = cv2.flip(frame, 1)
      
        # Konwertuj obraz do skali szarości
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Zaladuj klasyfikator twarzy
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # Wykryj twarze na obrazie
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Narysuj prostokąty wokół wykrytych twarzy
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Wyświetl obraz z narysowanymi prostokątami
        cv2.imshow("Twarze", image)








    elif mode == "4":

        # Capture frame-by-frame
        ret, frame = cap.read()
           # Konwersja obrazu do skali szarości
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Wykrywanie krawędzi za pomocą detektora Canny
        edges = cv2.Canny(gray, 50, 150)

        # Wykrywanie konturów w obrazie
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterowanie po wszystkich konturach
        for contour in contours:
            # Wyliczenie prostokąta otaczającego kontur
            x, y, w, h = cv2.boundingRect(contour)

            # Warunek sprawdzający czy kontur jest odpowiedniej wielkości i kształtu
            if w > 50 and h > 20 and w < 200 and h < 80:
                # Rysowanie prostokąta wokół wykrytej tablicy rejestracyjnej
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

                # Wycinanie fragmentu obrazu zawierającego tablicę rejestracyjną
                roi = frame[y:y+h, x:x+w]

                # Konwersja wyciętego fragmentu do skali szarości
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # Otsu's binarization
                _, thresh = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        # Zmniejszenie szumu przy pomocy morphological transformations
                kernel = np.ones((3,3), np.uint8)
                opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

                # Szybka progowanie obrazu
                sure_bg = cv2.dilate(opening, kernel, iterations=3)

                # Wyliczenie odległości między intensywnościami pikseli
                dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
                _, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

                # Znalezienie nieznanych obszarów
                sure_fg = np.uint8(sure_fg)
                unknown = cv2.subtract(sure_bg, sure_fg)

                # Wywołanie funkcji rozpoznawania tekstu
                text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6")

                # Iterowanie po wszystkich znakach w wykrytym tekście
                for i, char in enumerate(text):
                    # Sprawdzenie czy znak jest cyfrą
                    if char.isdigit():
                        # Rysowanie prostokąta wokół wykrytej cyfry
                        x1, y1, w1, h1 = i*10, 0, 10, h
                        cv2.rectangle(roi, (x1, y1), (x1+w1, y1+h1), (0, 0, 255), 2)

        # Wyświetlenie obrazu z kamery z naniesionymi prostokątami
        cv2.imshow("Frame", frame)








    else:
      print("Wybrano nieprawidłowy tryb wykrywania. Spróbuj ponownie.")


    if cv2.waitKey(1) & 0xFF == 27:
               break


   
    

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)