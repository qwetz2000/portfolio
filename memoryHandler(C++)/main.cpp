#include "memBatch.hpp" // includes the souce file

int main()
{
	// create a batch with starting byte-size of 2
	MemBatch batch(2);
	
	// create initial variables to copy from
	int a = 'a';
	int b = 'b';
	char c = 'c';
	char d = 'd';

	// getting pointers to the initial variables
	auto* ptr1 = &a;
	auto* ptr2 = &b;
	auto* ptr3 = &c;
	auto* ptr4 = &d;

	// request memory from the batch independent of type
	batch.request(ptr1);
	batch.request(ptr2);
	batch.request(ptr3);
	batch.request(ptr4);

	// show batch data to confirm insertion
	batch.debugView();

	// manipulate allocated data
	*ptr1 = 'A';
	*ptr2 = 'B';
	*ptr3 = 'C';
	*ptr4 = 'D';

	// show manipulation result
	batch.debugView();

	// remove element assigned to ptr2 from batch
	batch.pop(ptr2);

	// manipulate element assigned to ptr3
	*ptr3 = 'c';

	// re-request memory for ptr2 from batch and assign a value to it
	batch.request(ptr2);
	*ptr2 = 'b';

	// show final result
	batch.debugView();

	// remaining resources will be released on destructor call
	return 0;
}