#pragma once
#include "stdafx.h"
#include "config.h"
#include "FaceEngine.h"

FaceEngine::FaceEngine()
{

}

FaceEngine::~FaceEngine()
{

}
int FaceEngine::InitEngine()
{
	//����ӿ�
	MRESULT res = ASFActivation(APPID, SDKKEY);
	//ALActivation fail
	if (MOK != res && 90114 != res)
		return res;

	//��ʼ���ӿ�
	handle = NULL;
	MInt32 mask = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE;
	res = ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, 32, 30, mask, &handle);
	return res;
}

int FaceEngine::FaceDetection(ASF_MultiFaceInfo &detectedFaces, IplImage *img)
{
	int res = ASFDetectFaces(handle, img->width, img->height, ASVL_PAF_RGB24_B8G8R8, (MUInt8*)img->imageData, &detectedFaces);

	return res;
}

int FaceEngine::ExtractSingleFRFeature(ASF_SingleFaceInfo SingleDetectedFaces, ASF_FaceFeature & feature, IplImage * img)
{
	int res = ASFFaceFeatureExtract(handle, img->width, img->height, ASVL_PAF_RGB24_B8G8R8, (MUInt8*)img->imageData, &SingleDetectedFaces, &feature);
	
	return 0;
}

int FaceEngine::ExtractFRFeature(ASF_MultiFaceInfo detectedFaces, ASF_FaceFeature &feature, IplImage *img, int i)
{
	ASF_SingleFaceInfo SingleDetectedFaces = { 0 };

	SingleDetectedFaces.faceRect.left = detectedFaces.faceRect[i].left;
	SingleDetectedFaces.faceRect.top = detectedFaces.faceRect[i].top;
	SingleDetectedFaces.faceRect.right = detectedFaces.faceRect[i].right;
	SingleDetectedFaces.faceRect.bottom = detectedFaces.faceRect[i].bottom;
	SingleDetectedFaces.faceOrient = detectedFaces.faceOrient[i];

	int res = ASFFaceFeatureExtract(handle, img->width, img->height, ASVL_PAF_RGB24_B8G8R8, (MUInt8*)img->imageData, &SingleDetectedFaces, &feature);

	return res;
}

int FaceEngine::FacePairMatching(MFloat &confidenceLevel, ASF_FaceFeature feature1, ASF_FaceFeature feature2)
{
	int res = ASFFaceFeatureCompare(handle, &feature1, &feature2, &confidenceLevel);
	
	return res;
}


int FaceEngine::FaceASFProcess(ASF_MultiFaceInfo detectedFaces, IplImage *img)
{
	MInt32 lastMask = ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE;
	int res = ASFProcess(handle, img->width, img->height, ASVL_PAF_RGB24_B8G8R8, (MUInt8*)img->imageData, &detectedFaces, lastMask);
	return res;
}

int FaceEngine::AgeEstimation(ASF_MultiFaceInfo detectedFaces, IplImage *img, ASF_AgeInfo &ageInfo)
{
	// ��ȡ����
	int res = ASFGetAge(handle, &ageInfo);

	return res;
}

int FaceEngine::GenderEstimation(ASF_MultiFaceInfo detectedFaces, IplImage *img, ASF_GenderInfo &genderInfo)
{

	// ��ȡ�Ա�
	int res = ASFGetGender(handle, &genderInfo);

	return res;
}

int FaceEngine::Face3DAngle(ASF_MultiFaceInfo detectedFaces, IplImage *img, ASF_Face3DAngle &angleInfo)
{

	// ��ȡ3D�Ƕ�
	int res = ASFGetFace3DAngle(handle, &angleInfo);

	return res;
}



const ASF_VERSION* FaceEngine::GetVersion()
{
	const ASF_VERSION* pVersionInfo = ASFGetVersion(handle);
	return pVersionInfo;
}


int FaceEngine::UnInitEngine()
{
	//����ʼ��
	int res = ASFUninitEngine(handle);

	//getchar();

	return res;
}