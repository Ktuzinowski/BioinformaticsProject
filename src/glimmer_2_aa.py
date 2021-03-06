#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert GlimmerHMM GFF3 gene predictions into protein sequences.
This works with the GlimmerHMM GFF3 output format:
##gff-version 3
##sequence-region Contig5.15 1 47390
Contig5.15      GlimmerHMM      mRNA    323     325     .       +       .       ID=Contig5.15.path1.gene1;Name=Contig5.15.path1.gene1
Contig5.15      GlimmerHMM      CDS     323     325     .       +       0       ID=Contig5.15.cds1.1;Parent=Contig5.15.path1.gene1;Name=Contig5.15.path1.gene1;Note=final-exon
http://www.cbcb.umd.edu/software/GlimmerHMM/
Usage:
    glimmer_2_aa.py <work_path> <add_nuc> <glimmer gff3> <ref fasta>
"""
from __future__ import with_statement
import sys
import os
import operator
from functools import reduce
from Bio import SeqIO, Seq
from Bio.SeqRecord import SeqRecord
from BCBio import GFF

def main(work_path, add_nuc, glimmer_file, ref_file):

    with open(ref_file) as in_handle:
        ref_recs = SeqIO.to_dict(SeqIO.parse(in_handle, "fasta"))

    base, ext = os.path.splitext(glimmer_file)
    base = base.split("/")[-1]
    add_nuc = int(add_nuc)

    if add_nuc != 150:
        out_file = work_path + "Predictions/Proteines/glimmer/" + str(add_nuc) + "Kb/" + base + ".fasta"
    else:
        out_file = work_path + "Predictions/Proteines/glimmer/150bp/" + base + ".fasta"

    with open(out_file, "w") as out_handle:
        SeqIO.write(protein_recs(glimmer_file, ref_recs), out_handle, "fasta")


def protein_recs(glimmer_file, ref_recs):
    """Generate protein records from GlimmerHMM gene predictions.
    """
    with open(glimmer_file) as in_handle:
        for rec in glimmer_predictions(in_handle, ref_recs):
            for feature in rec.features:
                seq_exons = []
                for cds in feature.sub_features:
                    seq_exons.append(rec.seq[
                                     cds.location.nofuzzy_start:
                                     cds.location.nofuzzy_end])
                gene_seq = Seq.Seq(str(reduce(operator.add, seq_exons, "")))
                if feature.strand == -1:
                    gene_seq = gene_seq.reverse_complement()
                protein_seq = gene_seq.translate()
                yield SeqRecord(protein_seq, feature.qualifiers["ID"][0], "", "")


def glimmer_predictions(in_handle, ref_recs):
    """Parse Glimmer output, generating SeqRecord and SeqFeatures for predictions
    """
    for rec in GFF.parse(in_handle, target_lines=1000, base_dict=ref_recs):
        yield rec


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("oops")
        print(__doc__)
        exit()

    main(*sys.argv[1:])

