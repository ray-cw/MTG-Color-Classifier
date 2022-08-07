## Introduction

On August 5th, 1993, Wizards of the Coast released the first set of Magic: The Gathering, *Limited Edition Alpha*. This then unknown card game began with 295 cards. Today, it is one of the most popular trading card games, right up there with Yugioh and Pokemon TCG, with a cardbase exceeding 24,000 unique entries. 

In Magic, you the player are a 'planeswalker' (in layman terms, think of yourself as a spellcaster), your deck represents your spellbook, and the individual cards represent different spells. Each card contains a various bits of information: what your spell does, what it costs to cast it, the type of spell it is, et cetera. In this project, we will be looking at these features and fit them to a classification model, to determine our dependant: the color identity of the card.

### What do we mean by 'color identity'?

<div style="text-align: left; display: inline-block; margin-top: 1.5em;">
<img src="assets/fivecolors.jpg" style="height: 50px" >
</div>

There are 5 colors in MTG. We can also consider the absence of any color to be a 6th color identity. Cards with the same color identity will have similar themes, such as similar keywords. Cards can also be of multiple color identities. The aim of this project will be to train a model to recognize these patterns in the card's description, and other provided independants, to classify the card accordingly.

### The Dataset

I have obtained a dataset of all unique cards (up to July 8) from [MTGJSON.com](https://mtgjson.com).

### Writeup

If you are interested in learning more behind the process that went into this project, I encourage you to checkout my full write up at [my website](https://ray-cw.github.io).

### Demo

A demo of how my model works can be accessed at [this link](https://ray-cw-mtg-color-classifier-app-i4ciqj.streamlitapp.com/) so please check it out if you are curious.