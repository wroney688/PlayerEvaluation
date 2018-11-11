

import sys, imp, os, time
import PlayerEvaluation


VERSION='0.0.1'

print "\033[4;34mPlayer Evaluator Version: ", VERSION, "\033[0m"
print sys.version
start_gen = time.time()
PlayerEvaluation.Report().saveResult(sys.argv[1], "report.html")
end_gen = time.time()
print "\033[4;34m\tTotal Report Generation Elapsed: ", (end_gen - start_gen), " seconds.\033[0m"





