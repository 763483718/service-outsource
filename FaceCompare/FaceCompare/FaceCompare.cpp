#pragma once
#include "stdafx.h"
//#include "tool.h"
#include "RollCall.h"


int main(int argc, char** argv)
{
	RollCall rollCall("feature.txt");
	//string name;
	//cin >> name;
	//rollCall.AddFaceFeature("d");
	//rollCall.ReadFaceFeature("feature_1.txt");
	rollCall.Start(1,5,1);
	Sleep(5000000);

	//system("pause");
	return 0;
}

//int compara(char* shibiezhao = "C:\\picture\\2018-12-20\\diandao\\6.jpg", char* zhengjianzhao = "zhangchenyu.jpg")
//{
//	IplImage* img = cvLoadImage(shibiezhao);
//	IplImage* img22 = cvLoadImage(zhengjianzhao);
//	if (!img || !img22)
//	{
//		printf("please enter right path or name\n");
//		cvReleaseImage(&img);
//		cvReleaseImage(&img22);
//		return -1;
//	}
//	IplImage* img2 = cvCreateImage(cvSize(img22->width - img22->width % 4, img22->height), IPL_DEPTH_8U, img22->nChannels);
//	myCutOut(img22, img2, 0, 0);
//
//	FaceEngine faceHandle;
//	faceHandle.InitEngine();
//	SinglePictureCompare(img2, img, faceHandle);
//
//	faceHandle.UnInitEngine();
//	cvReleaseImage(&img);
//	cvReleaseImage(&img22);
//	cvReleaseImage(&img2);
//
//	return 0;
//}
//
//int main(int argc, char** argv)
//{
//
//	//VideoToPicture("F:\\服务外包\\视频\\2018-12-20\\1.mp4", "C:\\picture\\2018-12-20\\1\\");
//
//	time_t start, stop;
//	start = time(NULL);
//
//	//DeteFace("C:\\picture\\2018-12-20\\diandao", "C:\\picture\\2018-12-20\\face");
//	int a;
//	scanf("%d", &a);
//
//	switch (a)
//	{
//	case 1:
//	{
//		int num=-1;
//		char path[1024];
//		char name[256];
//		//while (true)
//		//{
//		//	num++;
//		//	if (num == 50)
//		//	{
//		//		break;
//		//	}
//		//	sprintf(path, "C:\\picture\\2018-12-20\\diandao\\%d.jpg", num);
//		//	compara(path, "xujingting.jpg");
//		//}
//		while (true) 
//		{
//			printf("please enter picture number of shibie\n");
//			scanf("%d", &num);
//			if (num == -1)
//			{
//				break;
//			}
//			printf("please enter picture name of zhuce\n");
//			scanf("%s", &name);
//			sprintf(name, "%s.jpg", name);
//			sprintf(path, "C:\\picture\\2018-12-20\\diandao\\%d.jpg", num);
//			compara(path, name);
//		}
//		break;
//	}
//	case 2:saveFeature(); break;
//	case 3:Compara("C:\\picture\\2018-12-20\\diandao"); break;
//	default:
//		break;
//	}
//
//	stop = time(NULL);
//	printf("Use Time:%ld\n", (stop - start));
//	
//	system("pause");
//	return 0;
//}
//
