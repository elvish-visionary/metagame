__author__ = 'Ben'
import pandas as pd
import numpy as np

class Card(object):
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return "%s %s" % (self.quantity, self.name)

class Deck(object):

    def __init__(self, name, pct):
        self.name = name
        self.pct = pct
        self.list = None

    def __str__(self):

        return "<Deck name: %s Percentage: %s>" % (self.name, self.pct)

    def __repr__(self):

        return self.__str__()

    def load_list(self):
        path = './decklists/' + self.name + '.txt'
        self.list = []
        self.cardnames = []
        with open(path, 'r') as f:
            for line in f:
                if 'Sideboard' in line:
                    break
                quant = line.split(' ', 1)[0]
                name = line.split(' ', 1)[1].split('\r')[0]
                self.list.append(Card(name, quant))
                self.cardnames.append(name)

    def __eq__(self, other):

        set1 = set(self.cardnames)
        set2 = set(other.cardnames)

        return len(set1-set2) < 10 and len(set2-set1) < 10


def run_sim():

    no_repeats = False

    df = pd.read_csv('modern_meta.csv')

    decks = []
    deck_probs = []

    for i, row in df.iterrows():

        d = Deck(row['Deck'], row['True_percentage'])
        d.load_list()

        decks.append(d)
        deck_probs.append(row['True_percentage'])


    results = [[] for i in range(len(decks))]

    n_sims = 10000

    for i in range(n_sims):

        if i % 100 == 0:
            print "Simulation %d/%d" % (i, n_sims)

        all_names = []

        for i in range(60):
            report_lists = []
            while len(report_lists) < 5:
                deck = np.random.choice(a=decks, p=deck_probs)
                if no_repeats and deck in report_lists:
                    #print "Not reporting %s!" % deck.name
                    continue
                report_lists.append(deck)
                all_names.append(deck.name)

        for i, deck in enumerate(decks):
            count = all_names.count(deck.name)
            percentage = float(count)/len(all_names)

            results[i].append(percentage)


    print '| Deck | "True" meta %| Reported meta %|'
    print '| ------------- | ---------------- | ------------------|'

    for i, deck in enumerate(decks):
        average_pct = 100*np.mean(results[i])
        std_pct = 100*np.std(results[i])

        print "| %s| %0.2f | %0.2f +- %0.2f |" % (deck.name, deck.pct*100, average_pct, 2*std_pct)



if __name__ == '__main__':
    run_sim()
