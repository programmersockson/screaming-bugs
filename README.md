# screaming-bugs

![image](https://user-images.githubusercontent.com/88203669/214677852-89e85992-ceb0-448e-8a3e-9cfe0e9bdefb.png)

Extended version:

There are 3 types of resources: red, green, blue, 3 types of bugs respectively, as well as a queen and scouts.

The task of bugs is to provide the queen with resources. The colony of bugs is dynamic: bugs die and new ones appear.

The bugs are blind, they move by "hearing" until they find a resource, then they carry it to the queen. Each turn, they "cry" the distance from them to the resource and the queen, adding the distance of "hearing".

The scouts walk without reacting to "cry", but if they find a resource, they carry it to the queen.

The queen is always shifted towards the farthest resource. Each turn, based on the availability of resources, she decides to create a new insect or prolong her life.

Complications:

Resources move, so the insects change their angle a little every turn, and everyone's speed is a little different. The queen shifts towards the farthest resource.
