# Docker
This guide assumes that you are in the docker group. If you are not, then you might want to replace `docker` with `sudo docker`
## Build once
If you just want to build the anthology once, then you can just start an interactive container. Open a shell on the host. 
```bash
docker run -it --rm -p 8000:8000 ubuntu:20.04 bash
```
Then follow the instructions in the [README](https://github.com/ir-anthology/ir-anthology/blob/master/README.md).

### Common errors

The docker image of `ubuntu:20.04` is stripped of the apt cache, which means that no `apt-get install <something>` commands can be executed. This results in the error `<package> not found`. This can be fixed by running `apt-get update`.

- `make` might not be installed.
- If the error `/bin/bash: venv/bin/activate: No such file or directory` happens, delete the directory `venv` and rerun the commands.
- You might encounter `failed building 'bdist_wheel'`. (See also: [What is the meaning of "Failed building wheel for X" in pip install?](https://stackoverflow.com/questions/53204916/what-is-the-meaning-of-failed-building-wheel-for-x-in-pip-install) on stackoverflow.) I could it fix by installing they python3 package `wheel` manually. I used the command `python3 -m pip install wheel`.


## For developers
This is just one way how you could setup a development environment to rapidly build the entire ir-anthology.

First, we create a daemon process in docker, so that we do not have to setup everything again. (You could alternativly create a docker image, but that is not what we are goind to do here.)
The following command will:
- create a detached docker process, thus creating an container that runs until it is stoped by docker or some higher process
- map your local port 8000 to the port 8000 inside the docker container
- mount your current working folder (which is assumed to be the ir-anthology folder) into the container at /ir-anthology
- assign the name `ir-anthology-dev` to the container
- the options `-d` and `--rm` simultanously cause the container to be deleted when the daemon exits (which happens e.g. when the host computer shuts down). I found it convenient to remove both options to use the same docker container over multiple sessions. In the new session, the container can be restarted using `docker start ir-anthology-dev`

Run this command from within the `ir-anthology` folder to make it a shared directory (to be found as `/ir-anthology` in the docker).

```bash
docker run -d --rm -it -p 8000:8000 -v $(pwd):/ir-anthology --name ir-anthology-dev ubuntu:20.04 bash -c "tail -f /dev/null"
```



### Spawning new shell inside the container
Now you can run as many additional commands in that container. Try it. Spawn a new shell inside the container:

```bash
docker exec -it ir-anthology-dev bash
```

Then create a file at /tmp and exit the shell.
```bash
ls /tmp
echo "test" > /tmp/test
exit
```

Spawn a new shell inside the container: 
```bash
docker exec -it ir-anthology-dev bash
```
And read the content of the just created file and exit:
```bash
ls /tmp
cat /tmp/test
exit
```
### Setup the container
If you don't already have one spawn a shell inside the container (see above) and install the dependencies.
```bash
apt-get update
apt-get install -y hugo python3-pip python3-venv wget git
```

### Building your code

The direction `/ir-anthology/` is shared between the host and the docker container.

Therefore the user inside the container will mostlikely have a different userid than you on the host. This can cause problems with file permission.

I found it most convinient to copy the entire anthology folder from `/ir-anthology` to `/tmp/ir-anthology` and build there.
(Inside the container, see above if you don't you how to spawn a shell inside the container.)

```bash
cp -rf /ir-anthology /tmp/
cd /tmp/ir-anthology
make site serve
```

### Results

- The html files of the site are generated into `ir-anthology/build/anthology`. In this directory, `python3 -m http.server` is run during `make serve`.

### Opening the site

Open `localhost:8000/anthology` in a browser to see the site. Note that `localhost:8000` redirects to `ir.webis.de/anthology` and is *not* the local instance.

### Advanced: Not redownloading every build.

Run `make <your_targets> DOWNLOAD=false`.

Note that when you want to download again (a different .bib file) `make` might think the file is new, so doesn't need to be replaced. Force the target `sampledata` or `data` to be run by using the flag `-B`. (`make -B data`)


### Advanced: Manually switching between different .bib files
Redownload manually by either undoing the changes or running `make clean` and afterwards putting your new `.bib` file in `data/` and rename it to `ir-anthology.bib`.

### Advanced: Hugo only build
You might find yourself in a situation where you only made changes to the hugo folder. In that case you can build anthology once like it is described in the previous section. For all subsequent alterations you run `make hugo_only`.

### Advanced: Using the sample .bib
There is a smaller file, the `minimal-sample.bib`. Use it by:

1. Follow the steps in "Advanced: Not redownloading every build" (This is necessary! Otherwise all your changes will be undone during a `make site`.)
2. If having build before with a different `.bib` file, run `make clean`
3. Run `make sampledata`. This will download the sampledata bib file
4. Run `make site` to build everything.
5. Run `make serve` so you can visit the page in your browser.

(Tip: You can run steps 2-5 using `make clean sampledata site serve`.)
