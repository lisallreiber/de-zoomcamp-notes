
## Linux

Here we'll show you how to install Spark 3.3.2 for Linux.
We tested it on Ubuntu 20.04 (also WSL), but it should work
for other Linux distros as well


### Installing Java

Download OpenJDK 17 or Oracle JDK 17 (from: 2023-03-02)

We'll use [OpenJDK](https://jdk.java.net/archive/)

Download it (e.g. to `~/spark`):

```bash
mkdir spark
cd spark
wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
```

Unpack it and then remove the tar file:

❓what does xzfv stand for?

```bash
tar xzfv openjdk-17.0.2_linux-x64_bin.tar.gz
rm openjdk-17.0.2_linux-x64_bin.tar.gz
```

define `JAVA_HOME` and add it to `PATH`:


```bash
# export JAVA_HOME and prepend it to path
export JAVA_HOME="${HOME}/spark/jdk-17.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"
```
ℹ️ `${HOME}` usually works better than tilde `~`

check that it works:

```bash
java --version
```

Output:

```
openjdk 17.0.2 2022-01-18
OpenJDK Runtime Environment (build 17.0.2+8-86)
OpenJDK 64-Bit Server VM (build 17.0.2+8-86, mixed mode, sharing)
```

### Installing Spark


Download Spark. Use 3.3.2 version:

```bash
# download
wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
# unpack
tar xzfv spark-3.3.2-bin-hadoop3.tgz
# rm
rm spark-3.3.2-bin-hadoop3.tgz
# add to PATH
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```

### Testing Spark

Execute `spark-shell` and run the following:

```scala
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

## Making the setup stable

```bash
cd
nano .bashrc
# add the previously defined constants to it
export JAVA_HOME="${HOME}/spark/jdk-17.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"

export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```

-> CTRL + O to save
-> Enter to save it with the same name
-> CTRL + X to exit

### PySpark

It's the same for all platforms. Go to [pyspark.md](pyspark.md). 

Tell the VM where it can find python libraries with
```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```
To start a jupyter notebook, create a folde rand start jupyter in it

```bash
mkdir notebooks
cd notebooks
jupyter notebook
```