from app.generators.fpl_parser import parse_fpl

fpl = """(FPL-PPP1441-IS
-A319/M-SDFGHIRWY/B1L
-ULMM1735
-K0768F320 ASGO1K ASGOR T693 PILAN/K0779F330 M856 KUKUM/K0788F340
M856 GIKUR/K0801F350 T458 BEPOL BEPO1A
-ULLI0142 UUEE
-PBN/B1D1A1S2O1 DOF/230220 REG/PP00000 EET/ULLL0005 SEL/SSSS
CODE/000000 OPR/PPP RALT/ULMM ULLI RMK/ACASII EQUIPPED)"""

plan = parse_fpl(fpl)
print(f"Callsign: {plan.callsign}")
print(f"Aircraft: {plan.aircraft_type}")
print(f"Departure: {plan.departure}")
print(f"Destination: {plan.destination}")
print(f"Alternate: {plan.alternate}")
print(f"Cruising level: {plan.cruising_level}")
print(f"Route points: {plan.get_route_points()}")