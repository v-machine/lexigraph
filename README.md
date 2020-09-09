# LEXIGRAPH

Lexigraph is a full-stack thesaurus-based vocabulary building application. 

The application displays lexical relationships between a new word and its synonyms (as pertained to each part-of-speech definition) to aid vocabulary learning. In other words, users can comprehend new words through familar ones. To achieve this, the application utilizes WordNet API from NLTK and visualizes lexical connections between a search word its synonyms as a graph. Users can interact with the graph to indicate known words and unknowns. In the meantime, a cluster algorithm in the backend partitions a vocabulary space (Google's Web Trillion Word Corpus) based on distribution of known words and assign each cluster an estimated known probability. Using these probability assignment, the application will automatically highlight "known" synonyms in all subsequent search visulization.

This is a three-week capstone project for CMU 15112: Fundamentals of Programming and Computer Science, Fall 2018, implemented entirely in python.

## Menu
In the main interface, users can choose the following modes to interact with new vocabularies.
LEXIGRAPH: visulizes the lexical relationships between a vocabulary and its synonyms.
explore: get the latest usage from Marriam Webster
search: look up a new word and return result as a lexigraph
dictionary: conventional dictionary definition provided by WordNet
pair: timed paring game for learned synonyms
archive: find all previously searched vocabularies

![](/demo/gif/00_menu.gif)

## Looking Up A New Word
Type in a word in the search mode to obtain a lexigraph. The synonyms are organized by search word's part-of-speech (POS) tags. Hover over each POS tag to see definitions.
![](/demo/gif/01_search_def.gif)

## Interact to Indicate Word Familiarity
Click to add (highlight) or subtract (unhighlight) synonyms to indicate whether a word is known or otherwise. Lexigraph will remember words indicated as familar or unfamiliar by the user.
![](/demo/gif/02_search_highlight.gif)
![](/demo/gif/03_search_dehilight.gif)

## Automatic Word Recommendation
Based on real-time user interactions, the application estimate words that are likely to be known by users and automatically recommend (highlight) them in subsequent searches.
![](/demo/gif/04_search_autohighlight.gif)

## Conventional Dictionary View
Allows for conventional display of dictionary definitions. 
![](/demo/gif/05_dict.gif)

## Get The Latest Usage from The Web
To get the latest example usage from Marriam Webster. 
![](/demo/gif/06_explore.gif)

## Paring Game to Strenthen Retention
This is a timed paring game in which users are tasked to pair new vocabularies with known synonyms. 
![](/demo/gif/07_pair.gif)

## Review Learned Words
All previously searched words is stored in the archive for easy retrieval.
![](/demo/gif/08_archive.gif)

## Backend Cluster Algorithm
a cluster algorithm in the backend partitions a vocabulary space (Google's Web Trillion Word Corpus) based on distribution of known words and assign each cluster an estimated known probability. 
![](/demo/gif/09_backend.gif)
