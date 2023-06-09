"""
Modified version of
https://github.com/moussaKam/BARThez/blob/main/compute_mean_std.py


Get valid and test accuracy:

Use the script compute_mean_std.py:

python compute_mean_std.py --path_events experiments/tensorboard_logs/sentence_prediction/NLI/greekbart/ms32_mu23200_lr1e-04_me10_dws1/

In case you ran the training for multiple seeds, this script helps getting the mean, the median and the standard deviation of the scores.
The valid score corresponds to the best valid score across the epochs, and the test score corresponds to the test score of the epoch with the best valid score.

"""


import os
import numpy as np
from tensorboard.backend.event_processing import event_accumulator
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('--path_events', type=str, help='path to the tensorboard events')
args = parse.parse_args()

path_events = args.path_events
assert os.path.isdir(path_events)

directories = [os.path.join(path_events, el) for el in os.listdir(path_events)]

best_test = []
best_valid = []

for directory in directories:
    valid_scores = []
    test_scores = []
    valid_events = os.path.join(directory,'valid')
    test_events = os.path.join(directory,'test')
    ea = event_accumulator.EventAccumulator(valid_events, size_guidance={event_accumulator.SCALARS: 0})
    ea.Reload()
    for el in ea.Scalars('accuracy'):
        valid_scores.append(el.value)
    best_valid.append(max(valid_scores))
    if os.path.isdir(test_events):
        ea = event_accumulator.EventAccumulator(test_events, size_guidance={event_accumulator.SCALARS: 0})
        ea.Reload()
        for el in ea.Scalars('accuracy'):
            test_scores.append(el.value)
        maxi = 0
        max_test = []
        for i, el in enumerate(valid_scores):
            if el >= maxi:
                maxi = el
                max_test = test_scores[i]
        best_test.append(max_test)

print('Number examples: {}'.format(len(directories)))

print('##### Valid set #####')
print('median: {}'.format(round(np.median(best_valid), 2)),
      'mean: {}'.format(round(np.mean(best_valid), 2)),
      'std: {}'.format(round(np.std(best_valid), 2)))

if os.path.isdir(test_events):
    print('\n##### Test set #####')
    print('median: {}'.format(round(np.median(best_test), 2)),
          'mean: {}'.format(round(np.mean(best_test), 2)),
          'std: {}'.format(round(np.std(best_test), 2)))
