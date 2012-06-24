"""
Module provides class for handling and gathering experiment results.
"""
import cPickle
import pprint


class ResultHandler(object):
    """
    ResultHandler class.

    Provide methods used to handle any type of operation results.

    @sort: __init__, add_result, export_to_file, get_results, pickle, save,
    save_synchronized, unpickle
    """

    def __init__(self):
        """
        Initialize ResultHandler.

        @type type: String
        @param type: Defines method of collecting results.
        It can be parallel (default) or sequence.
        """
        self.results = []


    def add_result(self, result):
        """
        Handle some operation (e.g. interaction, simulation)
        result and add it to the set of results.

        @type result: Result
        @param result: Result of any type operation.
        """
        self.save(result)


    def export_to_file(self, destination):
        """
        Export set of results to the file.

        @attention: You can call this function if results will be processed
        externally. If you want to process it in Python we recommend
        using pickle function.

        @type destination: String
        @param destination: File directory.
        """
        with open(destination, 'w') as file:
            pp = pprint.PrettyPrinter(stream=file, indent=4)
            if isinstance(self.results[0], ResultHandler):
                for result in self.results:
                    pp.pprint(result.results)
            else:
                pp.pprint(self.results)


    def get_results(self):
        """
        Return set of results.

        @rtype: list
        @return: List of collected results.
        """
        return self.results


    def pickle(self, destination):
        """
        Export set of result to the file as byte stream using pickle library.

        @type destination: String
        @param destination: File directory.
        """
        with open(destination, 'w') as file:
            cPickle.dump(self.results, file)


    def save(self, result):
        """
        Save result of one operation to the set of results.

        @type result: Result
        @param result: Result of any type operation.
        """
        self.results.append(result)


    def unpickle(self, source):
        """
        Import set of result from the file using pickle library.

        @type source: String
        @param source: Source file directory.
        """
        with open(source, 'r') as file:
            self.results = cPickle.load(file)



class ParallelResultHandler(ResultHandler):

    #TODO: Think if this is really needed
    pass
