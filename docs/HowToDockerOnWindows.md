# __How to build IR-Anthology on Windows__

  

___

  

## __What you need to do:__

__1.__ Install `Docker Desktop` [Link](https://www.docker.com/products/docker-desktop/)

__2.__ Install `wsl 2` with your administration account on a commandline or Powershell (which you prefer)

### __Problems that can come up:__

__1.__  `Ubuntu 20.04` (or other Version) button must be on

----> open `Docker Desktop`-> Settings-> Resources-> Ubuntu-20-04 -> on
  __2.__ It's importend to do the `wsl` installation with your administration profile

----> __Input:__  ```wsl.exe --set-version Ubuntu-20.04 2```

*  __2.1__ still wsl 1 even if you tiped the input from point 2?

----> __Input:__  ```wsl --set-default-version 2```

  

### **Next Step:**

Pull the IR-Anthology Git

  

#### __STEPS:__

* Create folder in a desired place

* Give the folder a specific name like 'IR_Anthology'

* click on the folder

* click on the path that shows you how to get to the folder, mark it and tipe `cmd`(Opens the commandline with the needed path)

#### __Git__

*  `git status` shows working tree status

*  `git pull` ir-anthology and ir-anthology data 
	* copy the links from the Git
		* __ir-anthology [Link](https://github.com/ir-anthology/ir-anthology):__-> click on `Code`and copy the HTTPS-Link
		* __ir-anthology data [Link](https://github.com/ir-anthology/ir-anthology-data):__ -> click on `Code`and copy the HTTPS-Link

  

#### __How to push? (Git)__

* `git add` 'what you need and changed'

__Example:__ ```git add shared-tasks.json```

* `git commit -m "message"`

__Example:__ ``` "shared-tasks updated"```

* `git push`

__->__ Now you pushed the git

  

### __How to Build?__

+ click into the downloaded `ir-anthology` folder and copy the path, mark it and tipe `wsl` (click Enter) 
	+ commandline should open with your rootname and the path to ir-anthology -> you are in docker
----> __Input:__ ```docker build -t ir-anthology-docker .```

----> __Input:__  ```docker run -v $(pwd):/anthology -v $(pwd)/../ir-anthology-data:/anthology-data -it --rm -p 8000:8000 ir-anthology-docker```

  

#### __After everything is downloaded:__

*  ```cd tmp``` (a folder where you can work without destroying anythong)

----> with ```ls``` You can see whats inside

__should see:__ ```hugo_cache ir-anthology```

*  ```cd ir-anthology```

----> ```ls```

__should see:__```Makefile bin build data hugo venv```

*  ```cd build ```

__should see:__ ```404.html anthology assets config.toml content data data-export index.html layouts resources static```

-  __Input:__  ```python3 -m http.server```

  

Go to your Browser and write: `localhost8000/anthology`

  

__Now you should see the the IR-Anthology-Website!__

    