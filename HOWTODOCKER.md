# Docker
This guide assumes that you are in the docker group. If you are not, then you might want to replace `docker` with `sudo docker`
## Build once
If you just want to build the anthology once, then you can just start an interactive container. Open a shell on the host. 
```bash
docker run -it --rm -p 8000:8000 ubuntu:20.04 bash
```
Then follow the instructions in the [README](https://github.com/ir-anthology/ir-anthology/blob/master/README.md).

## For developers
This is just one way how you could setup a development environment to rapidly build the entire ir-anthology.

First, we create a daemon process in docker, so that we do not have to setup everything again. (You could alternativly create a docker image, but that is not what we are goind to do here.)
The following command will:
- create a detached docker process, thus creating an container that runs until it is stoped by docker or some higher process
- map your local port 8000 to the port 8000 inside the docker container
- mount your current working folder (which is assumed to be the ir-anthology folder) into the container at /ir-anthology
- assign the name `ir-anthology-dev` to the container
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
apt-get install -y hugo python3-pip python3-venv wget git
```

### Building your code
The user inside the container will mostlikely have a different userid than you on the host. This can cause problems with file permission. I found it most convinient to copy the entire anthology folder from `/ir-anthology` to `/tmp/ir-anthology` and build there.
(Inside the container, see above if you don't you how to spawn a shell inside the container.)

```bash
cp -rf /ir-anthology/* /tmp/ir-anthology
cd /tmp/ir-anthology
make site serve
```

### Advanced: Partial builds
You might find yourself in a situation where you only made changes to the hugo folder. In that case you can build anthology once like it is described in the previous section. For all subsequent alterations you copy the anthology from the mount to the tmp folder, like before. Then open `/tmp/ir-anthology/Makefile` in your prefered editor and comment out the following lines: (caution: exact positions might differ, always compare the code) 
https://github.com/ir-anthology/ir-anthology/blob/989f63184cd8ff345db7c09e6cd51fa4b5921637/Makefile#L132-L133
https://github.com/ir-anthology/ir-anthology/blob/989f63184cd8ff345db7c09e6cd51fa4b5921637/Makefile#L139-L142
