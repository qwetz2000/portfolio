#include "vector3.hpp"

class Transform
{
public:
	Vec3 location;
	Vec3 rotation;
	Vec3 scale;

	Transform(Vec3 locationValue = Vec3(), Vec3 rotationValue = Vec3(), Vec3 scaleValue = Vec3(1, 1, 1))
		: location(locationValue), rotation(rotationValue), scale(scaleValue) {
	}
};