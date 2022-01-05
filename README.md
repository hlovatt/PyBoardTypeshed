# Micropython Typesheds (formerly known as Pyboard Typesheds)

Rich typeshed (a.k.a.: type hints, interface stubs, and `.pyi` files)
for [MicroPython](http://micropython.org).
They are *rich* typesheds because they give help document for
functions/methods, function/method arguments, function/method return types,
method overloads, classes, modules, protocols,
and constants/fields/properties. 
These typesheds are useful for IDEs that understand type hints,
like PyCharm and VSCode, and for IDE plugins like the PyCharm's MicroPython plugin.

## What the typesheds do

Once installed, see next section, the typesheds offer:

1. Code completion (in this case prompting completion for `pyb`):\
   ![Code completion example](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/code.png?raw=true "Possible code completions")

2. Rich help text (in this case constructor for `LCD160CR`
   showing argument types, argument defaults, return types and 
   overloads as well as a description):\
   ![Rich help example](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/help.png?raw=true "Rich help for overloaded constructor")

3. Type errors (in this case a `float` instead of an `int`):\
   ![Type error example](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/type.png?raw=true "Detects type error")

4. Typos (in this case `colour` instead of `color`; error can be avoided by 
   using code completion, see point 1 above):\
   ![Type error example](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/typo.png?raw=true "Detects missing attribute due to typo")

## Using the typesheds

There are four ways of installing the Typesheds:
via an IDE plugin, manually install into the IDE, 
use PyPI, copy the `.pyi` files into a project,
and manually copy the `.pyi` files into a project.

### Via an IDE plugin

#### For PyCharm

Currently, December 2021, JetBrains have added many of these typesheds to their 
MicroPython plugin (many thanks to JetBrains and in particular Andrey Vlasovskikh).
Therefore, installing the JetBrains Micropython plugin
will be the easiest solution and also 
the typesheds will get updated everytime the plugin is updated:

1. Install the
   [MicroPython plugin](https://plugins.jetbrains.com/plugin/9777-micropython).

2. Enable the plugin for the project
   (two stages in project preferences/options:
   add the plugin to the project and then select options in the plugin):\
   ![Enable MicroPython plugin for project part 1](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/enable_pt1.png?raw=true "Select MicroPython Language")
   ![Enable MicroPython plugin for project part 2](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/enable_pt2.png?raw=true "Enable MicroPython support, select Pyboard, and select device path)")

The other options, below, unfortunately require manual updating and are more 
involved (though not difficult).

### Manually install in an IDE

#### For PyCharm

If the very latest typesheds are required then they can be installed from
this repository directly.

**Note:** The following procedure, below, only needs to be done for one project; 
after which all projects using the
MicroPython plugin will pick up the typesheds.

1. Install and enable the plugin, see previous section above.

2. Download the ZIPed `.pyi` files from GitHub:\
   ![Download ZIPed files from GitHub](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/download.png?raw=true "Select 'Download Zip' from 'Code' dropdown")

3. Unpack the ZIP file.

4. Drag (or copy and past) the `.pyi` (only) files into the Micropython Plugin
   (see image for which directory to put each file in):\
   ![Drag `.pyi` files into Plugin](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/typesheds.png?raw=true "`.pyi` files in Micropython plugin")

5. Disable and re-enable plugin by going to preferences/options un-tick 
   Micropython support and Apply then re-tick
   MicroPython support and OK
   (so that it picks up the changes):\
   ![Re-enable MicroPython plugin](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/enable_pt2.png?raw=true "Un-tick and OK back into preferences re-tick MicroPython support and OK")

### Use PyPI to copy the `.pyi` files into a project or IDE

  1. Install the typesheds' installer

```bash
    pip install --upgrade micropython-typesheds
```

  2. Copy the typesheds to where they are required.
     EG typeshed location for IDE or plugin or top 
     level of project.
     **Note:** The following command, below, needs 
     to be done for *all* required locations:

```bash
    python -m micropython_typesheds <destination-directory>
```

### Copy `.pyi` files into a project

**Note:** The following procedure, below, needs to be done for *all* projects:

1. Download the ZIPed `.pyi` files from GitHub:\
   ![Download ZIPed files from GitHub](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/download.png?raw=true "Select 'Download Zip' from 'Code' dropdown")

2. Unpack the ZIP file.

3. Drag the `.pyi` (only) files from directory `micropython_typesheds` into the top level of a project:\
   ![Drag `.pyi` files in top level of project](https://github.com/hlovatt/PyBoardTypeshed/blob/master/media/files.png?raw=true "`.pyi` files in top level of project")

## Philosophy

The typesheds are generated by
[https://github.com/hlovatt/PyBoardTypeshedGenerator]()
from the MicroPython `.rst` doc files.

The philosophy of generating the typesheds is to take a superset of what is 
in the docs and what is listed by the `dir`
command on a MicroPython board
(the docs and `dir` don't agree!). 
An example of the `dir` command having more information than the docs is the docs
for `pyb.Pin` mentions `board` and `cpu` classes and implies they contain 
declarations of available `Pin`s;
`dir(pyb.Pin.cpu)` on the other hand lists the `Pin`s, 
therefore the generated typeshed contains `board` and `cpu`
*with* `Pin` definitions.
