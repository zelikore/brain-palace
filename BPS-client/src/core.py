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
                #verification logic
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
            return self.bpsconfig.concepts[concept]
        except:
            return False






@app.command()
def add(argument: str):
    bpsclient = BPSclient()
    bpsclient.printconfig()

    if argument == "concept":
        answers = inquirer.prompt(addConceptsquestions)

        print(bpsclient.getTopic(answers))




@app.command()
@yaspin(text="Fetching data...")
def list():
    # some heavy work
    print(pyfiglet.figlet_format("Welcome to the Brain Palace System"))
    print("result")


if __name__ == "__main__":
    app()
