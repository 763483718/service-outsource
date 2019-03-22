//#pragma once
//#include <stdlib.h>
//#include <stdio.h>
//#include <windows.h>
//#include <string>
//#include <opencv2/highgui/highgui.hpp> 
//#include <opencv2/imgproc/imgproc.hpp> 
//#include <opencv2/core/core.hpp>
//#include "cv.h"
//#include "config.h"
//#include "FaceEngine.h"
//#include "merror.h"
//#include "inc\Arc\arcsoft_face_sdk.h"
//#include <fstream>
//#include <list>
//
//using namespace std;
//using namespace cv;
//
//
//
//struct student {
//	string name;
//	ASF_FaceFeature feature;
//	bool operator ==(const student &d)
//	{
//		return name == d.name;
//	}
//};
//
//void myCutOut(IplImage* src, IplImage* dst, int x, int y)
//{
//	CvSize size = cvSize(dst->width, dst->height);
//	cvSetImageROI(src, cvRect(x, y, size.width, size.height));
//	cvCopy(src, dst); 
//	cvResetImageROI(src);
//}
//
//bool cmp(float a, float b) {
//	return a > b;
//}
//
//int Judge(list<float> listOfLevel,bool &judge)
//	{
//	int res = 0;
//	listOfLevel.sort(cmp);
//	list<float>::iterator iter = listOfLevel.begin();
//	float max = *iter;
//	iter++;
//	float secend = *iter;
//	if (max > 0.7)
//	{
//		judge = 1;
//		return res;
//	}
//	if (max > 0.55&&max / secend > 5)
//	{
//		judge = 1;
//		return res;
//	}
//	judge = 0;
//
//	return res;
//}
//
//int VideoToPicture(char* videoPath, char* picturePath)
//{
//	int res = 0;
//
//	char imagePath[1024];
//
//	CvCapture* capture = cvCreateFileCapture(videoPath);
//	IplImage* img;
//	int rate = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FPS);
//	int countFrame = 1;
//	int count = 1;
//	printf("’˝‘⁄÷¥––£¨«Î…‘∫Ú\n");
//	while (true)
//	{
//
//		img = cvQueryFrame(capture);
//
//		if (img == nullptr) break;
//		countFrame++;
//		if (countFrame%rate != 0)
//			continue;
//
//		sprintf(imagePath, "%s%d.jpg", picturePath, count);
//		cvSaveImage(imagePath, img);
//		count++;
//	}
//
//	return res;
//}
//
//int SingleDeteFace(char* picturePath, char* dstPath, FaceEngine faceHandle)//by file
//{
//	int res = 0;
//
//	if (res != MOK)
//	{
//		printf("InitEngine error\terrorCode:%d\n", res);
//		return res;
//	}
//	IplImage* img = cvLoadImage(picturePath);
//	if (img == nullptr) return -1;
//	ASF_MultiFaceInfo faceInfo = { 0 };
//	faceHandle.FaceDetection(faceInfo, img);
//	if (faceInfo.faceNum == 0)
//	{
//		remove(picturePath);
//		return res;
//	}
//	for (int i = 0; i < faceInfo.faceNum; i++)
//	{
//		cvRectangle(img, cvPoint(faceInfo.faceRect[i].left, faceInfo.faceRect[i].top), cvPoint(faceInfo.faceRect[i].right, faceInfo.faceRect[i].bottom), cvScalar(255, 100, 100));
//	}
//	cvSaveImage(dstPath, img);
//
//
//	cvReleaseImage(&img);
//
//	return res;
//}
//
//int DeteFace(char* pictureFile, char* dstFile)
//{
//	int res; int i = 0;
//	char path[1024];
//	char dstPath[1024];
//	FaceEngine faceHandle;
//	faceHandle.InitEngine();
//	int count = 0;
//	while (true)
//	{
//		sprintf(path, "%s\\%d.jpg", pictureFile, i);
//		sprintf(dstPath, "%s\\%d.jpg", dstFile, i);
//		res = SingleDeteFace(path, dstPath, faceHandle);
//		if (res != -1)
//		{
//			count++;
//			if (count == 270)
//				break;
//		}
//		i++;
//	}
//	faceHandle.UnInitEngine();
//	return res;
//}
//
//
//int SinglePictureCompare(IplImage* img1, IplImage* img2, FaceEngine faceHandle)
//{
//	int res = 0;
//	ASF_MultiFaceInfo faceInfo = { 0 };
//	res = faceHandle.FaceDetection(faceInfo, img1);
//	if (res != MOK)
//	{
//		printf("Error:%d\n", res);
//		return res;
//	}
//	if (faceInfo.faceNum == 0)
//	{
//		printf("no face\n");
//	}
//	ASF_FaceFeature feature1 = { 0 };
//	ASF_FaceFeature copyfeature1 = { 0 };
//	res = faceHandle.ExtractFRFeature(faceInfo, feature1, img1);
//	//øΩ±¥feature
//	copyfeature1.featureSize = feature1.featureSize;
//	copyfeature1.feature = (MByte *)malloc(feature1.featureSize);
//	memset(copyfeature1.feature, 0, feature1.featureSize);
//	memcpy(copyfeature1.feature, feature1.feature, feature1.featureSize);
//
//
//
//	//char *buff= (char*)malloc(feature1.featureSize);
//
//	//std::ifstream i("feature.txt", std::ios::in | std::ios::binary);
//	//char name[sizeOfName];
//	//i.read(name, sizeOfName);
//	//int pos = i.tellg();
//	//
//	//i.read(buff, feature1.featureSize);
//	//pos = i.tellg();
//	//memcpy(copyfeature1.feature, buff, feature1.featureSize);
//
//
//	res = faceHandle.FaceDetection(faceInfo, img2);
//	if (res != MOK)
//	{
//		printf("Error:%d\n", res);
//		return res;
//	}
//	if (faceInfo.faceNum == 0)
//	{
//		printf("no face\n");
//	}
//
//	ASF_SingleFaceInfo SingleDetectedFaces1 = { 0 };
//	int max = 0; float maxLevel = 0;
//	for (int i = 0; i < faceInfo.faceNum; i++)
//	{
//		res = faceHandle.ExtractFRFeature(faceInfo, feature1, img2, i);
//		if (res != MOK)
//		{
//			continue;
//		}
//		MFloat level = 0;
//		res = faceHandle.FacePairMatching(level, feature1, copyfeature1);
//		printf("%d level is :%f\n", i, level);
//		if (maxLevel < level)
//		{
//			max = i;
//			maxLevel = level;
//		}
//	}
//	cvRectangle(img2, cvPoint(faceInfo.faceRect[max].left, faceInfo.faceRect[max].top), cvPoint(faceInfo.faceRect[max].right, faceInfo.faceRect[max].bottom), cvScalar(100, 100, 255));
//	cvSaveImage("temp.jpg", img2);
//
//	SafeFree(copyfeature1.feature);
//	return res;
//}
//
//
//int saveFeature()
//{
//	char name[sizeOfName];
//	char path[1024];
//	FaceEngine faceHandle;
//	faceHandle.InitEngine();
//	std::ofstream out("feature.txt", std::ios::binary | std::ios::app);
//	while (true)
//	{
//		printf("please enter the name of picture\n");
//		scanf("%s", name);
//		if (name[0] == 'q'&&name[1]=='\0')
//		{
//			break;
//		}
//		sprintf(path, "%s.jpg", name);
//		IplImage* img22 = cvLoadImage(path);
//		if (img22 == nullptr)
//		{
//			printf("wrong name\n");
//			cvReleaseImage(&img22);
//			continue;
//		}
//		IplImage* img = cvCreateImage(cvSize(img22->width - img22->width % 4, img22->height), IPL_DEPTH_8U, img22->nChannels);
//		myCutOut(img22, img, 0, 0);
//		cvReleaseImage(&img22);
//
//
//		ASF_MultiFaceInfo faceInfo = { 0 };
//		faceHandle.FaceDetection(faceInfo, img);
//		if (faceInfo.faceNum == 0)
//		{
//			printf("no face\n");
//		}
//		ASF_FaceFeature feature = { 0 };
//		int res = faceHandle.ExtractFRFeature(faceInfo, feature, img);
//		float level;
//		res = faceHandle.FacePairMatching(level, feature, feature);
//		out.write(name, sizeOfName);
//		out.write((const char*)feature.feature, sizeOfFeature);
//		cvReleaseImage(&img);
//	}
//	out.close();
//	faceHandle.UnInitEngine();
//	return 0;
//}
//
//
//int Compara(char* filePath)
//{
//	int res = 0;
//	//****************************************************** read feature into list
//	list<student> listOfFeature;
//	char name[sizeOfName];
//	string preName;
//	char *buff = (char*)malloc(sizeOfFeature);
//	std::ifstream in("feature.txt", ios::binary | ios::in);
//	
//	while (!in.eof())
//	{
//		in.read(name, sizeOfName);
//		int p = in.tellg();
//		in.read(buff, sizeOfFeature);
//		p = in.tellg();
//		if (name == preName)
//			continue;
//		student temp;
//		temp.name = name;
//		temp.feature.featureSize = sizeOfFeature;
//
//		temp.feature.feature = (MByte *)malloc(sizeOfFeature);
//		memset(temp.feature.feature, 0, sizeOfFeature);
//		memcpy(temp.feature.feature, buff, sizeOfFeature);
//
//		listOfFeature.push_back(temp);
//		preName = name;
//
//		//SafeFree(temp.feature.feature);
//	}
//	SafeFree(buff);
//	printf("finish read feature\nCompara ing...\n");
//
//	int size = listOfFeature.size();
//	//for (int i = 0; i < size; i++)
//	//{
//	//	printf("%s\n", listOfFeature.front().name.c_str());
//	//	listOfFeature.pop_front();
//	//}
//
//	//****************************************************** get shibie picture and dete
//	FaceEngine faceHandle;
//	faceHandle.InitEngine();
//	char path[1024];
//	for (int i = 0; i < 50; i++)
//	{
//		sprintf(path, "%s\\%d.jpg", filePath, i);
//		IplImage* img22 = cvLoadImage(path);
//		if (img22 == nullptr)
//		{
//			cvReleaseImage(&img22);
//			continue;
//		}
//		IplImage* img = cvCreateImage(cvSize(img22->width - img22->width % 4, img22->height), IPL_DEPTH_8U, img22->nChannels);
//		myCutOut(img22, img, 0, 0);
//		cvReleaseImage(&img22);
//
//		ASF_MultiFaceInfo faceInfo = { 0 };
//		faceHandle.FaceDetection(faceInfo, img);
//		if (faceInfo.faceNum == 0)
//		{
//			printf("no face\n");
//		}
//		ASF_FaceFeature feature = { 0 };
//		for (int k = 0; k < faceInfo.faceNum; k++)
//		{
//			res = faceHandle.ExtractFRFeature(faceInfo, feature, img, k);
//			if (res != MOK)
//			{
//				continue;
//			}
//			float level, maxLevel = 0;
//			int max = 0;
//			student maxStudent;
//			list<float> listOfLevel;
//			list<student>::iterator iter = listOfFeature.begin();
//			for (int c=0; iter != listOfFeature.end(); c++)
//			{
//				res = faceHandle.FacePairMatching(level, feature, iter->feature);
//
//				if (res != MOK)
//				{
//					printf("There is an error when FacePairMatching\n");
//					iter++;
//					continue;
//				}
//				listOfLevel.push_back(level);
//				if (level > maxLevel)
//				{
//					maxLevel = level;
//					max = c;
//					maxStudent = *iter;
//				}
//
//				//if (level > 0.5)
//				//{
//				//	IplImage* faceImage = cvCloneImage(img);
//				//	cvRectangle(faceImage, cvPoint(faceInfo.faceRect[k].left, faceInfo.faceRect[k].top), cvPoint(faceInfo.faceRect[k].right, faceInfo.faceRect[k].bottom), cvScalar(100, 100, 255));
//				//	char temp[1024];
//				//	sprintf(temp, "%s\\%d_%s.jpg", "C:\\picture\\2018-12-20\\compara", i, iter->name.c_str());
//				//	cvSaveImage(temp, faceImage);
//				//	cvReleaseImage(&faceImage);
//				//	printf("%s\t%d\n", iter->name.c_str(), listOfFeature.size());
//				//	listOfFeature.erase(iter++);
//				//	continue;
//				//}
//				iter++;
//			}
//			bool judge = 0;
//			Judge(listOfLevel, judge);
//			if (judge)
//			{
//				IplImage* faceImage = cvCloneImage(img);
//				cvRectangle(faceImage, cvPoint(faceInfo.faceRect[k].left, faceInfo.faceRect[k].top), cvPoint(faceInfo.faceRect[k].right, faceInfo.faceRect[k].bottom), cvScalar(100, 100, 255));
//				char temp[1024];
//				sprintf(temp, "%s\\%d_%s.jpg", "C:\\picture\\2018-12-20\\compara", i, maxStudent.name.c_str());
//				cvSaveImage(temp, faceImage);
//				cvReleaseImage(&faceImage);
//				printf("%s\t%d\n", maxStudent.name.c_str(), listOfFeature.size());
//				//listOfFeature.remove(maxStudent);
//				iter = listOfFeature.begin();
//				for (int m = 0; m <= max; m++)
//					if (m != max)iter++;
//				SafeFree(iter->feature.feature);
//				listOfFeature.erase(iter);
//			}
//		}
//		cvReleaseImage(&img);
//	}
//
//	faceHandle.UnInitEngine();
//
//	return 0;
//}
//
//
////int test()
////{
////	IplImage* img = cvLoadImage("heyu.jpg");
////	int count = 0;
////	while (true)
////	{
////		IplImage* imgTemp = cvCreateImage(cvSize(img->width - img->width % 4, img->height), IPL_DEPTH_8U, img->nChannels);
////		myCutOut(img, imgTemp, 0, 0);
////		cvReleaseImage(&imgTemp);
////		count++;
////		if (count == 1000)
////			break;
////	}
////	printf("over\n");
////	return 0;
////}