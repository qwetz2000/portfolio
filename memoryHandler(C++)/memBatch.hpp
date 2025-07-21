#include <iostream> // only used in debugView()
#include <cstring> // for memcpy()

class MemBatch
{
	unsigned char* data;
	int length;
	unsigned char* cursor;
	void*** allVars;
	int nVars;

	void extendData(const int& extendNBytes)
	{
		int newLength = length + extendNBytes;
		if (newLength <= length) return;
		unsigned char* newData = new unsigned char[newLength];
		memcpy((void*)newData, data, length);
		delete[] data;
		cursor = newData + (cursor - data);
		for (int i = 0; i < nVars; i++)
		{
			*(allVars[i]) = newData + ((unsigned char*)(*(allVars[i])) - data);
		}
		length = newLength;
		data = newData;
	}

	void extendAllVars()
	{
		void*** newVars = new void**[nVars + 1];
		if (nVars > 0)
		{
			memcpy(newVars, allVars, sizeof(void**) * nVars);
			delete[] allVars;
		}
		nVars++;
		allVars = newVars;
	}

	void shrinkData()
	{
		int minLength = cursor - data;
		if (minLength < 1) minLength = 1;
		unsigned char* newData = new unsigned char[minLength];
		memcpy(newData, data, minLength);
		delete[] data;
		cursor = newData + (cursor - data);
		for (int i = 0; i < nVars; i++)
		{
			*(allVars[i]) = newData + ((unsigned char*)(*(allVars[i])) - data);
		}
		length = minLength;
		data = newData;
	}

	void shrinkAllVars()
	{
		nVars--;
		if (nVars < 1)
		{
			delete[] allVars;
			allVars = nullptr;
			return;
		}
		void*** newVars = new void** [nVars];
		memcpy(newVars, allVars, sizeof(void**) * nVars);
		delete[] allVars;
		allVars = newVars;
	}

	template <typename T>
	void remove(T* var, int element)
	{
		int Tsize = sizeof(T);
		int copyPosition = (unsigned char*)var - data;
		int cursorPosition = cursor - data;
		var = nullptr;
		while (copyPosition + Tsize < cursorPosition)
		{
			data[copyPosition] = data[copyPosition + Tsize];
			copyPosition++;
		}
		cursor -= Tsize;
		for (int i = element; i < nVars - 1; i++)
		{
			allVars[i] = allVars[i + 1];
			unsigned char* start = (unsigned char*)(*(allVars[i]));
			*(allVars[i]) = start - Tsize;
		}
	}

public:
	MemBatch(const int& startSize)
	{
		length = startSize;
		if (length < 1) length = 1;
		data = new unsigned char[length];
		cursor = data;
		nVars = 0;
		allVars = nullptr;
	}

	~MemBatch()
	{
		delete[] data;
		if (!(allVars == nullptr)) delete[]allVars;
	}

	template <typename T>
	void request(T*& any)
	{
		int Tsize = sizeof(T);
		int avaiableSpace = length - (cursor - data);
		if (Tsize > avaiableSpace) extendData(Tsize - avaiableSpace);
		if (any != nullptr) *(T*)cursor = *any;
		any = (T*)cursor;
		extendAllVars();
		allVars[nVars - 1] = (void**)(&any);
		cursor += Tsize;
	}

	template <typename T>
	void pop(T* var)
	{
		for (int i = 0; i < nVars; i++)
		{
			if (*(allVars[i]) == (void*)(var))
			{
				remove(var, i);
				shrinkAllVars();
				shrinkData();
				return;
			}
		}
	}

	// does not influence functionality, only a debug and preview tool
	void debugView()
	{
		std::string out;
		for (int i = 0; i < length; i++)
		{
			out += data[i];
		}
		out += '\n';
		std::cout << "batch data : " << out << '\n';
	}
};