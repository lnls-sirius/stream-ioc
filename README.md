# Stream-IOC

This project is an EPICS IOC based on StreamDevice. All StreamDevice-based EPICS interfaces created by LNLS Controls Group for Sirius control system will be contained in this application.

## System requirements

In order to get this software running, you should have installed in your system EPICS base (version 3.15.5 recommended) and asynDriver module (version 4-33 recommended). Stream-IOC is intended to run in a Linux environment.

## Supported devices

Currently Stream-IOC provides EPICS interfaces for:

* Agilent 4UHV Ion Pump Controller
* Berthold Technologies LB 6420
* [CountingPRU](https://wiki-sirius.lnls.br/mediawiki/index.php/CON:CountingPRU)
* [DCM SE-10](https://dcmtech.com.br/equipamentos-e-sistemas-para-monitorar-temperatura-e-umidade/se-10-monitor-de-ambientes-com-acionamento-de-cargas/)
* ELSE Nuclear SATURN 5702
* [MBTemp](https://wiki-sirius.lnls.br/mediawiki/index.php/CON:MBTemp)
* Thermo Fisher Scientific FHT 6020
* [SPIxCONV](https://wiki-sirius.lnls.br/mediawiki/index.php/CON:SPIxCONV)


## Directory structure

The repository should be cloned with the `--recursive` option:

```
$ git clone --recursive https://github.com/lnls-sirius/stream-ioc.git
```

This way the user will also obtain the StreamDevice source code from GitHub.com. StreamDevice is a Git submodule of Stream-IOC repository.

Here is a brief explanation of the directory structure:

* **configure** - Directory with configuration files for compiling the EPICS IOC.

* **database** - Contains files with record definitions for all devices this application supports.

* **interface** - Folder with Python programs that provide TCP, UDP or Unix sockets for communication between the EPICS IOC and some devices. An interface program may create a file with the ".data" extension in this directory, which will be used to store configuration parameters of the interface software or the controlled hardware.

* **iocBoot** - Directory where the IOC initialization scripts reside. These files must be properly configured, as described at the "Executing the IOC" section. In the future, definition of control system nodes structure will lead to many specific initialization scripts. In this folder, a file named `StreamDebug.log` will be created at execution time. All the error messages reported by StreamDevice will be logged into this file.

* **protocol** - Contains files with communication protocol definitions. Each file in this directory corresponds to a specific device.

* **StreamDevice** - StreamDevice version 2.7.7 source code, as a Git submodule.

## Compiling

This software is distributed in the form of source code. In order to compile it, first define at the `configure/RELEASE` file the system paths to EPICS base and asynDriver. By default, these configurations are:

```
EPICS_BASE=/opt/base-3.15.5
ASYN=/opt/asyn4-33
```

After editing `configure/RELEASE`, run these commands at the top directory:

```
$ rm StreamDevice/GNUmakefile
$ make
```

## Executing the IOC

To run this application, execute one of the scripts located at iocBoot directory.

The first line of script file must be the correct path to the application executable. If the system CPU is an ARM core, the first line must be:

```
#!../bin/linux-arm/streamApp
```

Instead, if we are working in a 64-bit computer:

```
#!../bin/linux-x86_64/streamApp
```

In the script file, four environment variables must be correctly defined:

* **EPICS_BASE** - Path to the system directory where EPICS base is installed.

* **ASYN** - Path to the system directory where asynDriver module is installed.

* **TOP** - Path to the application top directory.

* **ARCH** - System architecture ("linux-arm" for an ARM environment or "linux-x86_64" for a 64-bit Linux architecture, for example).

During IOC operation, the file `iocBoot/StreamDebug.log` is created. It will contain all error messages reported by StreamDevice. If no error happens, at the end of execution this file will be empty.

In practical situations, Stream-IOC should be launched with procServ at system's startup. Example command for doing that:

```
$ procServ --chdir <ioc_top_directory>/iocBoot 20200 ./<initialization_script_file_name>
```

## Uninstalling

To remove this software from a computer, just delete its parent directory.
