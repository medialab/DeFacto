import csv
import click
import networkx as nx
import pelote
from statistics import mean


@click.command
@click.option("--documents")
@click.option("--matrix")
def main(documents, matrix):

    #Step 1. In a dictionary, index documents and metadata by Id
    with open(documents) as f:
        reader = csv.DictReader(f)
        docs = {row["Id"]:row for row in reader}

    #Step 2. Parse the matrix
    with open(matrix) as f:
        reader = csv.DictReader(f)
        G = nx.Graph()
        for row in reader:
            # If the matrix refers to documents not in the original data, skip 
            if not docs.get(row["pid1"]) or not docs.get(row["pid2"]):
                continue
            
            # Base an edge's weight on the support that two related propositions received
            average_nb_votes = mean([int(docs[row["pid1"]]["Nb de votes"]), int(docs[row["pid2"]]["Nb de votes"])])
            weight = int(row["count"])/average_nb_votes

            # Unless already added to the Graph, add both nodes in the matrix row and create an edge between them
            if not G.has_node(row["pid1"]) and not str(docs[row["pid1"]]["topic"]) == "-1":
                G.add_node(row["pid1"], label=docs[row["pid1"]]["Proposition"], **docs[row["pid1"]])

            if not G.has_node(row["pid2"]) and not str(docs[row["pid2"]]["topic"]) == "-1":
                G.add_node(row["pid2"], label=docs[row["pid2"]]["Proposition"], **docs[row["pid2"]])

            if row["vote1"] == row["vote2"] and row["vote1"] == "agree" or row["vote1"] == "neutral":  # To-do: test if we can try all 3 types of cases
                G.add_edge(row["pid1"], row["pid2"], weight=weight)


        # pelote -- rétirer les liens moins signifactifs --> multiscale_backbone
        H = pelote.multiscale_backbone(G, alpha=0.05)
        nx.write_gexf(H, "defacto_covotes_agree_sparsification.gexf")



if __name__ == "__main__":
    main()