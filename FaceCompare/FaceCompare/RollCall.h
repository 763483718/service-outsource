#pragma once
#include "tool.h" 
#include <stdlib.h>
#include <stdio.h>
#include <windows.h>
#include <string>
#include <opencv2/highgui/highgui.hpp> 
#include <opencv2/imgproc/imgproc.hpp> 
#include <opencv2/core/core.hpp>
#include "cv.h"
#include "config.h"
#include "FaceEngine.h"
#include "merror.h"
#include "FileUtils.h"
#include "inc\Arc\arcsoft_face_sdk.h"
#include <fstream>
#include <list>
#include <iostream>

using namespace std;

class Student
{
public:
	string name;
	ASF_FaceFeature faceFeature;

public:
	Student(string name, ASF_FaceFeature faceFeature)
	{
		this->name = name;
		this->faceFeature.featureSize = faceFeature.featureSize;
		this->faceFeature.feature = (MByte *)malloc(faceFeature.featureSize);
		memset(this->faceFeature.feature, 0, faceFeature.featureSize);
		memcpy(this->faceFeature.feature, faceFeature.feature, faceFeature.featureSize);
	}
	Student(string name) { this->name = name; }

	string getName() { return name; }
	ASF_FaceFeature* getFaceFeature() { return &faceFeature; }

	void setName(string name) { this->name = name; }
	void setFaceFeature(char* buff,int size) 
	{	
		faceFeature.featureSize = size;
		faceFeature.feature = (MByte *)malloc(size);
		memset(faceFeature.feature, 0, size);
		memcpy(faceFeature.feature, buff, size);
	}


	bool operator ==(const Student &student)
	{
		return name == student.name;
	}
};


DWORD WINAPI ImageThread(LPVOID p);
DWORD WINAPI DeteThread(LPVOID p);
DWORD WINAPI FacePairMatchingThread(LPVOID p);


class RollCall
{
private:
	list<Student> m_listOfStudent;
	list<Student> m_listOfNotArraveStudent;
	list<Student> m_listOfArraveStudent;
	list<IplImage*> m_listOfImage;
	list<ASF_FaceFeature> m_listOfFaceFeature;
	list<char*> test;

	bool m_run = 0;
	list<HANDLE> m_listOfImageHandle;
	list<HANDLE> m_listOfDeteHandle;
	list<HANDLE> m_listOfMatchHandle;

	HANDLE m_Image_Empty;
	HANDLE m_Image_Full;
	HANDLE m_FaceFeature_Full;
	HANDLE m_FaceFeature_Empty;

	HANDLE m_Image_Mutex; //ª•≥‚¡ø
	HANDLE m_FaceInfo_Mutex;

	int ImageThreadImpl();
	int DeteThreadImpl();
	int FacePairMatchingThreadImpl();

public:
	RollCall(char* pathOfFeature = "feature.txt");
	int ReadFaceFeature(char* pathOfFeature);
	int Start(int numOfImageThread = 1, int numOfDeteThread = 1, int numOfCompareThread = 2);
	int AddFaceFeature(char* pathOfImage);
	int Terminate();

	friend DWORD WINAPI ImageThread(LPVOID p);
	friend DWORD WINAPI DeteThread(LPVOID p);
	friend DWORD WINAPI FacePairMatchingThread(LPVOID p);
};

class RollCallAdapter
{
private:
	RollCall* rollCall;
public:
	RollCallAdapter(RollCall* r) :rollCall(r) {};
	int Start(int numOfImageThread, int numOfDeteThread, int numOfCompareThread);
};

