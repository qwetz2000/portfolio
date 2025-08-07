
This memory handler was created with the following goals:

The ability to handle variables of any data type.
To keep those variables next to each other to reduce cache misses.
Allowing direct access to the variables with as little overhead as possible.
To allow dynamic resizing while retaining the aforementioned goals.
Requirements that still have to be met:

More elaborate error handling.
Further performance optimization (e.g., reduce the number of resizes).
Additional considerations:

Implementation of a more user-friendly access option instead of pointers (e.g., an additional translation layer).
This will cause additional overhead, so the option to use pointers should remain.