"""
Copyright <2019> <Jinhan Wu>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


1. Winning odd calculation: knowing the odd of the card sets on your hands
2. Monte Carlo simulation: Knowing the expectation value if other plays bet more than you do
3. General information: Knowing the odd to have different sets of cards


"""
import numpy as np
import random
import matplotlib.pyplot as plt

class rank: #self.K is sets of the cards, self.Q is quantity of the cards
    def __init__(self, card):
        self.suit = [card[0][0],card[1][0],card[2][0]]
        self.nums = [int(card[0][1:]),int(card[1][1:]),int(card[2][1:])]

    def classify(self):
        self.nums.sort()
        self.num_default = self.nums.copy()
        if len(set(self.nums)) == 1:
            # print ('triple')
            self.K = 5
            self.Q = list(set(self.nums))[0]

        elif len(set(self.suit)) == 1:
            if self.nums[2] - self.nums[1] == 1 and self.nums[1] - self.nums[0] == 1:
                # print ('straight flush')
                self.K = 4
                self.Q = self.nums[2]
            else:
                # print('flush')
                self.K = 3
                self.Q = self.nums[2]
                self.Q2 = self.nums[1]
                self.Q3 = self.nums[0]
        elif len(set(self.suit)) > 1:
            # self.nums.sort()
            if self.nums[2] - self.nums[1] == 1 and self.nums[1] - self.nums[0] == 1:
                # print ('straight')
                self.K = 2
                self.Q = self.nums[2]
            elif len(set(self.nums)) == 2:
                temp = list(set(self.nums))
                # print ('a pair')
                self.K = 1
                self.nums.remove(temp[0])
                self.nums.remove(temp[1])
                self.Q = self.nums[0]
                temp.remove(self.Q)
                self.Q2 = temp[0]
            else:
                # print ('high card')
                self.K = 0
                self.Q = self.nums[2]
                self.Q2 = self.nums[1]
                self.Q3 = self.nums[0]
def combinations(lst, depth, start=0, prepend=[]):
    if depth <= 0:
        yield prepend
    else:
        for i in range(start, len(lst)):
            for c in combinations(lst, depth - 1, i + 1, prepend + [lst[i]]):
                yield c

def who_win(card1, card2):
    global Win_P1, Win_P2, withdraw
    play1 = rank(card1)
    play1.classify()
    play2 = rank(card2)
    play2.classify()
    if play1.K == 5 and play2.K == 0 and play2.num_default[2]==5 and play2.num_default[1]==3 and play2.num_default[0]==2: #underdog case #1
        Win_P2 += 1
        return -1
    elif play2.K == 5 and play1.K ==0 and play1.num_default[2]==5 and play1.num_default[1]==3 and play1.num_default[0]==2: #underdog case #2
        Win_P1 += 1
        return 1
    elif play1.K > play2.K:
        Win_P1 += 1
        return 1
    elif play1.K == play2.K:
        if play1.Q > play2.Q:
            Win_P1 += 1
            return 1
        elif play1.Q == play2.Q:
            try:
                if play1.Q2 > play2.Q2:
                    Win_P1 += 1
                    return 1
                elif play1.Q2 == play2.Q2:
                        if play1.Q3 > play2.Q3:
                            Win_P1 += 1
                            return 1
                        elif play1.Q3 < play2.Q3:
                            Win_P2 += 1
                            return -1
                        else:
                            withdraw += 1
                            return 0
                else:
                    Win_P2 += 1
                    return -1
            except:
                withdraw += 1
                return 0
        else:
            Win_P2 += 1
            return -1
    else:
        Win_P2 += 1
        return -1

Win_P1 = 0
Win_P2 = 0
withdraw = 0
Matches = 0

suits = ['s', 'h', 'd', 'c'] #s = Spade, h= Heart, d = Dimond, c = Club
numbers = np.arange(2,15,1) #2-14, where 14 = ace
stack = []
for suit in suits: # create a poker stack
    for number in numbers:
        stack.append(suit+str(number))

''' Win_odd calculation'''
# random.shuffle(stack)
# card1 = stack[0:3] # randomly chosen cards
# print (card1)
# # card1 = ['s14', 'd14', 'c14'] # customized cards
# for card in card1:
#     stack.remove(card)
#
# for card in combinations(stack, 3):
#     Matches += 1
#     who_win(card1, card)
# print (Matches, Win_P1, Win_P2, withdraw)
# print ("Odd:", Win_P1/Matches)

'''Monte Carlo simulation'''
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(6, 6))
profit_list = []
expect_list = []
profit = 0
for _ in range(1000):
    Matches += 1
    random.shuffle(stack)
    card1 = stack[0:3]
    card2 = stack[3:6]
    result = who_win(card1, card2)
    if result == 1:
        profit += 11 # assuming that P2 bets 1 units more than P1 does
    elif result == -1:
        profit -= 10
    profit_list.append(profit)
    expect_list.append(profit/Matches)
print (Matches, Win_P1, Win_P2, withdraw)
print ("P1 Win_Odd:", Win_P1/Matches)
print ('Average benefit per match:', profit/Matches)
ax[0].semilogx(np.arange(1,1000+1,1), profit_list)
ax[1].semilogx(np.arange(1,1000+1,1), expect_list)
ax[0].plot([0, Matches], [0,0], ':r')
ax[1].plot([0, Matches], [0,0], ':r')
ax[0].set_title("Monte Carlo simulation")
ax[0].set_ylabel('Profit')
ax[1].set_ylabel('Expectation value of profit')
ax[1].set_xlabel('Matche times')
plt.show()


''' general information'''
total = 0
triple = 0
straight_flush = 0
flush = 0
straight = 0
pair = 0
high_card = 0
for card in combinations(stack, 3):
    total += 1
    play1 = rank(card)
    play1.classify()
    if play1.K == 5:
        triple += 1
    elif play1.K == 4:
        straight_flush += 1
    elif play1.K ==3:
        flush += 1
    elif play1.K == 2:
        straight += 1
    elif play1.K == 1:
        pair += 1
    else:
        high_card += 1
labels =  'triple', 'high_card', 'straight_flush', 'flush', 'straight', 'pair'
data = [triple/total, high_card/total, straight_flush/total, flush/total, straight/total, pair/total]

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-90)
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels[i]+' {:.3%}'.format(data[i]), xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)
ax.set_title("The odd of each sets")

plt.show()
