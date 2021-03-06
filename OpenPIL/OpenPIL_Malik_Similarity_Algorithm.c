//#ifdef _WIN32
//#   define API __declspec(dllexport)
//#else
//#   define API
//#endif

//The "Ahmed-Similarity Algorithm" - a measure of similarity between two string vectors, taking into account the following parameters: matching characters between strings and the distance between them and the quantity and distances of same-character occurence, providing a value between 0 and 1. Three vector values between 0 and 1 are calculated using the following string-distance algorithms: jaro-winkler (v1), ratcliff-overshelp (v2) and sorensen-dice (v3); these are then averaged to return a double value e.g. 0.95 is 95% similar. For class-similarity, the string will only be sent back to the python script if it attains a Ahmed-score of >0.91 (more than 91% similar); for drug-similarity, the string will only be sent back if it attains a Ahmed-score >0.94 (more than 94% similar).


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define SCALING_FACTOR 0.1
#include <ctype.h>
#include <time.h>

//https://github.com/miguelvps/c/blob/master/jarowinkler.c
static int max(int x, int y) {
    return x > y ? x : y;
}

static int min(int x, int y) {
    return x < y ? x : y;
}

double jaro_winkler_distance(const char *s, const char *a) {
    int i, j, l;
    int m = 0, t = 0;
    int sl = strlen(s);
    int al = strlen(a);
    int sflags[sl], aflags[al];
    int range = max(0, max(sl, al) / 2 - 1);
    double dw;

    if (!sl || !al)
        return 0.0;

    for (i = 0; i < al; i++)
        aflags[i] = 0;

    for (i = 0; i < sl; i++)
        sflags[i] = 0;

    /* calculate matching characters */
    for (i = 0; i < al; i++) {
        for (j = max(i - range, 0), l = min(i + range + 1, sl); j < l; j++) {
            if (a[i] == s[j] && !sflags[j]) {
                sflags[j] = 1;
                aflags[i] = 1;
                m++;
                break;
            }
        }
    }

    if (!m)
        return 0.0;

    /* calculate character transpositions */
    l = 0;
    for (i = 0; i < al; i++) {
        if (aflags[i] == 1) {
            for (j = l; j < sl; j++) {
                if (sflags[j] == 1) {
                    l = j + 1;
                    break;
                }
            }
            if (a[i] != s[j])
                t++;
        }
    }
    t /= 2;

    /* Jaro distance */
    dw = (((double)m / sl) + ((double)m / al) + ((double)(m - t) / m)) / 3.0;

    /* calculate common string prefix up to 4 chars */
    l = 0;
    for (i = 0; i < min(min(sl, al), 4); i++)
        if (s[i] == a[i])
            l++;

    /* Jaro-Winkler distance */
    dw = dw + (l * SCALING_FACTOR * (1 - dw));

    return dw;
}
//https://github.com/miguelvps/c/blob/master/jarowinkler.c










//https://github.com/wernsey/miscsrc/blob/master/simil.c
static int rsimil (const char *a, int alen, const char *b, int blen, int cs);

/*
 *	Case insensitive version of simil().
 *	It copies the strings internally using strdup(), converts the copies
 *	to uppercase, and compares those.
 *	It returns the same values as simil(), but it may also return zero if
 *	the calls to strdup() fail.
 */
int ratcliff_obershelp_distance(const char *a, const char *b)
{
  int alen, blen;

  alen = strlen (a);
  blen = strlen (b);

  if (alen == 0 || blen == 0)
    return 0;

  return ( (rsimil (a, alen, b, blen, 0) * 200) / (alen + blen) );

}

/*
 *	This is the core of the algorithm. It finds the longest matching substring
 *	and then recursively matches the left and right remaining strings.
 *	cs - Case sensitive
 */
static int
rsimil (const char *a, int alen, const char *b, int blen, int cs)
{
  int i, j, k, l, p = 0, q = 0, len = 0, left = 0, right = 0;

  /* Find a matching substring */
  for (i = 0; i < alen - len; i++)
    for (j = 0; j < blen - len; j++)
		{
			if(cs)
			{
				if (a[i] == b[j] && a[i + len] == b[j + len])
				{
					/* Find out whether this is the longest match */
					for (k = i + 1, l = j + 1; a[k] == b[l] && k < alen && l < blen; k++, l++);

					if (k - i > len)
					{
						p = i;
						q = j;
						len = k - i;
					}
				}
			} else {
				if (tolower(a[i]) == tolower(b[j]) && tolower(a[i + len]) == tolower(b[j + len]))
				{
					/* Find out whether this is the longest match */
					for (k = i + 1, l = j + 1; tolower(a[k]) == tolower(b[l]) && k < alen && l < blen; k++, l++);

					if (k - i > len)
					{
						p = i;
						q = j;
						len = k - i;
					}
				}
			}
		}

  /* No match */
  if (len == 0)
    return 0;

  /* Match the strings to the left */
  if (p != 0 && q != 0)
    left = rsimil (a, p, b, q, cs);

  i = (p + len);
  alen -= i;
  j = (q + len);
  blen -= j;

  /* Match the strings to the right */
  if (alen != 0 && blen != 0)
    right = rsimil (a + i, alen, b + j, blen, cs);

  /* Return the score */
  return len + left + right;
}
//https://github.com/wernsey/miscsrc/blob/master/simil.c



//There were no online resources of sorensen dice coefficient algorithms written in C online which were copyright-free, so I (Malik Ahmed) wrote the below. I establish it under CC0 license (public domain) incase someone else needs it. You don't have to, but if you could please link to OpenPIL if you use it, that would be appreciated, as it could help us expand and grow the open source project.

double malik_sorensen_dice_string_algorithm(const char *a, const char *b) {
    
    //strcmpi returns 0 if the strings are the same, and 1 if they are different.
//    int sameZero = strcmp(a, b);
    
    //checks if the words are exactly identical, if they are returns one value.
    if (a == b) {
        return 1;
    }
    //checks if either of the words are empty. if they are, then the comparison results in a zero value.
    if (a[0] == '\0') {
        return 0;
    }
    if (b[0] == '\0') {
        return 0;
    }
    
    //if both strings they are not the same, and one of them is a single character long, then it cannot be a match, so returns a zero value.
    size_t aLength = strlen(a);
    size_t bLength = strlen(b);
    
    if ((aLength == 1 || bLength == 1)) {
        return 0;
    }

    //count the number of bigrams (two-character matches) between the two strings:

    
    size_t aMinusOne = aLength - 1;
    size_t bMinusOne = bLength - 1;

    int aMinusOneInt = aLength - 1;
    int bMinusOneInt = bLength - 1;


    const char *bigramsA[aMinusOneInt];
    const char *bigramsB[bMinusOneInt];


    int i = 0;
    while (i < aMinusOne) {
        char tempA[3] = { a[i], a[i + 1], '\0' };
        bigramsA[i] = tempA;
        i++;
    }
    
    int j = 0;
    while (j < aMinusOne) {
        char tempB[3] = { a[i], a[i + 1], '\0' };
        bigramsB[j] = tempB;
        j++;
    }
    
    
    int z = 0;
    double bigramsN = 0;

    while (z < aLength && z < bLength) {
        int biCompare = strcmp(bigramsA[z], bigramsB[z]);
        if (biCompare == 0) {
            bigramsN += 1;
        }
        z++;
    }


    return (2*bigramsN) / (aMinusOne + bMinusOne);
        
 
}



//OpenPILAI Algorithm:
double similarity(const char *i, const char *j)
{
    double vx = malik_sorensen_dice_string_algorithm(i, j);
    double vy = jaro_winkler_distance(i, j);
    double vz = ((ratcliff_obershelp_distance(i, j))*1.0)/100;
    double v = (vx + vy + vz)/3;
    return v;
}

//char** mainForLoop(const char ** drug_names, const char ** combo) {
////    static char ** matches[25];
//    static char matches[10];
////    char ** matches = malloc(100 * sizeof(char*));
//    size_t i = 0;
//    size_t j = 0;
//    for (i = 0; i < sizeof(drug_names)/sizeof(drug_names[0]); i++) {
//        for (j = 0; j < sizeof(combo)/sizeof(combo); j++) {
//            double v = similarity(drug_names[i], combo[j]);
//            if (v > 0.72) {
//                strcpy(matches, drug_names[i]);
//            }
//        }
//    }
//    return matches;
//}

//#include <stdio.h>
//#include <stdlib.h>
//#include <string.h>
//#include <time.h>
//
//
//void free_list(char** list, size_t size) {
//    for(size_t i = 0; i < size; ++i) if (list[i]) free(list[i]);
//    free(list);
//}
//
//char ** append_lists(const char ** PyOne, const char ** PyTwo, size_t sizeOne, size_t sizeTwo) {
//    size_t i = 0;
//    size_t j = 0;
//
//    // Allocate an array of N string pointers where N is the size of PyOne
//    char ** matches = malloc(sizeOne * sizeof(char *));
//    // The temporary buffer
//    char temp[100] = {0};
//
//    for (i = 0; i < sizeOne; i++) {
//        // Cleared on each pass
//        temp[0] = 0;
//        for (j = 0; j < sizeTwo; j++) {
//            double v = similarity(PyOne[i], PyTwo[j]);
//            if (v > 4) {
//                // Works with the temp buffer
//                strcat(temp, (PyOne[i]));
//                strcat(temp, (";"));
//                int size = strlen(temp) + 1; //+1 for null termination
//
//                // Then allocates a string of the right size
//                char * str = malloc(size);
//                memcpy(str, temp, size);
//                str[size-1] = 0; //Null termination
//
//                // And collects it
//                matches[i] = str;
//            }
//        }
//    }
//    return matches;
//    free_list(matches, sizeOne);
//}


#include <stdlib.h>
#include <string.h>

char** append_lists(const char** list1, size_t size1, const char** list2, size_t size2, size_t* pSize) {
    char** total = malloc((20000) * sizeof(char*));
    size_t arrayCount = 0;
    for(size_t i = 0; i < size1; ++i) {
        for(size_t j = 0; j < size2; ++j) {
            double v = similarity(list1[i], list2[j]);
            if (v > 0.94) {
                total[arrayCount] = strdup(list1[i]);
                arrayCount++;
            }
        }
    }
    *pSize = arrayCount;
    return total;
}

char** append_lists_classes(const char** list1, size_t size1, const char** list2, size_t size2, size_t* pSize) {
    char** total = malloc((100) * sizeof(char*));
    size_t arrayCount = 0;
    for(size_t i = 0; i < size1; ++i) {
        for(size_t j = 0; j < size2; ++j) {
            double v = similarity(list1[i], list2[j]);
            if (v > 0.91) {
                total[arrayCount] = strdup(list1[i]);
                arrayCount++;
            }
        }
    }
    *pSize = arrayCount;
    return total;
}

void free_list(char** list, size_t size) {
    for(size_t i = 0; i < size; ++i)
        free(list[i]);
    free(list);
}




