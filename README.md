# ZeroSumGame
Comparison of the performances between min-max algorithm and alpha-beta pruning by implementing zero-sum game.

Alpha-beta algorithm is the improved version of the minimax using a heuristic. According the code it does not evaluate the node if it is worse than the previous evaluated node. So that further of the nodes do not needed to be evaluated as well. Let us see some results from my program:
Program is tested for 10 times per each algorithm and I recorded the min and max times of finding the optimal solution for first move because first move has the largest tree to evaluate.

### Algorithm          | Minimum Time |	 Maximum Time   |	N (Grid Value)

Minimax	            |  8.94 seconds	|   19.97 seconds	|  10

Alpha-beta pruning	| 0.0299 seconds |	 0.0309 seconds	|  10
