#ifndef PARSE_H
#define PARSE_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;


class Parse{
	public:
		vector<int> getNumber();
		void setNumber(vector<int> i_number);
		void parseNumber(string filename, int index);
		void printNumber();
	private:
		vector<int>number;
};

#endif
