We present the IR Anthology, a corpus of information retrieval publications accessible via a metadata browser and a full-text searchengine. Following the example of the well-known **[ACL Anthology](https://www.aclweb.org/anthology/)**, the IR Anthology serves as a hub for researchers interested in information retrieval.

This repository contains the code for the build of the static website. To deploy the website you need to extract the meta data first. 

To build the IR Anthology follow these steps:
```bash
git clone https://github.com/ir-anthology/ir-anthology.git
cd ir-anthology/devops-scripts
make real-data anthology local-server
```
A more detailed description is provided  in the README.MD [here](https://github.com/ir-anthology/ir-anthology/tree/master/devops-scripts/).
## Credits

The IR Anthology is a grassroots initative run entirely by contributions from volunteers.
The project has been initiated by the [Webis Group](https://webis.de/).

### Active Volunteers

+ Janek Bevendorff (Bauhaus-Universität Weimar)
+ Jan Philipp Bittner (Martin-Luther-Universität Halle-Wittenberg)
+ Alexander Bondarenko (Martin-Luther-Universität Halle-Wittenberg)
+ Maik Fröbe (Martin-Luther-Universität Halle-Wittenberg)
+ Sebastian Günther (Martin-Luther-Universität Halle-Wittenberg)
+ Christian Kahmann (Leipzig University)
+ Andreas Niekler (Leipzig University)
+ Michael Völske (Bauhaus-Universität Weimar)

### Directors

+ Martin Potthast (Leipzig University)
+ Matthias Hagen (Martin-Luther-Universität Halle-Wittenberg)
+ Benno Stein (Bauhaus-Universität Weimar)

### Donors

Contributions from the IR community and beyond are welcome.

### Sponsors

We welcome sponsorships to support future maintenance, development, and improvement of the IR Anthology. Please get in touch.

### Special Thanks

Thanks to the **[dblp](https://dblp.uni-trier.de/)** computer science bibliography for providing their curated dataset as open data. It serves as the primary data source for the meta information of this project.

Thanks to the **[ACL Anthology](https://www.aclweb.org/anthology/)** for releasing their software stack to build the ACL Anthology website, which we adapted to build the IR Anthology.
