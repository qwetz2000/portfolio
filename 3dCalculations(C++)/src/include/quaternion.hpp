#include "sharedResources.hpp" // for Global::PI"
#include "transform.hpp"

#include <cmath>	// used for sqrt, sin, cos,

struct Quaternion
{
	double w, x, y, z;

	Quaternion(double w, double x, double y, double z) : w(w), x(x), y(y), z(z) {}

	void normalize()
	{
		double length = sqrt(w * w + x * x + y * y + z * z);
		if (length > 0)
		{
			w /= length;
			x /= length;
			y /= length;
			z /= length;
		}
	}

	Quaternion conjugate() const
	{
		return { w,-x,-y,-z };
	}

	Quaternion operator*(const Quaternion& q) const // performs multiplication of 2 quaternions
	{
		return
		{
			w * q.w - x * q.x - y * q.y - z * q.z,
			w * q.x + x * q.w + y * q.z - z * q.y,
			w * q.y - x * q.z + y * q.w + z * q.x,
			w * q.z + x * q.y - y * q.x + z * q.w
		};
	}
};


//a set of functions to be used when working with euler angles
Quaternion Vec3ToQuaternion(Vec3 inputVector)
{
	return { 0, inputVector.x, inputVector.y, inputVector.z };
}

Vec3 QuaternionToVec3(Quaternion inputQuaternion)
{
	return { inputQuaternion.x, inputQuaternion.y, inputQuaternion.z };
}

Quaternion eulerXtoQuaternion(double degreeX)
{
	double radiansX = degreeX * (Global::PI / 180.0);

	return { cos(radiansX / 2), sin(radiansX / 2), 0.0, 0.0 };
}

Quaternion eulerYtoQuaternion(double degreeY)
{
	double radiansY = degreeY * (Global::PI / 180.0);

	return { cos(radiansY / 2), 0.0, sin(radiansY / 2), 0.0 };
}

Quaternion eulerZtoQuaternion(double degreeZ)
{
	double radiansZ = degreeZ * (Global::PI / 180.0);

	return { cos(radiansZ / 2), 0.0, 0.0, sin(radiansZ / 2) };
}

// in this case only given in order X->Y->Z. other orders produce different results!
// if other orders where to be used, the function can be dublicated, renamed and have the calculation order adjusted
Quaternion combineEulerXYZ(double eulerX, double eulerY, double eulerZ)
{
	return eulerXtoQuaternion(eulerX) * eulerYtoQuaternion(eulerY) * eulerZtoQuaternion(eulerZ);
}

Vec3 rotateByQuaternion(const Vec3& targetVector, const Quaternion& rotationQuaternion)
{
	return QuaternionToVec3(rotationQuaternion * Vec3ToQuaternion(targetVector) * rotationQuaternion.conjugate());
}