#include<iostream>
const float PI = 3.14;

class Circle
{
private:
	float r;
public:
	void setr(float x) {r = x;}		
	float area()
	{
		return r*r*PI;
	}	
	void show()
	{
		cout<<r<<","<<area()<<endl;
	}
};

int main()
{
	Circle c;
	c.setr(10);
	c.show();
	return 0;	
}










