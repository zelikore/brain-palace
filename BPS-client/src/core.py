import time

from yaspin import yaspin
import pyfiglet
import typer
import inquirer
import sys
import json

BPSConfigFile = "./BPS.data.json"

app = typer.Typer()

addConceptsquestions = [
    inquirer.Text(name='concept', message="name:"),
    inquirer.Text(name='topic', message="base topic of {concept}:")
]


class BPSclient:
    def __init__(self):
        try:
            f = open(BPSConfigFile, 'rb')
        except OSError:
            print('You are not in a BPS directory')
            sys.exit()

        with f:
            try:
                self.bpsconfig = json.load(f)
                # verification logic
            except:
                print("BPS.data.json corrupted")

    def printconfig(self):
        print(self.bpsconfig)

    def getTopic(self, topic):
        try:
            return self.bpsconfig
        except:
            return None

    def getConcept(self, concept):
        try:
            return self.bpsconfig["concepts"][concept]
        except:
            return False

    def getConcepts(self):
        concepts =  self.bpsconfig["concepts"]
        conceptList = []
        for concept in concepts:
            conceptList.append(concept)
        return conceptList





    def addConcept(self, name, topic):
        config = self.bpsconfig
        config['concepts'] = {name: {"topic": topic}}

        try:
            f = open(BPSConfigFile, 'w')
        except OSError:
            print('You are not in a BPS directory')
            sys.exit()

        with f:
            json_object = json.dumps(config, indent=4)
            f.write(json_object)


@app.command()
def add(argument: str):
    bpsclient = BPSclient()
    bpsclient.printconfig()

    if argument == "concept":
        answers = inquirer.prompt(addConceptsquestions)
        if not (bpsclient.getConcept(answers["concept"])):

            print("concept does not exist, creating concept")
            bpsclient.addConcept(answers["concept"], answers["topic"])

        else:
            print("concept exists")


@app.command()
@yaspin(text="Fetching data...")
def list():
    bpsclient = BPSclient()
    # some heavy work
    print(pyfiglet.figlet_format("Welcome to the Brain Palace System"))
    print("concepts:")
    for concept in bpsclient.getConcepts():
        print(concept)



if __name__ == "__main__":
    app()
