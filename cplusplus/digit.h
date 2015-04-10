#ifndef DIGIT_H
#define DIGIT_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;


class Digit{
	public:
		vector<int> getNumber();
		void setNumber(vector<int> i_number);
		void parseNumber(string filename, int index);
		void printNumber();
	private:
		vector<int>number;
};

#endif
