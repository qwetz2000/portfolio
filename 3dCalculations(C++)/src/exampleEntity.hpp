#include "include/quaternion.hpp"

class Entity
{
public:
	Transform transform; // included with "quaternion.hpp"

};


class Cube : public Entity
{
public:
	int size = 2; // example size

	Vec3 scaledCorner[8];
	Vec3 rotatedCorner[8];
	Vec3 translatedCorner[8];

	void updateCorners()
	{
		//scaling
		scaledCorner[0] = { 0 - size / 2 * transform.scale.x, 0 - size / 2 * transform.scale.y, 0 - size / 2 * transform.scale.z };
		scaledCorner[1] = { 0 + size / 2 * transform.scale.x, 0 - size / 2 * transform.scale.y, 0 - size / 2 * transform.scale.z };
		scaledCorner[2] = { 0 - size / 2 * transform.scale.x, 0 + size / 2 * transform.scale.y, 0 - size / 2 * transform.scale.z };
		scaledCorner[3] = { 0 + size / 2 * transform.scale.x, 0 + size / 2 * transform.scale.y, 0 - size / 2 * transform.scale.z };
		scaledCorner[4] = { 0 - size / 2 * transform.scale.x, 0 - size / 2 * transform.scale.y, 0 + size / 2 * transform.scale.z };
		scaledCorner[5] = { 0 + size / 2 * transform.scale.x, 0 - size / 2 * transform.scale.y, 0 + size / 2 * transform.scale.z };
		scaledCorner[6] = { 0 - size / 2 * transform.scale.x, 0 + size / 2 * transform.scale.y, 0 + size / 2 * transform.scale.z };
		scaledCorner[7] = { 0 + size / 2 * transform.scale.x, 0 + size / 2 * transform.scale.y, 0 + size / 2 * transform.scale.z };

		//rotation
		Quaternion rotationQuaternion = combineEulerXYZ(transform.rotation.x, transform.rotation.y, transform.rotation.z);
		rotationQuaternion.normalize();
		for (int i = 0; i < 8; i++)
		{
			rotatedCorner[i] = rotateByQuaternion(scaledCorner[i], rotationQuaternion);
		}

		//translation
		for (int i = 0; i < 8; i++)
		{
			translatedCorner[i] = { rotatedCorner[i].x + transform.location.x, rotatedCorner[i].y + transform.location.y, rotatedCorner[i].z + transform.location.z };
		}
	}

	Cube() { updateCorners(); } // to create default cube on init
};