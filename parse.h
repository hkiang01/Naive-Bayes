#ifndef PARSE_H
#define PARSE_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;


class Parse{
	public:
		vector<int> number;
		void parseNumber(string filename, int index);
		void printNumber();
};

#endif
