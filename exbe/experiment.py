import abc
import json
import os
import time


class Timer:
    def __init__(self):
        self._start_time = None
        self._end_time = None

    def start(self):
        self._end_time = None
        self._start_time = time.perf_counter()
        return self._start_time

    def stop(self):
        self._end_time = time.perf_counter()
        return self._end_time

    @property
    def total_time(self):
        if self._start_time is None or self._end_time is None:
            raise ValueError("Need to start and stop first.")

        return self._end_time - self._start_time


class Results:
    # TODO: add ability to serialize results
    def __init__(self, current=False, ignore=()):
        self._dict = {}
        self.current = current
        self.ignore = ignore

    def __getattr__(self, name):
        if name in self._dict:
            return self._dict[name]

        return super().__getattr__(name)

    @property
    def names(self):
        return tuple(self._dict.keys())

    def append(self, **kwargs):
        # TODO: add strategy for private values? e.g. _
        for name, value in kwargs.items():
            if name not in self._dict:
                self._dict[name] = []

            if self.current:
                self._dict[name][-1].append(value)

            else:
                self._dict[name].append([value])

    def to_dict(self, ignore=False):
        data = self._dict.copy()
        if not ignore:
            return data

        for name in self.ignore:
            del data[name]

        return data


class Experiment(abc.ABC):
    # TODO: add some reset mechanism?
    # TODO: add some id?

    def __init__(
        self, n_trials=3, timer=None, results=None, metadata=None, serializer=None
    ):
        self.n_trials = n_trials

        if timer is None:
            timer = Timer()

        if results is None:
            results = Results()

        if metadata is None:
            metadata = {}

        if serializer is None:
            serializer = JsonSerializer()

        self.timer = Timer()
        self.results = results
        self.metadata = metadata
        self.serializer = serializer

        self._update_metadata()

    def _update_metadata():
        pass

    def next_condition(self):
        return False

    def before_trial(self, trial_):
        pass

    def trial(self):
        return {}

    def after_trial(self, **kwargs):
        return {}

    def run_trials(self):
        # TODO: allow for (optional) failures while continuing running
        self.results.current = False
        for trial_index in range(self.n_trials):
            self.before_trial(trial_index)

            self.timer.start()
            out = self.trial()
            self.timer.stop()

            self.results.append(**out)
            self.results.append(total_time=self.timer.total_time)

            out_after = self.after_trial(**out)
            self.results.append(**out_after)
            self.results.current = True

        self.results.current = False

    def run(self):
        # TODO: return False if not successful
        # must be at trial level
        while self.next_condition():
            self.run_trials()

    def to_dict(self, ignore=False):
        data = {"metadata": self.metadata.copy()}
        data["results"] = self.results.to_dict(ignore=ignore)
        return data

    def serialize(self, filename=None):
        self.serializer.dump(self.to_dict(ignore=True), filename=filename)


class Serializer(abc.ABC):
    def __init__(self, dir_name=None):
        if dir_name is None:
            dir_name = ""

        self.dir_name = None
        self.set_dir(dir_name)

    def set_dir(self, dir_name):
        if dir_name and not os.path.exists(dir_name):
            os.mkdir(dir_name)
        self.dir_name = dir_name

    @property
    def default_filename(self):
        return time.strftime("%Y%m%d%H%M%S", time.gmtime())


class JsonSerializer(Serializer):
    def dump(self, data, filename=None):
        if filename is None:
            filename = self.default_filename

        name = os.path.join(self.dir_name, filename) + ".json"

        with open(name, "w") as file:
            json.dump(data, file, indent=4)
