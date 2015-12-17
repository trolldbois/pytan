

class Store(dict):

    def __str__(self):
        me = self.__class__.__name__
        ret = '\n'.join(["{} attribute '{}': '{}'".format(me, k, v) for k, v in self.iteritems()])
        return ret

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class Result(Store):
    pass
