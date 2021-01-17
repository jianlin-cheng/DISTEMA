#!/usr/bin/perl -w

use strict;

if (@ARGV ne 2 ){
  print STDERR "Usage: $0 <fasta> <file-dist>\n";
  exit;
}

my $fasta_fname = $ARGV[0];
my $dist_fname  = $ARGV[1];

my $id = $fasta_fname;
$id =~ s/\..*//;
$id =~ s/^.*\///;

open FASTA, "<" . $fasta_fname or die "Couldn't open fasta file\n";
my @lines = <FASTA>;
chomp(@lines);
close FASTA;

shift @lines;
my $seq = join('', @lines);
$seq =~ s/ //g;
my @seq = split(//, $seq);
my $seq_len = length($seq);

my %dist;
open CS, $dist_fname or die $!." $dist_fname";
while(<CS>){
	chomp $_;
	my @C = split /\s+/, $_;
	$dist{$C[0]." ".$C[1]} = $C[2];
	$dist{$C[1]." ".$C[0]} = $C[2];
}
close CS;
print "# True distance map\n";
for(my $i = 1; $i <= $seq_len; $i++) {
	for(my $j = 1; $j <= $seq_len; $j++) {
		my $xx = 0;
		$xx = 0 if $i == $j;
		$xx = $dist{$i." ".$j} if (defined $dist{$i." ".$j});
		print "$xx ";
	}
	print "\n";
}