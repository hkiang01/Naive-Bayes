#include "parse.h"

vector<int> Parse::getNumber()
{
	return number;
}

void Parse::setNumber(vector<int> i_number)
{
	number = i_number;
}

void Parse::parseNumber(string filename, int offset)
{
	string curr_line;
	ifstream myfile (filename.c_str());

	if(!myfile.is_open())
	{
		cout << "Error opening file" << endl;
		return;
	}
	int counter = 0;

	//skip 28*offset to get to correct number to parse
	for(int i = 0; i < offset; i++)
	{
		for(int j = 0; j < 28; j++)
		{
			getline(myfile, curr_line);
		}
	}

	while(getline(myfile, curr_line) && counter<28)
	{
		for(string::const_iterator it = curr_line.begin(); it!=curr_line.end(); ++it)
		{
			switch(*it)
			{
				case '#':
				case '+':
					number.push_back(1);
					break;
				default:
					number.push_back(0);
					break;
			}
		}
		counter++;
	}
	return;
}

void Parse::printNumber()
{
	int counter = 0;
	for(vector<int>::const_iterator it = number.begin(); it!=number.end(); ++it)
	{
		switch(*it)
		{
			case 1:
				cout << "*";
				break;
			default:
				cout << " ";
		}
		if(counter%28==0)
		{
			cout << endl;
		}
		counter++;
	}
}