#!/usr/bin/python3

# ## REQUIRES python 3 !!!!

# # Run:  ./sample.py
# # Reads from stdin and writes to stdout
# # For example:
# #     ./sample.py <test.txt >test_out.txt

import pyfreeling
import os
import sys

# # ------------  output a parse tree ------------


def printTree(ptree, depth):

    node = ptree.begin()

    print(''.rjust(depth*2), end='')
    info = node.get_info()
    if info.is_head():
        print('+', end='')

    nch = node.num_children()
    if nch == 0:
        w = info.get_word()
        print('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()), end='')
    else:
        print('{0}_['.format(info.get_label()))

        for i in range(nch):
            child = node.nth_child_ref(i)
            printTree(child, depth+1)

        print(''.rjust(depth*2), end='')
        print(']', end='')

    print('')

# # ------------  output a parse tree ------------


def printDepTree(dtree, depth):
    node = dtree.begin()

    print(''.rjust(depth*2),end='')

    info = node.get_info()
    link = info.get_link()
    linfo = link.get_info()
    print('{0}/{1}/'.format(link.get_info().get_label(), info.get_label()),end='')

    w = node.get_info().get_word()
    print('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()),end='')

    nch = node.num_children()
    if nch > 0:
        print(' [')

        for i in range(nch):
            d = node.nth_child_ref(i)
            if not d.begin().get_info().is_chunk():
                printDepTree(d, depth+1)

        ch = {}
        for i in range(nch):
            d = node.nth_child_ref(i)
            if d.begin().get_info().is_chunk():
                ch[d.begin().get_info().get_chunk_ord()] = d

        for i in sorted(ch.keys()):
            printDepTree(ch[i], depth + 1)

        print(''.rjust(depth*2), end='')
        print(']', end='')

    print('')



# # ----------------------------------------------
# # -------------    MAIN PROGRAM  ---------------
# # ----------------------------------------------

# # Check whether we know where to find FreeLing data files
if "FREELINGDIR" not in os.environ:
    if sys.platform == "win32" or sys.platform == "win64":
        os.environ["FREELINGDIR"] = "C:\\Program Files"
    else:
        os.environ["FREELINGDIR"] = "/usr/local"
    print("FREELINGDIR environment variable not defined, trying ", os.environ["FREELINGDIR"], file=sys.stderr)

if not os.path.exists(os.environ["FREELINGDIR"]+"/share/freeling") :
    print("Folder", os.environ["FREELINGDIR"]+"/share/freeling",
          "not found.\nPlease set FREELINGDIR environment variable to FreeLing installation directory",
          file=sys.stderr)
    sys.exit(1)


# Location of FreeLing configuration files.
DATA = os.environ["FREELINGDIR"]+"/share/freeling/"

# Init locales
pyfreeling.util_init_locale("default")

# create language detector. Used just to show it. Results are printed
# but ignored (after, it is assumed language is LANG)
la = pyfreeling.lang_ident(DATA+"common/lang_ident/ident-few.dat")

# create options set for maco analyzer. Default values are Ok, except for data files.
LANG = "es"
morphological_options = pyfreeling.maco_options(LANG)
morphological_options.set_data_files(
    "",  # USer
    DATA + "common/punct.dat",  # Punctuation
    DATA + LANG + "/dicc.src",  # Dictionary
    DATA + LANG + "/afixos.dat",  # Affixiation Rules (For Stemming)
    "",  # Com???
    DATA + LANG + "/locucions.dat",  # Common locutions
    DATA + LANG + "/np.dat",  # Named Entity Recognizer
    DATA + LANG + "/quantities.dat",  # Words for quantities
    DATA + LANG + "/probabilitats.dat"  # Words probabilities (probably based on an HMM)
)

# create analyzers
tokenizer = pyfreeling.tokenizer(DATA+LANG+"/tokenizer.dat")
splitter = pyfreeling.splitter(DATA+LANG+"/splitter.dat")
session_id = splitter.open_session()
morphological_analyzer = pyfreeling.maco(morphological_options)

# activate mmorpho odules to be used in next call
morphological_analyzer.set_active_options(
    False,  # User map for configuration
    True,  # Number Detection
    True,  # Punctuation
    True,  # Dates
    True,  # Dictionary Search
    True,  # Affixations
    False,  # Comp (Maybe compounds?)
    True,  # RTK?
    True,  # Multiword Reconngnition
    True,  # NER
    True,  # Quantity
    True  # Probability
)   # default: all created submodules are used

# create tagger, sense anotator, and parsers
POS_tagger = pyfreeling.hmm_tagger(DATA+LANG+"/tagger.dat", True, 2)
senses_desambiguator = pyfreeling.senses(DATA+LANG+"/senses.dat")
chart_parser = pyfreeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat")
dependency_parser = pyfreeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", chart_parser.get_start_symbol())

# process input text
lines = sys.stdin.readline()

print("Text language is: "+la.identify_language(lin)+"\n")

while lines:

    line = tokenizer.tokenize(lin)
    sentences = splitter.split(session_id, line, False)

    sentences = morphological_analyzer.analyze(sentences)
    sentences = POS_tagger.analyze(sentences)
    sentences = senses_desambiguator.analyze(sentences)
    sentences = chart_parser.analyze(sentences)
    sentences = dependency_parser.analyze(sentences)

    # # output results
    for sentence in sentences:
        words = sentence.get_words()
        for word in words:
            print(word.get_form()+" "+word.get_lemma()+" "+word.get_tag()+" "+word.get_senses_string())
        print("")

        tree = sentence.get_parse_tree()
        printTree(tree, 0)

        dependency_tree = sentence.get_dep_tree()
        printDepTree(dependency_tree, 0)

    lin = sys.stdin.readline()

# clean up
splitter.close_session(session_id)

