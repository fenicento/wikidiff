float sqSize=100;
float tPad=100;
float lPad=100;
float[] areas = new float[4];
float[] newAs = new float[4];
float[] heights = new float[4];
float[] realAs = new float[4];
int n = 4;
float sum=0;
int count=0;

void setup() {
  
 size(101,101);
 background(255); 

 
 for (int i =0; i<n; i++) {
   areas[i]=random(40);
 }
 
  
  
}


void draw() {
  
  if (count>0) {
    for (int i =0; i<n; i++) {
      areas[i]+=(newAs[i]-areas[i])/30;
      
    }
    count--;
    
   // if (count==30) count=0;
  
  }
  
  sum=0;
  float totH=0;
   float oldA=0;
  for (int i =0; i<n; i++) {
   oldA=oldA+areas[i];
 }
 
 
  float ratio=(sqSize*sqSize)/oldA;
  
  for(int i=0; i<n; i++) {
  
    realAs[i]=areas[i]*ratio;
     
    sum=sum+realAs[i];
    heights[i]= realAs[i]*2/sqSize;
    totH+=heights[i];
    
  }
  
  
  
  realAs=sort(realAs);
  float tmp = realAs[3];
  realAs[3]=realAs[2];
  realAs[2]=tmp;
  
  
  
  //best for now
  float bX=(sqSize*realAs[0])/(realAs[0]+realAs[2]);
  float bY=(sqSize*realAs[1])/(realAs[1]+realAs[3]);
  
  
  
 
  
  //float bX=(heights[0]*realAs[0]/(realAs[0]+realAs[2])+heights[2]*realAs[2]/(realAs[0]+realAs[2]))/2;
  //float bY=(heights[1]*realAs[1]/(realAs[1]+realAs[3])+heights[3]*realAs[3]/(realAs[1]+realAs[3]))/2;
  
  
  
  background(255);
  stroke(#000000);
  strokeWeight(2);
  fill(#824540);
  triangle(0,0,bX,bY,0,sqSize);
  fill(#948f85);
  triangle(0,0,bX,bY,sqSize,0);
  fill(#a1bdbd);
  triangle(sqSize,0,bX,bY,sqSize,sqSize);
  fill(#5c6a6b);
  triangle(0,sqSize,bX,bY,sqSize,sqSize);
  
  
  
  noFill();
  strokeWeight(3);
  rect(0,0,sqSize,sqSize);

  
  

}

float computeArea(float b, float h) {
  
  return b*h/2;

}

void mouseClicked() {
  
  for (int i =0; i<n; i++) {
    
    newAs[i]=random(40);
    count=30;
    
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
	
	newAs[0]=m1/q1.length;
	newAs[1]=m2/q2.length;
	newAs[2]=m3/q3.length;
	newAs[3]=m4/q4.length;
	
	count=30;

}


