from collections import deque
import random
import numpy as np

def quantize(value, num_levels=2, max_value=1, min_value=-1):
    assert max_value > min_value, 'ERROR: max_value must be greater than min_value'
    num_levels = np.maximum(num_levels, 2)  # A minimum of two leves is required
    q = (max_value - min_value)/(num_levels - 1)
    return (np.round(value/q) + (num_levels - 1)/2).astype(int)

class Replay_Buffer(object):
    def __init__(self, buffer_size=100000, random_seed=123):
        self._buffer_size = buffer_size
        self.count = 0
        self._buffer = deque()
        random.seed(random_seed)

    def add(self, state, action, next_state, reward, done):
        experience = np.hstack((state, action, next_state, reward, done))
        if self.count < self._buffer_size:
            self._buffer.append(experience)
            self.count += 1
        else:
            self._buffer.popleft()
            self._buffer.append(experience)

    def sample_batch(self, batch_size=1):
        batch = []
        if self.count < batch_size:
            batch = random.sample(self._buffer, self.count)
        else:
            batch = random.sample(self._buffer, batch_size)
        return np.stack(batch)

    def clear(self):
        self._buffer.clear()
        self.count = 0
