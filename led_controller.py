import asyncio
from concurrent import futures
import itertools
from collections import namedtuple

import gpiozero as gpio
from time import sleep

import numpy
from gpiozero import LEDBoard, LEDBarGraph, Button, PWMLED, LED
from helpers import Votes

##
from vote_getter import VoteGetter


# from signal import pause

# https://gpiozero.readthedocs.io/en/stable/recipes.html

class VotesToLeds:

    def __init__(self):
        # Init leds
        self.green_leds = LEDBarGraph(6, 13, 19, 26, pwm=True)
        self.red_leds = LEDBarGraph(12, 16, 20, 21, pwm=True)
        self.indicator = PWMLED(22)
        self.vote_getter = VoteGetter()
        self.curr_votes = Votes(1, 100)
        self.leds_from_votes(self.curr_votes)

    def leds_from_votes(self, votes: Votes):

        self._leds_from_ratio(*self._get_vote_ratios(votes))

    def _get_vote_ratios(self, votes: Votes):
        total_votes = sum(votes)
        green_ratio = votes.green / total_votes
        red_ratio = 1 - green_ratio

        return green_ratio, red_ratio

    def _leds_from_ratio(self, green_ratio, red_ratio):

        # Set leds
        self.green_leds.value = green_ratio
        self.red_leds.value = red_ratio

    def fade_to_poll(self, new_votes: Votes):

        print(f'Fading from poll {self.curr_votes} to poll {new_votes}...')

        fade_states = 50
        old_green_r, old_red_r = self._get_vote_ratios(self.curr_votes)
        green_r, red_r = self._get_vote_ratios(new_votes)


        def ratio_set_gen(old, new):
            return numpy.linspace(old, new, fade_states).tolist()
            # return [e for e in range(old, new,
            #                          abs(old - new) / fade_states)]

        ratio_set = list(zip(ratio_set_gen(old_green_r, green_r), ratio_set_gen(old_red_r, red_r)))
        print(f'Got {len(ratio_set)} vote ratios({ratio_set[1:2]}...)')

        # votes_set = []
        # for a in range(1, fade_states + 1):
        #     # print(self.curr_votes.green +((temp_curr_votes - temp_new_votes)*(a/fade_states)))
        #     votegen = lambda temp_new_votes, temp_curr_votes: temp_curr_votes + (
        #             (temp_new_votes - temp_curr_votes) * (a / fade_states))
        #     #
        #     votes_set.append(
        #         Votes(
        #             votegen(new_votes.green, self.curr_votes.green),
        #             votegen(new_votes.red, self.curr_votes.red))
        #     )

        # print(votes_set)

        async def hi_man():
            while True:
                print("hiIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIii")
                await asyncio.sleep(2)

        def hi_man_sync():
            # while True:
            # print("hiIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIii")
            # sleep(1)
            # print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
            self.indicator.pulse(0.8, 0.8, 1, False)

        def hi_man_sync_two():
            print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
            self.indicator.pulse()
            # pause()

        async def trans_lights(votes_set):
            for transition_votes in votes_set:
                self.leds_from_votes(transition_votes)

                await asyncio.sleep(0.1)

        def trans_lights_sync(votes_set):
            for transition_votes in votes_set:
                self.leds_from_votes(transition_votes)
                sleep(0.1)

        def trans_lights_ratio(ratios_set):
            for trans_ratios in ratios_set:
                self._leds_from_ratio(*trans_ratios)
                sleep(0.1)

        pool = futures.ThreadPoolExecutor()

        # fade_future = pool.submit(trans_lights_sync, votes_set)
        # hi_future = pool.submit(hi_man_sync_two)
        # futures.wait([fade_future, hi_future], return_when=futures.FIRST_COMPLETED)
        # pool.shutdown(wait=False, cancel_futures=True)

        # This works
        # fade_future = pool.submit(trans_lights_sync, votes_set)
        fade_future = pool.submit(trans_lights_ratio, ratio_set)
        # print(fade_future.running())
        while fade_future.running():
            hi_man_sync()

        # Optimal, but hi_man's while loop is not cancellable.
        # futures.wait([fade_future], return_when=futures.FIRST_COMPLETED)
        # hi_future = pool.submit(hi_man_sync)
        # futures.wait([fade_future, hi_future], return_when=futures.FIRST_COMPLETED)
        # pool.shutdown(wait=False)
        ##

        # fade_future = pool.submit(asyncio.run, trans_lights(votes_set))
        # hi_future = pool.submit(asyncio.run, hi_man())
        #
        # # while fade_future.running():
        # #     hi_man_sync()
        #
        # # pool.shutdown(wait=True)
        # futures.wait([fade_future, hi_future], return_when=futures.FIRST_COMPLETED)
        # print("first complete")
        # # pool.shutdown(wait=False)
        # hi_future.cancel()

        self.curr_votes = new_votes

        print("all done!")

    def toggle_lights(self, on: bool):
        if on:
            self.green_leds.on()
            self.red_leds.on()
        else:
            self.green_leds.off()
            self.red_leds.off()

    def testman(self):
        # Test votes
        # votes_set = [Votes(60, 40), Votes(50, 50), Votes(40, 60),]
        votes_set = [Votes(100 - a, 0 + a) for a in range(0, 100, 2)]

        for temp_votes in itertools.cycle(votes_set):
            self.leds_from_votes(temp_votes)
            sleep(0.2)
            # self.green_leds.off()
            # self.red_leds.off()
            # sleep(0.2)

    def poll_to_led(self, poll_id):
        votes: Votes = self.vote_getter.get_votes_from_poll(poll_id)
        self.leds_from_votes(votes)


def a(a, b):
    print(a, b)


def x():
    return 10, 2


# TESTING
t = VotesToLeds()
sleep(3)
votes = t.vote_getter.get_votes_from_poll(1)
t.fade_to_poll(votes)
sleep(4)
t.fade_to_poll(Votes(1,1000))
sleep(5)

# t.fade_to_poll(Votes(1, 80))

# VotesToLeds().testman()
#

# led = PWMLED(6)

# led.pulse()

# pause()
