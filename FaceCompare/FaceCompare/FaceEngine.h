#pragma once

#include "stdafx.h"
#include "merror.h"
#include "arcsoft_face_sdk.h"
#include <opencv2\opencv.hpp>

class FaceEngine
{
public:
	FaceEngine();
	~FaceEngine();
	int InitEngine();//初始化
	int UnInitEngine();//反初始化
	int FaceDetection(ASF_MultiFaceInfo &detectedFaces, IplImage *img);//人脸检测
	int ExtractSingleFRFeature(ASF_SingleFaceInfo SingleDetectedFaces, ASF_FaceFeature &feature, IplImage *img);
	int ExtractFRFeature(ASF_MultiFaceInfo detectedFaces, ASF_FaceFeature &feature, IplImage *img, int i = 0);//提取特征值
	int FacePairMatching(MFloat &confidenceLevel, ASF_FaceFeature feature1,ASF_FaceFeature feature2);//人脸对比

	int FaceASFProcess(ASF_MultiFaceInfo detectedFaces, IplImage *img);//Process
	int AgeEstimation(ASF_MultiFaceInfo detectedFaces, IplImage *img,ASF_AgeInfo &ageInfo);//年龄
	int GenderEstimation(ASF_MultiFaceInfo detectedFaces, IplImage *img,ASF_GenderInfo &genderInfo);//性别
	int Face3DAngle(ASF_MultiFaceInfo detectedFaces, IplImage *img,ASF_Face3DAngle &angleInfo);//3D角度
	const ASF_VERSION* GetVersion();
private:
	MHandle handle;
};