# M23 degree-23 action fingerprint helper.
# Usage inside GAP:
#   Read("experiments/m23/gap/group_fingerprints.g");
#
# GAP also has CycleStructurePerm; this script keeps a direct cycle-length helper
# so the printed output matches polynomial factorization degrees.

CycleTypeFromPermutation := function(perm, degree)
    local seen, lengths, i, j, length;
    seen := [];
    lengths := [];
    for i in [1..degree] do
        seen[i] := false;
    od;
    for i in [1..degree] do
        if not seen[i] then
            j := i;
            length := 0;
            while not seen[j] do
                seen[j] := true;
                length := length + 1;
                j := j ^ perm;
            od;
            Add(lengths, length);
        fi;
    od;
    Sort(lengths);
    return Reversed(lengths);
end;

PrintM23Fingerprints := function()
    local G, H, classes, cycleTypes, c, representative, cycleType;
    G := MathieuGroup(23);
    H := TransitiveGroup(23,5);
    Print("MathieuGroup(23) order: ", Size(G), "\n");
    Print("TransitiveGroup(23,5) order: ", Size(H), "\n");
    classes := ConjugacyClasses(G);
    cycleTypes := [];
    for c in classes do
        representative := Representative(c);
        cycleType := CycleTypeFromPermutation(representative, 23);
        if not cycleType in cycleTypes then
            Add(cycleTypes, cycleType);
        fi;
    od;
    Print("Unique cycle types in MathieuGroup(23):\n");
    for cycleType in cycleTypes do
        Print(cycleType, "\n");
    od;
end;

PrintM23Fingerprints();
