#include <iostream> // only used in debugView()
#include <cstring> // for memcpy()

class MemBatch
{
	unsigned char* data;
	int length;
	unsigned char* cursor;
	void*** allVars;
	int nVars;

	void extendData(const int& extendNBytes) // data is a unsigned char array, that holds the entire data of the batch
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

	void extendAllVars() // allVars is a void** array holding the memory adresses of pointers used to allocate partial data of the batch 
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

	void shrinkData() // resizes the data array to the minimum size required to hold the currently included batch data
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

	void shrinkAllVars() // resizes the allVars array to the minimum size given by the number of items in the batch
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
	void remove(T* var, int element) // takes the pointer used to allocate the data and the index of the pointer adress within allVars and removes the item (used index is provided by the pop method)
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
	MemBatch(const int& startSize) // creates a batch with a given starting byte size
	{
		length = startSize;
		if (length < 1) length = 1;
		data = new unsigned char[length];
		cursor = data;
		nVars = 0;
		allVars = nullptr;
	}

	~MemBatch() // releases remaining resources
	{
		delete[] data;
		if (!(allVars == nullptr)) delete[]allVars;
	}

	template <typename T>
	void request(T*& any) // takes an pointer of any type and allocates memory within the batch, sets the given pointer to the new adress within the batch and copys data if the pointer already points to a variable (previously heap allocated variables have to be manages carefully to avoid memory leaks!)
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
	void pop(T* var) // deallocates a in batch allocated variable with the same pointer used to allocate it
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