// rf95_server.pde
// -*- mode: C++ -*-

#include <SPI.h>
#include <RH_RF95.h>          // RF95 Lora module
#include <Adafruit_HTU21DF.h> // HTU21D sensor for Temperature/Humidity
#include <string.h>


// TPL5110 : Very low power Timer breakout (~35nA during sleep mode)
// Done pin used when the sending is completed
#define TPl5110_DONE_PIN A3

// Sensor network management
#define SENSOR_TYPE "TH"    // Define the type of sensor
#define SERVER_ADDRESS 0    // The server Adress where data is send
#define MY_ADDRESS 20       // The Adress of the sensor, should be unique for each sensor

// ADC management for battery voltage measurement
// 1024 : Reference Voltage
// 1023 : Maximum Measurable Voltage
// Internal Ref => 1.1V
// Vmax = 1,1*1023/1024 = 1.0989
#define ADC_PIN A0
#define V_REF 1.0989        // Internal reference voltage
#define R_div 4             // Corresponds to the ratio of the voltage divider (1M/(1M+3M)=1/4)  => Maximum measurable voltage : V_ref*R_div = 4,4V
#define CONV_FACTOR 0.0042926788
#define ADC_CORRECTION 5
// Voltage = R_div * V_REF * sensorValue / 1024.0;
// conversion factor = R_div * V_REF / 1024.0 = 0.0042926788


#define NB_MAX_NOT_ACK 3        // The number of times the frame must be retransmitted if the acknowledgement is not received
uint8_t cpt_not_ack = 0 ;

// Singleton instance of the radio driver
RH_RF95 rf95;
// Sensor instance
Adafruit_HTU21DF htu = Adafruit_HTU21DF();

// Message to send
uint8_t msg[50] = {0};
// Data to be transmitted : i : integer part  | f : decimal part
//                          t : temperature   | h : humidity  | v : voltage
uint8_t it,ft, ih,fh, iv,fv ;

uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];         // Reception buffer
//uint8_t len_buf = sizeof(buf);                // Buffer size

char ack_type();

bool msg_err = false ;


/***FUNCTIONS***/
void  acquisition(uint8_t *it,uint8_t *ft, uint8_t *ih,uint8_t * fh,uint8_t * iv,uint8_t * fv);
float mesure_batterie();
float mesure_temperature();
float mesure_humiditee();

void split_float(float *v, uint8_t *i,uint8_t *f);


void setup() 
{
  /*Serial.begin(9600);
  while (!Serial) ; // Wait for serial port to be available
  Serial.println("Setup");*/
  
  //pinMode(ADC_PIN, INPUT);
  pinMode(TPl5110_DONE_PIN, OUTPUT);
  digitalWrite(TPl5110_DONE_PIN, LOW);

  // Sensor init
  if (!htu.begin()) {
    //Serial.println("Couldn't find sensor!");
  }

  // ADC resolution => 10bits (2^10 - 1=1023)
  analogReference(INTERNAL);      // To use A_ref=1.1V for the ADC (independent of the battery voltage)

  // Lora module init
  if (!rf95.init()){
     // Serial.println("init failed");
  }
  rf95.setFrequency(868);         // Set frequency to 868MHz
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);    // false => use PA_boost
}

void loop()
{
  char ack='0';
  // Make a data acquisition only 
    // If the server detect a measurment error => msg_err = true
    // If the acknoledge is already receive
  if (msg_err == true or cpt_not_ack==0 )
  {
    acquisition(&it,&ft,&ih,&fh,&iv,&fv);
    sprintf(msg, "%d%s%d %d.%d %d.%d %d.%d",SERVER_ADDRESS,SENSOR_TYPE,MY_ADDRESS,it,ft,ih,fh,iv,fv);
    msg_err = false ;
  }

  // Message transmission
  rf95.send(msg, sizeof(msg));
  rf95.waitPacketSent();

  // Wait a response
  if (rf95.waitAvailableTimeout(1000)) // transmitter <--> receiver timeout minimum of 550ms
                                       // When receiving an msg, the server returns an acknowledgement 
                                       // If nothing is received before the end of the timeout (1s)
  { 
    // Should be a reply message for us now   
    if (rf95.recv(buf, sizeof(buf)))
   {
      /*Serial.print("got reply: ");
      Serial.println((char*)buf);*/

      //Serial.print("ack_type");
      ack = ack_type();               // Return the ack type : A=ok | E=erreur
      //Serial.println((char)ack);

      memset(buf, '\0', strlen(buf) - 1);       
    }
    else
    {
      //Serial.println("recv failed");
    }
  }
  else
  {
    //Serial.println("No reply, is rf95_server running?");
  }

  // RF95 LORA module in sleep mode 
  rf95.sleep();

  // IF an aknolage is receive OR if it is not receive after NB_MAX_NOT_ACK of time then power off
  if (ack=='A' or cpt_not_ack >= NB_MAX_NOT_ACK-1)
  { 
    cpt_not_ack = 0;
    digitalWrite(TPl5110_DONE_PIN, HIGH); // SLEEP MODE
    //delay(4000);
    //Watchdog.sleep(4000); //PAS TOP
    //LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF); //un peu mieux que watchdog mais plus de serial
    //LowPower.idle(SLEEP_4S, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF,SPI_OFF, USART0_OFF, TWI_OFF); // moins bien que powerdown
    
  }
  else if (ack=='E')
  {
    msg_err = true ;
    //Serial.println("msg err : refaire acquisition");
  }
  else
  {
    ++cpt_not_ack;
  }
}


/***Functions***/
char ack_type()
{
  int capt_adr;
  char capt_type[3];
  int serv_adr;
  char ack ;
  sscanf((char *)buf,"%d %s %d %c",&capt_adr,capt_type,&serv_adr,&ack);
  if ( (capt_adr==MY_ADDRESS) && (!strcmp(capt_type, SENSOR_TYPE)) && (serv_adr==SERVER_ADDRESS) )
  {
    return ack;
  }
  
  return -1 ; 
}

// split the float f into integer part i and decimal part f
void split_float(float *v, uint8_t *i,uint8_t *f)
{
  *i = (uint8_t) *v;                    // Make integer part
  *f = (uint8_t) ((*v - *i)*100);       // Fraction. Has same sign as integer part
  if (*f<0) *f = -*f;                   // So if it is negative make fraction positive again.
}


void acquisition(uint8_t *it,uint8_t *ft, uint8_t *ih,uint8_t * fh,uint8_t * iv,uint8_t * fv)
{
  // Mesure température
  float temp=mesure_temperature() ;
  split_float(&temp,it,ft);

  // Mesure humidité
  float humd=mesure_humiditee() ;
  split_float(&humd,ih,fh);

  // Mesure tension
  float tension=mesure_batterie();
  split_float(&tension,iv,fv);
}

float mesure_batterie()
{
  analogRead(A0) ; // When using the TPl5110 timer, the first measurement is not accurate.
  uint16_t sensorValue = analogRead(A0) - ADC_CORRECTION ; //read the A0 pin value

  return CONV_FACTOR * sensorValue ;
  //return R_div * V_REF * sensorValue1 / 1023.0 ;
  //To round to 1 decimal : floor(10*f+0.5)/10 
}
float mesure_temperature()
{
  return htu.readTemperature();
}
float mesure_humiditee()
{
  return htu.readHumidity();
}
