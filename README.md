# dnd-calculator
I was discussing with a friend various strengths and weaknesses of feats and class features found in Dungeons and Dragons 5th edition classes, but did not like the "rough" estimates that we were conducting. Thus, I built a python script that will run simulations of various classes, class features, feats, weapons, etc.

# Libraries used
pandas, numpy, matplotlib, pyMongo, flask, random, time, os

# Usage
Supports a little bit of multiclass (two classes), various weapons of rarity 0 to +3, several fighting styles and feats, Dual-Wield (assumes the same weapon in both hands), % of attacks you will expect to have advantage, and the ability to change the number of rounds per fight, number of short rests per long rest (assumes 1 fight between each short rest), and number of iterations. 

It then graphs the resulting DPR averages vs AC on a chart with any prior simulations run.

![Example page](./readme_figs/example.png)