# LEXIGRAPH

Lexigraph is a full-stack thesaurus-based vocabulary building application. 

The application displays lexical relationships between a new word and its synonyms (as pertained to each part-of-speech definition) to aid vocabulary learning. In other words, users can comprehend new words through familar ones. To achieve this, the application utilizes WordNet API from NLTK and visualizes lexical connections between a search word its synonyms as a graph. Users can interact with the graph to indicate known words and unknowns. In the meantime, a cluster algorithm in the backend partitions a vocabulary space (Google's Web Trillion Word Corpus) based on distribution of known words and assign each cluster an estimated known probability. Using these probability assignment, the application will automatically highlight "known" synonyms in all subsequent search visulization.

This is a three-week capstone project for CMU 15112: Fundamentals of Programming and Computer Science, Fall 2018, implemented entirely in python.

## Menu
![](/demo/gif/00_menu.gif)

## Looking Up A New Word
![](/demo/gif/01_search_def.gif)

## Interact to Indicate Word Familiarity
![](/demo/gif/02_search_highlight.gif)
![](/demo/gif/03_search_dehilight.gif)

## Automatic Word Recommendation
![](/demo/gif/04_search_autohighlight.gif)

## Conventional Dictionary View
![](/demo/gif/05_dict.gif)

## Get The Latest Usage from The Web
![](/demo/gif/06_explore.gif)

## Paring Game to Strenthen Retention
![](/demo/gif/07_pair.gif)

## Review Learned Words
![](/demo/gif/08_archive.gif)

## Backend Cluster Algorithm
![](/demo/gif/09_backend.gif)
