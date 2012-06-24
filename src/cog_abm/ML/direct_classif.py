from single_classif import *#a collector of points imported from here

#Use of a classifier that enables more than 2 categories

class DirectClassifier(object):
    """A classifier that uses a single multi-class classifier.
    """
    def __init__(self, simple_classifier_type):
        """@param simple_classifier_type: classifier wrapper implementing SimpleClassifier class.
        """
        self.categories = {}
        self.new_category_id = 0
        self.classif_type = simple_classifier_type
        self.classif = simple_classifier_type()

    def add_category(self, sample, class_id = None):
        """Adds a new category to the categories. Called in discrimination game. Ensures that there is >=2 num of categ.
        """
        if class_id is None:
            class_id = self.new_category_id
            self.new_category_id += 1
            tempDirClass = DataPointsCollector()
        else:
            tempDirClass = self.categories[class_id]

        if sample is not None:
            tempDirClass.add_points([sample])

        self.categories[class_id] = tempDirClass

        #if it is the only classifier, then don't retrain
        if len(self.categories) > 1:
            self.train()
        return class_id

    def del_category(self,  category_id):
        self.categories.pop(category_id, None)

    def increase_samples_category(self, sample):
        if self.count_categories() <= 1:
            self.add_category(sample)
        else:
            category_id = self.classify(sample)
            self.categories[category_id].increase_sample(sample)
        #if we are able to retrain:
        if len(self.categories) > 1:
            self.train()

    def forgetting(self):
        """
        """
        to_del = []
        for cat in self.categories:
            self.categories[cat].forgetting()
            if len(self.categories[cat].points)==0:
                to_del = to_del+[cat]
        #delete obsolete categories:
        map(self.del_category, to_del)
        self.train()

    def sample_strength(self, category_id, sample):
        return int(self.classify(sample)==category_id)

    def display_memory(self):
        """Display function for tests.
        """
        print 'display ml'
        for cat in self.categories:
            print 'category', cat
            print self.categories[cat].points
        print 'end of display ml'

    def display_time(self):
        """Display function for tests.
        """
        print 'display_time'
        for cat in self.categories:
            print 'category', cat
            print self.categories[cat].time_points
        print 'end of display_time'

    def count_categories(self):
        """Return number of active categories.
        """
        count = 0
        for cat in self.categories:
            if len(self.categories[cat].points) > 0:
                count += 1
        return count

    def classify(self, elem):
        """Returns id of the class that elem is instance of.
        """
        if self.count_categories() == 0:
            return 0
        #get number of a category, counting from 0:
        if self.count_categories() == 1:
            index = 0
        elif self.count_categories() == 2:
            index = int(self.classif.reaction(elem) > 0)
        else:
            index =  self.classif.reaction(elem)-1
        #get index from the categories list:
        for cat in self.categories:
            if len(self.categories[cat].points) > 0:
                if index == 0:
                    #print 'points: ', self.categories[cat].points, 'cat: ', cat
                    return cat
                else:
                    index = index-1

    def train(self):
        """Returns id of the class that elem is instance of.
        """
        #create values and etiquettes:
        arr = []
        etiq = []
        if self.count_categories() == 2:
            cat_val = -1
            for cat in self.categories:
                if len(self.categories[cat].points) > 0:
                    arr = arr + self.categories[cat].points
                    etiq = etiq + len(self.categories[cat].points) * [cat_val]
                    cat_val = 1
        else:
            cat_val = 1
            for cat in self.categories:
                if len(self.categories[cat].points) > 0:
                    arr = arr + self.categories[cat].points
                    etiq = etiq + len(self.categories[cat].points) * [cat_val]
                    cat_val += 1
        #retrain:
        if len(arr)>0 and etiq[0] <> etiq[len(etiq)-1]:
            #self.no_data = False
            self.classif.train(arr, etiq)
