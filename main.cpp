#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include "parse.h"

using namespace std;
int main(int argc, char* argv[])
{

	if (argc!=3) 
	{
		cout << "Error, usage: ./mp3 <int offset> <string filename>" << endl;
		return 1;
	}
	const char* i_offset = argv[1];
	int input_offset = atoi(i_offset);
	string input_file = argv[2];

	cout << "Offset: " << input_offset << endl;

	Parse parse_obj;
	parse_obj.parseNumber(input_file, input_offset);
	parse_obj.printNumber();

	cout << endl;
}
