# Self-driving-Car-Neural-Network

A self-driving car using neural networks in Python 3.6 and [pygame](https://www.pygame.org).

The car casts 5 rays in a cone in front of itself.
Each frame per ray, the distance to a wall is calculated.
This distance is fed into the network (2 layers each 10 nodes by default) which classifies if the car needs to (steer left, steer right, don't steer) and if the car needs to (brake,accelerate,neither).

The network is trained based on me playing the game for 5 minutes on a simple level (see image 2.png).
After training the car is able to easily complete a much more difficult level (see image 1.png).


# You can draw a level youself!

Just make a 1024x720 image and draw away! The car will see any black pixel (RGB = 0,0,0) as a wall and try to avoid it.

It works best to create a circuit type of level, the car may have trouble in wide open areas if it cannot detect any walls.

If you do make a level, please share it with me. I'd love to see what you can create!

![Image of the selfdriving car in a level](https://github.com/Niels-van-den-Hork/Self-driving-Car-Neural-Network/blob/master/example.png "Image of the selfdriving car in a level")

# File contents
  Code:
    car.py: High-level gameloop & I/O
    classes.py: Low-level implementation
    utils.py: General helper functions & File I/O
  Data:
    tdata.in: ~5 minutes of the ray distances
    tdata.out: ~5 minutes of users reaction to those states
    
    
  

