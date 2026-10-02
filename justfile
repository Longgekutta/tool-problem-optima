# UCFS v1.0 standard Justfile for tool-problem-optima

default:
    @python main.py --help

setup:
    @python main.py setup

run TARGET=".":
    @python main.py run {{TARGET}}

audit TARGET:
    @python main.py audit {{TARGET}}

test:
    @python main.py test

health:
    @python main.py health

clean:
    @python main.py clean

catalog:
    @python main.py catalog

tensor CODE="PRB-E101":
    @python main.py tensor {{CODE}}
