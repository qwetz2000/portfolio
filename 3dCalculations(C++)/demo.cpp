#include "src/exampleEntity.hpp"

#include <iostream> // for std::cout

void demoCalculations()
{
	// creates an example obj and manipulates its location, rotation and scale
	Cube testCube;

	testCube.transform.scale.x = 1.5;
	testCube.transform.scale.z = 0.5;
	testCube.transform.scale.y = 1.2;

	testCube.transform.rotation.y = 10;
	testCube.transform.rotation.x = 20;
	testCube.transform.rotation.z = 30;

	testCube.transform.location.x = 2;
	testCube.transform.location.z = 3;
	testCube.transform.location.y = 4;


	// performs all needed calculations based on the given transform
	testCube.updateCorners();
	

	// prints the results in a way they are  easily copied to " https://www.geogebra.org/3d " for visual representation
	for (int i = 0; i < 8; i++)
	{
		std::cout << char('A' + i) << " = (" << testCube.translatedCorner[i].x << "," << testCube.translatedCorner[i].y << "," << testCube.translatedCorner[i].z << ")" << "\n\n";
	}
}