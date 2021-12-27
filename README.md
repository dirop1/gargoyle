# Gargoyle SSR

Very Simple Website Static Generator writen in python.

### Objectives
The main objective is to use a good CMS like wordpress to wright content without worring about hosting and bad performance, after turning the output folder to a git repository you can use a a service like Clouflare Pages or something similar to have a super fast website deployed in a CDN without worring with server side security and hosting costs. 

# Instalation
```
git clone https://github.com/dirop1/gargoyle.git
cd gargoyle
python3 -m pip install -r requirements.txt
```

### Usage
- create a folder to store your html files
- Inside that create a gargoyle folder and inside it a config.yaml like the one in [config_example](config_example.yaml)
- inside the root folder run the following: (Don't forget to correct your path to Gargoyle if it is different)
```
python ../Gargoyle/gargoyle.py petrify .
```

### What to expect
- This is in a very beta stage testing / developping is very apreciated.
- Everything that is dynamic (Server Side) will stop working, like your WordPress Comments or a contact form.
- That can be corrected with some java script and cloud functions or some external service like Discus for comments.


### Websites turned int to stone by this tool:

- [https://www.slashlogs.com](https://www.slashlogs.com) (Was WordPress)
