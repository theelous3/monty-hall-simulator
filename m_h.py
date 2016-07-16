from random import choice, randint
import time


def main():
#   main
    
    while True:
        try:
            req_permuz = int(input('Enter # of permutations to simulate:\n'))
        except TypeError:
            print('Enter an int')
        else:
            break

    print('Running...\n')

    start_time = time.time()

    monty_pie = MontyHall(req_permuz)
    host_random = monty_pie.run_host_random()
    monty_pie.reset_scores()
    host_avoid = monty_pie.run_host_avoid()
    end_time = time.time()

    print('Random host choice results:')
    print('Universe exploded {} times.'.format(host_random[0]))
    print('When the player switched, they won {} times and lost {} times.'.format(host_random[3], host_random[4]))
    print('Switching gave a {:.2%} win rate. (Expected 50%)'.format(host_random[3] / host_random[6]))
    print('When the player didn\'t switch, they won {} times and lost {} times.'.format(host_random[1], host_random[2]))
    print('Not switching gave a {:.2%} win rate. (Expected 50%)\n'.format(host_random[1] / host_random[5]))

    print('Host avoid results:')
    print('When the player switched, they won {} times and lost {} times.'.format(host_avoid[2], host_avoid[3]))
    print('Switching gave a {:.2%} win rate. (Expected 66.66%)'.format(host_avoid[2] / host_avoid[5]))
    print('When the player didn\'t switch, they won {} times and lost {} times.'.format(host_avoid[0], host_avoid[1]))
    print('Not switching gave a {:.2%} win rate. (Expected 33.33%)\n'.format(host_avoid[0] / host_avoid[4]))

    print('{} simulations in {:.4f} seconds.'.format(req_permuz, (end_time - start_time)))


class MontyHall:

    def __init__(self, permuz):
        self.permuz = permuz

        self.universe_death = 0
        self.no_switch_win = 0
        self.no_switch_loss = 0
        self.switch_win = 0
        self.switch_loss = 0
        self.switch_games = 0
        self.no_switch_games = 0

    def run_host_random(self):
    #   runs x simulations of a control version

        for i in range(self.permuz):
            #   sets up the game
            doors = {1:'pie', 2:'pie', 3:'pie'}
            doors[randint(1,3)] = 'car'
            #   player picks random door
            available_for_player = [1, 2, 3]
            player_choice = choice(available_for_player)
            #   host informed of player choice and randomly picks a door to open
            #   that door is removed from player options
            available_for_host = [1, 2, 3]
            available_for_host.remove(player_choice)
            host_choice = choice(available_for_host)
            available_for_player.remove(host_choice)
            #   destroy simulation if the host picks the car
            if doors[host_choice] is 'car':
                self.universe_death += 1
            else:
                #   test what happens when player decides to switch / not swtich
                switch_or_no = randint(0,1)
                if switch_or_no == 0:
                    self.no_switch_games += 1
                    if doors[player_choice] is 'car':
                        self.no_switch_win += 1
                    else:
                        self.no_switch_loss += 1
                else:
                    self.switch_games += 1
                    available_for_player.remove(player_choice)
                    if doors[available_for_player[0]] is 'car':
                        self.switch_win += 1
                    else:
                        self.switch_loss += 1

        return (self.universe_death,
                self.no_switch_win,
                self.no_switch_loss,
                self.switch_win,
                self.switch_loss,
                self.no_switch_games,
                self.switch_games)
        

    def run_host_avoid(self):

        for i in range(self.permuz):
            #   sets up the game
            doors = {1:'pie', 2:'pie', 3:'pie'}
            doors[randint(1,3)] = 'car'
            #   player picks random door
            available_for_player = [1, 2, 3]
            player_choice = choice(available_for_player)
            #   host informed of player choice and picks a losing door to open
            #   that door is removed from player options
            available_for_host = [1, 2, 3]
            #   host checks to see if the player's first guess is a win
            #   if it is not, we remove the car from his available options, 
            #   leaving him with only a lose to select from 
            if doors[player_choice] is not 'car':
                for i in doors:
                    if doors[i] is 'car':
                        available_for_host.remove(i)
            available_for_host.remove(player_choice)
            host_choice = available_for_host[0]
            available_for_player.remove(host_choice)

            switch_or_no = randint(0,1)
            #   test what happens when player decides to switch / not swtich
            if switch_or_no == 0:
                self.no_switch_games += 1
                if doors[player_choice] is 'car':
                    self.no_switch_win += 1
                else:
                    self.no_switch_loss += 1
            else:
                self.switch_games += 1
                available_for_player.remove(player_choice)
                if doors[available_for_player[0]] is 'car':
                    self.switch_win += 1
                else:
                    self.switch_loss += 1

        return (self.no_switch_win,
                self.no_switch_loss,
                self.switch_win,
                self.switch_loss,
                self.no_switch_games,
                self.switch_games)


    def reset_scores(self):
    #   method to reset instance vars, kind of hacky, in future replace with yields
        inst_vars = vars(self)
        for key, value in inst_vars.items():
            if key is not 'permuz':
                self.__dict__[key] = 0


if __name__ == '__main__':
    main()