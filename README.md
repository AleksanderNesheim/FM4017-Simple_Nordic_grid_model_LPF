# FM4017-Project
This GitHUB is part of the FM4017 - Project course at the University of South-Eastern Norway.
The GitHUB provides the neccessary files to use the developed simplified network model of the Nordic Synchronous grid.

The base network provided is created using the PyPSA-eur workflow, and is a result of the specifications used in the config file.
If you want to use the model, you need have an environment which contains the necessary packages for PyPSA. If you do not have this yes, you can follow the guide provided here: https://pypsa-eur.readthedocs.io/en/latest/installation.html#installation 

This repositary contains the necessary files for the user to perform lpf on the devoloped 65 bus model of the Nordic synchronous grid. 

To use the model, clone the repo and run "workflow.ipynb". This is a first iteration, so some bugs could occur. If you encounter this, feel free to modify the workflow or helper functions to fix this, and then report it in this Github with the fix. You can also of course just report the bug without fixing it. 

Limitations of the model, drawbacks and missing data
- Can only do LPF as (at least) data is missing for components.
- The model is not a realistic representation of the installed capacity in each biddiing zone.
- Some production technologies are aggregated into 'other' in PyPSA, as the generators related to these technologies did not get placed in the model we retrieved from the PyPSA-eur workflow. Technologies aggregated in 'other' was then distributed equally among the buses for zones where unplaced production happened. 
