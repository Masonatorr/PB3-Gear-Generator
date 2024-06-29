# PB3-Gear-Generator
A program to easily create gears of different shapes and sizes.

This program is relatively self explanatory, but I will give some extra info here:


## Gear Type:
This is the type of gear that will be created. These are the six types currently available:
1. Triangle Tooth Spur Gear
2. Trapezoidal Tooth Spur Gear
3. Triangle Tooth Ring Gear
4. Trapezoidal Tooth Ring Gear
5. Triangle Tooth Rack Gear
6. Trapezoidal Tooth Rack Gear  

![Triangle Tooth Spur Gear](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/8cd10270-53a7-4e22-9675-e7a11eeaa40b "Triangle Tooth Spur Gear")
![Trapezoidal Tooth Spur Gear](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/dd277978-750b-44b4-89c8-ded285cb7f6e "Trapezoidal Tooth Spur Gear")
![Triangle Tooth Ring Gear](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/80686a40-066b-4e1a-890d-06a6cda1163d "Triangle Tooth Ring Gear")
![Trapezoidal Tooth Ring Gear](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/459710e2-e25e-4f8a-ae1a-66ce0713c2f8 "Trapezoidal Tooth Ring Gear")
![Triangle Tooth Rack Gear](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/63bb4894-1088-49ab-a527-c5214c2dc82e "Triangle Tooth Rack Gear")
![Trapezoidal Tooth Rack Gear](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/62268870-cc55-433c-89e2-049ac8882e56 "Trapezoidal Tooth Rack Gear")  


To select which gear you want to generate, type the gear's number into the input field.

## Number of Teeth:
Self explanatory. Whatever number you enter is the number of teeth that the resulting gear will have. Increasing this number will make the teeth thinner unless you increase the gear radius.

## Gear Radius:
This one isn't as intuitive. The gear's radius is measured via this red ring here:  
![Gear radius](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/21415c14-2acd-47d9-960b-0265ed2338dc "Gear radius")  
When the teeth are generated, the highest and lowest points of the teeth will be an equal distance away from this line.  
Why have the line here instead of at the base of the teeth? Well, here's an example:  
![Gears meshing](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/2055e226-d7be-4cef-9a5b-628b8c96b379 "Two gears' radii intersecting")  
See how the red circles are touching when the gears are meshing together? Having the teeth heights be relative to these circles makes it easier to generate meshing gears. If the radius was based on the tips or the bases of the teeth, you wouldn't be able to measure from a common point (the intersection), and so it wouldn't be as intuitive.

## Tooth Height:
The tooth height controls the total height of the tooth from tip to base, as shown here:  
![Tooth height](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/77d97b42-797d-4a83-8131-f7185e7f692b "Tooth height")  
As mentioned previously, the tip and base of each tooth are both an equal distance away from the gear's radius.  
I would recommend a tooth height of around 0.5m, as higher values can make the teeth too long to properly mesh with each other.

## Outer Radius of Ring (Ring Gears):
Ring gears have almost exactly the same shape as their respective spur gears, except they are inverted, with an empty space on the inside and an outside ring. The outer radius is measured as the distance from the center of the gear to any point on the outside ring, as shown here:  
![Outer ring](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/fa252f2f-3a2d-4c56-bd61-c30b06785401 "Outer ring")

## Make Gear Editable (Ring Gears):
Because you cannot have a shape with two disconnected edge loops, ring gears need to have a seam. However, one issue with this is that if two vertices are too close to each other, the game gets upset and will not allow you to drag the shape's vertices. And unfortunately, widening the seam enough to edit the shape results in the seam being visible.  
Therefore, you have two options: a) keep the seam invisible but leave the gear uneditable, or b) widen the seam enough that you can edit the gear, but be left with a visible seam.  
(Seam vs no seam)  
![Seam](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/ac73b086-c986-4ef1-9ab9-47fc78b94260 "Seam")
![No seam](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/eb2888db-5a7e-4bfe-9e20-34e96abfca78 "No seam")  
To keep your seam invisible, type "N" into the input field. To widen the seam, type "Y".

## Rack Gears:
Rack gears are unique in that they are not round like the rest. Instead, they are flattened into strips of teeth. Because of their unique shape, it is much harder to generate them in such a way that they mesh perfectly with other gears. Therefore, these gears are formed using a "reference gear", basically being the gear that this rack is designed to mesh with.  
![Reference gear and resulting rack](https://github.com/Masonatorr/PB3-Gear-Generator/assets/42453670/d4bc9180-6aa5-47ef-a3f8-79611a33d7e5 "Reference gear and resulting rack")  
The first three properties (num teeth, gear radius, and tooth height) shape this "reference" gear, and the final two (num teeth and clearance) directly shape the resulting rack gear.

## Clearance:
This one is relatively simple, adding a small amount of clearance between meshing gears. For the spur and rack gears, the tips of the teeth are shortened slightly by whatever amount you set. For the ring gears, the bases of the inverse "teeth" are pulled slighty away from the center so that they do not rub against the bases of the spur gears' teeth.
