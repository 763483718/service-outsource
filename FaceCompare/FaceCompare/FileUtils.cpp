#pragma once
#include "stdafx.h"
#include "FileUtils.h"

int Str2CStr(WCHAR src[], int len, char dst[])
{
	return WideCharToMultiByte(CP_ACP, NULL, src, -1, dst, len + 1, NULL, NULL);
}

void FileUtils::getFile(const std::string & path, vector<std::string> &vecFileLists, std::string type)
{
	//文件句柄  
	long hFile = 0;
	//文件信息，_finddata_t需要io.h头文件  
	struct _finddata_t fileinfo;
	std::string strPath;
	std::string p;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					getFile(p.assign(path).append("\\").append(fileinfo.name), vecFileLists, type);
			}
			else
			{
				std::string namess = fileinfo.name;
				std::string str = namess.substr(namess.length() - 3); //截取文件名后3位
				if (str == type)
		        vecFileLists.push_back(p.assign(path).append("\\").append(fileinfo.name).c_str());
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
}

bool FileUtils::haveFile(const std::string & path)
{
	//文件句柄  
	long hFile = 0;
	struct _finddata_t fileinfo;
	std::string p;
	bool bHaveFile = false;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				//if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
				//{
				//	//folderLists.push_back(p.assign(path).append("\\").append(fileinfo.name));
				////	getFolders(p.assign(path).append("\\").append(fileinfo.name), folderLists);
				//}
			}
			else
			{
				bHaveFile = true;
				break;
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
	return bHaveFile;
}

void FileUtils::getFolders(const std::string & path, vector<std::string> &folderLists)
{
	//文件句柄  
	long hFile = 0;
	struct _finddata_t fileinfo;
	std::string p;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
				{

					folderLists.push_back(p.assign(path).append("\\").append(fileinfo.name));
					getFolders(p.assign(path).append("\\").append(fileinfo.name), folderLists);
				}
			}
			else
			{
				break;
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
}

bool FileUtils::isEmptyFolder(const std::string & path)
{
	long hFile = 0;
	struct _finddata_t fileinfo;
	std::string p;
	bool bEmpty = true;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				if (strcmp(fileinfo.name, "noFace") != 0 && strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
				{
					bEmpty = false;
					break;
				}
			}
			else
			{
				bEmpty = false;
				break;
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
	return bEmpty;
}

void FileUtils::MakeDir(std::string download_path, std::string path)
{
	std::string temp = path.substr(download_path.length(), path.length() - download_path.length());
	std::string temp_path = download_path;
	std::string folder_name;
	int npos;// = temp.find("\\");
	while (true)
	{
		npos = temp.find("\\");
		if (npos == -1)
			break;
		//npos = temp_path.length() + npos;
		folder_name = temp.substr(0, npos);
		temp = temp.substr(npos + 1, temp.length() +1 - npos);
		temp_path = temp_path + folder_name + "\\";
		if (_access(temp_path.c_str(), 0) == -1)
		{
			_mkdir(temp_path.c_str());
		}
		//	break;
	}
}