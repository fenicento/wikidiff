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
 
 float pastL=0;
 
  float ratio=(sqSize*sqSize)/oldA;
  
 noStroke(); 
  
 for (int i =0; i<n; i++) {
   realLs[i]=  lines[i]*ratio;
   println(realLs[i]);
   
   // fill(cols[i]);
   //rect(0,pastL,sqSize,pastL+realLs[i]/100);
   //pastL+=realLs[i]/100;
   }
 
 
 float fha=(realLs[0]+realLs[1])/100;
 float fbr=realLs[0]/fha;

 float sha=sqSize-fha;
 float sbr=realLs[2]/sha;
 
 fill(cols[0]);
 rect(0,0,fbr,fha);
 fill(cols[1]);
 rect(fbr,0,sqSize,fha);
 fill(cols[2]);
 rect(0,fha,sbr,sqSize);
 fill(cols[3]);
 rect(sbr,fha,sqSize,sqSize);
 
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