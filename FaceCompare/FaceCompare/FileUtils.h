#pragma once
#include "stdafx.h"
#include <stdio.h>
//#include "merror.h"
#include <malloc.h>
#include <memory.h>
#include <stdlib.h>
#include <io.h>
#include <direct.h>
#include <vector>
#include <string>
#include <windows.h>
#include <TCHAR.h>
using std::vector;

class FileUtils
{
public:
	FileUtils()
	{
	}

	void getFile(const std::string & path, vector<std::string> &vecFileLists, std::string type);
	bool isEmptyFolder(const std::string & path);
	void getFolders(const std::string & path, vector<std::string> &folderLists);
	bool haveFile(const std::string & path);
	void MakeDir(std::string download_path, std::string path);
	~FileUtils()
	{
	}

private:	
	
};