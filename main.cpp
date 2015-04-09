#include <iostream>
#include <fstream>
#include <string>
#include "parse.h"

using namespace std;
int main(int argc, char* argv[])
{

	if (argc!=3) 
	{
		cout << "Error, usage: ./mp3 <task A,B,C> <input filename>" << endl;
		return 1;
	}
	
	char mode = argv[1][0]; //first letter
	string input_file = argv[2];
	
	switch(mode)
	{
		case 'a':
		case 'A':
			mode = 'A';
			break;
			
		case 'b':
		case 'B':
			mode = 'B';
			break;
			
		case 'c':
		case 'C':
			mode = 'C';
			break;
			
		default:
			mode = 'A';
			cout << "Invalid task mode. Defaulting to A" << endl;
	}
	
	cout << "Task mode: " << mode << endl;

	Parse parse_obj;
	parse_obj.parseNumber(input_file, 0);
	parse_obj.printNumber();

	cout << endl;
}
