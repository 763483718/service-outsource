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
	int InitEngine();//��ʼ��
	int UnInitEngine();//����ʼ��
	int FaceDetection(ASF_MultiFaceInfo &detectedFaces, IplImage *img);//�������
	int ExtractSingleFRFeature(ASF_SingleFaceInfo SingleDetectedFaces, ASF_FaceFeature &feature, IplImage *img);
	int ExtractFRFeature(ASF_MultiFaceInfo detectedFaces, ASF_FaceFeature &feature, IplImage *img, int i = 0);//��ȡ����ֵ
	int FacePairMatching(MFloat &confidenceLevel, ASF_FaceFeature feature1,ASF_FaceFeature feature2);//�����Ա�

	int FaceASFProcess(ASF_MultiFaceInfo detectedFaces, IplImage *img);//Process
	int AgeEstimation(ASF_MultiFaceInfo detectedFaces, IplImage *img,ASF_AgeInfo &ageInfo);//����
	int GenderEstimation(ASF_MultiFaceInfo detectedFaces, IplImage *img,ASF_GenderInfo &genderInfo);//�Ա�
	int Face3DAngle(ASF_MultiFaceInfo detectedFaces, IplImage *img,ASF_Face3DAngle &angleInfo);//3D�Ƕ�
	const ASF_VERSION* GetVersion();
private:
	MHandle handle;
};