"""A recreation of Flappy Bird for the NCEA 3.7 internal."""
from tkinter import *  # importing tkinter
import random  # importing random


class Player:
    """Create a player object.

    Creates an object which will be controlled by player inputs to flap
    upwards.

    Instance Variables
    ----------
    _canvas : tk
        canvas on which to draw objects on
    _player_rectangle : tk
        player tk rectangle object
    _control_key : str
        key that controls the player
    _control_button : int
        number to represent which button click controls player
    _y_velocity : int
        players y axis speed
    _movement_stack : list
        stack to control player movement

    Methods
    ----------
    __init__(self, canvas, x, y, control_key, control_button):
        Establishes the attributes that are used by the class.

        :param canvas: specifies where the object is made.
        :param x: specifies the Birds starting x position in the game.
        :param y: specifies the Birds starting y position in the game.
        :param control_key: specifies which button/s are used to control
        the birds movement.

    move(self):
        Manage the movement of the bird.

    _fall(self):
        Move the bird downwards in an increasing amount.

    _flap(self):
        Move the bird upwards with a natural increase.

    event_checked(self, event):
        Check event and triggers flap.

        :param event: contains information on what key was pressed

    get_coordinates(self):
        Return player position.

        :return: player_position.
    """

    _BIRD_WIDTH = 40  # integer constant for the birds x size in pixels
    _BIRD_HEIGHT = 40  # integer constant for the birds y size in pixels

    TOP_Y = 1  # index for bird_position top y
    RIGHT_X = 2  # index for bird_position right x
    BOTTOM_Y = 3  # index for bird_position bottom y

    _ACCELERATION = 5  # integer constant for acceleration
    _JUMP_TIME = 1.6  # integer constant for jump exponent
    _FALL_TIME = 0.1  # integer constant for fall exponent

    def __init__(self, canvas, x, y, control_key, control_button):
        """Establish the attributes that are used by the class.

        :param canvas: specifies where the object is made.
        :param x: specifies the Birds starting x position in the game.
        :param y: specifies the Birds starting y position in the game.
        :param control_key: specifies which button/s are used to control
        the birds movement.
        """
        self._canvas = canvas
        self.player_rectangle = canvas.create_rectangle(x, y,
                                                        x + self._BIRD_HEIGHT,
                                                        y + self._BIRD_WIDTH,
                                                        fill="yellow")
        self._control_key = control_key  # controls are defined when
        # making an object
        self._control_button = control_button
        self._y_velocity = 0  # sets initial speed of 0 to build from
        self._movement_stack = []  # empty movement stack makes bird fall

    def move(self):
        """Manage the movement of the bird.

        Uses the state of the movement stack to run either the _fall or the
        _flap methods. Runs the _fall method if the stack is empty and _flap
        if the movement stack has "True" in it .
        """
        if len(self._movement_stack) == 0:  # checks if user input jump
            self._fall()  # if no input is in list the object falls.
        if len(self._movement_stack) == 1:  # checks if user input jump
            self._flap()  # if input is in the list the object jumps
        if len(self._movement_stack) > 1:  # checks if stack is too large
            self._movement_stack.pop()  # pops one of the stack items

    def _fall(self):
        """Move the bird downwards in an increasing amount.

        A method which is ran as long as the stack is empty. Calculates the
        birds increasing velocity by adding the acceleration constant
        multiplied by the constant fall time and moves it by that amount.
        """
        self._y_velocity += self._ACCELERATION * self._FALL_TIME  # sets
        # velocity
        self._canvas.move(self.player_rectangle, 0,
                          self._y_velocity)  # moves bird

    def _flap(self):
        """Move the bird upwards with a natural increase.

        Calculates new velocity by using the negative of the acceleration
        constant and moves bird upwards by that amount.
        Removes the variable from the movement_stack in order to make the bird
        fall again.
        """
        self._y_velocity = -self._ACCELERATION * self._JUMP_TIME  # sets
        # velocity
        self._canvas.move(self.player_rectangle, 0,
                          self._y_velocity)  # moves object
        self._movement_stack.remove("True")  # removes true so bird falls

    def event_entered(self, event):
        """Check event and makes bird flap.

        Appends true to the movement stack if the entered event is equal to
        the player control key or button. This makes the bird flap.

        :param event: contains information on what key was pressed
        """
        if event.keysym == self._control_key or event.num == \
                self._control_button:  # checks if the event key code or
            # button number are in the player controls
            self._movement_stack.append("True")  # appends true to trigger jump

    def get_coordinates(self):
        """Return player position.

        Gets the player coordinates and stores them in a variable. Returns
        variable.

        :return: player_position.
        """
        player_position = self._canvas.coords(
            self.player_rectangle)  # sets new bird coordinates
        return player_position


class Obstacle:
    """Create an obstacle object.

    Creates two objects, one for each pipe that move towards the left side
    of the screen. Manages the variables halfway() and off_screen() which
    influence how the pipes are managed in the game.

    Attributes
    ----------
    _canvas : tk
        canvas on which to draw objects on
    _top_rectangle : tk
        top obstacle tk rectangle object
    _bottom_rectangle : tk
        bottom obstacle tk rectangle object
    top_obstacle_position : tuple
        tuple which contains the coordinates for all object sides
    bottom_obstacle_position : tuple
        tuple which contains the coordinates for all object sides
    halfway : boolean
        boolean represents whether or not object is halfway on the canvas
    off_screen : boolean
        boolean which represents whether or not object is off the canvas


    Methods
    ----------
    __init__(self, canvas, x, y):
        Establishes the attributes that are used by the class.

        :param canvas: specifies where the object is made.
        :param x: specifies the obstacles starting x position in the game.
        :param y: specifies the obstacles starting y position in the game.

    move_obstacles(self):
        Move obstacles to the left, update positions and check position of
        the objects.

    _check_obstacle_positions(self):
        Check positions of the objects and change halfway and off_screen
        variables.

        :return: If the location is off screen or halfway return True,
        otherwise return False.
    """

    _OBSTACLE_WIDTH = 70  # integer constant for width of pipes
    _OBSTACLE_GAP = 150  # integer constant for gap between top and bottom pipe
    _MOVEMENT_SPEED = -2  # integer constant movement speed for the x axis

    _LEFT_X = 0  # index for obstacle position on the left x axis
    RIGHT_X = 2  # index for obstacles position on the right x axis

    _SCREEN_WIDTH = 360  # integer constant for screen width
    _SCREEN_HEIGHT = 640  # integer constant for screen height

    def __init__(self, canvas, x, y):
        """Establish the attributes that are used by the class.

        :param canvas: specifies where the object is made.
        :param x: specifies the obstacles starting x position in the game.
        :param y: specifies the obstacles starting y position in the game.
        """
        self._canvas = canvas
        self._top_rectangle = canvas.create_rectangle(x,
                                                      y - self._OBSTACLE_GAP,
                                                      x +
                                                      self._OBSTACLE_WIDTH,
                                                      y - self._SCREEN_HEIGHT,
                                                      fill="green3")
        self._bottom_rectangle = canvas.create_rectangle(x, y,
                                                         x +
                                                         self._OBSTACLE_WIDTH,
                                                         y +
                                                         self._SCREEN_HEIGHT,
                                                         fill="green3")
        self.top_obstacle_position = canvas.coords(self._top_rectangle)
        # coordinates for the top pipe
        self.bottom_obstacle_position = canvas.coords(
            self._bottom_rectangle)  # coordinates for the bottom pipe
        self.halfway = False  # boolean for if the object is halfway
        self.off_screen = False  # boolean for if the object is off screen

    def move_obstacle(self):
        """Move obstacles to the left, update positions and check locations.

        Moves each of the two objects/rectangles at a constant rate towards
        the left. Updates positions of each object and then checks the
        locations.
        """
        self._canvas.move(self._top_rectangle, self._MOVEMENT_SPEED,
                          0)  # moves the top object by the movement speed
        self._canvas.move(self._bottom_rectangle, self._MOVEMENT_SPEED,
                          0)  # moves the bottom object by the movement speed
        self.top_obstacle_position = self._canvas.coords(
            self._top_rectangle)  # updates position of the top obstacle
        self.bottom_obstacle_position = self._canvas.coords(
            self._bottom_rectangle)  # updates position of the bottom obstacle
        self._check_obstacle_positions()

    def _check_obstacle_positions(self):
        """Check positions of the objects.

        Checks locations of the bottom object (which doesnt matter as both
        move at the same speed and will always be in the same x position.
        Changes appropriate variables if the object is in a determined
        location. This includes whether the object is halfway or off screen.

        :return: If the location is off screen or halfway return True,
        otherwise return False.
        """
        if self.bottom_obstacle_position[Obstacle.RIGHT_X] <= 0:  # checks
            # if the coordinates of the right side of one of the objects is
            # less than zero/off screen
            self.off_screen = True
        if self.bottom_obstacle_position[Obstacle._LEFT_X] == \
                self._SCREEN_WIDTH / 2:  # checks if the coordinates of the
            # left side of one of the objects is equal to half the screen
            # width/halfway
            self.halfway = True
        else:  # the object is neither off screen or halfway
            self.halfway = False


class Scoreboard:
    """Create a visual score board.

    Makes a text widget which is configured to reflect the score.

    Attributes
    ----------
    _canvas : tk
        canvas on which to draw objects on
    _x : int
        specifies the objects x position in the game
    _y : int
        specifies the objects y position in the game
    score : int
        a variable to store the score
    _text : tk
        text widget to display the score

    Methods
    ----------
    __init__(self, canvas, x, y):
        Establishes the attributes that are used by the class.

        :param canvas: specifies where the object is made.
        :param x: specifies the objects x position in the game.
        :param y: specifies the objects y position in the game.

    increase_score(self):
        Increase the score.
    """

    _FONT_SIZE = 25  # integer constant for font size

    _POINT_WORTH = 1  # integer to increase the score by

    def __init__(self, canvas, x, y):
        """Establish the attributes that are used by the class.

        :param canvas: specifies where the object is made.
        :param x: specifies the objects x position in the game.
        :param y: specifies the objects y position in the game.
        """
        self._canvas = canvas
        self._x = x
        self._y = y
        self.score = 0  # score is initially set to zero
        self._text = Label(self._canvas, fg="black", text=self.score,
                           font=("Arial", self._FONT_SIZE))  # makes text
        # widget
        self._text.place(x=self._x, y=self._y)  # places text widget

    def increase_score(self):
        """Increase the score.

        Increases score by the point worth and configures score label show the
        change.
        """
        self.score += self._POINT_WORTH  # score is increased by the point
        # worth
        self._text.config(text=self.score)  # configures the text widget to
        # show the score


class Game:
    """Creates a game object.

    Creates instances of the player, obstacle and scoreboard class and runs
    them and manages interactions between them and runs methods pertaining
    to them.

    Attributes
    ----------
    _application : class object
        instance of the Application class
    _canvas : tk
        canvas on which to draw objects on
    _player : class object
        instance of the Player class
    _obstacles : list
        a list to contain all the generated pipes on the canvas
    _scoreboard : class object
        instance of the Scoreboard class
    score : int
        a variable to store the score
    _window : tk
        the tkinter window

    Methods
    ----------
    __init__(self, canvas, x, y):
        Establishes the attributes that are used by the class.

        :param application: instance of the application class.

    _event_entered(self, event)
        Route control event to player class.

        :param event: contains the code for the key entered

    run_game(self):
        Run the game and related processes/methods.

    _manage_pipes(self):
        Move and manage pipes.

    manage_collisions(self):
        Manage collisions.

    _manage_score(self):
        Manage and increase score.
    """

    _DISTANCE_BETWEEN_OBSTACLES = 80  # integer constant for distance between
    # obstacles
    _MIN_RANGE_OF_PIPES = 200  # integer constant for minimum pipe y generation
    _MAX_RANGE_OF_PIPES = 600  # integer constant for maximum pipe y generation

    _REFRESH_SPEED = 15  # integer constant for amount of milliseconds to
    # refresh window

    _SCREEN_WIDTH = 360  # integer constant for screen height
    _SCREEN_HEIGHT = 640  # integer constant for screen width

    def __init__(self, application):
        """Establish the attributes that are used by the class.

        :param application: instance of the application class.
        """
        self._application = application  # instance of application class
        self._canvas = application.game_canvas
        self._player = Player(self._canvas, 40, 300, 'space', 1)
        self._obstacles = []  # list to contain active obstacles
        self._scoreboard = Scoreboard(self._canvas, 0, 0)
        self.score = 0  # variable to store the score
        self._window = application.window  # gives class access to window
        # functions
        self._window.bind('<Key>', self._event_entered)  # binds all keys
        # to the _event_entered function
        self._window.bind('<Button>', self._event_entered)  # binds all
        # mouse buttons to the _event_entered function

    def _event_entered(self, event):
        """Route control event to player class.

        Runs the event_entered method of the bird class and passes in the
        event code.

        :param event: contains the code for the key entered
        """
        self._player.event_entered(event)  # runs the players event_entered
        # function and passes in the event

    def run_game(self):
        """Run the game and related processes/methods.

        Manages and moves objects in the game. This includes managing the
        birds movement, the pipes movement and generation, collisions,
        score and checks if the game has been lost. Refreshes/runs every
        REFRESH_SPEED milliseconds.
        """
        self._player.move()  # runs the players move() method
        self._manage_pipes()  # runs the _manage_pipes() method
        self.manage_collisions()  # runs the manage_collisions() method
        self._manage_score()  # runs the _manage_score() method
        self._application.check_restart()  # runs the applications
        # check_restart() method
        self._window.after(self._REFRESH_SPEED, self.run_game)  # runs the
        # run_game() method every REFRESH_SPEED milliseconds

    def _manage_pipes(self):
        """Move and manage pipes.

        Runs the move_obstacle method for all obstacles in the obstacles
        list. Creates a new pipe object when the one in front reaches
        halfway. Removes pipes when the pipe leave the game boundaries.
        """
        for obstacle in self._obstacles:  # runs the move_obstacle command
            # for all obstacles in the _obstacles list
            obstacle.move_obstacle()
        if len(self._obstacles) == 0:  # if the length of the obstacles list
            # is 0, a obstacle is generated
            obstacle = Obstacle(self._canvas, self._SCREEN_WIDTH,
                                random.randrange(self._MIN_RANGE_OF_PIPES,
                                                 self._MAX_RANGE_OF_PIPES))
            self._obstacles.append(obstacle)
        for obstacle in self._obstacles:  # checks the halfway and
            # off_screen boolean variables for every obstacle in the
            # _obstacles list and either generates a new one of deletes the
            # obstacle depending on what returns true
            if obstacle.halfway:  # checks if halfway
                new_obstacle = Obstacle(self._canvas, self._SCREEN_WIDTH +
                                        self._DISTANCE_BETWEEN_OBSTACLES,
                                        random.randrange(
                                            self._MIN_RANGE_OF_PIPES,
                                            self._MAX_RANGE_OF_PIPES))  #
                # generates new obstacle object
                self._obstacles.append(new_obstacle)  # adds obstacle to
                # list of obstacles
            if obstacle.off_screen:  # checks if obstacle is off_screen
                self._canvas.delete(obstacle)  # deletes object from the
                # canvas to stop memory leaks
                self._obstacles.remove(obstacle)  # removes obstacle from
                # list of obstacles

    def manage_collisions(self):
        """Manage collisions.

        Manages collisions of the player and obstacles by accessing the most
        recent obstacle and looking to see if the player rectangle is
        overlapping with the bottom and top obstacles. Also manages boundary
        collisions with the player object by comparing its values to the screen
        boarders.

        :return: True if collision has occurred, False if no collision has
        occurred.
        """
        try:  # tries to run the following code and excepts IndexError
            obstacle = self._obstacles[0]  # stores closest obstacle
            if self._player.player_rectangle in self._canvas.find_overlapping(
                    *obstacle.bottom_obstacle_position) or \
                    self._player.player_rectangle in \
                    self._canvas.find_overlapping(
                        *obstacle.top_obstacle_position):  # checks if the
                # players rectangle's coordinates overlap with that of both
                # the top and the bottom pipe
                return True
            elif self._player.get_coordinates()[Player.BOTTOM_Y] >= \
                    self._SCREEN_HEIGHT or \
                    self._player.get_coordinates()[Player.TOP_Y] <= 0:
                # checks if the players coordinates are greater than the
                # screen height or less than zero to check for boundary
                # collisions
                return True
        except IndexError:  # index error may be raised as this is run
            # before the first pipe is generated
            return False

    def _manage_score(self):
        """Manage and increase score.

        Manages the game score by accessing the most recent obstacle and
        looking to see if the player rectangle's right side is equal to the
        obstacles right position to award a point.
        """
        obstacle = self._obstacles[0]  # stores closest obstacle
        if self._player.get_coordinates()[Player.RIGHT_X] == \
                obstacle.bottom_obstacle_position[Obstacle.RIGHT_X]:  #
            # checks if the right side of the bird is at the same location
            # as the obstacles right side
            self._scoreboard.increase_score()  # runs the increase score
            # method of the scoreboard class
            self.score = self._scoreboard.score  # sets the Game objects
            # score to the scoreboards count


class Application:
    """Create an application object.

    Creates an application object which houses all menu widgets/objects.
    Creates a game canvas and a game object which house all game
    information. Has methods to load the game and is responsible for
    returning to the menu if the game is lost.

    Attributes
    ----------
    window : tk
        tkinter window instance
    _menu_frame : tk
        tkinter frame object to house menu widgets and code
    _title : tk
        tkinter label object to house text
    _instructions : tk
        tkinter label object to house text
    _play_button : tk
        tkinter button object to run the play code when clicked
    _exit_button : tk
        tkinter button object to exit the window when clicked
    _score : tk
        tkinter label object to house text
    game_canvas : tk
        tkinter canvas object
    game_object : class object
        instance of the game class

    Methods
    ----------
    __init__(self):
        Establishes the attributes that are used by the class.

    _play_game(self):
        Change frame to game canvas and run game.

    check_restart(self):
        Unpack and replaces game frame and class and pack menu.
    """

    _BUTTON_HEIGHT = 2
    _BUTTON_WIDTH = 12

    _SCREEN_HEIGHT = 640
    _SCREEN_WIDTH = 360

    _TITLE_FONT_SIZE = 30
    _GENERAL_FONT_SIZE = 15

    _INSTRUCTIONS_TEXT = """Navigate between the pipes.
    Try to beat your score.
    Use the space-bar or mouse-1 button.
    (left mouse click)
    to flap upwards.
    Use F10 to pause. \n """

    def __init__(self):
        """Establish attributes that are used by the class."""
        self.window = Tk()  # creating the window
        self.window.resizable(False, False)  # makes the window not resizeable
        self.window.title("Flappy Bird")  # titles the window
        self.window.unbind_all('<<NextWindow>>')
        # menu frame
        self._menu_frame = Frame(self.window, width=self._SCREEN_WIDTH,
                                 height=self._SCREEN_HEIGHT)
        self._menu_frame.pack_propagate(0)  # keeps window at a fixed size
        self._menu_frame.pack()
        # title label widget
        self._title = Label(self._menu_frame, text="Flappy Bird",
                            font=("arial", self._TITLE_FONT_SIZE, "bold"),
                            justify="center")
        self._title.pack()
        # instructions label widget
        self._instructions = Label(self._menu_frame,
                                   text=self._INSTRUCTIONS_TEXT,
                                   font=("Arial", self._GENERAL_FONT_SIZE))
        self._instructions.pack()
        # play button widget
        self._play_button = Button(self._menu_frame, text="Play",
                                   font=(
                                       "Arial", self._GENERAL_FONT_SIZE),
                                   command=lambda: self._play_game(),
                                   width=self._BUTTON_WIDTH,
                                   height=self._BUTTON_HEIGHT)
        self._play_button.pack()
        # exit button widget
        self._exit_button = Button(self._menu_frame, text="Exit!",
                                   font=(
                                       "Arial", self._GENERAL_FONT_SIZE),
                                   command=lambda: exit(),
                                   width=self._BUTTON_WIDTH,
                                   height=self._BUTTON_HEIGHT)
        self._exit_button.pack()
        # score label widget
        self._score = Label(self._menu_frame, text="",
                            font=("arial", self._GENERAL_FONT_SIZE),
                            justify="center")
        self._score.pack()
        # game canvas and object
        self.game_canvas = Canvas(self.window, width=self._SCREEN_WIDTH,
                                  height=self._SCREEN_HEIGHT,
                                  background="skyblue")
        self.game_object = Game(self)

    def _play_game(self):
        """Change frame to game canvas and run game.

        Is triggered by the play button and will unpack the menu and pack
        the game canvas instead, sets focus on the game canvas to ensure
        that buttons cannot be tabbed to and then runs the game.
        """
        self._menu_frame.pack_forget()  # unpacks the menu frame
        self.game_canvas.pack()  # packs the game canvas
        self.game_object.run_game()  # runs the main game function
        self.game_canvas.focus_set()  # sets focus to the game_canvas

    def check_restart(self):
        """Unpack and replaces game frame and class and pack menu.

        Runs the manage_collisions method and if that returns True the game
        will be unpacked and the menu frame packed. The score widget will be
        configured to reflect the score and new game canvas and object are
        made using the same variables ensuring the old game is completely
        unloaded.
        """
        if self.game_object.manage_collisions():  # if the manage_collisions
            # method returns True indicating a collision the code is run
            self.game_canvas.pack_forget()  # unpacks the game
            self.game_canvas.delete()  # deleted instance of the canvas to
            # stop memory leaks
            self._menu_frame.pack()  # packs the menu frame
            self._score.config(text="Score: " + str(self.game_object.score))
            # configures the score label widget to the game_object score
            self.game_canvas = Canvas(self.window, width=self._SCREEN_WIDTH,
                                      height=self._SCREEN_HEIGHT,
                                      background="skyblue")  # creates a new
            # canvas
            self.game_object = Game(self)  # creates a new game


if __name__ == "__main__":
    FlappyBird = Application()  # creates instance of the application class
    FlappyBird.window.mainloop()  # runs the tkinter mainloop to start GUI
