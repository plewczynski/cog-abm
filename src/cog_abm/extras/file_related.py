

# Found somewhere in Internet:
class CommentedFile(object):
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring

    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring):
            line = self.f.next()
        return line

    def __iter__(self):
        return self

