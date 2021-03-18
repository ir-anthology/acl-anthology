## How to run and develop the IR Anthology:
You need:
- docker
- make
- bash
- an internet connection (to pull the data)

This folder contains a Makefile which has several targets. The targets will be explained one by one.

The builder reads the data directory in the root direcoty of the repository. Different targets make sure that this direcotry exists and that it contains the desired data.

- **example-data** creates a symlink from `../data` to the directory `example-data`
- **real-data**  if the real-data has not been compiled yet it downloads the necessary code, compiles the data from source and stores it into `.cache`. symlinks `../data` to the `.cache/real-data` folder.
- **anthology** builds the anthology using the data in the directory `../data`. the result is stored in `.cache/ir-anthology.github.io`
- **local-server** serves the files in `.cache/ir-anthology.github.io` on localhost:8000
- **clean** removes the `.cache` folder and all created images
- **quick** runs the targets example-data anthology local-server
- **deploy** runs the targets real-data anthology and then commits and pushed the changes in `.cache/ir-anthology.github.io`

#### data independent layout changes
If you make data independent layout changes, then ```make quick``` should cover your needs. You can always add files to the example-data to cover special cases. 

#### run local with real-data
Before you push changes you should always have a look at the produced site with the real-data. Run 
```
make clean real-data anthology local-server
```

#### deploy
You can push changes by running:
```
make deploy
```
