float sqSize=10;
float tPad=100;
float lPad=100;
int n = 30;
l=400/n;
h=100/4;

float[] line1 = new float[n];
float[] line2 = new float[n];
float[] line3 = new float[n];
float[] line4 = new float[n];



void setup() {
  
 size(401,101);
 background(255); 
 l=400/n;
 h=100/4;
 
 for (int i =0; i<n; i++) {
   line1[i]=random(100);
   line2[i]=random(100);
   line3[i]=random(100);
   line4[i]=random(100);

 } 
}


void draw() {
  
  background(255);
  
  for (int i=0; i<line1.length; i++) {
  	
  	stroke(#000000);
  	
  	colorMode(RGB, 100);
  	
  	fill(100,line1[i],line1[i]);
  	rect(i*l,0,i*l+l,h);
  	
  	fill(100,line2[i],line2[i]);
  	rect(i*l,h,i*l+l,h+h);
  	
  	fill(100,line3[i],line3[i]);
  	rect(i*l,2*h,i*l+l,2*h+h);
  	
  	fill(100,line4[i],line4[i]);
  	rect(i*l,3*h,i*l+l,3*h+h);
  	
  }
 }



void updateLogo(float[] q1, float[] q2, float[] q3, float[] q4) {

	n=q1.length;
	
	l=400/n;
 	
 	
	line1=q1;
	line2=q2;
	line3=q3;
	line4=q4;


}


