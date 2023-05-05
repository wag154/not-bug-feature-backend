# Running the project

Before running the project make sure to have a venv installed on your machine. To do it so:
```
    python3 -m venv venv  
```

After having venv installed properly on your machine, run the following command to enable/activate your virtual environment:
* for MacOs
```commandline
    source venv/bin/activate    
```

* for Windows
```commandline
    .\venv\Scripts\activate
```

Having both steps completed, your command line should look like `(venv) username@101 project-name`
Almost there... just need to install the requirements from our project through the command:
```commandline
    pip install -r requirements.txt
```

NOTE: All commands should be executed on the root folder from the project.

## Keeping the requirements.txt file up-to-date

The benefit of using requirements.txt is that it will control all dependencies required to run the project successfully (including the right version).
But with great powers come great responsibilities, everytime that you install a new package in the project, make sure to run 
```
    pip3 freeze > requirements.txt  # For Python3
    pip freeze > requirements.txt  # For Python2
```

## Disabling virtual environment

Simply run:
```commandline
    deactivate
```