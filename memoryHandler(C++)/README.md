
this memory handler was created with the following goals:

	- the ability to handle variables of any data type 
	- to keep those variables next to each other to reduce cache misses
	- allowing direct access to the variables with as little overhead as possible
	- to allow dynamic resizing while retaining the aforementioned goals


requirements that still have to be met:

	- more elaborate error handling
	- further performance optimisation (e.g. reduce number of resizes)

additional considerations:

	- implementation of a more user-friendly access option instead of pointers
		(e.g. a additional translation layer. this will cause additional overhead, so the option to use pointers should remain)