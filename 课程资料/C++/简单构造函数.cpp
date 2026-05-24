#include<iostream>
using namespace std;

class Circle
{
private:
	float r;
public:
	Circle(float x)
	{
		r = x; 
	}
	void setr(float x)
	{
		r = x;
	}
	void show()
	{
		cout<<r<<endl;
	}
	
};

int main()
{
	Circle c(10);
	int n;cin>>n;
	Circle c2(n);
	c.show();
	c2.show();
	return 0;	
}













