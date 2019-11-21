\ Model mip1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  - 9 y[1,1,0] - 3 y[2,1,0] + 24 y[3,1,0] + slack1[1,0,0] + slack1[1,1,0]
   + slack1[1,2,0] + slack1[2,0,0] + slack1[2,1,0] + slack1[2,2,0]
   + slack1[3,0,0] + slack1[3,1,0] + slack1[3,2,0]
Subject To
 c2[1,1,0]: - x[1,0,0] + x[1,1,0] - x[2,0,0] <= 0
 c2[1,2,0]: - x[1,1,0] + x[1,2,0] - x[2,1,0] <= 0
 c2[2,1,0]: - x[1,0,0] - x[2,0,0] + x[2,1,0] <= 0
 c2[2,2,0]: - x[1,1,0] - x[2,1,0] + x[2,2,0] <= 0
 c2[3,1,0]: - x[3,0,0] + x[3,1,0] <= 0
 c2[3,2,0]: - x[3,1,0] + x[3,2,0] <= 0
 c3[0,0]: x[1,0,0] + x[2,0,0] + x[3,0,0] = 1
 c3[1,0]: x[1,1,0] + x[2,1,0] + x[3,1,0] = 1
 c3[2,0]: x[1,2,0] + x[2,2,0] + x[3,2,0] = 1
 c4[1]: y[1,1,0] = 9
 c4[2]: y[2,1,0] = 7
 c4[3]: y[3,1,0] = 9
 c5[1,0]: y[1,0,0] <= 13
 c5[1,1]: y[1,1,0] <= 13
 c5[1,2]: y[1,2,0] <= 13
 c5[2,0]: y[2,0,0] <= 15
 c5[2,1]: y[2,1,0] <= 15
 c5[2,2]: y[2,2,0] <= 15
 c6[3,0]: y[3,0,0] <= 9
 c6[3,1]: y[3,1,0] <= 9
 c6[3,2]: y[3,2,0] <= 9
 c7[0,0]: y[1,0,0] - y[1,1,0] + y[2,0,0] - y[2,1,0] + y[3,0,0] - y[3,1,0]
   + b[0,0] - b[1,0] = 0
 c7[1,0]: = 0
 c7[2,0]: - y[1,1,0] + y[1,2,0] - y[2,1,0] + y[2,2,0] - y[3,1,0] + y[3,2,0]
   - b[1,0] + b[2,0] = 0
 R24: y[1,0,0] - y[1,1,0] + newVar1[1,1,0] = 0
 c8[1,1,0]: - 13 x[1,1,0] + newVar2[1,1,0] <= 0
 R26: y[1,1,0] - y[1,2,0] + newVar1[1,2,0] = 0
 c8[1,2,0]: - 13 x[1,2,0] + newVar2[1,2,0] <= 0
 R28: y[2,0,0] - y[2,1,0] + newVar1[2,1,0] = 0
 c8[2,1,0]: - 13 x[2,1,0] + newVar2[2,1,0] <= 0
 R30: y[2,1,0] - y[2,2,0] + newVar1[2,2,0] = 0
 c8[2,2,0]: - 13 x[2,2,0] + newVar2[2,2,0] <= 0
 R32: y[3,0,0] - y[3,1,0] + newVar1[3,1,0] = 0
 c8[3,1,0]: - 13 x[3,1,0] + newVar2[3,1,0] <= 0
 R34: y[3,1,0] - y[3,2,0] + newVar1[3,2,0] = 0
 c8[3,2,0]: - 13 x[3,2,0] + newVar2[3,2,0] <= 0
 R36: - y[1,0,0] + newVar3[1,0,0] = 0
 R37: - x[1,0,0] + newVar4[1,0,0] = 0
 c9[1,0,0]: newVar5[1,0,0] + 13 newVar6[1,0,0] - slack1[1,0,0] <= 13
 R39: y[1,0,0] - y[1,1,0] + newVar3[1,1,0] = 0
 R40: x[1,0,0] - x[1,1,0] + newVar4[1,1,0] = 0
 c9[1,1,0]: newVar5[1,1,0] + 13 newVar6[1,1,0] - slack1[1,1,0] <= 13
 R42: y[1,1,0] - y[1,2,0] + newVar3[1,2,0] = 0
 R43: x[1,1,0] - x[1,2,0] + newVar4[1,2,0] = 0
 c9[1,2,0]: newVar5[1,2,0] + 13 newVar6[1,2,0] - slack1[1,2,0] <= 13
 R45: - y[2,0,0] + newVar3[2,0,0] = 0
 R46: - x[2,0,0] + newVar4[2,0,0] = 0
 c9[2,0,0]: newVar5[2,0,0] + 13 newVar6[2,0,0] - slack1[2,0,0] <= 13
 R48: y[2,0,0] - y[2,1,0] + newVar3[2,1,0] = 0
 R49: x[2,0,0] - x[2,1,0] + newVar4[2,1,0] = 0
 c9[2,1,0]: newVar5[2,1,0] + 13 newVar6[2,1,0] - slack1[2,1,0] <= 13
 R51: y[2,1,0] - y[2,2,0] + newVar3[2,2,0] = 0
 R52: x[2,1,0] - x[2,2,0] + newVar4[2,2,0] = 0
 c9[2,2,0]: newVar5[2,2,0] + 13 newVar6[2,2,0] - slack1[2,2,0] <= 13
 R54: - y[3,0,0] + newVar3[3,0,0] = 0
 R55: - x[3,0,0] + newVar4[3,0,0] = 0
 c9[3,0,0]: newVar5[3,0,0] + 13 newVar6[3,0,0] - slack1[3,0,0] <= 13
 R57: y[3,0,0] - y[3,1,0] + newVar3[3,1,0] = 0
 R58: x[3,0,0] - x[3,1,0] + newVar4[3,1,0] = 0
 c9[3,1,0]: newVar5[3,1,0] + 13 newVar6[3,1,0] - slack1[3,1,0] <= 13
 R60: y[3,1,0] - y[3,2,0] + newVar3[3,2,0] = 0
 R61: x[3,1,0] - x[3,2,0] + newVar4[3,2,0] = 0
 c9[3,2,0]: newVar5[3,2,0] + 13 newVar6[3,2,0] - slack1[3,2,0] <= 13
Bounds
Binaries
 x[1,0,0] x[1,1,0] x[1,2,0] x[2,0,0] x[2,1,0] x[2,2,0] x[3,0,0] x[3,1,0]
 x[3,2,0]
Generals
 y[1,0,0] y[1,1,0] y[1,2,0] y[2,0,0] y[2,1,0] y[2,2,0] y[3,0,0] y[3,1,0]
 y[3,2,0] b[0,0] b[1,0] b[2,0] newVar1[1,1,0] newVar2[1,1,0] newVar1[1,2,0]
 newVar2[1,2,0] newVar1[2,1,0] newVar2[2,1,0] newVar1[2,2,0] newVar2[2,2,0]
 newVar1[3,1,0] newVar2[3,1,0] newVar1[3,2,0] newVar2[3,2,0] newVar3[1,0,0]
 newVar4[1,0,0] newVar5[1,0,0] newVar6[1,0,0] slack1[1,0,0] newVar3[1,1,0]
 newVar4[1,1,0] newVar5[1,1,0] newVar6[1,1,0] slack1[1,1,0] newVar3[1,2,0]
 newVar4[1,2,0] newVar5[1,2,0] newVar6[1,2,0] slack1[1,2,0] newVar3[2,0,0]
 newVar4[2,0,0] newVar5[2,0,0] newVar6[2,0,0] slack1[2,0,0] newVar3[2,1,0]
 newVar4[2,1,0] newVar5[2,1,0] newVar6[2,1,0] slack1[2,1,0] newVar3[2,2,0]
 newVar4[2,2,0] newVar5[2,2,0] newVar6[2,2,0] slack1[2,2,0] newVar3[3,0,0]
 newVar4[3,0,0] newVar5[3,0,0] newVar6[3,0,0] slack1[3,0,0] newVar3[3,1,0]
 newVar4[3,1,0] newVar5[3,1,0] newVar6[3,1,0] slack1[3,1,0] newVar3[3,2,0]
 newVar4[3,2,0] newVar5[3,2,0] newVar6[3,2,0] slack1[3,2,0]
General Constraints
 GC0: newVar2[1,1,0] = ABS ( newVar1[1,1,0] )
 GC1: newVar2[1,2,0] = ABS ( newVar1[1,2,0] )
 GC2: newVar2[2,1,0] = ABS ( newVar1[2,1,0] )
 GC3: newVar2[2,2,0] = ABS ( newVar1[2,2,0] )
 GC4: newVar2[3,1,0] = ABS ( newVar1[3,1,0] )
 GC5: newVar2[3,2,0] = ABS ( newVar1[3,2,0] )
 GC6: newVar5[1,0,0] = ABS ( newVar3[1,0,0] )
 GC7: newVar6[1,0,0] = ABS ( newVar4[1,0,0] )
 GC8: newVar5[1,1,0] = ABS ( newVar3[1,1,0] )
 GC9: newVar6[1,1,0] = ABS ( newVar4[1,1,0] )
 GC10: newVar5[1,2,0] = ABS ( newVar3[1,2,0] )
 GC11: newVar6[1,2,0] = ABS ( newVar4[1,2,0] )
 GC12: newVar5[2,0,0] = ABS ( newVar3[2,0,0] )
 GC13: newVar6[2,0,0] = ABS ( newVar4[2,0,0] )
 GC14: newVar5[2,1,0] = ABS ( newVar3[2,1,0] )
 GC15: newVar6[2,1,0] = ABS ( newVar4[2,1,0] )
 GC16: newVar5[2,2,0] = ABS ( newVar3[2,2,0] )
 GC17: newVar6[2,2,0] = ABS ( newVar4[2,2,0] )
 GC18: newVar5[3,0,0] = ABS ( newVar3[3,0,0] )
 GC19: newVar6[3,0,0] = ABS ( newVar4[3,0,0] )
 GC20: newVar5[3,1,0] = ABS ( newVar3[3,1,0] )
 GC21: newVar6[3,1,0] = ABS ( newVar4[3,1,0] )
 GC22: newVar5[3,2,0] = ABS ( newVar3[3,2,0] )
 GC23: newVar6[3,2,0] = ABS ( newVar4[3,2,0] )
End
