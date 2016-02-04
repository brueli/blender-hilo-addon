# blender-hilo-addon

**A Blender addon for working with high- and lowpoly meshes.**


The Hilo Addon adds functionality to finalize and export complex high- and lowpoly models for texturing with external tools like the Allegorithmic tool suite.


## The idea behind it

When I started developing my first game-engine models with Blender, I was often frustrated when I had to "destroy" my properly designed objects and modifiers for joining them into the final export mesh.
And it always took me a decent amount of time to do that. After that frustrating period, I decided to learn python and write an addon which simplifies that process by automatically creating copies of the model parts and combining them into the final meshes.

Texturing high- and lowpoly models often involves baking a highpoly mesh onto a lowpoly mesh. 
But in most cases, the models are too complex to bake all meshes in one pass.
Sometimes you need a cage, sometimes you need to separate objects before baking, etc.
The highpoly meshes must be grouped by feature, and to baked them one-by-one to their corresponding lowpoly part.

This is, where the Hilo Addon comes in.
It allows you to create the final export meshes, by copying and joining mesh objects feature-by-feature using a naming convention.
In the end you will have only two meshes for each model feature. One lowpoly mesh and one highpoly mesh, which are exported as _low or _high




#### Supported Versions
Blender v2.76 or higher

