float sqSize=100;
int n = 4;
float[] lines = new float[n];
float[] newLs = new float[n];
float[] realLs = new float[n];
int count=0;
float sum=0;
int[] cols=new int[]{#824540,#948f85,#a1bdbd,#5c6a6b};

void setup() {
  
 size(101,101);
 background(255); 
 
 
 for (int i =0; i<n; i++) {
   lines[i]=random(100);
 } 
}


void draw() {
  
  background(255);
  
  if (count>0) {
    for (int i =0; i<n; i++) {
      lines[i]+=(newLs[i]-lines[i])/30;
      
    }
    count--;
    
  }
  
  sum=0;
   float oldA=0;
  for (int i =0; i<n; i++) {
   oldA=oldA+lines[i];
 }
 
 float pastL=radians(-90);
 
  float ratio=90/oldA;
  
 for (int i =0; i<n; i++) {
   realLs[i]=  lines[i]*ratio;
   
    fill(cols[i]);
    stroke(0);
   arc(0,sqSize,sqSize*3,sqSize*3,pastL,pastL+radians(realLs[i]));
   
   pastL+=radians(realLs[i]);
  
 
   }
 }

void updateLogo(float[] q1, float[] q2, float[] q3, float[] q4) {

  float m1=0;
  float m2=0;
  float m3=0;
  float m4=0;

  for (int i = 0; i<q1.length; i++) {
  
    m1+=q1[i];
    m2+=q2[i];
    m3+=q3[i];
    m4+=q4[i];
  }
  
  newLs[0]=m1/q1.length;
  newLs[1]=m2/q2.length;
  newLs[2]=m3/q3.length;
  newLs[3]=m4/q4.length;
  
  count=30;


}