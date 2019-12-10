\ Model mip1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  y[1,3,0]
Subject To
 c2[1,1,0]: - x[1,0,0] + x[1,1,0] - x[2,0,0] <= 0
 c2[1,2,0]: - x[1,1,0] + x[1,2,0] - x[2,1,0] <= 0
 c2[1,3,0]: - x[1,2,0] + x[1,3,0] - x[2,2,0] <= 0
 c2[2,1,0]: - x[1,0,0] - x[2,0,0] + x[2,1,0] <= 0
 c2[2,2,0]: - x[1,1,0] - x[2,1,0] + x[2,2,0] <= 0
 c2[2,3,0]: - x[1,2,0] - x[2,2,0] + x[2,3,0] <= 0
 c3[0,0]: x[1,0,0] + x[2,0,0] = 1
 c3[1,0]: x[1,1,0] + x[2,1,0] = 1
 c3[2,0]: x[1,2,0] + x[2,2,0] = 1
 c3[3,0]: x[1,3,0] + x[2,3,0] = 1
 c4[1]: y[1,1,0] = 6
 c4[2]: y[2,1,0] = 5
 c5pt1[1,0]: y[1,0,0] >= 6
 c5pt2[1,0]: y[1,0,0] <= 7
 c5pt1[1,1]: y[1,1,0] >= 6
 c5pt2[1,1]: y[1,1,0] <= 7
 c5pt1[1,2]: y[1,2,0] >= 6
 c5pt2[1,2]: y[1,2,0] <= 7
 c5pt1[1,3]: y[1,3,0] >= 6
 c5pt2[1,3]: y[1,3,0] <= 7
 c6pt1[2,0]: y[2,0,0] >= 4
 c6pt2[2,0]: y[2,0,0] <= 5
 c6pt1[2,1]: y[2,1,0] >= 4
 c6pt2[2,1]: y[2,1,0] <= 5
 c6pt1[2,2]: y[2,2,0] >= 4
 c6pt2[2,2]: y[2,2,0] <= 5
 c6pt1[2,3]: y[2,3,0] >= 4
 c6pt2[2,3]: y[2,3,0] <= 5
 c7[0,0]: = 0
 c7[1,0]: - y[1,0,0] + y[1,1,0] - y[2,0,0] + y[2,1,0] - b[0,0] + b[1,0]
   = 0
 c7[2,0]: - y[1,0,0] + y[1,2,0] - y[2,0,0] + y[2,2,0] - b[0,0] + b[2,0]
   = 0
 c7[3,0]: - y[1,0,0] + y[1,3,0] - y[2,0,0] + y[2,3,0] - b[0,0] + b[3,0]
   = 0
 R32: y[1,0,0] - y[1,1,0] + newVar1[1,1,0] = 0
 c8[1,1,0]: - 13 x[1,1,0] + newVar2[1,1,0] <= 0
 R34: y[1,1,0] - y[1,2,0] + newVar1[1,2,0] = 0
 c8[1,2,0]: - 13 x[1,2,0] + newVar2[1,2,0] <= 0
 R36: y[1,2,0] - y[1,3,0] + newVar1[1,3,0] = 0
 c8[1,3,0]: - 13 x[1,3,0] + newVar2[1,3,0] <= 0
 R38: y[2,0,0] - y[2,1,0] + newVar1[2,1,0] = 0
 c8[2,1,0]: - 13 x[2,1,0] + newVar2[2,1,0] <= 0
 R40: y[2,1,0] - y[2,2,0] + newVar1[2,2,0] = 0
 c8[2,2,0]: - 13 x[2,2,0] + newVar2[2,2,0] <= 0
 R42: y[2,2,0] - y[2,3,0] + newVar1[2,3,0] = 0
 c8[2,3,0]: - 13 x[2,3,0] + newVar2[2,3,0] <= 0
 R44: - y[1,0,0] + newVar3[1,0,0] = 0
 R45: - x[1,0,0] + newVar4[1,0,0] = 0
 c9[1,0,0]: newVar5[1,0,0] + 13 newVar6[1,0,0] - slack1[1,0,0] <= 13
 R47: y[1,0,0] - y[1,1,0] + newVar3[1,1,0] = 0
 R48: x[1,0,0] - x[1,1,0] + newVar4[1,1,0] = 0
 c9[1,1,0]: newVar5[1,1,0] + 13 newVar6[1,1,0] - slack1[1,1,0] <= 13
 R50: y[1,1,0] - y[1,2,0] + newVar3[1,2,0] = 0
 R51: x[1,1,0] - x[1,2,0] + newVar4[1,2,0] = 0
 c9[1,2,0]: newVar5[1,2,0] + 13 newVar6[1,2,0] - slack1[1,2,0] <= 13
 R53: y[1,2,0] - y[1,3,0] + newVar3[1,3,0] = 0
 R54: x[1,2,0] - x[1,3,0] + newVar4[1,3,0] = 0
 c9[1,3,0]: newVar5[1,3,0] + 13 newVar6[1,3,0] - slack1[1,3,0] <= 13
 R56: - y[2,0,0] + newVar3[2,0,0] = 0
 R57: - x[2,0,0] + newVar4[2,0,0] = 0
 c9[2,0,0]: newVar5[2,0,0] + 13 newVar6[2,0,0] - slack1[2,0,0] <= 13
 R59: y[2,0,0] - y[2,1,0] + newVar3[2,1,0] = 0
 R60: x[2,0,0] - x[2,1,0] + newVar4[2,1,0] = 0
 c9[2,1,0]: newVar5[2,1,0] + 13 newVar6[2,1,0] - slack1[2,1,0] <= 13
 R62: y[2,1,0] - y[2,2,0] + newVar3[2,2,0] = 0
 R63: x[2,1,0] - x[2,2,0] + newVar4[2,2,0] = 0
 c9[2,2,0]: newVar5[2,2,0] + 13 newVar6[2,2,0] - slack1[2,2,0] <= 13
 R65: y[2,2,0] - y[2,3,0] + newVar3[2,3,0] = 0
 R66: x[2,2,0] - x[2,3,0] + newVar4[2,3,0] = 0
 c9[2,3,0]: newVar5[2,3,0] + 13 newVar6[2,3,0] - slack1[2,3,0] <= 13
 c12[0]: b[3,0] = 0
Bounds
Binaries
 x[1,0,0] x[1,1,0] x[1,2,0] x[1,3,0] x[2,0,0] x[2,1,0] x[2,2,0] x[2,3,0]
Generals
 y[1,0,0] y[1,1,0] y[1,2,0] y[1,3,0] y[2,0,0] y[2,1,0] y[2,2,0] y[2,3,0]
 b[0,0] b[1,0] b[2,0] b[3,0] newVar1[1,1,0] newVar2[1,1,0] newVar1[1,2,0]
 newVar2[1,2,0] newVar1[1,3,0] newVar2[1,3,0] newVar1[2,1,0] newVar2[2,1,0]
 newVar1[2,2,0] newVar2[2,2,0] newVar1[2,3,0] newVar2[2,3,0] newVar3[1,0,0]
 newVar4[1,0,0] newVar5[1,0,0] newVar6[1,0,0] slack1[1,0,0] newVar3[1,1,0]
 newVar4[1,1,0] newVar5[1,1,0] newVar6[1,1,0] slack1[1,1,0] newVar3[1,2,0]
 newVar4[1,2,0] newVar5[1,2,0] newVar6[1,2,0] slack1[1,2,0] newVar3[1,3,0]
 newVar4[1,3,0] newVar5[1,3,0] newVar6[1,3,0] slack1[1,3,0] newVar3[2,0,0]
 newVar4[2,0,0] newVar5[2,0,0] newVar6[2,0,0] slack1[2,0,0] newVar3[2,1,0]
 newVar4[2,1,0] newVar5[2,1,0] newVar6[2,1,0] slack1[2,1,0] newVar3[2,2,0]
 newVar4[2,2,0] newVar5[2,2,0] newVar6[2,2,0] slack1[2,2,0] newVar3[2,3,0]
 newVar4[2,3,0] newVar5[2,3,0] newVar6[2,3,0] slack1[2,3,0]
General Constraints
 GC0: newVar2[1,1,0] = ABS ( newVar1[1,1,0] )
 GC1: newVar2[1,2,0] = ABS ( newVar1[1,2,0] )
 GC2: newVar2[1,3,0] = ABS ( newVar1[1,3,0] )
 GC3: newVar2[2,1,0] = ABS ( newVar1[2,1,0] )
 GC4: newVar2[2,2,0] = ABS ( newVar1[2,2,0] )
 GC5: newVar2[2,3,0] = ABS ( newVar1[2,3,0] )
 GC6: newVar5[1,0,0] = ABS ( newVar3[1,0,0] )
 GC7: newVar6[1,0,0] = ABS ( newVar4[1,0,0] )
 GC8: newVar5[1,1,0] = ABS ( newVar3[1,1,0] )
 GC9: newVar6[1,1,0] = ABS ( newVar4[1,1,0] )
 GC10: newVar5[1,2,0] = ABS ( newVar3[1,2,0] )
 GC11: newVar6[1,2,0] = ABS ( newVar4[1,2,0] )
 GC12: newVar5[1,3,0] = ABS ( newVar3[1,3,0] )
 GC13: newVar6[1,3,0] = ABS ( newVar4[1,3,0] )
 GC14: newVar5[2,0,0] = ABS ( newVar3[2,0,0] )
 GC15: newVar6[2,0,0] = ABS ( newVar4[2,0,0] )
 GC16: newVar5[2,1,0] = ABS ( newVar3[2,1,0] )
 GC17: newVar6[2,1,0] = ABS ( newVar4[2,1,0] )
 GC18: newVar5[2,2,0] = ABS ( newVar3[2,2,0] )
 GC19: newVar6[2,2,0] = ABS ( newVar4[2,2,0] )
 GC20: newVar5[2,3,0] = ABS ( newVar3[2,3,0] )
 GC21: newVar6[2,3,0] = ABS ( newVar4[2,3,0] )
End
