#include "stdafx.h"
#include "RollCall.h"

#define IMAGE_N 10
#define FACE_INFO_N 10



void myCutOut(IplImage* src, IplImage* dst, int x, int y);
int Judge(list<float> listOfLevel, bool &judge);

DWORD WINAPI ImageThread(LPVOID p)
{
	RollCall * pdlg = (RollCall *)p;
	pdlg->ImageThreadImpl();
	return 0;
}

DWORD WINAPI DeteThread(LPVOID p)
{
	RollCall * pdlg = (RollCall *)p;
	pdlg->DeteThreadImpl();
	return 0;
}

DWORD WINAPI FacePairMatchingThread(LPVOID p)
{
	RollCall * pdlg = (RollCall *)p;
	pdlg->FacePairMatchingThreadImpl();
	return 0;
}


RollCall::RollCall(char * pathOfFeature)
{
	m_Image_Empty = CreateSemaphore(NULL, IMAGE_N, IMAGE_N, NULL);
	m_Image_Full = CreateSemaphore(NULL, 0, IMAGE_N, NULL);

	m_FaceFeature_Empty = CreateSemaphore(NULL, FACE_INFO_N, FACE_INFO_N, NULL);
	m_FaceFeature_Full = CreateSemaphore(NULL, 0, FACE_INFO_N, NULL);

	m_Image_Mutex = CreateMutex(NULL, FALSE, NULL);
	m_FaceInfo_Mutex = CreateMutex(NULL, FALSE, NULL);

	ReadFaceFeature(pathOfFeature);

}

int RollCall::ReadFaceFeature(char * pathOfFeature)
{
	char name[sizeOfName];
	string preName;
	char *buff = (char*)malloc(sizeOfFeature);
	std::ifstream in(pathOfFeature, ios::binary | ios::in);
	if (!in.is_open()) { return -1; }
	while (!in.eof())
	{
		in.read(name, sizeOfName);
		in.read(buff, sizeOfFeature);
		if (name == preName)
			continue;
		printf("%s\n", name);
		Student temp(name);
		temp.setFaceFeature(buff, sizeOfFeature);
		m_listOfStudent.push_back(temp);
		preName = name;
	}
	SafeFree(buff);
	//for (list<Student>::iterator i = m_listOfStudent.begin(); i != m_listOfStudent.end(); i++)
	//{
	//	printf("lalalal   %s\n", i->name.c_str());
	//}
	printf("\n\n\n");
	return 0;
}

int RollCall::Start(int numOfImageThread, int numOfDeteThread, int numOfCompareThread)
{
	m_run = 1;
	//list<HANDLE>::iterator ImageIter = m_listOfImageHandle.begin();
	//list<HANDLE>::iterator DeteIter = m_listOfDeteHandle.begin();
	//list<HANDLE>::iterator MatchIter = m_listOfMatchHandle.begin();
	HANDLE ImageTest=NULL;
	HANDLE DeteTest;
	HANDLE MatchTest;
	for (int i = 0; i < numOfImageThread; i++)
	{
		ImageTest = CreateThread(NULL, 0, ImageThread, this, 0, NULL);
		m_listOfImageHandle.push_back(ImageTest);
		//m_listOfImageHandle.push_back(CreateThread(NULL, 0, ImageThread, 0, 0, NULL));
		Sleep(500);
	}
	for (int i = 0; i < numOfDeteThread; i++)
	{
		DeteTest = CreateThread(NULL, 0, DeteThread, this, 0, NULL);
		m_listOfDeteHandle.push_back(DeteTest);
		//m_listOfDeteHandle.push_back(CreateThread(NULL, 0, DeteThread, 0, 0, NULL));
		Sleep(500);
	}
	for (int i = 0; i < numOfCompareThread; i++)
	{
		MatchTest = CreateThread(NULL, 0, FacePairMatchingThread, this, 0, NULL);
		m_listOfMatchHandle.push_back(MatchTest);
		//m_listOfMatchHandle.push_back(CreateThread(NULL, 0, FacePairMatchingThread, 0, 0, NULL));
		Sleep(500);
	}

	//printf("working...\n");

	for (int i = 0; i < numOfImageThread; i++)
	{
		if (WaitForSingleObject(ImageTest, INFINITE) == WAIT_OBJECT_0)
		{
			CloseHandle(m_listOfImageHandle.front());
			m_listOfImageHandle.pop_front();
		}
	}

	for (int i = 0; i < numOfDeteThread; i++)
	{
		if (WaitForSingleObject(m_listOfDeteHandle.front(), INFINITE) == WAIT_OBJECT_0)
		{
			CloseHandle(m_listOfDeteHandle.front());
			m_listOfDeteHandle.pop_front();
		}
	}

	for (int i = 0; i < numOfCompareThread; i++)
	{
		if (WaitForSingleObject(m_listOfMatchHandle.front(), INFINITE) == WAIT_OBJECT_0)
		{
			CloseHandle(m_listOfMatchHandle.front());
			m_listOfMatchHandle.pop_front();
		}
	}
	CloseHandle(m_Image_Empty);
	CloseHandle(m_Image_Full);
	CloseHandle(m_FaceFeature_Full);
	CloseHandle(m_FaceFeature_Empty);
	CloseHandle(m_Image_Mutex);
	CloseHandle(m_FaceInfo_Mutex);

	printf("over\n");

	return 0;
}

int RollCall::ImageThreadImpl()
{
	FileUtils fileUtils;
	vector<std::string> imagePath;
	fileUtils.getFile("C:\\picture\\2018-12-20\\diandao", imagePath, "jpg");
	//char file[1024] = "F:\\服务外包\\picture\\2018-12-27\\diandao\\";
	//char path[1024];
	vector<std::string>::iterator iter = imagePath.begin();
	IplImage* img = nullptr;
	for (;iter!=imagePath.end();iter++)
	{
		//sprintf(path, "%s%d.jpg", file, i);
		
		IplImage* imgBefore = cvLoadImage(iter->c_str());
		if (!imgBefore)
		{
			cvReleaseImage(&imgBefore);
			continue;
		}
		img = cvCreateImage(cvSize(imgBefore->width - imgBefore->width % 4, imgBefore->height), imgBefore->depth, imgBefore->nChannels);
		myCutOut(imgBefore, img, 0, 0);
		cvReleaseImage(&imgBefore);
		if (WaitForSingleObject(m_Image_Empty, INFINITE) == WAIT_OBJECT_0)
		{
			if (WaitForSingleObject(m_Image_Mutex, INFINITE) == WAIT_OBJECT_0)
			{
				m_listOfImage.push_back(img);
			}
		}
		ReleaseMutex(m_Image_Mutex);
		ReleaseSemaphore(m_Image_Full, 1, NULL);

		Sleep(300);
	}
	printf("have done reading image\n");
	int a;
	scanf("%d", &a);
	m_run = 0;
	return 0;
}

int RollCall::DeteThreadImpl()
{
	int res = 0;
	FaceEngine faceHandle;
	res = faceHandle.InitEngine();
	if (res != MOK)
	{
		printf("There is an error when InitEngine at DeteThreadImpl:%d\n", res);
		return res;
	}
	ASF_MultiFaceInfo faceInfo = { 0 };
	IplImage* img = nullptr;
	while (m_run)
	{
		if (WaitForSingleObject(m_Image_Full, 500) == WAIT_OBJECT_0)
		{
			if (WaitForSingleObject(m_Image_Mutex, 500) == WAIT_OBJECT_0)
			{
				img = m_listOfImage.front();
				m_listOfImage.pop_front();
			}
			else continue;
		}
		else continue;
		ReleaseMutex(m_Image_Mutex);
		ReleaseSemaphore(m_Image_Empty, 1, NULL);

		res = faceHandle.FaceDetection(faceInfo, img);
		if (res != MOK)
		{
			printf("There is an error when faceDetection at DeteThreadImpl%d\n", res);
			cvReleaseImage(&img);
			continue;
		}
		if (faceInfo.faceNum == 0)
		{
			cvReleaseImage(&img);
			continue;
		}
		ASF_FaceFeature faceFeature = { 0 };
		ASF_FaceFeature copyFeature = { 0 };
		for (int i = 0; i < faceInfo.faceNum; i++)
		{
			res = faceHandle.ExtractFRFeature(faceInfo, faceFeature, img, i);
			if (res != MOK)
			{
				//printf("There is an error when ExtractFRFeature at DeteThreadImpl%d\n", res);
				continue;
			}
			copyFeature.featureSize = faceFeature.featureSize;
			copyFeature.feature = (MByte*)malloc(faceFeature.featureSize);
			memset(copyFeature.feature, 0, faceFeature.featureSize);
			memcpy(copyFeature.feature, faceFeature.feature, faceFeature.featureSize);
			if (WaitForSingleObject(m_FaceFeature_Empty, INFINITE) == WAIT_OBJECT_0)
			{
				if (WaitForSingleObject(m_FaceInfo_Mutex, INFINITE) == WAIT_OBJECT_0)
				{
					m_listOfFaceFeature.push_back(copyFeature);
				}
			}
			ReleaseMutex(m_FaceInfo_Mutex);
			ReleaseSemaphore(m_FaceFeature_Full, 1, NULL);
		}
		cvReleaseImage(&img);
	}
	
	faceHandle.UnInitEngine();
	if (m_listOfImage.size() != 0)
	{
		for (list<IplImage*>::iterator iter = m_listOfImage.begin(); iter != m_listOfImage.end();)
		{
			cvReleaseImage(&*iter);
			m_listOfImage.erase(iter++);
		}
	}
	return 0;
}

int RollCall::FacePairMatchingThreadImpl()
{
	FaceEngine faceHandle;
	faceHandle.InitEngine();
	list<float> listOflevel; float level = -1;
	ASF_FaceFeature faceFeature = { 0 };
	while (m_run)
	{
		if (WaitForSingleObject(m_FaceFeature_Full, 500) == WAIT_OBJECT_0)
		{
			if (WaitForSingleObject(m_FaceInfo_Mutex, 500) == WAIT_OBJECT_0)
			{
				faceFeature = m_listOfFaceFeature.front();
				m_listOfFaceFeature.pop_front();
			}
			else continue;
		}
		else continue;
		ReleaseMutex(m_FaceInfo_Mutex);
		ReleaseSemaphore(m_FaceFeature_Empty, 1, NULL);
		int max = 0; float maxLevel = -1; int count = 0;
		list<Student>::iterator iter = m_listOfStudent.begin();
		for (; iter != m_listOfStudent.end(); iter++)
		{
			int res = faceHandle.FacePairMatching(level, faceFeature, iter->faceFeature);
			if (res != MOK)
			{
				printf("There is an error when FacePairMatching\n");
				continue;
			}
			if (maxLevel < level)
			{
				max = count;
				maxLevel = level;
			}
			listOflevel.push_back(level);
			count++;
		}
		bool judge = 0;
		if (listOflevel.size() == 0)
		{
			listOflevel.clear();
			SafeFree(faceFeature.feature);
			continue;
		}
		int res = Judge(listOflevel, judge);
		if (judge)
		{
			iter = m_listOfStudent.begin();
			int i = 0;
			for (; i <= max; i++)
			{
				if (i != max) iter++;
			}
			printf("%s\n", iter->getName().c_str());
			m_listOfArraveStudent.push_back(*iter);
			m_listOfStudent.erase(iter);
		}
		listOflevel.clear();
		SafeFree(faceFeature.feature);
		if (m_listOfStudent.size() == 0)
		{
			printf("finish diandao\n");
			
			m_run = 0;
		}
	}
	if (m_listOfFaceFeature.size() != 0)
	{
		for (list<ASF_FaceFeature>::iterator iter = m_listOfFaceFeature.begin(); iter != m_listOfFaceFeature.end(); )
		{
			SafeFree(iter->feature);
			m_listOfFaceFeature.erase(iter++);
		}
	}
	return 0;
}

int RollCall::AddFaceFeature(char * pathOfImage)
{
	char name[sizeOfName];
	char path[1024];
	FaceEngine faceHandle;
	faceHandle.InitEngine();
	std::ofstream out("feature_1.txt", std::ios::binary | std::ios::app);
	while (true)
	{
		printf("please enter the name of picture\n");
		scanf("%s", name);
		if (name[0] == 'q'&&name[1] == '\0')
		{
			break;
		}
		sprintf(path, "%s.jpg", name);
		IplImage* img22 = cvLoadImage(path);
		if (img22 == nullptr)
		{
			printf("wrong name\n");
			cvReleaseImage(&img22);
			continue;
		}
		IplImage* img = cvCreateImage(cvSize(img22->width - img22->width % 4, img22->height), IPL_DEPTH_8U, img22->nChannels);
		myCutOut(img22, img, 0, 0);
		cvReleaseImage(&img22);

		ASF_MultiFaceInfo faceInfo = { 0 };
		faceHandle.FaceDetection(faceInfo, img);
		if (faceInfo.faceNum == 0)
		{
			printf("no face\n");
		}
		ASF_FaceFeature feature = { 0 };
		int res = faceHandle.ExtractFRFeature(faceInfo, feature, img);
		float level;
		res = faceHandle.FacePairMatching(level, feature, feature);
		out.write(name, sizeOfName);
		out.write((const char*)feature.feature, sizeOfFeature);
		cvReleaseImage(&img);
	}
	out.close();
	faceHandle.UnInitEngine();
	return 0;
}

int RollCall::Terminate()
{
	return 0;
}




void myCutOut(IplImage* src, IplImage* dst, int x, int y)
{
	CvSize size = cvSize(dst->width, dst->height);
	cvSetImageROI(src, cvRect(x, y, size.width, size.height));
	cvCopy(src, dst);
	cvResetImageROI(src);
}


bool cmp(float a, float b) {
	return a > b;
}

int Judge(list<float> listOfLevel, bool &judge)
{
	int res = 0;
	listOfLevel.sort(cmp);
	list<float>::iterator iter = listOfLevel.begin();
	float max = *iter;
	if (listOfLevel.size() < 2)
	{
		if(max>0.7)
			judge = 1;
		return res;
	}
	iter++;
	float secend = *iter;
	if (max > 0.7)
	{
		judge = 1;
		return res;
	}
	if (max > 0.55&&max / secend > 5)
	{
		judge = 1;
		return res;
	}
	judge = 0;

	return res;
}