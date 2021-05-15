"""A recreation of Flappy Bird for the NCEA 3.7 internal."""
from tkinter import *  # importing tkinter
import random

window = Tk()  # creating the window
canvas = Canvas(window, width=360, height=640,
                background="sandy brown")
canvas.pack()
SCREEN_HEIGHT = 640
SCREEN_WIDTH = 360


class Bird:
    """Creates a bird which will be controlled by player inputs and flaps
        upwards. If it collides with a obstacle the game is lost."""
    BIRD_WIDTH = 40  # Constant for the birds x size in pixels
    BIRD_HEIGHT = 40  # Constant for the birds y size in pixels

    TOP_Y = 1  # index for bird_position top y
    RIGHT_X = 2  # index for bird_position right x
    BOTTOM_Y = 3  # index for bird_position bottom y

    ACCELERATION = 5  # Constant for acceleration
    JUMP_TIME = 1.6  # Constant for jump exponent
    FALL_TIME = 0.1  # Constant for fall exponent

    def __init__(self, canvas, x, y, control_key, control_button):
        """
        :param canvas: specifies where the object is made.
        :param x: specifies the Birds starting x position in the game.
        :param y: specifies the Birds starting y position in the game.
        :param control_key: specifies which button/s are used to control
        the birds movement.
        """
        self._canvas = canvas
        self._rectangle = canvas.create_rectangle(x, y,
                                                  x + self.BIRD_HEIGHT,
                                                  y + self.BIRD_WIDTH,
                                                  fill="azure")
        self.control_key = control_key  # Controls are defined when
        # making an object
        self.control_button = control_button
        self._y_velocity = 0  # Sets initial speed of 0 to build from
        self._movement_stack = []  # Empty movement stack makes bird fall

    def move(self):
        """ A method which manages the movement of the bird character using
        stack management"""
        if len(self._movement_stack) == 0:  # Checks if user input jump
            self._fall()  # If no input is in list the object falls.
        if "True" in self._movement_stack:  # Checks if user input jump
            self._flap()  # If input is in the list the object jumps
        bird_position = self.get_coords()  # Sets new bird coords
        self._collisions(bird_position)  # Checks for bottom collisions

    def _fall(self):
        """ A method which is ran as long as the stack is empty. Calculates
        the birds increasing velocity and moves it by that amount."""
        self._y_velocity += self.ACCELERATION * self.FALL_TIME  # Sets velocity
        self._canvas.move(self._rectangle, 0, self._y_velocity)  # Moves bird

    def _flap(self):
        """ A method which is ran when the user inputs a flap command.
        Calculates new velocity and moves bird upwards by that amount.
        Removes the variable from the stack in order to make the bird fall
        again."""
        self._y_velocity = -self.ACCELERATION * self.JUMP_TIME  # Sets velocity
        self._canvas.move(self._rectangle, 0, self._y_velocity)  # Moves object
        self._movement_stack.remove("True")  # Removes true so bird falls

    def control_entered(self):
        """ A method which checks whether the user has inputted something
        that is in the list of controls for the character. Appends true if
        this is the case in order to make the bird flap"""
        self._movement_stack.append("True")  # Appends true to trigger jump

    def _collisions(self, bird_position):
        """ A method which manages the collisions of the bird with the
        environment and obstacles. Uses coordinates of these objects to
        discern whether or not the character has collided with anything. If
        a collision occurs the game is stopped"""
        if bird_position[Bird.BOTTOM_Y] >= SCREEN_HEIGHT:  # Checks if bird
            # touches the floor of the window
            self._movement_stack.append("L")

    def _increase_score(self):
        pass

    def get_coords(self):
        bird_position = canvas.coords(self._rectangle)  # Sets new bird coords
        return bird_position


class Obstacle:
    """Creates obstacles where if the player/Bird object collides with it,
    the game is stopped."""
    OBSTACLE_WIDTH = 70
    OBSTACLE_GAP = 150
    MOVEMENT_SPEED = -2

    LEFT_X = 0  # index for obstacle position on the left x axis
    TOP_Y = 1  # index for obstacle position on the top y axis
    RIGHT_X = 2  # index for obstacles position on the right x axis
    BOTTOM_Y = 3  # index for obstacle position on the bottom y axis

    def __init__(self, canvas, x, y):
        """
        :param canvas: specifies where the object is made.
        :param x: specifies the obstacles starting x position in the game.
        :param y: specifies the obstacles starting y position in the game.
        """
        self._canvas = canvas
        self._top_rectangle = canvas.create_rectangle(x, y - self.OBSTACLE_GAP,
                                                      x +
                                                      self.OBSTACLE_WIDTH,
                                                      y - SCREEN_HEIGHT,
                                                      fill="coral")
        self._bottom_rectangle = canvas.create_rectangle(x, y,
                                                         x +
                                                         self.OBSTACLE_WIDTH,
                                                         y + SCREEN_HEIGHT,
                                                         fill="coral")
        self.top_obstacle_position = canvas.coords(self._top_rectangle)
        self.bottom_obstacle_position = canvas.coords(self._bottom_rectangle)
        self.halfway = False
        self.off_screen = False

    def move_obstacle(self):
        """ A method which moves the two objects at a constant speed towards
        the player. The coordinate positions of the obstacles are updated."""
        self._canvas.move(self._top_rectangle, self.MOVEMENT_SPEED, 0)
        self._canvas.move(self._bottom_rectangle, self.MOVEMENT_SPEED, 0)
        self.top_obstacle_position = canvas.coords(self._top_rectangle)
        self.bottom_obstacle_position = canvas.coords(self._bottom_rectangle)
        self.check_checkpoints()

    def check_checkpoints(self):
        if self.bottom_obstacle_position[Obstacle.RIGHT_X] <= 0:
            self.off_screen = True
        if self.bottom_obstacle_position[Obstacle.LEFT_X] == SCREEN_WIDTH / 2:
            self.halfway = True
        else:
            self.halfway = False


class Game:
    """ Creates a game object which houses all game related controls and
    objects."""
    DISTANCE_BETWEEN_OBSTACLES = 80

    def __init__(self, canvas):
        self.canvas = canvas
        self.player = Bird(canvas, 40, 40, 'space', "Button-1")
        self.obstacles = []
        self.score = 0
        window.bind('<Key>', self.check_control_press)
        window.bind('<Button>', self.check_control_press)

    def check_control_press(self, event):
        """ A method to check whether the inputted event is in the
        player controls."""
        if event.keysym == self.player.control_key:
            self.player.control_entered()

    def run_game(self):
        """ A method which manages and moves objects in the game. This
        includes managing the birds movement and the pipes movement."""
        self.player.move()
        self.manage_pipes()
        self.player_obstacle_collisions()
        window.after(14, self.run_game)

    def manage_pipes(self):
        """ Manages the creation and deletion of pipes. Creates a new pipe
        object when the one in front reaches halfway. Removes pipes when the
        pipe leave the game boundaries."""
        for obstacle in self.obstacles:
            obstacle.move_obstacle()
        if len(self.obstacles) == 0:
            obstacle = Obstacle(canvas, SCREEN_WIDTH,
                                random.randrange(150, 600))
            self.obstacles.append(obstacle)
        for obstacle in self.obstacles:
            if obstacle.halfway:
                new_obstacle = Obstacle(canvas, SCREEN_WIDTH +
                                        self.DISTANCE_BETWEEN_OBSTACLES,
                                        random.randrange(150, 600))
                self.obstacles.append(new_obstacle)
            if obstacle.off_screen:
                self.obstacles.remove(obstacle)

    def player_obstacle_collisions(self):
        player_position = self.player.get_coords()
        obstacle = self.obstacles[0]
        if player_position[Bird.RIGHT_X] == \
                obstacle.bottom_obstacle_position[Obstacle.LEFT_X] and \
                player_position[Bird.BOTTOM_Y] >  \
                obstacle.bottom_obstacle_position[Obstacle.TOP_Y]:
            print("Something")
        if player_position[Bird.RIGHT_X] == \
                obstacle.top_obstacle_position[Obstacle.LEFT_X] and \
                player_position[Bird.TOP_Y] <  \
                obstacle.top_obstacle_position[Obstacle.BOTTOM_Y]:
            print("Something else")
        if player_position[Bird.TOP_Y] == \
                obstacle.top_obstacle_position[Obstacle.BOTTOM_Y]:
            print("Something completely different")
            #if player_position[Bird.BOTTOM_Y] == \
                    #obstacle.bottom_obstacle_position[Obstacle.TOP_Y]:
                #print("Gooba")

    def increase_score(self):
        player_position = self.player.get_coords()
        obstacle = self.obstacles[0]
        if player_position[Bird.RIGHT_X] == \
                obstacle.bottom_obstacle_position[Obstacle.RIGHT_X]:
            self.score += 1
            print(self.score)




if __name__ == "__main__":
    Game_object = Game(canvas)
    Game_object.run_game()
    window.mainloop()
