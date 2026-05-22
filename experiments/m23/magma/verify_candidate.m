// M23 candidate verification helper.
// Usage inside Magma:
//   load "experiments/m23/magma/verify_candidate.m";
//   VerifyCandidate("x^23 - x - 1", [2,3,5,7,11,13,17,19,23,29,31]);

function ParseCandidate(poly_string)
    Qx<x> := PolynomialRing(Rationals());
    return eval poly_string;
end function;

procedure VerifyCandidate(poly_string, primes)
    Qx<x> := PolynomialRing(Rationals());
    f := eval poly_string;

    print "candidate:", f;
    print "degree:", Degree(f);
    print "is_irreducible:", IsIrreducible(f);
    print "discriminant:", Discriminant(f);

    for p in primes do
        Fp<t> := PolynomialRing(GF(p));
        fp := Fp!f;
        print "prime:", p;
        print "factorization:", Factorization(fp);
    end for;

    print "Attempting GaloisGroup. This may be expensive.";
    G, roots, data := GaloisGroup(f);
    print "galois_group_order:", #G;
    print "galois_group:", G;
end procedure;
