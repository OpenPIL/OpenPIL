

#The three major datasets used:
from . import drugClassDataset
from . import drugNameDataset
from . import drugClassSynonymDataset

from . import greekAlphabet

classes = drugClassDataset.classes
drugs = drugNameDataset.drugs
class_synonyms = drugClassSynonymDataset.class_synonyms

greek_alphabet = greekAlphabet.greek_alphabet
#############################################



import PyPDF2
import pdftotext
import re
import string
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
from itertools import combinations
import math
import sys
import platform
# import ctypes
from ctypes import *

# flattens class synonym dataset from dictionary to array for use in analysis:
def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt
class_intermediate = []
[class_intermediate.extend([k,v]) for k,v in class_synonyms.items()]
class_synonyms_array = flatten(class_intermediate)

#lowercases all string tokens for drug names, drug-classification names and drug-classification-synonym names to ensure no token-match is missed due to CAPITAL letters. The pdf document which is converted to text will also be lowercased to ensure this.
DRUGS = []
for i in drugs:
    x = i.lower()
    DRUGS.append(x)
    
CLASSES = []
for i in classes:
    x = i.lower()
    CLASSES.append(x)
    
CLASSSYNONYMS = [x.lower() for x in class_synonyms_array]


#loading bar to track progress when analysing multiple pdfs. Each pdf takes approx. 4 mins.
def update_progress(progress):
    barLength = 100
    if isinstance(progress, int):
        progress = float(progress)
    block = int(round(barLength*progress))
    timeHours = (((len(DRUGS)-(progress*len(DRUGS)))/60)/60)
    timeHoursRounded = math.floor((((len(DRUGS)-(progress*len(DRUGS)))/60)/60))
    text = "\rCompletion: {0}% [{1}] {2} Hours {3} Minutes Remaining".format(round(progress*100,1), "#"*block + "-"*(barLength-block), timeHoursRounded, math.floor(timeHours*60 - timeHoursRounded*60))
    sys.stdout.write(text)
    sys.stdout.flush()
    

def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

#function to find words in sentences
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#the function that isolates text between two other strings in the pdf
def find_between(y, first, last ):
    try:
        start = y.index( first ) + len( first )
        end = y.index( last, start )
        return y[start:end]
    except ValueError:
        return ""

#splits text into sentences, "set([..])" makes it so that sentence break points don't occur for these instances, and removes paragraphs
def sentenceGenerator(segment, emptyArray):
    tempArray = []
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['e.g', "St", "st"])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(segment)
    # cleans up extra white space which occurs in interactions text due to some smpcs having tabular format

    for i in sentences:
        j = i.replace('\n',' ')
        new = " ".join(j.split())
        emptyArray.append(new)


#splits text into sentences, "set([..])" makes it so that sentence break points don't occur for these instances, and removes paragraphs
def intSentenceGenerator(segment, emptyArray):
    tempArray = []
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['e.g', "St", "st"])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(segment)
    # cleans up extra white space which occurs in interactions text due to some smpcs having tabular format
    for i in sentences:
        j = i.replace('\n',' ')
        new = " ".join(j.split())
        tempArray.append(new)


    for i in sentences:
        j = i.replace('\n', ' ')
        new = " ".join(j.split())
        emptyArray.append(new)



#splits text into sentences, "set([..])" makes it so that sentence break points don't occur for these instances, and removes paragraphs
def intSentenceGeneratorPOSNEG(segment, pos, neg, cau):
    tempArray = []
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['e.g', "St", "st"])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(segment)
    # cleans up extra white space which occurs in interactions text due to some smpcs having tabular format
    for i in sentences:
        j = i.replace('\n',' ')
        new = " ".join(j.split())
        tempArray.append(new)
    # removes sentences which contain 'negative words' that imply the sentence is saying there is NOT an interaction, as    opposed to there being one. It appends these negative sentences to 'removeInteractiveSentences' array
    negativeWords = ['no dose', 'no clinically', 'does not', 'did not', 'not suggest', 'not expected', 'negligible',
                     'unlikely', 'without any evidence', 'not to be expected', 'without evidence', 'low potential',
                     'no clinical evidence', 'safely', 'small delay', 'unaffected', 'can be administered',
                     'no significant', 'no effect', 'no clinical', 'not clinically', 'no evidence', 'no expected',
                     'has not', 'be safely', 'were not', 'no pharmacokinetic', 'no interaction', 'not interact', 'no pharmacokinectic interaction', 'no kinetic interaction', 'no kinetic']
    excemptionWords = ["but", "however"]
    cautionWords = ['caution', 'cautionary', 'care']

    for i in tempArray:
        if any(word in i for word in negativeWords) == False:
            if any(word in i for word in cautionWords) == False:
                pos.append(i)
        if any(word in i for word in negativeWords) == True:
            if any(word in i for word in cautionWords) == False:
                neg.append(i)

    for i in neg:
        if any(word in i for word in excemptionWords) == True:
            pos.append(i)
            neg.remove(i)

    for i in tempArray:
        if any(word in i for word in cautionWords) == True:
            cau.append(i)

def sentenceSplitterInteractions(sentences, combination):
    combinationsIntermediate = []
    combinationsIntermediateFlat = []

    singleWords = []
    singleWordsIntermediate = []
    for i in sentences:
        words = i.split()
        singleWords.append(words)
        for start, end in combinations(range(len(words)), 2):
            if len(words[start:end + 1]) <= 4:
                combinationsIntermediate.append(words[start:end + 1])

    singleWordsFlat = [j for i in singleWords for j in i]

    for i in combinationsIntermediate:
        combinationsIntermediateFlat.append(' '.join(i))

    removeSpecials = str.maketrans('', '', '{}()[]!.,%')
    combinationsIntermediateFlatClean = [x.translate(removeSpecials) for x in combinationsIntermediateFlat]
    singleWordsFlatClean = [x.translate(removeSpecials) for x in singleWordsFlat]

    for i in combinationsIntermediateFlatClean:
        j = [key for key in greek_alphabet.keys() if key in i]
        if len(j) >= 1:
            x = i.replace(j[0], greek_alphabet[j[0]])
            if x not in combination:
                combination.append(''.join(x))
        if len(j) == 0 :
            if i not in combination:
                combination.append(''.join(i))

    for i in singleWordsFlatClean:
        j = [key for key in greek_alphabet.keys() if key in i]
        if len(j) >= 1:
            x = i.replace(j[0], greek_alphabet[j[0]])
            if x not in combination:
                if x in CLASSSYNONYMS:
                    combination.append(''.join(x))
        if len(j) == 0:
            if i not in combination:
                if i in CLASSSYNONYMS:
                    combination.append(i)

def sentenceSplitterInteractionsDrugs(sentences, combination):
    combinationsIntermediate = []
    combinationsIntermediateFlat = []

    singleWords = []
    singleWordsIntermediate = []
    for i in sentences:
        words = i.split()
        singleWords.append(words)
        for start, end in combinations(range(len(words)), 2):
            if len(words[start:end + 1]) <= 3:
                combinationsIntermediate.append(words[start:end + 1])

    singleWordsFlat = [j for i in singleWords for j in i]

    for i in combinationsIntermediate:
        combinationsIntermediateFlat.append(' '.join(i))

    removeSpecials = str.maketrans('', '', '{}()[]!.,%')
    combinationsIntermediateFlatClean = [x.translate(removeSpecials) for x in combinationsIntermediateFlat]
    singleWordsFlatClean = [x.translate(removeSpecials) for x in singleWordsFlat]

    for i in combinationsIntermediateFlatClean:
        j = [key for key in greek_alphabet.keys() if key in i]
        if len(j) >= 1:
            x = i.replace(j[0], greek_alphabet[j[0]])
            if x not in combination:
                combination.append(''.join(x))
        if len(j) == 0 :
            if i not in combination:
                combination.append(''.join(i))

    for i in singleWordsFlatClean:
        j = [key for key in greek_alphabet.keys() if key in i]
        if len(j) >= 1:
            x = i.replace(j[0], greek_alphabet[j[0]])
            if x not in combination:
                combination.append(''.join(x))
        if len(j) == 0:
            if i not in combination:
                combination.append(i)

def sentenceSplitter(sentences, combination):
    combinationsIntermediate = []
    combinationsIntermediateFlat = []

    singleWords = []
    singleWordsIntermediate = []
    for i in sentences:
        words = i.split()
        singleWords.append(words)
        for start, end in combinations(range(len(words)), 2):
            if len(words[start:end + 1]) <= 4:
                combinationsIntermediate.append(words[start:end + 1])

    singleWordsFlat = [j for i in singleWords for j in i]


    for i in combinationsIntermediate:

        combinationsIntermediateFlat.append(' '.join(i))

    removeSpecials = str.maketrans('', '', '{}()[]!.,%')
    combinationsIntermediateFlatClean = [x.translate(removeSpecials) for x in combinationsIntermediateFlat]
    singleWordsFlatClean = [x.translate(removeSpecials) for x in singleWordsFlat]




    for i in combinationsIntermediateFlatClean:
        j = [key for key in greek_alphabet.keys() if key in i]
        if len(j) >= 1:
            x = i.replace(j[0], greek_alphabet[j[0]])
            if x not in combination:
                combination.append(''.join(x))
        if len(j) == 0:
            if i not in combination:
                combination.append(''.join(i))


    for i in singleWordsFlatClean:
        j = [key for key in greek_alphabet.keys() if key in i]
        if len(j) >= 1:
            x = i.replace(j[0], greek_alphabet[j[0]])
            if x not in combination:
                    combination.append(''.join(x))
        if len(j) == 0:
            if i not in combination:
                    combination.append(i)

                    
#Running every drug name, drug class name and every drug-class synonym to carry out a heavy mathematical string comparison calculation (which I have selfishly coined the 'Malik-Similarity Algorithm'), would take a very long time to process through python alone (approx. 1 hour per pdf document based on tests I've had to endure running). In order to overcome this, I have ported this most taxing portion of the code to C, which as anyone who loves their for-loops knows, is the arguably the fastest language on earth today to run for-loops with heavy string calculations on (alongside machine code, assembly and C++). So thats what the below code does for you. It sends the strings to C, where they are compared to the datasets, and then sends back the mathematical percentage similarity as a Double value (e.g. 0.95, representing 95% similarity between the token from the pdf and the drug datasets).

#if you have issues with this section, try to change "libfun.so" to the full path name e.g. "/User/YourName/Documents/OpenPIL/libfun.so"

dll = CDLL("/Volumes/HARRISDRIVE/OpenPIL/OpenPIL/libfun.{}".format("so.6" if platform.uname()[0] != "Darwin" else "dylib"))
#ctypes.cdll.LoadLibrary("libfun.so")
dll.append_lists.argtypes = POINTER(c_char_p),c_size_t,POINTER(c_char_p),c_size_t,POINTER(c_size_t)
dll.append_lists.restype = POINTER(c_char_p)
dll.append_lists_classes.argtypes = POINTER(c_char_p),c_size_t,POINTER(c_char_p),c_size_t,POINTER(c_size_t)
dll.append_lists_classes.restype = POINTER(c_char_p)
dll.free_list.argtypes = POINTER(c_char_p),c_size_t
dll.free_list.restype = None

# Helper function to turn Python list of Unicode strings
# into a ctypes array of byte strings.
def make_clist(lst):
    return (c_char_p * len(lst))(*[x.encode() for x in lst])

# Helper function to convert the lists, make the call correctly,
# convert the return result back into a Python list of Unicode strings,
# and free the C allocations.
def append_lists(list1,list2):
    size = c_size_t()
    result = dll.append_lists(make_clist(list1),len(list1),make_clist(list2),len(list2),byref(size))
    data = [x.decode() for x in result[:size.value]]
    dll.free_list(result,size.value)
    return data

def append_lists_classes(list1,list2):
    size = c_size_t()
    result = dll.append_lists_classes(make_clist(list1),len(list1),make_clist(list2),len(list2),byref(size))
    data = [x.decode() for x in result[:size.value]]
    dll.free_list(result,size.value)
    return data



#'PDF_Path' should be the path to the .pdf file on your computer, and this must be in quotation marks,
#FOR EXAMPLE --> PDF_Path = "/User/YourName/Documents/PDFs/SummaryOfProductCharacters_Abacavir.pdf"


def AI(PDF_Path):
    
#checks to see if PDF is a valid and uncorrupted document. If so, the function will terminate displaying the error message "invalid PDF file":
    try:
        PyPDF2.PdfFileReader(open(PDF_Path, "rb"))
    except PyPDF2.utils.PdfReadError:
        print("invalid PDF file")
    else:
        pass


    drugDictionary = {
        "SMPC NAME" : [],
        "BRAND NAME": [],
        "ACTIVE SUBSTANCE(S)": [],
        "ACTIVE EXCIPIENT(S)": [],
        "FORMULATION": [],
        "INTERACTIVE DRUG CLASSES": [],
        "INTERACTIVE DRUGS": [],
        "CAUTIONS": []
    }
    #makes text file ("xx") from pdf
    with open(PDF_Path, "rb") as f:
        pdf = pdftotext.PDF(f)
    PDF = "".join(pdf)
    #lower_case for pdf doc
    pdf = PDF.lower()



    #BRANDNAME:
    brandName_segment = find_between(pdf, "name of the medicinal product", "qualitative")
    #CHECKS IF SEGMENT IS DETECTECTED CORRECTLY IN TERMINAL:
#       print(brandName_segment)

    #splits brandName_segment into words and numbers to extract
    brandName = re.split(r'\s+(?=\d)|(?<=\d)\s+', brandName_segment)
    #removes spacing
    brandNameClean = []
    for x in brandName:
        new = " ".join(x.split())
        brandNameClean.append(new)
    #Brand Name below:
    BRANDNAME = brandNameClean[0]

    #FORMULATION:
    #array of formulations to compare with text in the brand name segment:
    formulations = ["chewable tablet", "tablet", "film coated tablet","capsule", "caplet", "for injection", "powder", "syrup", "oral solution", "solution", "patch", "nasal drop", "eye drop", "drop", "ear drop", "mouthwash", "", "emulsion", "mixture", "nasal spray", "inhalor", "vaginal", "cream", "ointment", "rectal", "suppository", "suppositories", "pessary", "liquid", "suspension"]

    #find formulations in brandNameClean:
    formulation = []
    for i in brandNameClean:
        new = [x for x in formulations if x in i]
        for j in new:
            if j != "":
                if j not in formulation:
                    formulation.append(j)

    #removes duplicates from array of formulations, i.e. if it contains 'oral solution' and 'solution' it will leave only 'oral solution'.

    FORMULATION = []
    for i in formulation:
        if i not in FORMULATION:
            FORMULATION.append(i)
    #ACTIVESUBSTANCES:
    segmentOne = find_between(pdf, "qualitative and quantitative composition", "pharmaceutical form")

    if "excipient" in segmentOne:
        activeSubstance_segment = find_between(pdf, "qualitative and quantitative composition", "excipient")
        activeExcipient_segment = find_between(pdf, "excipient", "pharmaceutical form")
        # splits activeSubstance_Segment into sentences:
        activeSubstance_sentences = []
        activeExcipient_sentences = []
        sentenceGenerator(activeSubstance_segment, activeSubstance_sentences)
        sentenceGenerator(activeExcipient_segment, activeExcipient_sentences)


        # splits activeSubstance_Sentences into all combinations of possible words
        activeSubstance_segmentSplitClean = []
        sentenceSplitter(activeSubstance_sentences, activeSubstance_segmentSplitClean)

        activeExcipient_segmentSplitClean = []
        sentenceSplitter(activeExcipient_sentences, activeExcipient_segmentSplitClean)
        # finds cosine similarity between each activeSubstance_segmentSplitClean and DRUGS, if >95%, it appends to activeSubstances

        activeSubstances = append_lists(DRUGS, activeSubstance_segmentSplitClean)

        activeExcipients = append_lists(DRUGS, activeExcipient_segmentSplitClean)

        # removes duplicates from array of active substances, i.e. if it contains 'cyp3a4 inhibitor' and 'inhibitor' it will leave only 'cyp3a4 inhibitor'.
        ACTIVESUBSTANCES = []
        for i in activeSubstances:
            if i not in ACTIVESUBSTANCES:
                ACTIVESUBSTANCES.append(i)

        ACTIVEEXCIPIENTS = []

        for i in activeExcipients:
            if i not in ACTIVESUBSTANCES:
                if i not in ACTIVEEXCIPIENTS:
                    ACTIVEEXCIPIENTS.append(i)

        for i in DRUGS:
            if i in activeExcipient_segmentSplitClean:
                if i not in ACTIVEEXCIPIENTS:
                    if i not in ACTIVESUBSTANCES:
                        ACTIVEEXCIPIENTS.append(i)

    else:
        activeSubstance_segment = segmentOne
        #splits activeSubstance_Segment into sentences:
        activeSubstance_sentences = []
        sentenceGenerator(activeSubstance_segment, activeSubstance_sentences)
        #splits activeSubstance_Sentences into all combinations of possible words
        activeSubstance_segmentSplit = []
        activeSubstance_segmentSplitClean = []
        sentenceSplitter(activeSubstance_sentences, activeSubstance_segmentSplitClean)
        #finds cosine similarity between each activeSubstance_segmentSplitClean and DRUGS, if >95%, it appends to activeSubstances
        activeSubstances = append_lists(DRUGS, activeSubstance_segmentSplitClean)
        # removes duplicates from array of active substances, i.e. if it contains 'cyp3a4 inhibitor' and 'inhibitor' it will leave only 'cyp3a4 inhibitor'.
        ACTIVESUBSTANCES = []
        for i in activeSubstances:
            if i not in ACTIVESUBSTANCES:
                ACTIVESUBSTANCES.append(i)

    #INTERACTIONS:
    interactions_segment = find_between(pdf, "other forms of interaction", "fertility, pregnancy and lactation")
    if interactions_segment == "":
        interactions_segment == find_between(pdf, "other forms of interaction", "pregnancy and lactation")
    if interactions_segment == "":
        interactions_segment = find_between(pdf, "other forms of interaction", "pregnancy and breastfeeding")
    if interactions_segment =="":
        interactions_segment = find_between(pdf, "other forms of", "pregnancy and breast-feeding")
    if interactions_segment == "":
        interactions_segment = find_between(pdf, "other forms of interaction", "fertility, pregnancy and breast feeding")
    if interactions_segment == "":
        interactions_segment = find_between(pdf, "other forms of", "fertility, pregnancy and lactation")

    # splits interactions_Segment into sentences:
    positiveSentences = []
    negativeSentences = []
    cautionSentences = []
    intSentenceGeneratorPOSNEG(interactions_segment, positiveSentences, negativeSentences, cautionSentences)

    interactionsPos_segmentSplitClean = []
    sentenceSplitterInteractions(positiveSentences, interactionsPos_segmentSplitClean)
    interactionsPosDrugs_segmentSplitClean = []
    sentenceSplitterInteractionsDrugs(positiveSentences, interactionsPosDrugs_segmentSplitClean)



    cautionDrugs_segmentSplitClean = []
    sentenceSplitterInteractionsDrugs(cautionSentences, cautionDrugs_segmentSplitClean)

    interactionsNeg_segmentSplitClean = []
    sentenceSplitterInteractions(negativeSentences, interactionsNeg_segmentSplitClean)
    interactionsNegDrugs_segmentSplitClean = []
    sentenceSplitterInteractionsDrugs(negativeSentences, interactionsNegDrugs_segmentSplitClean)

    # finds cosine similarity between each interactions_segmentSplitClean and DRUGS, if >85%, it appends to interactions_classes
    print("Compiling positive class interactions...")
    interactionsPos_classes = append_lists_classes(CLASSSYNONYMS, interactionsPos_segmentSplitClean)
    print("Compiling negative class interactions...")
    interactionsNeg_classes = append_lists_classes(CLASSSYNONYMS, interactionsNeg_segmentSplitClean)

    # removes duplicates from array of interactions, i.e. if it contains 'cyp3a4 inhibitor' and 'inhibitor' it will leave only 'cyp3a4 inhibitor'.

    CLASSINTERMEDIATEPOS = []

    for i in interactionsPos_classes:
        if i not in CLASSINTERMEDIATEPOS:
            CLASSINTERMEDIATEPOS.append(i)

    for i in CLASSSYNONYMS:
        if i in interactionsPos_segmentSplitClean:
            if i not in CLASSINTERMEDIATEPOS:
                CLASSINTERMEDIATEPOS.append(i)

    CLASSINTERMEDIATENEG = []
    for i in interactionsNeg_classes:
        if i not in CLASSINTERMEDIATENEG:
            CLASSINTERMEDIATENEG.append(i)


    for i in CLASSSYNONYMS:
        if i in interactionsNeg_segmentSplitClean:
            if i not in CLASSINTERMEDIATENEG:
                CLASSINTERMEDIATENEG.append(i)


    CLASSINTERMEDIATEPOSNEG = []

    for i in CLASSINTERMEDIATEPOS:
        if i not in CLASSINTERMEDIATENEG:
            CLASSINTERMEDIATEPOSNEG.append(i)

    classessPOSNEG = []
    for i in CLASSINTERMEDIATEPOSNEG:
        original = [key for (key, value) in class_synonyms.items() if i in value]


        if len(original) >= 1:
            if original[0] not in classessPOSNEG:
                classessPOSNEG.append(original[0])
        original2 = [key for key in class_synonyms.keys() if i == key]
        if len(original2) >= 1:
            if original2[0] not in classessPOSNEG:
                classessPOSNEG.append(original2[0])

    CLASSESPOSNEG = []
    for i in classessPOSNEG:
        if i not in CLASSESPOSNEG:
            CLASSESPOSNEG.append(i)

    # finds cosine similarity between each interactions_segmentSplitClean and DRUGS, if >85%, it appends to interactions

    #CAUTIONS INTERLUDE:
    print("Compiling caution classes...")
    cautionsClasses = append_lists_classes(CLASSSYNONYMS, cautionDrugs_segmentSplitClean)
    print("Compiling caution drugs...")
    cautionsDrugs = append_lists(DRUGS, cautionDrugs_segmentSplitClean)

    print("Compiling positive interaction drugs...")
    interactionsPos = append_lists(DRUGS, interactionsPosDrugs_segmentSplitClean)
    # print("Interactions Pos: ", interactionsPos)

    print("Compiling negative interaction drugs...")
    interactionsNeg = append_lists(DRUGS, interactionsNegDrugs_segmentSplitClean)



    # removes duplicates from array of active substances, i.e. if it contains 'cyp3a4 inhibitor' and 'inhibitor' it will leave only 'cyp3a4 inhibitor'.
    INTERACTIONS = []

    for i in DRUGS:
        if i in interactionsPos_segmentSplitClean:
            if i not in interactionsPos:
                if i not in interactionsNeg:
                    interactionsPos.append(i)

    for i in interactionsPos:
        if i not in interactionsNeg:
            if i not in INTERACTIONS:
                if i not in ACTIVESUBSTANCES:
                    INTERACTIONS.append(i)

    CAUTIONS = []

    for i in cautionsClasses:
        original = [key for (key, value) in class_synonyms.items() if i in value]
        if len(original) >= 1:
            if original[0] not in CAUTIONS:
                if original[0] not in CLASSESPOSNEG:
                    CAUTIONS.append(original[0])
        original2 = [key for key in class_synonyms.keys() if i == key]
        if len(original2) >= 1:
            if original2[0] not in CAUTIONS:
                if original2[0] not in CLASSESPOSNEG:
                    CAUTIONS.append(original2[0])

    for i in cautionsDrugs:
        if i in DRUGS:
            if i not in CAUTIONS:
                if i not in INTERACTIONS:
                    if i not in ACTIVESUBSTANCES:
                        CAUTIONS.append(i)

    INTERACTIONS_NEW = [x for i, x in enumerate(INTERACTIONS) if
                        all(x not in y for j, y in enumerate(INTERACTIONS) if i != j)]
    ACTIVESUBSTANCES_NEW = [x for i, x in enumerate(ACTIVESUBSTANCES) if
                        all(x not in y for j, y in enumerate(ACTIVESUBSTANCES) if i != j)]
    CLASSESPOSNEG_NEW = [x for i, x in enumerate(CLASSESPOSNEG) if
                        all(x not in y for j, y in enumerate(CLASSESPOSNEG) if i != j)]
    CAUTIONS_NEW = [x for i, x in enumerate(CAUTIONS) if
                        all(x not in y for j, y in enumerate(CAUTIONS) if i != j)]
    if "excipient" in segmentOne:
        ACTIVEEXCIPIENTS_NEW = [x for i, x in enumerate(ACTIVEEXCIPIENTS) if
                    all(x not in y for j, y in enumerate(ACTIVEEXCIPIENTS) if i != j)]


    for i in CLASSESPOSNEG:
        if i not in CLASSESPOSNEG_NEW:
            if i in DRUGS:
                CLASSESPOSNEG_NEW.append(i)
    drugDictionary["SMPC NAME"] = PDF_Path
    drugDictionary["BRAND NAME"] = BRANDNAME
    drugDictionary["ACTIVE SUBSTANCE(S)"] = ACTIVESUBSTANCES_NEW
    if "excipient" in segmentOne:
        if len(ACTIVEEXCIPIENTS_NEW) >= 1:
            drugDictionary["ACTIVE EXCIPIENT(S)"] = ACTIVEEXCIPIENTS_NEW

    drugDictionary["FORMULATION"] = FORMULATION
    drugDictionary["INTERACTIVE DRUG CLASSES"] = CLASSESPOSNEG_NEW
    drugDictionary["INTERACTIVE DRUGS"] = INTERACTIONS_NEW
    drugDictionary["CAUTIONS"] = CAUTIONS_NEW


    # print("\nBRAND NAME: ", BRANDNAME)
    # print("FORMULATION(S): ", FORMULATION)
    # print("ACTIVE SUBSTANCE(S): ", ACTIVESUBSTANCES)
    # if len(ACTIVEEXCIPIENTS) >= 1:
    #     print("ACTIVE EXCIPIENT(S): ", ACTIVEEXCIPIENTS)
    # print("CLASS INTERACTION(S): ", CLASSES)
    # print("DRUG INTERACTION(S): ", INTERACTIONS)


    print("SmPC Complete!")

    print("FINAL DICTIONARY:\n")
    print(drugDictionary)

AI("/Volumes/HARRISDRIVE/Dosewolf PDF Database/Ciclosporin.pdf")