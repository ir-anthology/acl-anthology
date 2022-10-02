#Shared Tasks

###what's shared task
A shared task is a task given by somebody at a conference, where everybody
can participate and try to solve the given task. This is kinda like kaggle
challenges, where the answers aren't known and there might not be the 
optimal solution.


###Data structure:
Our shared tasks are sorted by year, conference (in wich they originated) and then
by task
```
{
  "2020": {
    "conferences":[
      {
        "id":"clef",
        "label":"CLEF",
        "tasks":[
          {
            "id":"arqmath",
            "label":"ARQMath",
            "overviewpapers":[
              "zanibbi-2020-overview"
             ],
            "sharedtasks":[
              "Find Answers",
              "Formula Search"
            ],
            "participantpapers":[
              "dadure-2020-analysis",
              "mansouri-2020-dprl",
              "ng-2020-dowsing",
              "novotny-2020-three",
              "rohatgi-2020-psu",
              "scharpf-2020-arqmath"
            ]
          },
        ...],
      },
    ...]
    },
  ...
}
```
###Problems and stuff

Currently, new years need to be manually added to the index.html in line 98.  
```{{ $allyears := seq 2020 -1 2020}}```

####Names
All names have been split into labels and ids. Label is just the name and ids are the names.to_lower() without special characters.
Those are important/used for urls, etc...

####Tasknames   
Tasknames are currently given by the responsible conference.
These are most of the time not really descriptive.
Sometimes using the tasks own website provides better ones.

####_index.md  
As one might notice, most of the other parts (like events, papers, people,...)
have an _index.md for hugo that gets used for listing. Shared tasks doesn´t, because it raises 
an "index of untyped nil". Not sure why, but because we don´t need the file, that´s the reason,
why it´s not there.


###Paper

Papers are linked using their bibTeX - Keys.  
To get them, search for the paper on the IR-Anthology.  
Example:  
https://ir.webis.de/anthology/2018.coria_conference-2018.3/
```
@inproceedings{lamercerie-2018-analyse,
  crossref = {DBLP:conf/coria/2018},
  author    = {Aur{\'{e}}lien Lamercerie},
  editor    = {Josiane Mothe and
               Peggy Cellier and
               Anne{-}Laure Ligozat},
  title     = {Analyse formelle d'exigences en langue naturelle pour la conception
               de syst{\`{e}}mes cyber-physiques},
  booktitle = {COnf{\'{e}}rence en Recherche d'Informations et Applications - {CORIA}
               2018, 15th French Information Retrieval Conference, Rennes, France,
               May 16-18, 2018. Proceedings},
  publisher = {{ARIA}},
  year      = {2018},
  url       = {https://doi.org/10.24348/coria.2018.RJCpaper6},
  doi       = {10.24348/coria.2018.RJCpaper6},
  timestamp = {Fri, 29 Mar 2019 10:41:32 +0100},
  biburl    = {https://dblp.org/rec/conf/coria/Lamercerie18.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
BibTeX - Key: **lamercerie-2018-analyse**

The idmap.json in the data folder maps these keys to their Anthology-ID,
because both of those get created when building the Anthology.

To find participantpaper maybe visit http://ceur-ws.org/  
There is also a python script to automatically get them in the ir-anthology-data repository

##