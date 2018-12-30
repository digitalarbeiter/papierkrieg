# Papierkrieg

THIS IS WORK IN PROGRESS. AND BY NO MEANS READY FOR PRODUCTION.
NOT EVEN CLOSE. IN FACT, PROJECT'S IN ITS INFANCY.

I envision project "Papierkrieg" to be a toolkit for managing the red-tape
workload, organizing the incoming flood of letters from banks, insurance
companies, pension fonds, health service, tax stuff etc.

## Vision

Scan any incoming paper mail and push it through an OCR and spell checker,
then have some machine learning models date and classify it ("tax", "car",
etc). Put it in an index to make it searchable and filterable. Provide a
nice web frontend.

Papierkrieg should also provide fetching mechanisms for web pages or mail
like phone bills, electronic paychecks etc.

## Status and Plans

This is all utterly experimental. The third party tools (Tesseract for OCR,
SOLR for search, the spell checker, the machine learning, etc) are all
still being evaluated.

Tesseract seems to work okay but produces quite some spelling errors.

The spell checkers I've tried are utterly not up to the task. Their
suggestions are ridiculously bad, with Levenshtein distances approaching
what must be damn close to infinity. I'll need a custom spell checker.
Currently experimenting with Peter Norvig's approach of an a priori plus
limited Levenshtein algorithm: https://www.norvig.com/spell-correct.html

I have yet to think of how I want to train the classifiers, or even what
tags (classes) I want to assign. SOLR comes with its own classification
features, kNN and Naive Bayes. But for a start I think I'll use scikit.learn
and its linear support vector machine, because I find it easier to actually
understand the models. Maybe I'll switch to something Neural later.

