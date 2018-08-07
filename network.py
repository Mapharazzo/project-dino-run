import os
import time
import pandas as pd
from pynput.keyboard import Key, Controller
keyboard = Controller()


def press_key(key):
    keyboard.press(key)
    keyboard.release(key)


def hold_key(key, duration=0.1):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)


class Game:
    def __init__(self, custom_config=True):
        self.keyboard = keyboard
        self.elapsed = 0

    def get_crashed(self):
        return False  # TBD

    def restart(self):
        time.sleep(4)

    def press_up(self):
        press_key(Key.up)

    def hold_down(self):
        hold_key(Key.down)

    def get_score(self):
        return self.elapsed


class DinoAgent:
    def __init__(self,game):  # takes game as input for taking actions
        self._game = game
        self.jump()  # to start the game, we need to jump once

    def is_crashed(self):
        return self._game.get_crashed()

    def jump(self):
        self._game.press_up()

    def duck(self):
        self._game.hold_down()


class GameState:
    def __init__(self, agent, game):
        self._agent = agent
        self._game = game

    def get_state(self, actions):
        actions_df.loc[len(actions_df)] = actions[1]  # storing actions in a dataframe
        score = self._game.get_score()
        reward = 0.1
        is_over = False  # game over
        if actions[1] == 1:
            self._agent.jump()
        if self._agent.is_crashed():
            scores_df.loc[len(loss_df)] = score  # log the score when game is over
            self._game.restart()
            reward = -1
            is_over = True
        return reward, is_over  # return the Experience tuple

# Intialize log structures from file if exists else create new
loss_file_path = "logs\\loss_df.csv"
scores_file_path = "logs\\scores_df.csv"
q_value_file_path = "logs\\q_values_df.csv"
actions_file_path = "logs\\actions_df.csv"

loss_df = pd.read_csv(loss_file_path) if os.path.isfile(loss_file_path) else pd.DataFrame(columns =['loss'])
scores_df = pd.read_csv(scores_file_path) if os.path.isfile(loss_file_path) else pd.DataFrame(columns = ['scores'])
actions_df = pd.read_csv(actions_file_path) if os.path.isfile(actions_file_path) else pd.DataFrame(columns = ['actions'])
q_values_df = pd.read_csv(actions_file_path) if os.path.isfile(q_value_file_path) else pd.DataFrame(columns = ['qvalues'])

