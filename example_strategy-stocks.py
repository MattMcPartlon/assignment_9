from example_strategy import *
from stats import *
from stocks import *
from random import shuffle


def ucb1Stocks(stockTable, augment_stocks = False):
   #if augment_stocks is set to true, then a stock is added with 0 variance-
   #equivalent to choosing an "empty" action when things are uncertain
   tickers = list(stockTable.keys())
   if augment_stocks:
      if 'empty' not in stockTable:
         stockTable['empty']=[(1,1) for _ in range(len(stockTable['amzn']))]
   shuffle(tickers) # note that this makes the algorithm unstable/randomized
   numRounds = len(stockTable[tickers[0]])
   numActions = len(tickers)

   #the true reward
   reward = lambda choice, t: payoff(stockTable, t, tickers[choice])
   singleActionReward = lambda j: sum([reward(j,t) for t in range(numRounds)])

   bestAction = max(range(numActions), key=singleActionReward)
   bestActionCumulativeReward = singleActionReward(bestAction)

   cumulativeReward = 0
   t = 0
   example_Generator = alg(numActions, reward)
   for (chosenAction, reward, means) in example_Generator:
      cumulativeReward += reward
      t += 1
      if t == numRounds:
         break

   return cumulativeReward, bestActionCumulativeReward, means, tickers[bestAction]

n_trials = 30
pretty_list = lambda L: ', '.join(['%.3f' % x for x in L])
payoff_stats = lambda data: get_stats([ucb1Stocks(data)[0] for _ in range(n_trials)])


def runExperiment(table):
   print("(Expected payoff, variance) over "+str(n_trials)+" trials is %r" % (payoff_stats(table),))
   reward, bestActionReward, expectations, bestStock = ucb1Stocks(table)
   print("For a single run: ")
   print("Payoff was %.2f" % reward)
   print("Regret was %.2f" % (bestActionReward - reward))
   print("Best stock was %s at %.2f" % (bestStock, bestActionReward))
   print("expectations: %r" % pretty_list(expectations))


if __name__ == "__main__":
   table = read_stock_table('./fortune-500.csv')
   runExperiment(table)
   payoff_graph(table, list(sorted(table.keys())), cumulative=True)
   print()


