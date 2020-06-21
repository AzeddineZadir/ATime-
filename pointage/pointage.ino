
#include <Adafruit_Fingerprint.h>
#include <HardwareSerial.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char *ssid = "TP-LINK_9C42F4";
const char *password = "26839158";

String postData;                                            // post array that will be send to the website
String linkee = "http://192.168.1.222:8000/pointage/getid"; //computer IP or the server domain
uint8_t id;                                                 // The Fingerprint ID from the scanner

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&Serial2);
int FingerID = 0;

void setup()
{
  pinMode(2, OUTPUT);
  Serial.begin(115200);

  //---------------------------------------------

  connectToWiFi();

  //---------------------------------------------

  // set the data rate for the sensor serial port
  finger.begin(57600);
  Serial.println("\n\nAdafruit finger detect test");

  if (finger.verifyPassword())
  {
    Serial.println("Found fingerprint sensor!");
  }
  else
  {
    Serial.println("Did not find fingerprint sensor :(");
    while (1)
    {
      delay(1);
    }
  }

  //---------------------------------------------

  finger.getTemplateCount();
  Serial.print("Sensor contains ");
  Serial.print(finger.templateCount);
  Serial.println(" templates");
   //checkToAdd();
  

  //------------*test the connection*------------

  //SendFingerprintID( FingerID );
  //-------------* ddeleating all templates"-----------
  //emptyDataBase();
  //checkToAdd();

  delay(10000);
}

void loop()
{
  //check if there's a connection to WiFi or not
  if (WiFi.status() != WL_CONNECTED)
  {
    connectToWiFi();
  }
  //---------------------------------------------
  //If there no fingerprint has been scanned return -1 or -2 if there an error or 0 if there nothing, The ID start form 1 to 127
  FingerID = getFingerprintID(); // Get the Fingerprint ID from the Scanner
                                 //don't need to run this at full speed.
  Serial.println(FingerID);
  delay(50);
  checkfinger();
  if (FingerID == 1)
  {
    Serial.println("dans le if ");
    checkToDelete();
    delay(5000);
    checkToAdd();
  }

  //checkToDelete();
}
// connecte to the WIFI
void connectToWiFi()
{
  WiFi.mode(WIFI_OFF); //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP()); //IP address assigned to your ESP
}
// scane and get the finger print id if it exists else get -1 -2
int getFingerprintID()
{
  uint8_t p = finger.getImage();
  switch (p)
  {
  case FINGERPRINT_OK:
    Serial.println("Image taken");
    break;
  case FINGERPRINT_NOFINGER:
    Serial.println("No finger detected");
    return 0;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return -2;
  case FINGERPRINT_IMAGEFAIL:
    Serial.println("Imaging error");
    return -2;
  default:
    Serial.println("Unknown error");
    return -2;
  }
  // OK success!
  p = finger.image2Tz();
  switch (p)
  {
  case FINGERPRINT_OK:
    Serial.println("Image converted");
    break;
  case FINGERPRINT_IMAGEMESS:
    Serial.println("Image too messy");
    return -1;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return -2;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return -2;
  case FINGERPRINT_INVALIDIMAGE:
    Serial.println("Could not find fingerprint features");
    return -2;
  default:
    Serial.println("Unknown error");
    return -2;
  }
  // OK converted!
  p = finger.fingerFastSearch();
  if (p == FINGERPRINT_OK)
  {
    Serial.println("Found a print match!");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("Communication error");
    return -2;
  }
  else if (p == FINGERPRINT_NOTFOUND)
  {
    Serial.println("Did not find a match");
    return -1;
  }
  else
  {
    Serial.println("Unknown error");
    return -2;
  }
  // found a match!
  Serial.print("Found ID #");
  Serial.print(finger.fingerID);
  Serial.print(" with confidence of ");
  Serial.println(finger.confidence);

  return finger.fingerID;
}
void checkfinger()
{
  //Fingerprint has been detected
  if (FingerID > 0)
  {
    // Serial.println("a fingerprint found");
    SendFingerprintID(FingerID); // Send the Fingerprint ID to the website.
  }
  //---------------------------------------------
  //No finger detected
  else if (FingerID == 0)
  {
    Serial.println("NO  fingerprint found");
  }
  //---------------------------------------------
  //Didn't find a match
  else if (FingerID == -1)
  {
    Serial.println("Didn't find a match");
  }
  //---------------------------------------------
  //Didn't find the scanner or there an error
  else if (FingerID == -2)
  {
    Serial.println("Didn't find the scanner or there an error");
  }
}
void SendFingerprintID(int fingerid)
{

  HTTPClient http; //Declare object of class HTTPClient
  //Post Data
  postData = "Check_employe=" + String(fingerid); // Add the Fingerprint ID to the Post array in order to send it
  // Post methode

  http.begin(linkee);                                                  //initiate HTTP request, put your Website URL or Your Computer IP
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header

  int httpCode = http.POST(postData); //Send the request
  String payload = http.getString();  //Get the response payload

  //Serial.println(httpCode); //Print HTTP return code
  //Serial.println(payload);  //Print request response payload
  //Serial.println(postData); //Post Data
  //Serial.println(finger);   //Print fingerprint ID
  String id_recue = "";
  if (payload.substring(0, 2) == "ID")
  {
    digitalWrite(2, HIGH);
    delay(1000);
    digitalWrite(2, LOW);
    id_recue = payload.substring(2);
    Serial.println("jai recu cete id ");
    Serial.println(id_recue);
  }
  delay(1000);

  postData = "";
  http.end(); //Close connection
}

void checkToAdd()
{
  HTTPClient http; //Declare object of class HTTPClient
  //Post Data
  postData = "Get_Fingerid=get_id"; // Add the Fingerprint ID to the Post array in order to send it
  // Post methode

  http.begin(linkee);                                                  //initiate HTTP request, put your Website URL or Your Computer IP
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header

  int httpCode = http.POST(postData); //Send the request
  String payload = http.getString();  //Get the response payload

  if (payload.substring(0, 6) == "add-id")
  {
    // Serial.println("jai recu une reponse qui contiens add id");
    String add_id = payload.substring(6);
    Serial.println(add_id);
    id = add_id.toInt();
    if (id != 0)
    {
      Serial.println("posez votre empreinte svp nous allols commancer leregistrement ");
      getFingerprintEnroll();
    }
  }
  http.end(); //Close connection
}

uint8_t getFingerprintEnroll()
{

  int p = -1;
  while (p != FINGERPRINT_OK)
  {
    p = finger.getImage();
    switch (p)
    {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(1);
  switch (p)
  {
  case FINGERPRINT_OK:
    break;
  case FINGERPRINT_IMAGEMESS:
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return p;
  case FINGERPRINT_INVALIDIMAGE:
    Serial.println("Could not find fingerprint features");
    return p;
  default:
    Serial.println("Unknown error");
    return p;
  }
  Serial.println("Remove finger");
  delay(2000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER)
  {
    p = finger.getImage();
  }
  Serial.print("ID ");
  Serial.println(id);
  p = -1;
  while (p != FINGERPRINT_OK)
  {
    p = finger.getImage();
    switch (p)
    {
    case FINGERPRINT_OK:
      //Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.println(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(2);
  switch (p)
  {
  case FINGERPRINT_OK:
    //Serial.println("Image converted");
    break;
  case FINGERPRINT_IMAGEMESS:
    Serial.println("Image too messy");
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return p;
  case FINGERPRINT_INVALIDIMAGE:
    Serial.println("Could not find fingerprint features");
    return p;
  default:
    Serial.println("Unknown error");
    return p;
  }

  // OK converted!
  Serial.print("Creating model for #");
  Serial.println(id);

  p = finger.createModel();
  if (p == FINGERPRINT_OK)
  {
    Serial.println("Prints matched!");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_ENROLLMISMATCH)
  {
    Serial.println("Fingerprints did not match");
    return p;
  }
  else
  {
    Serial.println("Unknown error");
    return p;
  }

  Serial.print("ID ");
  Serial.println(id);
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK)
  {
    Serial.println("Stored!");
    confirmAdding();
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_BADLOCATION)
  {
    Serial.println("Could not store in that location");
    return p;
  }
  else if (p == FINGERPRINT_FLASHERR)
  {
    Serial.println("Error writing to flash");
    return p;
  }
  else
  {
    Serial.println("Unknown error");
    return p;
  }
}

void confirmAdding()
{
  // make is_uplodeaed a true if we stored the fingerprint with the correcte id
  HTTPClient http; //Declare object of class HTTPClient
  //Post Data
  postData = "confirm_id=" + String(id); // Add the Fingerprint ID to the Post array in order to send it
  // Post methode

  http.begin(linkee);                                                  //initiate HTTP request, put your Website URL or Your Computer IP
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header

  int httpCode = http.POST(postData); //Send the request
  String payload = http.getString();  //Get the response payload

  Serial.println("la reponse de la confirmations");
  Serial.println(payload);

  http.end(); //Close connection
}
void emptyDataBase()
{
  Serial.println("\n\nDeleting all fingerprint templates!");

  Serial.begin(115200);
  while (!Serial)
    ; // For Yun/Leo/Micro/Zero/...
  delay(100);

  Serial.println("\n\nDeleting all fingerprint templates!");
  Serial.println("Press 'Y' key to continue");

  while (1)
  {
    if (Serial.available() && (Serial.read() == 'Y'))
    {
      break;
    }
  }

  // set the data rate for the sensor serial port
  finger.begin(57600);

  if (finger.verifyPassword())
  {
    Serial.println("Found fingerprint sensor!");
  }
  else
  {
    Serial.println("Did not find fingerprint sensor :(");
    while (1)
      ;
  }

  finger.emptyDatabase();

  Serial.println("Now database is empty :)");
}

void checkToDelete()
{
  HTTPClient http; //Declare object of class HTTPClient
  //Post Data
  postData = "DeleteID=check"; // Add the Fingerprint ID to the Post array in order to send it
  // Post methode

  http.begin(linkee);                                                  //initiate HTTP request, put your Website URL or Your Computer IP
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header

  int httpCode = http.POST(postData); //Send the request
  String payload = http.getString();  //Get the response payload

  if (payload.substring(0, 6) == "del-id")
  {
    String del_id = payload.substring(6);
    //Serial.print("the finger print id to deleat is ");
    Serial.println(del_id);
    if (del_id.toInt() != 0)
    {
      //Serial.print("the finger print id to delete is ");
      //Serial.println(del_id);
      deleteFingerprint(del_id.toInt());
    }
    else
    {
      //Serial.print("jai recu un id = 0 donc je ne supprime pas ");
      http.end(); //Close connection
    }
  }

  http.end(); //Close connection
}

uint8_t deleteFingerprint(int id)
{
  uint8_t p = -1;

  p = finger.deleteModel(id);

  if (p == FINGERPRINT_OK)
  {
    Serial.println("Deleted!");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_BADLOCATION)
  {
    Serial.println("Could not delete in that location");
    return p;
  }
  else if (p == FINGERPRINT_FLASHERR)
  {
    Serial.println("Error writing to flash");
    return p;
  }
  else
  {
    Serial.print("Unknown error: 0x");
    Serial.println(p, HEX);
    return p;
  }
}
