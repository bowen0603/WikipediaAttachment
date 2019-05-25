__author__ = 'bobo'

# import matplotlib.pyplot as plt
import networkx as nx

# Command to run:
# python3 /home/grad00/bowen/wiki_user_dropout/code/category_graph.py
#  /scratch/flagon/bowen/wiki_user_dropout/data/parsed_data_20150602/all_cat_pairs.json
#  /scratch/flagon/bowen/wiki_user_dropout/data/parsed_data_20150602/all_cat.json
#  /scratch/flagon/bowen/wiki_user_dropout/data/parsed_data_20150602/parsed_article_merged_super_category.json

class CateGraph:
    def __init__(self, cate_pair_file, art_cate_file, art_top_cate_output):
        self.input = cate_pair_file
        self.art_cate_file = art_cate_file
        self.output = art_top_cate_output
        self.fout = open(self.output, 'w')
        self.top_cates = ["arts", "geography", "health", "history", "science", "people", "philosophy", "religion"]

        self.cate_maps = {"arts": "arts", "culture": "arts", # arts
                          "geography": "geography", "places": "geography", # geography
                          "health": "health", "self care": "health", "healthcare occupations": "health", # health
                          "history": "history", "events": "history", # history
                          "mathematics": "mathematics", "logic": "mathematics", # mathematics
                          "science": "science", "natural sciences": "science", "nature": "science", # science
                          "people": "people", "personal life": "people", "self": "people", "surnames": "people", # people
                          "philosophy": "philosophy", "thought": "philosophy", # philosophy
                          "religion": "religion", "belief": "religion", # religion
                          "society": "society", "social sciences": "society", # society
                          "technology": "technology", "applied sciences": "technology"} # technology

        self.cate_stat = {"arts": 0, "culture": 0, # arts
                          "geography": 0, "places": 0, # geography
                          "health": 0, "self care": 0, "healthcare occupations": 0, # health
                          "history": 0, "events": 0, # history
                          "mathematics": 0, "logic": 0, # mathematics
                          "science": 0, "natural sciences": 0, "nature": 0, # science
                          "people": 0, "personal life": 0, "self": 0, "surnames": 0, # people
                          "philosophy": 0, "thought": 0, # philosophy
                          "religion": 0, "belief": 0, # religion
                          "society": 0, "social sciences": 0, # society
                          "technology": 0, "applied sciences": 0} # technology

        self.super_cate_stat = {"arts": 0, "geography": 0, "health": 0, "mathematics": 0,
                                "history": 0, "science": 0, "people": 0, "philosophy": 0,
                                "religion": 0, "society": 0, "technology": 0}


        self.visited_cats = None
        self.di_graph = nx.DiGraph()

        self.construct_graph()


    def construct_graph(self):

        for line in open(self.input, 'r'):
            from json import loads
            raw_record = loads(line)
            cate = raw_record["cate"]
            super_cate = raw_record["super_cate"]

            # add an edge from a category to its super category
            if not self.di_graph.has_edge(cate, super_cate):
                self.di_graph.add_edge(cate, super_cate)


    ## TODO: to have all the paths from a category to super categories, can path a list of current
    ## TODO: exploring path as a parameter, and return the entire path when hitting the end.
    def traverse_graph(self, cat, height):
            # reach the top super category
            if not self.di_graph.successors(cat):
                return cat, height, [cat]

            opt_cat = None
            opt_height = -1
            opt_cat_list = list()

            for super_cat in self.di_graph.successors(cat):
                if super_cat not in self.visited_cats:
                    self.visited_cats.append(super_cat)
                    cur_cat, cur_height, cat_list = self.traverse_graph(super_cat, height+1)

                    ## TODO need to deal with ties
                    if cur_height > opt_height:
                        opt_height = cur_height
                        opt_cat = cur_cat
                        opt_cat_list = cat_list

            opt_cat_list.append(cat)
            return opt_cat, opt_height, opt_cat_list


    def search_super_category(self, cat):
        cat = cat.lower()
        if not self.di_graph.has_node(cat):
            print("The Category {} is invalid.".format(cat))
            return

        self.visited_cats = []
        return self.traverse_graph(cat, 1)


    def search_top_category(self, cat):
        cat = cat.lower()
        if not self.di_graph.has_node(cat):
            # print("The Category {} is invalid.".format(cat))
            return None, 0

        # from Queue import Queue
        from queue import Queue
        que = Queue()
        que.put(cat)

        # it is possible an article belongs to multiple top categories
        identified_top_cats = []
        visited = [cat]
        path_len = 1
        while not que.empty():

            # find and return top categories
            if len(identified_top_cats) != 0:
                return identified_top_cats, path_len

            path_len += 1
            cur_cats = []
            while not que.empty():
                cur_cats.append(que.get())

            # all the nodes in the next level
            for cur_cat in cur_cats:
                # extend next successors
                for super_cat in self.di_graph.successors(cur_cat):
                    # changed to use the keys of the category map that maps to super category, not list
                    if super_cat in self.cate_maps.keys() and super_cat not in identified_top_cats:
                        identified_top_cats.append(super_cat)

                    if super_cat not in visited:
                        visited.append(super_cat)
                        que.put(super_cat)

        # cannot find a top category - cycles
        return None, path_len

    def get_leaf_top_categories(self):

        ## TODO: check the average top category per leaf
        ## TODO: average length of paths
        fout = open(self.output, 'w')
        for leaf in self.get_all_leaves():
            top_cats, path_len = self.search_top_category(leaf)
            if top_cats is None:
                # print("Cannot find a top category: {}, {}".format(leaf, path_len), file=fout)
                record = {"cat": leaf, "top_cat": "Not Found", "path_len":path_len}
                from json import dumps
                print(dumps(record), file=fout)
            else:
                for top_cat in top_cats:
                    record = {"cat": leaf, "top_cat": top_cat, "path_len":path_len}
                    from json import dumps
                    print(dumps(record), file=fout)

    ## total # of leaf articles: 625648
    def get_all_leaves(self):
        leaves = []
        for node in self.di_graph.nodes():
            if not self.di_graph.predecessors(node):
                leaves.append(node)
        print("Total number of leaf nodes: {}".format(len(leaves)))
        return leaves


    def get_all_super_categories(self):
        super_cats = []
        max_level = -1
        for cat in self.get_all_leaves():
            super_cat, height, cat_list = self.search_super_category(cat)
            max_level = max(max_level, height)

            if super_cat not in super_cats:
                super_cats.append(super_cat)
                # print(super_cat, cat_list, height)
                print("{},{}".format(cat_list, height), file=self.fout)

        print(max_level)


    def convert_article_cate_to_top_cate(self):

        tot_cats = 0
        tot_path_len = 0
        unique_article = []
        fout = open(self.output, 'w')

        # # of sub_category-article pairs
        # total_lines = 20485960
        cnt_lines = 0
        for line in open(self.art_cate_file, 'r'):
            cnt_lines += 1
            if cnt_lines % 2000000 == 0:
                print("{}% done..".format((int)(cnt_lines / 2000000) * 10))

            from json import loads
            record = loads(line)
            title = record["title"]
            pageId = record["pageId"]
            category = record["category"]

            if title not in unique_article:
                unique_article.append(title)

            top_cats, path_len = self.search_top_category(category)
            if top_cats is None:
                record = {"title": title, "pageId": pageId, "category": category, "super_category": "Not Found", "path_len": path_len}
                from json import dumps
                print(dumps(record), file=fout)
            else:
                tot_cats += len(top_cats)
                tot_path_len += path_len * len(top_cats)

                for sub_super_cat in top_cats:
                    cnt_cat = self.cate_stat[sub_super_cat]
                    self.cate_stat[sub_super_cat] = cnt_cat + 1

                    super_cat = self.cate_maps[sub_super_cat]
                    cnt_cat = self.super_cate_stat[super_cat]
                    self.super_cate_stat[super_cat] = cnt_cat + 1

                    record = {"title": title, "pageId": pageId, "category": category, "super_category": super_cat, "path_len": path_len}
                    from json import dumps
                    print(dumps(record), file=fout)

        from sys import stdout
        print("Average top categories per article: {}".format(1.0*tot_cats/len(unique_article)), file=stdout)
        print("Average path length to a top category: {}".format(1.0*tot_path_len/tot_cats), file=stdout)

        # print out category distributions
        print("Sub super category distributions: ")
        for sub_super_cat in self.cate_stat.keys():
            print(sub_super_cat, self.cate_stat[sub_super_cat], 1.0*self.cate_stat[sub_super_cat]/top_cats)

        print("Super category distributions: ")
        for super_cat in self.super_cate_stat.keys():
            print(super_cat, self.super_cate_stat[super_cat], 1.0*self.super_cate_stat[super_cat]/top_cats)


    def get_cate_graph(self):
        return self.di_graph


    def plot_cate_graph(self):
        nx.draw_networkx(self.di_graph)
        # plt.show()
        nx.draw(self.di_graph)


def main(argv=None):
    # give the parsed category json file
    if len(argv) != 4:
        print("usage: <category_pair__file> <article_category_file> <art_top_cate_output>")
        return

    catG = CateGraph(argv[1], argv[2], argv[3])
    # catG.plot_cate_graph()
    # catG.search_super_category("High school association football video games".lower())
    # catG.get_all_leaves()
    # catG.get_all_super_categories()
    # catG.get_leaf_top_categories()
    catG.convert_article_cate_to_top_cate()


if __name__ == '__main__':

    from time import time
    start_time = time()

    from sys import argv
    main(argv)
    print("Program execution time {} mins".format((time() - start_time) / 60))
